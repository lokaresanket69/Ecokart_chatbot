# FAQ Chatbot (LangChain + Ollama + ChromaDB)

## How to Run Locally

### 1. Start Ollama LLM
Install Ollama from https://ollama.com/

Start the Llama 3 model:
```
ollama pull llama3
ollama run llama3
```

### 2. Install Python Dependencies
```
pip install -r requirements.txt
```

### 3. Run the Backend API
```
uvicorn app:app --reload
```

The API will be available at http://localhost:8000

### 4. Open the Frontend
Open `frontend/index.html` in your browser.

---

- Edit `backend/faqs.json` to add or update FAQs.
- The chatbot will answer based on your FAQ data using local LLM and vector search.
- No cloud or paid APIs required.
