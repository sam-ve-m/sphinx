import json

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.routers.suitability import router as suitability_router

app = FastAPI()
app.include_router(suitability_router)
client = TestClient(app)
basic_payload_data_for_replace_values = {
    "questions": [
        {
            "value_text": "primeira pergunta",
            "score": 20,
            "order": 1,
            "answers": [
                {"value_text": "primeira resposta", "weight": 20},
                {"value_text": "segunda resposta", "weight": 25},
                {"value_text": "terceira resposta", "weight": 22},
            ],
        },
        {
            "value_text": "segunda pergunta",
            "score": 20,
            "order": 2,
            "answers": [
                {"value_text": "primeira resposta", "weight": 20},
                {"value_text": "segunda resposta", "weight": 25},
                {"value_text": "terceira resposta", "weight": 22},
            ],
        },
    ],
}

basic_payload_data_for_mutable_type = {
    "questions": [
        {
            "value_text": "primeira pergunta",
            "score": 20,
            "order": 1,
            "answers": [
                {"value_text": "primeira resposta", "weight": 20},
                {"value_text": "segunda resposta", "weight": 25},
                {"value_text": "terceira resposta", "weight": 22},
            ],
        }
    ],
}


def test_suitability_quiz_without_payload():
    response = client.post("/suitability/quiz", data=json.dumps({}))
    assert response.status_code == 422


def test_suitability_quiz_payload_without_questions():
    payload = dict(basic_payload_data_for_replace_values)
    del payload["questions"]
    response = client.post("/suitability/quiz", data=json.dumps(payload))
    assert response.status_code == 422


def test_suitability_quiz_payload_without_question_value_text():
    payload = dict(basic_payload_data_for_replace_values)
    payload["questions"][0]["value_text"] = ""
    response = client.post("/suitability/quiz", data=json.dumps(payload))
    assert response.status_code == 422


def test_suitability_quiz_payload_without_question_score():
    payload = dict(basic_payload_data_for_replace_values)
    del payload["questions"][0]["score"]
    response = client.post("/suitability/quiz", data=json.dumps(payload))
    assert response.status_code == 422


def test_suitability_quiz_payload_without_question_order():
    payload = dict(basic_payload_data_for_replace_values)
    del payload["questions"][0]["order"]
    response = client.post("/suitability/quiz", data=json.dumps(payload))
    assert response.status_code == 422


def test_suitability_quiz_payload_without_answers():
    payload = dict(basic_payload_data_for_replace_values)
    del payload["questions"][0]["answers"]
    response = client.post("/suitability/quiz", data=json.dumps(payload))
    assert response.status_code == 422


def test_suitability_quiz_payload_without_answer_value_text():
    payload = dict(basic_payload_data_for_replace_values)
    del payload["questions"][1]["answers"][0]["value_text"]
    response = client.post("/suitability/quiz", data=json.dumps(payload))
    assert response.status_code == 422


def test_suitability_quiz_payload_without_answer_weight():
    payload = dict(basic_payload_data_for_replace_values)
    del payload["questions"][1]["answers"][0]["weight"]
    response = client.post("/suitability/quiz", data=json.dumps(payload))
    assert response.status_code == 422


def test_suitability_profile_without_payload():
    res = client.post("/suitability/profile", data=json.dumps({}))
    assert res.status_code == 401
