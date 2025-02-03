from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from dbconfig.db_config import Base

class EmployeeInfo(Base):
    __tablename__ = "Employee_Info"  # Must match exactly with your SQL table name

    ID = Column(Integer, primary_key=True, index=True)
    EmployeeName = Column(String(255), nullable=False)
    EmployeeID = Column(Integer, unique=True, index=True, nullable=False)  
    Queue = Column(String(255))  # Fixed to match SQL DDL
    AvailableShift = Column(String(255))
    CurrentWorkingQueueID = Column(Integer)

    # Relationship to TicketInfo table
    tickets_assigned = relationship("TicketInfo", back_populates="assigned_employee", cascade="all, delete-orphan")


class TicketInfo(Base):
    __tablename__ = "Ticket_Info"  # Must match SQL table name exactly

    ID = Column(Integer, primary_key=True, index=True)
    TicketRaisedBy = Column(String(255), nullable=False)
    TicketAssignToEmployeeID = Column(Integer, ForeignKey("Employee_Info.EmployeeID", onupdate="CASCADE", ondelete="SET NULL"))
    TicketDescription = Column(Text)

    # Define relationship to EmployeeInfo (assigned employee)
    assigned_employee = relationship("EmployeeInfo", back_populates="tickets_assigned")
