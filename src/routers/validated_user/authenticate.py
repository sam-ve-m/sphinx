from fastapi import Request

from src.domain.validators.onboarding_validators import DeviceInformationOptional
from src.domain.validators.authenticate_validators import SignatureCheck
from src.services.jwts.service import JwtService
from src.controllers.base_controller import BaseController
from src.controllers.authentications.controller import AuthenticationController
from src.routers.routes_registers.validated_user import ValidatedUserRouter

router = ValidatedUserRouter.instance()


@router.get("/thebes_nock", tags=["authentication"])
async def thebes_hall(request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    return await BaseController.run(
        AuthenticationController.thebes_nock,
        {},
        request,
    )


@router.put("/thebes_hall", tags=["authentication"])
async def thebes_hall(device_information: DeviceInformationOptional, request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)

    device_and_thebes_answer_from_request = {
        "device_information": device_information.dict(),
        "x-thebes-answer": jwt_data,
    }
    return await BaseController.run(
        AuthenticationController.thebes_hall,
        device_and_thebes_answer_from_request,
        request,
    )


@router.put("/logout", tags=["authentication"])
async def logout(device_information: DeviceInformationOptional, request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)

    device_jwt_and_thebes_answer_from_request = {
        "jwt": JwtService.get_jwt_from_request(request=request),
        "jwt_user": jwt_data["user"],
        "device_information": device_information.dict(),
    }
    return await BaseController.run(
        AuthenticationController.logout,
        device_jwt_and_thebes_answer_from_request,
        request,
    )


@router.post("/validate_electronic_signature", tags=["authentication"])
async def change_electronic_signature(
    electronic_signature: SignatureCheck, request: Request
):
    electronic_signature = electronic_signature.dict()
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)

    change_electronic_signature_request = {
        "electronic_signature": electronic_signature,
        "jwt_user": jwt_data["user"],
    }
    return await BaseController.run(
        AuthenticationController.validate_electronic_signature,
        change_electronic_signature_request,
        request,
    )
