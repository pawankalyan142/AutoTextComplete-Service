from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from models import EmployeeInfo
from fastapi import HTTPException

class EmployeeInfoDAO:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find(self, employee_id: int):
        try:
            result = await self.db.execute(select(EmployeeInfo).filter(EmployeeInfo.EmployeeID == employee_id))
            employee = result.scalars().first()
            if not employee:
                raise HTTPException(status_code=404, detail="Employee not found")
            return employee
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def count(self):
        try:
            result = await self.db.execute(select([EmployeeInfo.EmployeeID]).distinct())
            return len(result.scalars().all())  # Return the count of distinct employees
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def update(self, employee_id: int, **kwargs):
        try:
            employee = await self.find(employee_id)  # Reuse the find method to get the employee
            
            # Update employee attributes
            for key, value in kwargs.items():
                setattr(employee, key, value)

            self.db.add(employee)
            await self.db.commit()
            return employee
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    async def find_all(self):
        try:
            result = await self.db.execute(select(EmployeeInfo))
            employees = result.scalars().all()  # Fetch all employees from the database
            return employees
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
