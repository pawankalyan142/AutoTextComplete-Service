from fastapi import APIRouter
from src.routes.employee_routes import employee
from src.routes.tickets_routes import tickets
from src.routes.services_routes import services


apiRouter = APIRouter()

apiRouter.include_router(tickets, prefix="/api/1.0", tags=["tickets_info"])
apiRouter.include_router(employee, prefix="/api/1.0", tags=["employee_info"])
apiRouter.include_router(services, prefix="/api/1.0", tags=["services_info"])

