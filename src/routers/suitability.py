# STANDARD LIBS
from typing import List

# OUTSIDE LIBRARIES
from fastapi import APIRouter, Request, Response

# SPHINX
from src.controllers.suitabilities.controller import SuitabilityController
from src.controllers.base_controller import BaseController
from src.routers.validators.suitability_validators import Suitability
from src.utils.jwt_utils import JWTHandler

router = APIRouter()


@router.post("/suitability/quiz", tags=["suitability"])
async def create_quiz_suitability(suitability: Suitability, request: Request):
    jwt_data_or_error_response = JWTHandler.get_thebes_answer_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response

    payload = {
        "x-thebes-answer": jwt_data_or_error_response,
        "suitability": suitability.dict(),
    }

    return BaseController.run(SuitabilityController.create_quiz, payload, request)


@router.post("/suitability/profile", tags=["suitability"])
async def crate_user_profile_suitability(request: Request):
    jwt_data_or_error_response = JWTHandler.get_thebes_answer_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response

    payload = {"x-thebes-answer": jwt_data_or_error_response}

    return BaseController.run(SuitabilityController.create_profile, payload, request)


@router.get("/suitability/profile", tags=["suitability"])
async def get_user_profile_suitability(request: Request):
    jwt_data_or_error_response = JWTHandler.get_thebes_answer_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response

    payload = {"x-thebes-answer": jwt_data_or_error_response}

    return BaseController.run(SuitabilityController.get_user_profile, payload, request)
