import asyncio
import logging
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from constants import api_key, google_api_key
from src.routes import apiRouter


# Configure logging to write to app.log
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = FastAPI()
# Enable CORS middleware
origins = [
    "http://localhost:5173",  # Adjust this to the frontend URL if different
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow the frontend domain
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize Groq API for autocomplete and summarization
groq_api_key = api_key
google_ai_key = google_api_key

if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

model = "llama3-8b-8192"
groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name=model)

# Define LLM chains for autocomplete and summarization
autocomplete_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="Complete the given text with a plausible continuation. Do not provide explanations or additional context, only complete the sentence."),
    HumanMessagePromptTemplate.from_template("{user_input}"),
])

autocomplete_chain = LLMChain(llm=groq_chat, prompt=autocomplete_prompt)

summarization_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="check grammer and spelling mistakes give me with good quality"),
    HumanMessagePromptTemplate.from_template("Summarize the following text:\n{text_to_summarize}. \n Give me the direct sentence output, without any additional information, summary or context. Just a simple output sentence."),
])

summarization_chain = LLMChain(llm=groq_chat, prompt=summarization_prompt)

# Define request/response models
class AutocompleteRequest(BaseModel):
    user_input: str

class SummarizeRequest(BaseModel):
    text_to_summarize: str


@app.post("/autocomplete")
async def autocomplete(request: AutocompleteRequest):
    logging.info(f"Received autocomplete request: {request.dict()}")

    # Simulate delay
    await asyncio.sleep(0.5)  # 500ms delay

    try:
        result = autocomplete_chain.predict(user_input=request.user_input)
        logging.info(f"Autocomplete result: {result}")
        return {"suggestions": result.split("\n")}  # Split suggestions into a list
    except Exception as e:
        logging.error(f"Error during autocomplete: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
async def summarize(request: SummarizeRequest):
    logging.info(f"Received summarize request: {request.dict()}")

    try:
        result = summarization_chain.predict(text_to_summarize=request.text_to_summarize)

        # Extract only the content from the generated response
        if 'Summary:' in result:
            result = result.split("Summary:")[-1].strip()

        logging.info(f"Returning summary: {result}")
        return {"summary": result}  # Wrap result in a dictionary
    except Exception as e:
        logging.error(f"Error during summarization: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
app.include_router(apiRouter)

from fastapi import FastAPI
print(app.routes)