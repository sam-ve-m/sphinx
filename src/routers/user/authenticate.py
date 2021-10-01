from fastapi import Request

from src.domain.validators.onboarding_validators import DeviceInformationOptional
from src.domain.validators.authenticate_validators import SignatureCheck
from src.services.jwts.service import JwtService
from src.controllers.base_controller import BaseController
from src.controllers.authentications.controller import AuthenticationController
from src.routers.routes_registers.user import UserRouter

router = UserRouter.instance()


@router.put("/thebes_hall", tags=["authentication"])
def thebes_hall(device_information: DeviceInformationOptional, request: Request):
    jwt_data = JwtService.get_thebes_answer_from_request(request=request)

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
    jwt_data = JwtService.get_thebes_answer_from_request(request=request)

    return BaseController.run(
        AuthenticationController.get_thebes_hall,
        jwt_data,
        request,
    )


@router.put("/logout", tags=["authentication"])
def logout(device_information: DeviceInformationOptional, request: Request):
    jwt_data = JwtService.get_thebes_answer_from_request(request=request)

    device_jwt_and_thebes_answer_from_request = {
        "jwt": JwtService.get_jwt_from_request(request=request),
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
    jwt_data = JwtService.get_thebes_answer_from_request(request=request)

    change_electronic_signature_request = {
        "electronic_signature": electronic_signature,
        "email": jwt_data["email"],
    }
    return BaseController.run(
        AuthenticationController.validate_electronic_signature,
        change_electronic_signature_request,
        request,
    )
