from fastapi import APIRouter, Depends, HTTPException
from src.services.custom_services import get_employee_ticket_info
from dbconfig.db_config import get_db
from sqlalchemy.ext.asyncio import AsyncSession

# Create a new APIRouter for employee-ticket data
services = APIRouter()

# Route to fetch employee and ticket info
@services.get("/employee_ticket_info")
async def employee_ticket_info(db: AsyncSession = Depends(get_db)):
    try:
        return await get_employee_ticket_info(db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching employee-ticket info: {str(e)}")

