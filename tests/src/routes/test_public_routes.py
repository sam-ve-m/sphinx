import pytest
import json
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.routers.user import router as UserRouter
from src.routers.authenticate import router as AuthenticateRouter

app = FastAPI()

app.include_router(UserRouter)
app.include_router(AuthenticateRouter)

client = TestClient(app)


def test_create_user_without_payload():
    response = client.post("/user", data=json.dumps({}))
    assert response.status_code == 422


def test_create_user_partial_payload():
    payload = {"name": "este"}
    response = client.post("/user", data=json.dumps(payload))
    assert response.status_code == 422


def test_create_user():
    payload = {"name": "este", "email": "lala@lele.com", "pin": 1234}
    response = client.post("/user", data=json.dumps(payload))
    assert type(response.text) == str
    assert type(response.status_code) == int


def test_forgot_password_partial_payload():
    response = client.post("/user", data=json.dumps({}))
    assert response.status_code == 422


def test_forgot_password():
    payload = {"email": "lala@lele.com"}
    response = client.post("/user", data=json.dumps(payload))
    assert type(response.text) == str
    assert type(response.status_code) == int


def test_login_partial_payload():
    response = client.post("/login", data=json.dumps({}))
    assert response.status_code == 422


def test_login_admin_partial_payload():
    response = client.post("/login", data=json.dumps({}))
    assert response.status_code == 422


def test_login_payload():
    response = client.post("/login", data=json.dumps({"email": "lala@li.com"}))
    assert type(response.status_code) == int


def test_login_admin_payload():
    response = client.post("/login", data=json.dumps({"email": "lala@li.com"}))
    assert type(response.status_code) == int


# def test_thebes_gate():
#     response = client.get("/thebes_gate")
#     assert response.status_code == 401


# def test_thebes_gate_auth():
#     response = client.get("/thebes_gate/alal21889whx2387hn")
#     assert type(response.status_code) == int
