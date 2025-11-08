# 🤖 Personal AI Chatbot (with RAG)

> A personal AI chatbot designed to act as a "digital twin," answering questions about professional experience, projects, and skills using Retrieval-Augmented Generation (RAG).

---

## 🚀 Key Features

- **Conversational Interface** — A clean, simple chat UI built with React
- **Custom Knowledge Base** — Answers based on curated personal documents (.md files)
- **RAG Architecture** — Context-aware, factual answers by retrieving relevant information before generation
- **Decoupled Stack** — Modern frontend (React/Vite) communicating with high-performance Python backend (FastAPI)
- **Extensible** — Built in two distinct phases, from simple proxy-chat to full RAG system

---

## 🏛️ Technical Architecture

This project uses a **decoupled, service-oriented architecture**.

### Frontend (React/Vite)
A lightweight client that manages UI state and handles user interaction. It has no knowledge of AI logic—it simply sends fetch requests to the backend API.

### Backend (Python/FastAPI)
A robust API server that acts as the "brain," responsible for all AI-related tasks.

### Data Ingestion (One-Time Script)
An `ingest.py` script uses LangChain to:
- Load personal data from text files
- Split it into chunks
- Create vector embeddings
- Store them in a local ChromaDB instance

### RAG-Powered Chat Logic (`/chat` Endpoint)

1. **Receive Query** — Backend receives user's message from React app
2. **Embed Query** — Query converted into vector embedding
3. **Retrieve Context** — ChromaDB searched for most similar document chunks
4. **Augment Prompt** — Query and context combined into detailed prompt
5. **Generate Response** — Augmented prompt sent to LLM (Gemini, Claude, or GPT)
6. **Return** — Final answer sent back to React app

---

## 🛠️ Tech Stack & Rationale

| Component | Technology | Why This Choice? |
|-----------|-----------|------------------|
| **Frontend** | React (via Vite) | Vite provides extremely fast modern development, far superseding create-react-app. React is ideal for managing conversational state. |
| **Backend** | Python & FastAPI | Python is the standard for AI/ML ecosystem. FastAPI is high-performance and leverages type hints for validation. |
| **AI Orchestration** | LangChain | Simplifies the entire RAG pipeline—from loading documents to managing prompts and chaining retrieval/generation. |
| **Vector Database** | ChromaDB | Developer-first vector store. Free, open-source, runs locally without separate server. |
| **LLM & Embeddings** | Gemini/OpenAI/Claude | Uses foundational models via API. Keeps backend lightweight by offloading computation. |

---

## 🚀 Project Evolution

### Phase 1: The Simple "Proxy" Chatbot

**Goal:** Establish core communication pipeline between frontend and backend.

**Logic:** 
```
React App → FastAPI /chat → External LLM API → FastAPI → React App
```

This phase confirmed frontend UI and backend API communication, with proper API keys and CORS configuration.

### Phase 2: The "Smart" RAG Chatbot

**Goal:** Upgrade backend to use RAG architecture, forcing answers based on personal data.

**Logic:**
```
React App → FastAPI /chat (with RAG) → External LLM API → FastAPI → React App
```

This involved creating `ingest.py` to build the vector database and modifying `/chat` endpoint for full Retrieve-Augment-Generate flow. **No frontend changes needed.**

---

## ⚙️ Getting Started

> **Requirements:** Node.js (v18+) and Python (v3.10+)

### 1️⃣ Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate  # (or venv\Scripts\activate on Windows)

# Install required Python packages
pip install -r requirements.txt
# Or manually:
# pip install fastapi "uvicorn[standard]" langchain langchain-openai chromadb

# Create a .env file and add your LLM API key
echo "OPENAI_API_KEY='your_api_key_here'" > .env

# Run the one-time ingestion script to build your vector database
python ingest.py

# Run the backend server
uvicorn main:app --reload
```

✅ Your backend is now running on **http://localhost:8000**

### 2️⃣ Frontend Setup

```bash
# In a separate terminal, navigate to the frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Run the frontend development server
npm run dev
```

✅ Your frontend is now running on **http://localhost:5173**

---

## 📝 Notes

This ensures the chatbot's answers are **grounded in a custom knowledge base** rather than the LLM's general knowledge, preventing hallucinations and providing accurate, specific information.