from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from dbconfig.db_config import get_db
from models import TicketInfo 
from src.DAO.tickets_dao import  TicketInfoDAO



# TicketInfo Service Layer
async def get_all_ticket_info(db: AsyncSession = Depends(get_db)):
    ticket_dao = TicketInfoDAO(db)
    tickets = await ticket_dao.find_all()
    return [
        {
            "ticket_id": ticket.ID,
            "ticket_raised_by": ticket.TicketRaisedBy,
            "ticket_assign_to_employee_id": ticket.TicketAssignToEmployeeID,
            "ticket_description": ticket.TicketDescription
        } for ticket in tickets
    ]

async def get_ticket_info(ticket_id: int, db: AsyncSession = Depends(get_db)):
    ticket_dao = TicketInfoDAO(db)
    ticket = await ticket_dao.find(ticket_id)
    return {
        "ticket_id": ticket.ID,
        "ticket_raised_by": ticket.TicketRaisedBy,
        "ticket_assign_to_employee_id": ticket.TicketAssignToEmployeeID,
        "ticket_description": ticket.TicketDescription
    }

async def update_ticket_info(ticket_id: int, db: AsyncSession = Depends(get_db), **kwargs):
    ticket_dao = TicketInfoDAO(db)
    updated_ticket = await ticket_dao.update(ticket_id, **kwargs)
    return {
        "ticket_id": updated_ticket.ID,
        "ticket_raised_by": updated_ticket.TicketRaisedBy,
        "ticket_assign_to_employee_id": updated_ticket.TicketAssignToEmployeeID,
        "ticket_description": updated_ticket.TicketDescription
    }