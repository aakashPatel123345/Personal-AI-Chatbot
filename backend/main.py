# --- Standard Library Imports ---
import os

# --- Third-Party Imports ---
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

# --- Hugging Face / Langchain Imports --
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# --- Langchain Importing Chroma DB

# 1. Initializing the embedding function
embeddings = HuggingFaceEmbeddings (
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True} # Recommended for BGE
)

# 2. Specifying directory of chroma
persist_dir = "./chroma_db"

# 3. Loading the vector db
vectordb_loaded = Chroma(
    persist_directory = persist_dir,
    embedding_function = embeddings
)

"""
# Let's test the loader to ensure data was "understood" properly
query = "What were the key achievements of the Software Engineering Internship at Seleccion Consulting?"
docs = vectordb_loaded.similarity_search(query)
print(f"Testing loading with query: {query}")
print(docs)
"""




load_dotenv()

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_message = request.message
    print(f"Received Message: {user_message}")


    # Retrieve relevant context (k = 5 means the 5 most similar chunks)
    # Increased from 3 to 5 for better context coverage
    top_docs = vectordb_loaded.similarity_search(user_message, k=5)
    context = "\n".join(doc.page_content for doc in top_docs)

    # Build the full prompt for our LLM (gemini)
    # The model should act AS the user, not as an assistant talking about the user
    full_prompt = f"""You are Aakash Patel. Answer the following question about yourself based on the information provided below. Respond naturally in first person, as if you are having a conversation about yourself.

Information about you:
{context}

Question: {user_message}

Answer (respond as Aakash Patel, in first person):"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt,
    )

    return {"response": response.text}