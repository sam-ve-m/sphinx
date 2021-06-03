from fastapi import APIRouter, Request, Response, status
from src.utils.jwt_utils import JWTHandler
from src.controllers.base_controller import BaseController
from src.routers.validators.base import OptionalPIN, Email
from src.controllers.authentications.controller import AuthenticationController
import json

from src.i18n.i18n_resolver import i18nResolver as i18n
from src.utils.language_identifier import get_language_from_request

router = APIRouter()


class Login(Email, OptionalPIN):
    pass


@router.post("/login", tags=["authenticate"])
def login(payload: Login, request: Request):
    return BaseController.run(AuthenticationController.login, dict(payload), request)


@router.get("/thebes_gate", tags=["authenticate"])
def answer(request: Request):
    thebes_answer_data = JWTHandler.get_payload_from_request(request=request)
    if isinstance(thebes_answer_data, Response):
        return thebes_answer_data
    return BaseController.run(
        AuthenticationController.answer, thebes_answer_data, request
    )


@router.put("/forgot_password", tags=["authenticate"])
def forgot_password(payload: Login, request: Request):
    return BaseController.run(
        AuthenticationController.forgot_password, dict(payload), request
    )
