import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


SIMILARITY_THRESHOLD = 0.35
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


class TopicKeywords(BaseModel):
	"""
	Keywords for a **single topic**.
	"""
	keywords: List[str] = Field(..., description="keywords for the **single topic**")


def init_pipeline():

	embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
	vector_store = Chroma(
		collection_name="ausscheibungen_meta",
		embedding_function=embeddings,
		persist_directory="./chroma_ausscheibungen_meta_db",
	)

	gpt = ChatOpenAI(model="gpt-4o-mini", temperature=0)


	template = ChatPromptTemplate.from_template(KEYWORDS_PROMPT)
	gpt_structured = gpt.with_structured_output(TopicKeywords)	# no Output Parser needed

	def retrieve(message: AIMessage) -> List[dict]:
		# adjoin retrieved keywords into a query (by the Pydantic schema)
		query = " ".join(message.keywords)
		res = vector_store.similarity_search_with_relevance_scores(
			query,
			k=100,
			score_threshold=SIMILARITY_THRESHOLD
		)
		outputs = []
		for doc, score in res:
			outputs.append({
				"text": doc.metadata.pop("text"),
				"metadata": doc.metadata,
				"score": score
			})
		return outputs

	pipeline = template | gpt_structured | retrieve

	return pipeline


pipeline = init_pipeline()