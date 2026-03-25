from fastapi import APIRouter
from infrastructure.web.api.api_v1.endpoints import auth, task, user

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(task.router, prefix="/tasks", tags=["task"])
