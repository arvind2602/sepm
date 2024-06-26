from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from llama_index.llms.anthropic import Anthropic
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

app = FastAPI()

# Initialize Anthropic API client
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
llm = Anthropic(api_key=ANTHROPIC_API_KEY, model="claude-3-opus-20240229")

# Configure CORS to allow requests from localhost

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def complete_message_async(message):
    return await asyncio.to_thread(llm.complete, message)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/complete")
async def complete_message(request: Request):
    data = await request.json()
    message = data.get('message', '')
    final=os.getenv("MESSAGE")+message
    
    if not message:
        return {"error": "Please provide a message to complete."}

    try:
        completion = await complete_message_async(final)
        return {"result": completion}
    except Exception as e:
        return {"error": f"Error completing message: {str(e)}"}
    
@app.post("/consell")
async def complete_message(request: Request):
    data = await request.json()
    message = data.get('message', '')
    final=os.getenv("MESSAGE_CONSELL")+message
    
    if not message:
        return {"error": "Please provide a message to complete."}

    try:
        completion = await complete_message_async(final)
        return {"result": completion}
    except Exception as e:
        return {"error": f"Error completing message: {str(e)}"}
    

