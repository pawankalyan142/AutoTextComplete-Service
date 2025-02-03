from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
from src.services.chat_service import generate_troubleshooting_steps

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Define API Router
chatapi = APIRouter()

# Request model
class TroubleshootingRequest(BaseModel):
    problem_statement: str

# Response model
class TroubleshootingResponse(BaseModel):
    troubleshooting_steps: str

@chatapi.post("/troubleshoot", response_model=TroubleshootingResponse)
async def troubleshoot(request: TroubleshootingRequest):
    """
    Endpoint to generate troubleshooting steps based on a given problem statement.
    """
    logging.info(f"Received troubleshooting request: {request.problem_statement}")

    try:
        steps = generate_troubleshooting_steps(request.problem_statement)
        logging.info(f"Generated troubleshooting steps: {steps}")
        return TroubleshootingResponse(troubleshooting_steps=steps)
    except Exception as e:
        logging.error(f"Error in troubleshooting API: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
