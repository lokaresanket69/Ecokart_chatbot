import json
print('[DEBUG] app.py imported, __name__ =', __name__)
import os
# Prefer FAISS (fast) but it's unavailable on Windows.
try:
    from langchain_community.vectorstores import FAISS  # type: ignore
except ModuleNotFoundError:
    FAISS = None  # type: ignore
    from langchain_community.vectorstores import Chroma  # type: ignore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_together import Together
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# -------------------- Load FAQ data and build documents --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
from glob import glob

faqs = []
for path in glob(os.path.join(BASE_DIR, "faqs*.json")):
    with open(path, "r", encoding="utf-8") as f:
        faqs.extend(json.load(f))

# Build documents from all loaded FAQs
documents: list[Document] = []
for faq in faqs:
    questions = faq["question"] if isinstance(faq["question"], list) else [faq["question"]]
    for q in questions:
        documents.append(Document(page_content=q.strip().lower() + "\n" + faq["answer"]))
# --------------------------------------------------------------------------

# -------------------- Load Together.ai API key --------------------
from pathlib import Path

def _load_key_from_dotenv():
    dotenv = Path(__file__).with_name('.env')
    if dotenv.exists():
        for line in dotenv.read_text().splitlines():
            if line.startswith('TOGETHER_API_KEY='):
                return line.partition('=')[2].strip()
    return ''

# first try env var, else .env file
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY") or _load_key_from_dotenv()
# --------------------------------------------------------------------------
if not TOGETHER_API_KEY:
    print("[Warning] TOGETHER_API_KEY not set – running in mock mode.\nResponding with a placeholder reply.")
    def chatbot_fn(message, history):
        return "(mock) Sorry, the language model is not configured on this machine."
else:
    os.environ["TOGETHER_API_KEY"] = TOGETHER_API_KEY  # make sure underlying libs see it
    # Initialize HuggingFace Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Build vector store – prefer FAISS if it was imported successfully, otherwise use Chroma
    if FAISS is not None:
        try:
            vectorstore = FAISS.from_documents(documents, embeddings)
            print("[DEBUG] Using FAISS vector store")
        except Exception as e:
            print("[WARN] FAISS runtime error (", e, ") – falling back to Chroma", sep="")
            from langchain_community.vectorstores import Chroma  # fallback import
            vectorstore = Chroma.from_documents(documents, embeddings)
    else:
        from langchain_community.vectorstores import Chroma
        vectorstore = Chroma.from_documents(documents, embeddings)
    retriever = vectorstore.as_retriever()

    # Initialize Together.ai Mixtral LLM
    llm = Together(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        temperature=0.2,
        max_tokens=512,
    )

    # Create RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=False)

    # define chatbot function using real QA chain
    def chatbot_fn(message, history):
        return qa_chain.run(message)




# Create Flask app for JSON API
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "../frontend"))
app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="")
CORS(app)
print('[DEBUG] Flask app created')

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
        import traceback,sys
        traceback.print_exc(file=sys.stdout)
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index_html():
    return send_from_directory(app.static_folder, "index.html")

# Serve static assets (JS, CSS, etc.)
@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    print("[DEBUG] Starting Ecokart backend...")
    # Determine port based on environment variable for Render compatibility
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, use_reloader=False, debug=True)
