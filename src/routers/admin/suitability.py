# STANDARD LIBS
from typing import List

# OUTSIDE LIBRARIES
from fastapi import Request, Response
from pydantic import BaseModel

# SPHINX
from src.routers.validators.base import Weight, Score, ValueText, Order
from src.controllers.suitabilities.controller import SuitabilityController
from src.controllers.base_controller import BaseController
from src.utils.jwt_utils import JWTHandler
from src.routers.routes_registers.admin import AdminRouter

router = AdminRouter.instance()


# TODO: remove from herer the validators


class Answer(Weight, ValueText):
    pass


class Question(Score, ValueText, Order):
    answers: List[Answer]


class Suitability(BaseModel):
    questions: List[Question]


@router.post("/suitability/quiz", tags=["suitability"])
async def create_quiz_suitability(suitability: Suitability, request: Request):
    jwt_data_or_error_response = JWTHandler.get_thebes_answer_from_request(
        request=request
    )
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response

    payload = {
        "x-thebes-answer": jwt_data_or_error_response,
        "suitability": suitability.dict(),
    }

    return BaseController.run(SuitabilityController.create_quiz, payload, request)
