import json
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_together import Together
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Load Together.ai API key from environment variable
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")
if not TOGETHER_API_KEY:
    raise ValueError("Please set your Together.ai API key in the TOGETHER_API_KEY environment variable.")

# Base directory of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAQ_PATH = os.path.join(BASE_DIR, "faqs_expanded.json")
# Load expanded FAQs with paraphrased questions
with open(FAQ_PATH, "r", encoding="utf-8") as f:
    faqs = json.load(f)

# Create one document per paraphrased question (case-insensitive)
documents = []
for faq in faqs:
    questions = faq["question"] if isinstance(faq["question"], list) else [faq["question"]]
    for q in questions:
        documents.append(Document(page_content=q.strip().lower() + "\n" + faq["answer"]))

# Initialize HuggingFace Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Build FAISS vector store
vectorstore = FAISS.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever()

# Initialize Together.ai Mixtral LLM
llm = Together(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    temperature=0.2,
    max_tokens=512,
)

# Create RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=False)

def chatbot_fn(message, history):
    response = qa_chain.run(message)
    return response

# Create Flask app for JSON API
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "../frontend"))
app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="")
CORS(app)

@app.route("/chat", methods=["POST"])
def chat_endpoint():
    data = request.get_json(force=True)
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "No message provided"}), 400
    try:
        response = chatbot_fn(message, [])
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index_html():
    return send_from_directory(app.static_folder, "index.html")

# Serve static assets (JS, CSS, etc.)
@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    # Determine port based on environment variable for Render compatibility
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
