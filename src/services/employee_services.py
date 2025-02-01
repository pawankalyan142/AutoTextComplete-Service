from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import EmployeeInfo  # Assuming this is your model for EmployeeInfo
from dbconfig.db_config import get_db
from src.DAO.employee_dao import  EmployeeInfoDAO # Import the DAO module for employee


async def get_all_employee_info(db: AsyncSession = Depends(get_db)):
    employee_dao = EmployeeInfoDAO(db)
    employees = await employee_dao.find_all()  # Use the find_all method to get all employees
    return [
        {
            "employee_id": employee.EmployeeID,
            "employee_name": employee.EmployeeName,
            "queue": employee.Queue,
            "available_shift": employee.AvailableShift,
            "current_working_queue_id": employee.CurrentWorkingQueueID
        } for employee in employees
    ]

async def get_employee_info(employee_id: int, db: AsyncSession = Depends(get_db)):
    employee_dao = EmployeeInfoDAO(db)
    employee = await employee_dao.find(employee_id)
    return {
        "employee_id": employee.EmployeeID,
        "employee_name": employee.EmployeeName,
        "queue": employee.Queue,
        "available_shift": employee.AvailableShift,
        "current_working_queue_id": employee.CurrentWorkingQueueID
    }

async def update_employee_info(employee_id: int, db: AsyncSession = Depends(get_db), **kwargs):
    employee_dao = EmployeeInfoDAO(db)
    updated_employee = await employee_dao.update(employee_id, **kwargs)
    return {
        "employee_id": updated_employee.EmployeeID,
        "employee_name": updated_employee.EmployeeName,
        "queue": updated_employee.Queue,
        "available_shift": updated_employee.AvailableShift,
        "current_working_queue_id": updated_employee.CurrentWorkingQueueID
    }