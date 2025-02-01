from collections import deque
import random
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from dbconfig.db_config import get_db
from src.DAO.service_dao import EmployeeTicketDAO
from models import TicketInfo

async def get_employee_ticket_info(db: AsyncSession = Depends(get_db)):
    try:
        # Instantiate DAO and get data
        dao = EmployeeTicketDAO(db)
        employee_ticket_data = await dao.find_employee_ticket_info()

        # Format the response to return as a list of dictionaries
        response = [
            {
                "employee_id": row.EmployeeID,
                "employee_name": row.EmployeeName,
                "queue": row.Queue,
                "ticket_raised_by": row.TicketRaisedBy,
                "ticket_description": row.TicketDescription
            }
            for row in employee_ticket_data
        ]
        return response
    except HTTPException as e:
        raise e  # If HTTPException is raised in DAO, propagate it
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# async def assign_ticket_to_member(ticket_data: dict, db: AsyncSession = Depends(get_db)):
#     try:
#         # Extract data from ticket payload
#         ticket_raised_by = ticket_data["ticket_raised_by"]
#         ticket_description = ticket_data["ticket_description"]
#         # ticket_created_at = ticket_data["ticket_created_at"]

#         # Instantiate the DAO to interact with the database
#         dao = EmployeeTicketDAO(db)

#         # Get available employees whose queue size is <= 4
#         available_employees = await dao.get_available_employees()
#         if not available_employees:
#             raise HTTPException(status_code=404, detail="No available employees found with a queue size <= 4")

#         # Assign ticket to a random employee from the available list
#         assigned_employee = random.choice(available_employees)

#         # Create a new ticket and assign the selected employee's ID to the ticket
#         new_ticket = TicketInfo(
#             TicketRaisedBy=ticket_raised_by,
#             TicketDescription=ticket_description,
#             # TicketCreatedAt=ticket_created_at,
#             TicketAssignToEmployeeID=assigned_employee.EmployeeID
#         )
        
#         # Add the new ticket to the database
#         db.add(new_ticket)
#         await db.commit()
#         await db.refresh(new_ticket)

#         # Prepare the response data
#         response = {
#             "employee_id": assigned_employee.EmployeeID,
#             "employee_name": assigned_employee.EmployeeName,
#             "ticket_description": new_ticket.TicketDescription,
#             "ticket_raised_by": new_ticket.TicketRaisedBy
#         }

#         return response

#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error assigning ticket: {str(e)}")

async def assign_ticket_to_member(ticket_data: dict, db: AsyncSession = Depends(get_db)):
    try:
        # Extract data from ticket payload
        ticket_raised_by = ticket_data["ticket_raised_by"]
        ticket_description = ticket_data["ticket_description"]

        # Instantiate the DAO to interact with the database
        dao = EmployeeTicketDAO(db)

        # Get available employees whose queue size is <= 4
        available_employees = await dao.get_available_employees()
        if not available_employees:
            raise HTTPException(status_code=404, detail="No available employees found with a queue size <= 4")

        # Create a queue with employees
        employee_queue = deque(available_employees)

        # Try to find an employee with the smallest queue size first
        while employee_queue:
            employee = employee_queue.popleft()  # Pop the employee from the front of the queue
            
            # You can implement a check here to see if the employee still has a queue size <= 4
            # This depends on how you track the employee's current workload in the database
            
            if employee.Queue <= 4:  # Assuming you have current_queue_size attribute for employees
                assigned_employee = employee
                break
        else:
            # If no available employees are found
            raise HTTPException(status_code=404, detail="No employees with queue size <= 4 available")

        # Create a new ticket and assign the selected employee's ID to the ticket
        new_ticket = TicketInfo(
            TicketRaisedBy=ticket_raised_by,
            TicketDescription=ticket_description,
            TicketAssignToEmployeeID=assigned_employee.EmployeeID
        )
        
        # Add the new ticket to the database
        db.add(new_ticket)
        await db.commit()
        await db.refresh(new_ticket)

        # Update the employee's queue size (you should track how many tickets they are assigned to)
        await dao.update_employee_queue_size(assigned_employee.EmployeeID)

        # Prepare the response data
        response = {
            "employee_id": assigned_employee.EmployeeID,
            "employee_name": assigned_employee.EmployeeName,
            "ticket_description": new_ticket.TicketDescription,
            "ticket_raised_by": new_ticket.TicketRaisedBy
        }

        return response

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error assigning ticket: {str(e)}")