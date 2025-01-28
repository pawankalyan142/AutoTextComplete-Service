import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from constants import api_key, google_api_key

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
    SystemMessage(content="You are a helpful AI that autocompletes user input in real-time."),
    HumanMessagePromptTemplate.from_template("{user_input}"),
])

autocomplete_chain = LLMChain(llm=groq_chat, prompt=autocomplete_prompt)

summarization_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a concise summarizer that summarizes text into a clear and brief format."),
    HumanMessagePromptTemplate.from_template("Summarize the following text:\n{text_to_summarize}"),
])

summarization_chain = LLMChain(llm=groq_chat, prompt=summarization_prompt)

# Define request/response models
class AutocompleteRequest(BaseModel):
    user_input: str

class SummarizeRequest(BaseModel):
    text_to_summarize: str

@app.post("/autocomplete")
async def autocomplete(request: AutocompleteRequest):
    # Log the incoming request data
    logging.info(f"Received autocomplete request: {request.dict()}")
    
    try:
        result = autocomplete_chain.predict(user_input=request.user_input)
        logging.info(f"Autocomplete result: {result}")
        return {"suggestions": result}
    except Exception as e:
        logging.error(f"Error during autocomplete: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
async def summarize(request: SummarizeRequest):
    # Log the incoming request data
    logging.info(f"Received summarize request: {request.dict()}")
    
    try:
        result = summarization_chain.predict(text_to_summarize=request.text_to_summarize)
        logging.info(f"Summarization result: {result}")
        return {"summary": result}
    except Exception as e:
        logging.error(f"Error during summarization: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.options("/autocomplete")
async def options_autocomplete():
    # Handle the preflight OPTIONS request
    return {"message": "Preflight request passed"}

@app.options("/summarize")
async def options_summarize():
    # Handle the preflight OPTIONS request
    return {"message": "Preflight request passed"}

