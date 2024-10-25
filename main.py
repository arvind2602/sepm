from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from llama_index.llms.gemini import Gemini  # Update to use Gemini
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

app = FastAPI()

# Initialize Gemini API client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
llm = Gemini(api_key=GEMINI_API_KEY, model="models/gemini-1.5-pro")

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
    studentData = data.get('data', '')
    # print(studentData)
    final = "question : " + message + "My details in JSON format :" + \
        studentData + os.getenv("MESSAGE")

    if not message:
        return {"error": "Please provide a message to complete."}

    try:
        completion = await complete_message_async(final)
        return {"result": completion}
    except Exception as e:
        return {"error": f"Error completing message: {str(e)}"}


@app.post("/consell")
async def complete_message_consell(request: Request):
    data = await request.json()
    message = data.get('message', '')
    final = os.getenv("MESSAGE_CONSELL") + message

    if not message:
        return {"error": "Please provide a message to complete."}

    try:
        completion = await complete_message_async(final)
        return {"result": completion}
    except Exception as e:
        return {"error": f"Error completing message: {str(e)}"}
