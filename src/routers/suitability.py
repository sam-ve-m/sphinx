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


@router.post("/suitability/quiz", tags=["suitability"])
async def create_quiz_suitability(suitability: Suitability, request: Request):
    return BaseController.run(
        SuitabilityController.create_quiz, suitability.dict(), request
    )


@router.post("/suitability/profile", tags=["suitability"])
async def crate_user_profile_suitability(suitability: Suitability, request: Request):
    return BaseController.run(
        SuitabilityController.create_profile, suitability.dict(), request
    )


