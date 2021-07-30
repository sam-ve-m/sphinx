# STANDARD LIBS
from functools import reduce
from operator import mul
from typing import Optional, List

# SPHINX
from src.exceptions.exceptions import InternalServerError


class SuitabilityAnswersProfileBuilder:
    def __init__(self):
        self.__suitability: dict = {}

    @property
    def suitability(self) -> dict:
        return self.__suitability

    @suitability.setter
    def suitability(self, suitability: dict) -> Optional[Exception]:
        if type(suitability) is not dict:
            raise InternalServerError("common.process_issue")
        self.__suitability = suitability
        return

    @property
    def profile(self) -> dict:
        if not self.suitability:
            raise InternalServerError("common.process_issue")

        questions_with_best_answers = self.__get_questions_with_best_answer()
        score_profile = self.__calc_suitability_score_profile(
            questions_with_best_answers
        )
        answers_profile_composition = {
            "score": score_profile,
            "suitability_version": self.suitability.get("version"),
            "suitability_submission_date": self.suitability.get("date"),
            "answers": questions_with_best_answers,
        }
        return answers_profile_composition

    def __get_questions_with_best_answer(self) -> List[dict]:
        questions_with_best_answers = []
        for question in self.__suitability.get("questions"):
            buffer_answer = {"value_text": "", "weight": 0}
            for answer in question.get("answers"):
                if answer.get("weight") > buffer_answer.get("weight"):
                    buffer_answer["weight"] = answer.get("weight")
                    buffer_answer["value_text"] = answer.get("value_text")
            questions_with_best_answers.append(
                {
                    "question": question.get("value_text"),
                    "question_id": question.get("order"),
                    "question_score": question.get("score"),
                    "answer": buffer_answer.get("value_text"),
                    "answer_weight": buffer_answer.get("weight"),
                }
            )
        return questions_with_best_answers

    @staticmethod
    def __calc_suitability_score_profile(questions: List[dict]) -> float:

        _question_score_with_max_response_wight = [
            question.get("question_score") * question.get("answer_weight")
            for question in questions
        ]
        question_score_with_max_response_wight = reduce(
            lambda x, y: x + y, _question_score_with_max_response_wight
        )
        score_profile = (
            question_score_with_max_response_wight
            / question_score_with_max_response_wight
        )
        return score_profile
