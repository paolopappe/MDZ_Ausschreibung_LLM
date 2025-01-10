import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
import openai

from utils.db_management import _db_manager

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


SIMILARITY_THRESHOLD = 0.35
# Prompt zum Stichwörter aus der Anfrage extrahieren;
# der Nutzer gibt eine Anfrage ein, die Stichwörter werden extrahiert
# und weiter benutzt um mit den Zusammenfassungen abgegliechen zu werden
KEYWORDS_PROMPT = """\
You have a document that you need to do a search over. The search \
is made by keywords that you need to extract from the query. \
Your task is to define all the keywords from the input query.\
If the query is meaningless, return no keywords.

The keywords might include both words and numbers of sections of the document.\
There might be occasional typos; if and only if that's the case, correct them.

Example
-------
query:
"Finde alle Informationen zu Halenanbau und Aussenanlagen, Erd- u. Pflasterarbeiten."

output:
["Hallenanbau", "Aussenanlagen", "Erd- u. Pflasterarbeiten"]


Your task
-----
query
{input}

output:
"""


# Class für Structured Output; Das bestimmt in welchem Format das LLM
# den Output ausgeben muss. In unserem Fall sagt es: Gib eine Liste von Stichwörtern
class TopicKeywords(BaseModel):
	"""
	Keywords for a **single topic**.
	"""
	keywords: List[str] = Field(..., description="keywords for the **single topic**")


def init_pipeline():

	gpt = ChatOpenAI(model="gpt-4o-mini", temperature=0)
	template = ChatPromptTemplate.from_template(KEYWORDS_PROMPT)
	# jetzt wird das LLM den Output nach `TopicKeywords` ausgeben
	gpt_structured = gpt.with_structured_output(TopicKeywords)	# no Output Parser needed

	def retrieve(message: AIMessage) -> List[dict]:
		# adjoin retrieved keywords into a query (by the Pydantic schema)
		# die AIMessage ist ein Instance von `TopicKeywords`, das eine Attribute `keywords` hat
		query = " ".join(message.keywords)	# Stichwörter zusammenstellen
		res = _db_manager.vector_store.similarity_search_with_relevance_scores(
			query,	# Liste von Stichwörtern
			k=100,	# gross genug damit all die relevanten Chunks extrahiert werden
			score_threshold=SIMILARITY_THRESHOLD	# nur Chunks die relevanter als SIMILARITY_THRESHOLD sind
		)
		outputs = []
		for doc, score in res:	# je höher der Score ist, desto relevanter ist der entschprechende Chunk
			outputs.append({	# in ein dict einpacken
				"text": doc.metadata.pop("text"),
				"metadata": doc.metadata,
				"score": score
			})
		return outputs

	# 1. Der Nutzer gibt die Anfrage ein
	# 2. Die Anfrage wird in den Prompt eingesetzt
	# 3. Der formatierte Prompt wird ins LLM eingegeben
	# 4. Das LLM extrahiert eine Liste von Stichwörtern (als AIMessage)
	# 5. Die Stichwörter werden in `retrieve` in eine Anfrage zusammengetellt,
	#	und dann werden alle Chunks mit dem höheren als SIMILARITY_THRESHOLD Score zurückgegeben
	pipeline = template | gpt_structured | retrieve

	return pipeline


pipeline = init_pipeline()