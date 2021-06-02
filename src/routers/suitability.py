from typing import List
from fastapi import APIRouter
from src.routers.validators.base import Version, Date, Weight, Score, ValueText

router = APIRouter()


class Answer(Weight, ValueText):
    pass


class Question(Score, ValueText):
    answers: List[Answer]


class Suitability(Version, Date):
    questions: List[Question]


@router.post("/suitability/quiz", tags=["authenticate"])
def persist_quiz_suitability(suitability: Suitability):
    return suitability, 200


