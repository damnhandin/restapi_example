from fastapi import APIRouter

from .health import router as health_router
from .v1.answers import router as answers_router
from .v1.questions import router as questions_router

api_router = APIRouter(prefix="/api")

api_router.include_router(health_router, prefix="/health", tags=["health"])
# Версия v1
api_router.include_router(questions_router, prefix="/v1", tags=["questions"])
api_router.include_router(answers_router, prefix="/v1", tags=["answers"])
