from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from dbconfig.db_config import Base

class EmployeeInfo(Base):
    __tablename__ = "employee_info"
    
    ID = Column(Integer, primary_key=True, index=True)
    EmployeeName = Column(String(255))
    EmployeeID = Column(Integer, unique=True, index=True)  # Assuming EmployeeID is unique
    Queue = Column(Integer, unique=True, index=True)
    AvailableShift = Column(String(255))
    CurrentWorkingQueueID = Column(Integer)

    # Relationship to TicketInfo table
    tickets_assigned = relationship("TicketInfo", back_populates="assigned_employee")

class TicketInfo(Base):
    __tablename__ = "ticket_info"
    
    ID = Column(Integer, primary_key=True, index=True)
    TicketRaisedBy = Column(String(255))
    TicketAssignToEmployeeID = Column(Integer, ForeignKey("employee_info.EmployeeID", onupdate="RESTRICT", ondelete="RESTRICT"))
    TicketDescription = Column(Text)

    # Define relationship to EmployeeInfo (assigned employee)
    assigned_employee = relationship("EmployeeInfo", back_populates="tickets_assigned")
