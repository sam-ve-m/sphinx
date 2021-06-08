from typing import List
from fastapi import APIRouter, Request, Response
from src.routers.validators.base import Version, Weight, Score, ValueText, Order
from src.controllers.suitabilities.controller import SuitabilityController
from src.controllers.base_controller import BaseController
from src.utils.jwt_utils import JWTHandler

router = APIRouter()


class Answer(Weight, ValueText):
    pass


class Question(Score, ValueText, Order):
    answers: List[Answer]


class Suitability(Version):
    questions: List[Question]


@router.post("/suitability/quiz", tags=["suitability"])
async def create_quiz_suitability(suitability: Suitability, request: Request):
    return BaseController.run(
        SuitabilityController.create_quiz, suitability.dict(), request
    )


@router.post("/suitability/profile", tags=["suitability"])
async def crate_user_profile_suitability(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response

    payload = {
        "thebes_answer": jwt_data_or_error_response
    }

    return BaseController.run(
        SuitabilityController.create_profile, payload, request
    )
