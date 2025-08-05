# src/crew_blog_backend/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from src.latest_ai_development.crew import BlogContentCrew
from src.latest_ai_development.ingestion import retrieve_similar_docs
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str  # The only input from the chatbot

def extract_blog_metadata(prompt: str) -> dict:
    """Use Gemini to auto-extract topic, tone, audience, and platform"""
    model = genai.GenerativeModel("gemini-1.5-flash")  # lightweight, fast
    response = model.generate_content(f"""
    Analyze the user's request: "{prompt}"
    Return JSON with 4 fields:
    - topic
    - tone (like friendly, formal, or informative)
    - audience (like students, developers, general)
    - platform (like blog, LinkedIn, Twitter)
    Example output:
    {{ "topic": "...", "tone": "...", "audience": "...", "platform": "..." }}
    """)
    
    # Extract clean JSON (Gemini often outputs a JSON-like text)
    try:
        import json
        return json.loads(response.text)
    except:
        # fallback defaults
        return {
            "topic": prompt,
            "tone": "informative",
            "audience": "general",
            "platform": "blog"
        }

@app.post("/chatbot/send-message")
def chatbot_reply(req: ChatRequest):
    try:
        # 1️⃣ Extract structured blog data from user input
        metadata = extract_blog_metadata(req.prompt)

        # 2️⃣ Retrieve context docs
        context = retrieve_similar_docs(metadata["topic"])

        # 3️⃣ Generate blog using Crew
        crew = BlogContentCrew()
        result = crew.crew().kickoff(inputs={
            **metadata,
            "context": "\n\n".join(context)
        })

        return {"reply": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
