from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

app = FastAPI()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

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