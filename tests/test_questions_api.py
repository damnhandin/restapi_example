# test_questions_api.py
from datetime import UTC, datetime

import pytest


@pytest.mark.asyncio
async def test_list_questions_200(client, db):
    async def _list_questions():
        return [
            {"text": "test", "id": 1, "created_at": datetime.now(UTC)},
            {"text": "test2", "id": 2, "created_at": datetime.now(UTC)},
        ]

    db.list_questions = _list_questions

    r = await client.get("/questions")
    assert r.status_code == 200
    body = r.json()
    assert "questions" in body
    assert isinstance(body["questions"], list)


@pytest.mark.asyncio
async def test_list_questions_500(client, db):
    async def _boom():
        raise RuntimeError("db down")

    db.list_questions = _boom

    r = await client.get("/questions")
    assert r.status_code == 500
    assert r.json()["detail"] == "Internal Server Error"


@pytest.mark.asyncio
async def test_create_question_201(client, db, valid_question_payload):
    async def _create_question(data):
        payload = data.model_dump()
        return {"id": 123, **payload, "created_at": datetime.now(UTC)}

    db.create_question = _create_question

    r = await client.post("/questions", json=valid_question_payload)
    assert r.status_code == 201
    body = r.json()
    assert body["id"] == 123


@pytest.mark.asyncio
async def test_create_question_500(client, db, valid_question_payload):
    async def _boom(data):
        raise RuntimeError("unexpected")

    db.create_question = _boom

    r = await client.post("/questions", json=valid_question_payload)
    assert r.status_code == 500
    assert r.json()["detail"] == "Internal Server Error"


@pytest.mark.asyncio
async def test_get_question_with_answers_200(client, db):
    async def _get_question(question_id: int):
        # Должно соответствовать QuestionWithAnswersRead
        return {
            "text": "test",
            "id": question_id,
            "created_at": datetime.now(UTC),
            "answers": [],
        }

    db.get_question = _get_question

    r = await client.get("/questions/42")
    assert r.status_code == 200
    assert r.json()["id"] == 42


@pytest.mark.asyncio
async def test_get_question_with_answers_404(client, db):
    async def _get_question(question_id: int):
        return None

    db.get_question = _get_question

    r = await client.get("/questions/9999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Question not found"


@pytest.mark.asyncio
async def test_get_question_with_answers_500(client, db):
    async def _boom(question_id: int):
        raise RuntimeError("crash")

    db.get_question = _boom

    r = await client.get("/questions/1")
    assert r.status_code == 500
    assert r.json()["detail"] == "Internal Server Error"


@pytest.mark.asyncio
async def test_delete_question_204(client, db):
    async def _del(question_id: int):
        return True

    db.delete_question_by_id = _del

    r = await client.delete("/questions/10")
    assert r.status_code == 204
    assert r.text == ""  # no body


@pytest.mark.asyncio
async def test_delete_question_404(client, db):
    async def _del(question_id: int):
        return False

    db.delete_question_by_id = _del

    r = await client.delete("/questions/10")
    assert r.status_code == 404
    assert r.json()["detail"] == "Question not found"


@pytest.mark.asyncio
async def test_delete_question_500(client, db):
    async def _boom(question_id: int):
        raise RuntimeError("db error")

    db.delete_question_by_id = _boom

    r = await client.delete("/questions/10")
    assert r.status_code == 500
    assert r.json()["detail"] == "Internal Server Error"
