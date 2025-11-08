# --- Standard Library Imports ---
import os

# --- Third-Party Imports ---
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_message,
    )

    return {"response": response.text}