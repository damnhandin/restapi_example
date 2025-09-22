from fastapi import APIRouter

from .v1.answers import router as answers_router
from .v1.questions import router as questions_router

api_router = APIRouter(prefix="/api")

# Версия v1
api_router.include_router(questions_router, prefix="/v1", tags=["questions"])
api_router.include_router(answers_router, prefix="/v1", tags=["answers"])
