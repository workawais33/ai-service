from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
import os
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
load_dotenv()

app = FastAPI()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise Exception("GROQ_API_KEY is missing in Railway environment variables")

client = Groq(api_key=api_key)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "AI Service Running"}

@app.post("/chat")
def chat(data: ChatRequest):

    def generate():

        stream = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": data.message
                }
            ],
            model="llama-3.3-70b-versatile",
            stream=True
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content

            if content:
                yield content

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )