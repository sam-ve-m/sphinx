from fastapi import APIRouter, Request
from pydantic import BaseModel
from src.utils.jwt_utils import JWTHandler
from src.controllers.base_controller import BaseController
from src.controllers.authentications.controller import AuthenticationController
from typing import Optional

router = APIRouter()


class Login(BaseModel):
    email: str
    pin: Optional[int]


@router.post("/login", tags=["authenticate"])
async def login(payload: Login, request: Request):
    return BaseController.run(AuthenticationController.login, dict(payload), request)


@router.get("/thebes_gate", tags=["authenticate"])
async def answer(request: Request):
    thebes_answer_data = JWTHandler.get_payload_from_request(request=request)
    return BaseController.run(
        AuthenticationController.answer, thebes_answer_data, request
    )


@router.put("/forgot_password", tags=["authenticate"])
async def forgot_password(payload: Login, request: Request):
    return BaseController.run(
        AuthenticationController.forgot_password, dict(payload), request
    )
