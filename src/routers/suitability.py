from typing import List
from fastapi import APIRouter, Request
from src.routers.validators.base import Version, Date, Weight, Score, ValueText
from src.controllers.suitability.controller import SuitabilityController
from src.controllers.base_controller import BaseController

router = APIRouter()


class Answer(Weight, ValueText):
    pass


class Question(Score, ValueText):
    answers: List[Answer]


class Suitability(Version, Date):
    questions: List[Question]


@router.post("/suitability/quiz", tags=["authenticate"])
def persist_quiz_suitability(suitability: Suitability, request: Request):
    return BaseController.run(SuitabilityController.persist, dict(suitability), request)


