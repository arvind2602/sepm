from fastapi import FastAPI, Request
from llama_index.llms.anthropic import Anthropic
from llama_index.core import Settings
from dotenv import load_dotenv
import os
import uvicorn
import asyncio
load_dotenv()

app = FastAPI()

# Set up Anthropic API
tokenizer = Anthropic().tokenizer
Settings.tokenizer = tokenizer
os.environ["ANTHROPIC_API_KEY"]=os.getenv("ANTHROPIC_API_KEY")
llm = Anthropic(model="claude-3-opus-20240229")

async def complete_message_async(message):
    return await asyncio.to_thread(llm.complete, message)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/complete")
async def complete_message(request: Request):
    data = await request.json()
    message = data.get('message', '')
    
    if message:
        completion = await complete_message_async(message)
        return {"result": completion}
    else:
        return {"error": "Please provide a message to complete."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
