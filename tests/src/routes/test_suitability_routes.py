import json
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.routers.suitability import router as suitability_router

app = FastAPI()
app.include_router(suitability_router)
client = TestClient(app)
basic_payload_data_for_replace_values = {
    "version": 1,
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
    "version": 1,
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


def test_suitability_without_payload():
    response = client.post("/suitabilities/quiz", data=json.dumps({}))
    assert response.status_code == 422


def test_suitability_payload_without_version():
    payload = dict(basic_payload_data_for_replace_values)
    del payload["version"]
    response = client.post("/suitabilities/quiz", data=json.dumps(payload))
    assert response.status_code == 422


def test_suitability_payload_without_questions():
    payload = dict(basic_payload_data_for_replace_values)
    del payload["questions"]
    response = client.post("/suitabilities/quiz", data=json.dumps(payload))
    assert response.status_code == 422


def test_suitability_payload_without_question_value_text():
    payload = dict(basic_payload_data_for_replace_values)
    payload["questions"][0]["value_text"] = ""
    response = client.post("/suitabilities/quiz", data=json.dumps(payload))
    assert response.status_code == 422


def test_suitability_payload_without_question_score():
    payload = dict(basic_payload_data_for_replace_values)
    del payload["questions"][0]["score"]
    response = client.post("/suitabilities/quiz", data=json.dumps(payload))
    assert response.status_code == 422


def test_suitability_payload_without_question_order():
    payload = dict(basic_payload_data_for_replace_values)
    del payload["questions"][0]["order"]
    response = client.post("/suitabilities/quiz", data=json.dumps(payload))
    assert response.status_code == 422


def test_suitability_payload_without_answers():
    payload = dict(basic_payload_data_for_replace_values)
    del payload["questions"][0]["answers"]
    response = client.post("/suitabilities/quiz", data=json.dumps(payload))
    assert response.status_code == 422


def test_suitability_payload_without_answer_value_text():
    payload = dict(basic_payload_data_for_replace_values)
    del payload["questions"][1]["answers"][0]["value_text"]
    response = client.post("/suitabilities/quiz", data=json.dumps(payload))
    assert response.status_code == 422


def test_suitability_payload_without_answer_weight():
    payload = dict(basic_payload_data_for_replace_values)
    del payload["questions"][1]["answers"][0]["weight"]
    response = client.post("/suitabilities/quiz", data=json.dumps(payload))
    assert response.status_code == 422


# TODO Verify if Pydantic contains type in validator
# def test_suitability_payload_version_with_different_type():
#     payload = dict(basic_payload_data_for_mutable_type)
#     payload['version'] = "2"
#     response = client.post("/suitabilities/quiz", data=json.dumps(payload))
#     assert response.status_code == 422
#
#
# def test_suitability_payload_question_value_text_with_different_type():
#     payload = dict(basic_payload_data_for_mutable_type)
#     payload['questions'][0]['value_text'] = 123
#     response = client.post("/suitabilities/quiz", data=json.dumps(payload))
#     assert response.status_code == 422
#
#
# def test_suitability_payload_question_score_with_different_type():
#     payload = dict(basic_payload_data_for_mutable_type)
#     payload['questions'][0]['score'] = "123"
#     response = client.post("/suitabilities/quiz", data=json.dumps(payload))
#     assert response.status_code == 422
#
#
# def test_suitability_payload_question_order_with_different_type():
#     payload = dict(basic_payload_data_for_mutable_type)
#     payload['questions'][0]['order'] = "2"
#     response = client.post("/suitabilities/quiz", data=json.dumps(payload))
#     assert response.status_code == 422
