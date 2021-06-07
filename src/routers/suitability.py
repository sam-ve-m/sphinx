from typing import List
from fastapi import APIRouter, Request
from src.routers.validators.base import Version, Weight, Score, ValueText, Order
from src.controllers.suitabilities.controller import SuitabilityController
from src.controllers.base_controller import BaseController

router = APIRouter()


class Answer(Weight, ValueText):
    pass


class Question(Score, ValueText, Order):
    answers: List[Answer]


class Suitability(Version):
    questions: List[Question]


@router.post("/suitabilities/quiz", tags=["suitabilities"])
async def persist_quiz_suitability(suitability: Suitability, request: Request):
    return BaseController.run(
        SuitabilityController.persist, suitability.dict(), request
    )
