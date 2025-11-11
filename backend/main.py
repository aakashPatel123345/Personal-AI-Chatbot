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
    top_docs = vectordb_loaded.similarity_search(user_message, k=5)
    context = "\n\n".join([f"[Context {i+1}]: {doc.page_content}" for i, doc in enumerate(top_docs)])
    
    # Debug: Print retrieved context (remove in production if desired)
    print(f"\n📚 Retrieved {len(top_docs)} context chunks")
    if top_docs:
        print(f"Context preview: {top_docs[0].page_content[:200]}...")

    # Build the full prompt for our LLM (gemini)
    # The model should act AS the user, not as an assistant talking about the user
    system_instruction = """You are Aakash Patel. Answer questions about yourself in a casual, friendly way - like you're texting a friend. Be personable, authentic, and conversational.

CRITICAL RULES:
- ONLY use information from the provided context. NEVER make up, invent, or use placeholder text.
- If information isn't in the context, say something casual like "Yea, I can't really answer that bro" or "Hmm, I don't have much to say about that."
- Write casually - use contractions (I'm, don't, can't), be friendly, like texting.
- Use first person (I, me, my).
- Never use placeholders like "[insert]" or "[mention]" - only real information from context."""

    user_prompt = f"""Here's what I know about myself:
{context}

Question: {user_message}

Answer (casual, like texting a friend):"""

    # Combine system instruction and user prompt
    full_prompt = system_instruction + "\n\n" + user_prompt
    
    # Generate response - removed generation_config as it's not supported in this API format
    # The model will use default settings which should work fine
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=full_prompt,
    )

    return {"response": response.text}