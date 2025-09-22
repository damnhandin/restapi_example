# conftest.py

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.api.v1 import (
    answers as answers_router_module,
    questions as questions_router_module,
)

# === Фейковая "БД" с асинхронными методами =============================


class FakeDB:
    """
    Фейковая БД. Методы можно переназначать в конкретных тестах:
    """

    async def list_questions(self): ...

    async def create_question(self, data): ...

    async def get_question(self, question_id: int): ...

    async def delete_question_by_id(self, question_id: int): ...

    async def create_answer_for_question(self, question_id: int, data): ...

    async def get_answer_by_id(self, answer_id: int): ...

    async def delete_answer_by_id(self, answer_id: int): ...


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(questions_router_module.router)
    app.include_router(answers_router_module.router)
    return app


@pytest.fixture
def db():
    return FakeDB()


@pytest.fixture
def override_get_db(app, db):
    from app.api.v1 import deps

    async def _override():
        return db

    app.dependency_overrides[deps.get_db] = _override
    yield
    app.dependency_overrides.clear()


# ВАЖНО: асинхронная фикстура должна быть под pytest_asyncio.fixture
@pytest_asyncio.fixture
async def client(app, override_get_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as c:
        yield c


# === Хелперы для валидных пэйлоадов ====================================


@pytest.fixture
def valid_question_payload():
    """
    МИНИМАЛЬНО валидный payload под QuestionCreate.
    """
    return {"text": "Правда, что музыка меняет восприятие вкуса?"}


@pytest.fixture
def valid_answer_payload():
    """
    МИНИМАЛЬНО валидный payload под AnswerCreate.
    """
    return {
        "user_id": "e2b50b32-76ae-42f9-a012-4e5ae315645b",
        "text": "Мне кажется, что да",
    }
