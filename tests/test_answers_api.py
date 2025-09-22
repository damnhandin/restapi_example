# test_answers_api.py
from datetime import UTC, datetime

import pytest
from sqlalchemy.exc import IntegrityError

from app.schemas.answer import AnswerCreate


@pytest.mark.asyncio
async def test_create_answer_201(client, db, valid_answer_payload):
    async def _create_answer_for_question(question_id: int, data: AnswerCreate):
        payload = data.model_dump()
        # Должно соответствовать AnswerRead
        return {
            "id": 555,
            "question_id": question_id,
            **payload,
            "created_at": datetime.now(UTC),
        }

    db.create_answer_for_question = _create_answer_for_question

    question_id = 123
    r = await client.post(
        f"/questions/{question_id}/answers", json=valid_answer_payload
    )
    assert r.status_code == 201
    body = r.json()
    assert body["id"] == 555
    assert body.get("question_id") == question_id


@pytest.mark.asyncio
async def test_create_answer_404_on_integrity_error(client, db, valid_answer_payload):
    async def _create_answer_for_question(question_id: int, data):
        # Имитация внешнего ключа на несуществующий вопрос
        raise IntegrityError("insert", "params", "fk violation")

    db.create_answer_for_question = _create_answer_for_question

    r = await client.post("/questions/999/answers", json=valid_answer_payload)
    assert r.status_code == 404
    assert r.json()["detail"] == "Question not found"


@pytest.mark.asyncio
async def test_create_answer_500_on_unexpected(client, db, valid_answer_payload):
    async def _boom(question_id: int, data):
        raise RuntimeError("unexpected")

    db.create_answer_for_question = _boom

    r = await client.post("/questions/1/answers", json=valid_answer_payload)
    assert r.status_code == 500
    assert r.json()["detail"] == "Internal Server Error"


@pytest.mark.asyncio
async def test_get_answer_200(client, db):
    async def _get_answer_by_id(answer_id: int):
        # Должно соответствовать AnswerRead
        return {
            "id": answer_id,
            "question_id": 1,
            "user_id": "e2b50b32-76ae-42f9-a012-4e5ae315645b",
            "text": "ok",
            "created_at": datetime.now(UTC),
        }

    db.get_answer_by_id = _get_answer_by_id
    answer_id = 7
    r = await client.get(f"/answers/{answer_id}")
    assert r.status_code == 200
    assert r.json()["id"] == answer_id


@pytest.mark.asyncio
async def test_get_answer_404(client, db):
    async def _get_answer_by_id(answer_id: int):
        return None

    db.get_answer_by_id = _get_answer_by_id

    r = await client.get("/answers/777")
    assert r.status_code == 404
    assert r.json()["detail"] == "Answer not found"


@pytest.mark.asyncio
async def test_get_answer_500(client, db):
    async def _boom(answer_id: int):
        raise RuntimeError("db fail")

    db.get_answer_by_id = _boom

    r = await client.get("/answers/1")
    assert r.status_code == 500
    assert r.json()["detail"] == "Internal Server Error"


@pytest.mark.asyncio
async def test_delete_answer_204(client, db):
    async def _del(answer_id: int):
        return True

    db.delete_answer_by_id = _del

    r = await client.delete("/answers/5")
    assert r.status_code == 204
    assert r.text == ""


@pytest.mark.asyncio
async def test_delete_answer_404(client, db):
    async def _del(answer_id: int):
        return False

    db.delete_answer_by_id = _del

    r = await client.delete("/answers/5")
    assert r.status_code == 404
    assert r.json()["detail"] == "Answer not found"


@pytest.mark.asyncio
async def test_delete_answer_500_on_exception(client, db):
    async def _boom(answer_id: int):
        raise RuntimeError("db fail")

    db.delete_answer_by_id = _boom

    r = await client.delete("/answers/5")
    assert r.status_code == 500
    assert r.json()["detail"] == "Internal Server Error"
