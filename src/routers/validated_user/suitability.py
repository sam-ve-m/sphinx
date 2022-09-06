# OUTSIDE LIBRARIES
from fastapi import Request

# SPHINX
from src.controllers.suitabilities.controller import SuitabilityController
from src.controllers.base_controller import BaseController
from src.services.jwts.service import JwtService
from src.routers.routes_registers.validated_user import ValidatedUserRouter

router = ValidatedUserRouter.instance()


@router.post("/suitability/profile", tags=["suitability"])
async def crate_user_profile_suitability(request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)

    payload = {"x-thebes-answer": jwt_data}

    return await BaseController.run(
        SuitabilityController.create_profile, payload, request
    )


@router.get("/suitability/profile", tags=["suitability"])
async def get_user_profile_suitability(request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)

    payload = {"x-thebes-answer": jwt_data}

    return await BaseController.run(
        SuitabilityController.get_user_profile, payload, request
    )
