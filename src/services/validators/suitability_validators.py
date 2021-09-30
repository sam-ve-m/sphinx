from typing import List

from pydantic import BaseModel

from src.services.validators.onboarding_validators import Weight, ValueText, Score, Order


class Answer(Weight, ValueText):
    pass


class Question(Score, ValueText, Order):
    answers: List[Answer]


class Suitability(BaseModel):
    questions: List[Question]
