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
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    return BaseController.run(
        AuthenticationController.answer, jwt_data_or_error_response, request
    )


@router.put("/forgot_password", tags=["authenticate"])
def forgot_password(payload: Login, request: Request):
    return BaseController.run(
        AuthenticationController.forgot_password, dict(payload), request
    )
