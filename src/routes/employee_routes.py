import logging
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from dbconfig.db_config import get_db
from src.services.employee_services import get_employee_info, update_employee_info , get_all_employee_info
from fastapi import APIRouter

# Create the router for employee info
employee = APIRouter()

# Define the request model for employee info
class EmployeeInfoRequest(BaseModel):
    employee_id: int

@employee.get("/employee_info")
async def employee_info(request: EmployeeInfoRequest, db: AsyncSession = Depends(get_db)):
    return await get_all_employee_info(request.employee_id, db)

@employee.post("/employee_info")
async def employee_info(request: EmployeeInfoRequest, db: AsyncSession = Depends(get_db)):
    return await get_employee_info(request.employee_id, db)

@employee.put("/employee_info")
async def employee_info_update(request: EmployeeInfoRequest, db: AsyncSession = Depends(get_db), **kwargs):
    return await update_employee_info(request.employee_id, db, **kwargs)
