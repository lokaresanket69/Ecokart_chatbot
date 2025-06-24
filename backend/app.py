import json
import os
from glob import glob
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_together import Together

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

faqs = []
for path in glob(os.path.join(BASE_DIR, "faqs*.json")):
    with open(path, "r", encoding="utf-8") as f:
        faqs.extend(json.load(f))

documents: list[Document] = []
for faq in faqs:
    questions = faq["question"] if isinstance(faq["question"], list) else [faq["question"]]
    for q in questions:
        documents.append(Document(page_content=q.strip().lower() + "\n" + faq["answer"]))


def _load_key_from_dotenv():
    dotenv = Path(__file__).with_name(".env")
    if dotenv.exists():
        for line in dotenv.read_text().splitlines():
            if line.startswith("TOGETHER_API_KEY="):
                return line.partition("=")[2].strip()
    return ""


TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY") or _load_key_from_dotenv()

if not TOGETHER_API_KEY:

    def chatbot_fn(message, history):
        print("[Warning] TOGETHER_API_KEY not set – running in mock mode.")
        return "(mock) Sorry, the language model is not configured on this machine."

else:
    os.environ["TOGETHER_API_KEY"] = TOGETHER_API_KEY
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-MiniLM-L3-v2"
    )
    vectorstore = Chroma.from_documents(documents, embeddings)
    retriever = vectorstore.as_retriever()
    llm = Together(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        temperature=0.2,
        max_tokens=512,
    )
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm, retriever=retriever, return_source_documents=False
    )

    def chatbot_fn(message, history):
        return qa_chain.run(message)


STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "../frontend"))
app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="")
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/chat", methods=["POST", "OPTIONS"])
def chat_endpoint():
    data = request.get_json(force=True)
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "No message provided"}), 400
    try:
        response = chatbot_fn(message, [])
        return jsonify({"response": response})
    except Exception as e:
        import traceback, sys

        traceback.print_exc(file=sys.stdout)
        return jsonify({"error": str(e)}), 500


@app.route("/")
def index_html():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory(app.static_folder, path)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, use_reloader=False, debug=True)
