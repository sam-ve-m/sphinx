from fastapi import Request, Response

from src.routers.validators.onboarding_validators import DeviceInformationOptional
from src.utils.jwt_utils import JWTHandler
from src.controllers.base_controller import BaseController
from src.routers.validators.base import OptionalPIN, Email
from src.controllers.authentications.controller import AuthenticationController
from src.routers.validators.base import SignatureCheck
from src.routers.router_registers.user import UserRouter

router = UserRouter.instance()


class Login(Email, OptionalPIN):
    pass


@router.get("/thebes_gate", tags=["authentication"])
def answer(request: Request):
    # This will be called from the frontend after open TARGET_LINK (.env) received on the email confirmation
    thebes_answer_from_request_or_error = JWTHandler.get_thebes_answer_from_request(request=request)
    if isinstance(thebes_answer_from_request_or_error, Response):
        return thebes_answer_from_request_or_error
    return BaseController.run(
        AuthenticationController.thebes_gate, thebes_answer_from_request_or_error, request
    )


@router.put("/thebes_hall", tags=["authentication"])
def thebes_hall(device_information: DeviceInformationOptional, request: Request):
    thebes_answer_from_request_or_error = JWTHandler.get_thebes_answer_from_request(request=request)
    if isinstance(thebes_answer_from_request_or_error, Response):
        return thebes_answer_from_request_or_error
    device_and_thebes_answer_from_request = {
        "device_information": device_information.dict(),
        "x-thebes-answer": thebes_answer_from_request_or_error
    }
    return BaseController.run(
        AuthenticationController.thebes_hall, device_and_thebes_answer_from_request, request
    )


@router.get("/thebes_hall", tags=["authentication"])
def get_thebes_hall(request: Request):
    thebes_answer_from_request_or_error = JWTHandler.get_thebes_answer_from_request(request=request)
    if isinstance(thebes_answer_from_request_or_error, Response):
        return thebes_answer_from_request_or_error
    return BaseController.run(
        AuthenticationController.get_thebes_hall, thebes_answer_from_request_or_error, request
    )


@router.put("/logout", tags=["authentication"])
def logout(device_information: DeviceInformationOptional, request: Request):
    thebes_answer_from_request_or_error = JWTHandler.get_thebes_answer_from_request(request=request)
    if isinstance(thebes_answer_from_request_or_error, Response):
        return thebes_answer_from_request_or_error
    device_jwt_and_thebes_answer_from_request = {
        "jwt": JWTHandler.get_jwt_from_request(request=request),
        "email": thebes_answer_from_request_or_error.get("email"),
        "device_information": device_information.dict(),
    }
    return BaseController.run(
        AuthenticationController.logout, device_jwt_and_thebes_answer_from_request, request
    )


@router.post("/validate_electronic_signature", tags=["authentication"])
def change_electronic_signature(electronic_signature: SignatureCheck, request: Request):
    electronic_signature = electronic_signature.dict()
    jwt_data_or_error_response = JWTHandler.get_thebes_answer_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    change_electronic_signature_request = {
        "electronic_signature": electronic_signature,
        "email": jwt_data_or_error_response.get("email"),
    }
    return BaseController.run(
        AuthenticationController.validate_electronic_signature, change_electronic_signature_request, request
    )
