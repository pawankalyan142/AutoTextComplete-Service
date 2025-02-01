import logging
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dbconfig.db_config import get_db
from src.services.ticketemploye import get_ticket_info, update_ticket_info , get_all_ticket_info
from src.services.custom_services import assign_ticket_to_member
from pydantic import BaseModel
from fastapi import APIRouter

# Create a router for tickets
tickets = APIRouter()

# Define a model to accept ticket_id as input
class TicketInfoRequest(BaseModel):
    ticket_id: int

@tickets.get("/ticket_info")
async def all_ticket_info(db: AsyncSession = Depends(get_db)):
    return await get_all_ticket_info(db)

@tickets.post("/ticket_info")
async def ticket_info(request: TicketInfoRequest, db: AsyncSession = Depends(get_db)):
    return await get_ticket_info(request.ticket_id, db)

@tickets.put("/ticket_info")
async def ticket_info_update(request: TicketInfoRequest, db: AsyncSession = Depends(get_db), **kwargs):
    return await update_ticket_info(request.ticket_id, db, **kwargs)

# Define the request body model
class TicketAssignmentRequest(BaseModel):
    ticket_raised_by: str
    ticket_description: str

# POST endpoint for assigning ticket to a member
@tickets.post("/assign_to_member")
async def assign_to_member(ticket_data: TicketAssignmentRequest, db: AsyncSession = Depends(get_db)):
    try:
        # Call service to assign ticket to a member
        return await assign_ticket_to_member(ticket_data.model_dump(), db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error assigning ticket: {str(e)}")