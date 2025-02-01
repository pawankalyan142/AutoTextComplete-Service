from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from models import TicketInfo
from fastapi import HTTPException

class TicketInfoDAO:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find(self, ticket_id: int):
        try:
            result = await self.db.execute(select(TicketInfo).filter(TicketInfo.ID == ticket_id))
            ticket = result.scalars().first()
            if not ticket:
                raise HTTPException(status_code=404, detail="Ticket not found")
            return ticket
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def find_all(self):
        try:
            result = await self.db.execute(select(TicketInfo))
            tickets = result.scalars().all()  # Fetch all tickets from the database
            return tickets
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    async def count(self):
        try:
            result = await self.db.execute(select([TicketInfo.ID]).distinct())
            return len(result.scalars().all())  # Return the count of distinct tickets
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def update(self, ticket_id: int, **kwargs):
        try:
            ticket = await self.find(ticket_id)  # Reuse the find method to get the ticket
            
            # Update ticket attributes
            for key, value in kwargs.items():
                setattr(ticket, key, value)

            self.db.add(ticket)
            await self.db.commit()
            return ticket
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
