import json

from fastapi import FastAPI, Request
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


def test_create_user_profile_is_active():
    response = client.post("/suitability/profile", data=json.dumps({}))
    assert response.status_code == 401


def test_create_user_profile_is_active_with_headers():
    response = client.post("/suitability/profile", data=json.dumps({}), headers={"thebes_answer": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJuYW1lIjogIk1hcmNvIFNpZXZlcnMgZGUgQWxtZWlkYSIsICJlbWFpbCI6ICJtc2FAbGlvbnguY29tLmJyIiwgInNjb3BlIjogeyJ2aWV3X3R5cGUiOiBudWxsLCAiZmVhdHVyZXMiOiBbXX0sICJpc19hY3RpdmUiOiBmYWxzZSwgInRlcm1zIjogeyJ0ZXJtX2FwcGxpY2F0aW9uIjogbnVsbCwgInRlcm1fb3Blbl9hY2NvdW50IjogbnVsbCwgInRlcm1fcmV0YWlsX2xpcXVpZF9wcm92aWRlciI6IG51bGwsICJ0ZXJtX3JlZnVzYWwiOiBudWxsLCAidGVybV9ub25fY29tcGxpYW5jZSI6IG51bGx9LCAic3VpdGFiaWxpdHlfbW9udGhzX3Bhc3QiOiAwLCAidXNlcl9hY2NvdW50X2RhdGFfbW9udGhzX3Bhc3QiOiBudWxsfQ.QsThERITKm-1wFvXWk62NiO3siSUZdrXeTyb2zZz_BJY1EVnwDm3RCLS1ADvlgzzcEigKbCO7_xbRjzdVTBw9pMm7V8tSrqA9zxe1Smxv3ER179qarQfR4jv8dCjTobZJV-17LEvKIQaMqtd2jviL-LuH-TJgtuS9Cy05nrmP5izUGbyMc7vzTB2c9lLM-gVkYM7zaCwyZa9GmBLWi0m4LfBX9-Uj5HxWk-6_C6lT4dV2n8-YEEoAKoZ07ysEU50iklM1Tyfiw_959GVTlajdF8jHqIq2QxbcjNRi4qyGs1PiHVGv_KeoaGbEazfgMSQ55DGGt8idwfEs4uvczsKnw"})
    assert response.status_code == 201


def test_get_user_profile_is_active():
    response = client.get("/suitability/profile", data=json.dumps({}))
    assert response.status_code == 401


def test_get_user_profile_with_headers():
    response = client.get("/suitability/profile", data=json.dumps({}), headers={"thebes_answer": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJuYW1lIjogIk1hcmNvIFNpZXZlcnMgZGUgQWxtZWlkYSIsICJlbWFpbCI6ICJtc2FAbGlvbnguY29tLmJyIiwgInNjb3BlIjogeyJ2aWV3X3R5cGUiOiBudWxsLCAiZmVhdHVyZXMiOiBbXX0sICJpc19hY3RpdmUiOiBmYWxzZSwgInRlcm1zIjogeyJ0ZXJtX2FwcGxpY2F0aW9uIjogbnVsbCwgInRlcm1fb3Blbl9hY2NvdW50IjogbnVsbCwgInRlcm1fcmV0YWlsX2xpcXVpZF9wcm92aWRlciI6IG51bGwsICJ0ZXJtX3JlZnVzYWwiOiBudWxsLCAidGVybV9ub25fY29tcGxpYW5jZSI6IG51bGx9LCAic3VpdGFiaWxpdHlfbW9udGhzX3Bhc3QiOiAwLCAidXNlcl9hY2NvdW50X2RhdGFfbW9udGhzX3Bhc3QiOiBudWxsfQ.QsThERITKm-1wFvXWk62NiO3siSUZdrXeTyb2zZz_BJY1EVnwDm3RCLS1ADvlgzzcEigKbCO7_xbRjzdVTBw9pMm7V8tSrqA9zxe1Smxv3ER179qarQfR4jv8dCjTobZJV-17LEvKIQaMqtd2jviL-LuH-TJgtuS9Cy05nrmP5izUGbyMc7vzTB2c9lLM-gVkYM7zaCwyZa9GmBLWi0m4LfBX9-Uj5HxWk-6_C6lT4dV2n8-YEEoAKoZ07ysEU50iklM1Tyfiw_959GVTlajdF8jHqIq2QxbcjNRi4qyGs1PiHVGv_KeoaGbEazfgMSQ55DGGt8idwfEs4uvczsKnw"})
    assert response.status_code == 201
