from fastapi import APIRouter, Request, Response, status
from src.utils.jwt_utils import JWTHandler
from src.controllers.base_controller import BaseController
from src.routers.validators.base import OptionalPIN, Email
from src.controllers.authentications.controller import AuthenticationController
from src.routers.validators.base import SignatureCheck

router = APIRouter()


class Login(Email, OptionalPIN):
    pass


@router.post("/login", tags=["authentication"])
def login(payload: Login, request: Request):
    return BaseController.run(AuthenticationController.login, dict(payload), request)


@router.get("/thebes_gate", tags=["authentication"])
def answer(request: Request):
    # This will be called from the frontend after open TARGET_LINK (.env) received on the email confirmation
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    return BaseController.run(
        AuthenticationController.thebes_gate, jwt_data_or_error_response, request
    )


@router.get("/thebes_hall", tags=["authentication"])
def thebes_hall(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    return BaseController.run(
        AuthenticationController.thebes_hall, jwt_data_or_error_response, request
    )


@router.get("/logout", tags=["authentication"])
def logout(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "jwt": JWTHandler.get_jwt_from_request(request=request),
        "email": jwt_data_or_error_response.get("email"),
    }
    return BaseController.run(
        AuthenticationController.logout, payload, request
    )


@router.post("/validate_electronic_signature", tags=["authentication"])
def change_electronic_signature(electronic_signature: SignatureCheck, request: Request):
    electronic_signature = electronic_signature.dict()
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "electronic_signature": electronic_signature,
        "email": jwt_data_or_error_response.get("email"),
    }
    return BaseController.run(
        AuthenticationController.validate_electronic_signature, payload, request
    )
