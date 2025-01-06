from flask import Flask, request
from waitress import serve

from utils.pipeline import pipeline

app = Flask(__name__)
HOST = "127.0.0.1"
PORT = 5000
BASE_URL = f"http://{HOST}:{PORT}"

# this app only listens to input queries and returns the results
@app.route("/get", methods=["GET"])
def get_relevant_docs():
	# main.py ensures we have a query
	query = request.args.get("query")
	# will return up to 100 relevant docs
	try:
		res = pipeline.invoke({"input": query})
		return res, 200
	except Exception as e:
		return str(e), 400
	

def start_server():
    serve(app, host=HOST, port=PORT)