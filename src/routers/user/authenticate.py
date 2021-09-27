from fastapi import Request, Response

from src.routers.validators.onboarding_validators import DeviceInformationOptional
from src.utils.jwt_utils import JWTHandler
from src.controllers.base_controller import BaseController
from src.routers.validators.base import OptionalPIN, Email
from src.controllers.authentications.controller import AuthenticationController
from src.routers.validators.base import SignatureCheck
from src.routers.routes_registers.user import UserRouter

router = UserRouter.instance()


class Login(Email, OptionalPIN):
    pass


@router.get("/thebes_gate", tags=["authentication"])
def answer(request: Request):
    # This will be called from the frontend after open TARGET_LINK (.env) received on the email confirmation
    jwt_data = JWTHandler.get_thebes_answer_from_request(request=request)

    return BaseController.run(
        AuthenticationController.thebes_gate,
        jwt_data,
        request,
    )


@router.put("/thebes_hall", tags=["authentication"])
def thebes_hall(device_information: DeviceInformationOptional, request: Request):
    jwt_data = JWTHandler.get_thebes_answer_from_request(request=request)

    device_and_thebes_answer_from_request = {
        "device_information": device_information.dict(),
        "x-thebes-answer": jwt_data,
    }
    return BaseController.run(
        AuthenticationController.thebes_hall,
        device_and_thebes_answer_from_request,
        request,
    )


@router.get("/thebes_hall", tags=["authentication"])
def get_thebes_hall(request: Request):
    jwt_data = JWTHandler.get_thebes_answer_from_request(request=request)

    return BaseController.run(
        AuthenticationController.get_thebes_hall,
        jwt_data,
        request,
    )


@router.put("/logout", tags=["authentication"])
def logout(device_information: DeviceInformationOptional, request: Request):
    jwt_data = JWTHandler.get_thebes_answer_from_request(request=request)

    device_jwt_and_thebes_answer_from_request = {
        "jwt": JWTHandler.get_jwt_from_request(request=request),
        "email": jwt_data["email"],
        "device_information": device_information.dict(),
    }
    return BaseController.run(
        AuthenticationController.logout,
        device_jwt_and_thebes_answer_from_request,
        request,
    )


@router.post("/validate_electronic_signature", tags=["authentication"])
def change_electronic_signature(electronic_signature: SignatureCheck, request: Request):
    electronic_signature = electronic_signature.dict()
    jwt_data = JWTHandler.get_thebes_answer_from_request(request=request)

    change_electronic_signature_request = {
        "electronic_signature": electronic_signature,
        "email": jwt_data["email"],
    }
    return BaseController.run(
        AuthenticationController.validate_electronic_signature,
        change_electronic_signature_request,
        request,
    )
