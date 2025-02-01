from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from models import EmployeeInfo, TicketInfo
from fastapi import HTTPException

class EmployeeTicketDAO:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Method to perform the join query
    async def find_employee_ticket_info(self):
        try:
            # Perform the join query
            query = (
                select(EmployeeInfo.EmployeeID, EmployeeInfo.EmployeeName, EmployeeInfo.Queue,
                       TicketInfo.TicketRaisedBy, TicketInfo.TicketDescription)
                .join(TicketInfo, TicketInfo.TicketAssignToEmployeeID == EmployeeInfo.EmployeeID)
            )
            result = await self.db.execute(query)
            data = result.fetchall()  # Fetch all results
            return data
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    # # Method to fetch employees whose queue size is <= 4
    # async def get_available_employees(self):
    #     try:
    #         # Query to fetch employees with queue size <= 4
    #         query = (
    #             select(EmployeeInfo)
    #             .filter(EmployeeInfo.Queue <= 4)
    #         )
    #         result = await self.db.execute(query)
    #         employees = result.scalars().all()  # Get all employees that match the condition
    #         return employees
    #     except SQLAlchemyError as e:
    #         raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    # Method to assign ticket to an employee
    async def assign_ticket_to_employee(self, ticket_id: int, employee_id: int):
        try:
            # Query to update the ticket's assigned employee
            query = (
                select(TicketInfo)
                .filter(TicketInfo.ID == ticket_id)
            )
            result = await self.db.execute(query)
            ticket = result.scalars().first()
            if not ticket:
                raise HTTPException(status_code=404, detail="Ticket not found")
            
            # Assign ticket to employee
            ticket.TicketAssignToEmployeeID = employee_id
            self.db.add(ticket)
            await self.db.commit()
            return ticket
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
    async def get_available_employees(self):
        result = await self.db.execute(
            select(EmployeeInfo).filter(EmployeeInfo.Queue <= 4)
        )
        return result.scalars().all()

    async def update_employee_queue_size(self, employee_id: int):
        # Update the employee's queue size after they are assigned a ticket
        result = await self.db.execute(
            select(EmployeeInfo).filter(EmployeeInfo.EmployeeID == employee_id)
        )
        employee = result.scalars().first()
        if employee:
            employee.Queue += 1
            self.db.add(employee)
            await self.db.commit()
            await self.db.refresh(employee)