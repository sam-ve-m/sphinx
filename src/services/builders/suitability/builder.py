# STANDARD LIBS
from typing import Optional, Tuple, List

# SPHINX
from src.exceptions.exceptions import InternalServerError
from src.utils.suitability_calc import SuitabilityCalc


class SuitabilityAnswersProfileBuilder:
    def __init__(self, suitability_calc=SuitabilityCalc()):
        self.__suitability_calc = suitability_calc
        self.__suitability: dict = {}

    @property
    def suitability(self) -> dict:
        return self.__suitability

    @suitability.setter
    def suitability(self, suitability: dict) -> Optional[Exception]:
        if not suitability:
            # Exception
            pass

        self.__suitability = suitability
        return

    @property
    def profile(self) -> dict:
        best_answer = self.__get_questions_with_best_answer()
        answers = self.__calc_suitability_profile(best_answer)
        answers_profile_composition = {
            "score": 0,
            "suitability_version": self.suitability.get("version"),
            "answers": answers,
        }
        return answers_profile_composition

    def __get_questions_with_best_answer(self) -> List[dict]:
        """TODO IMPLEMENT"""
        pass

    @staticmethod
    def __calc_suitability_profile(questions: List[dict]) -> List[dict]:
        """TODO IMPLEMENT"""
        pass

    @staticmethod
    def __get_more_value_from_answers(answers: dict) -> int:
        highest_value = 0
        for answer in answers:
            weight = answer.get('weight')
            if weight > highest_value:
                highest_value = weight

        return highest_value

