# STANDARD LIBS
from datetime import datetime

# OUTSIDE LIBRARIES
from typing import List

from fastapi import status

# SPHINX
from src.exceptions.exceptions import InternalServerError, BadRequestError
from src.repositories.base_repository import BaseRepository
from src.repositories.suitability.repository import SuitabilityRepository, SuitabilityUserProfileRepository, \
    SuitabilityAnswersRepository
from src.repositories.user.repository import UserRepository
from src.services.builders.suitability.builder import SuitabilityProfileBuilder
from src.interfaces.services.suitability.interface import ISuitability


class SuitabilityService(ISuitability):
    @staticmethod
    def __get_last_suitability_answers(
            suitability_answers_repository: BaseRepository = SuitabilityAnswersRepository()
    ) -> List[dict]:
        pass

    @staticmethod
    def __get_score_for_aggressive_profile() -> int:
        pass

    @staticmethod
    def __update_suitability_score_and_submission_date_in_user_db(
            user_repository: BaseRepository, user_email: str, score: int, submission_date: datetime
    ) -> None or Exception:
        """TODO IMPLEMENT EXCEPTIONS"""
        old = user_repository.find_one({"_id": user_email})
        if not old:
            raise BadRequestError("common.register_not_exists")
        new = dict(old)
        new.update({
            "suitability": {
                "score": score,
                "submission_date": submission_date
            }
        })
        if user_repository.update_one(old=old, new=new):
            return

    @staticmethod
    def __insert_suitability_answers_and_submission_date_in_user_profile_db(
            suitability_user_profile_repository: BaseRepository,
            answers: List[dict],
            submission_date: datetime,
            user_email: str
    ) -> None or Exception:
        """TODO IMPLEMENT EXCEPTIONS"""
        payload = {
            "email": user_email,
            "date": submission_date,
            "answered_questions": answers

        }
        if suitability_user_profile_repository.insert(payload):
            return

    @staticmethod
    def create_quiz(payload: dict, suitability_repository=SuitabilityRepository()) -> dict:
        payload.update({"date": datetime.utcnow()})

        if suitability_repository.insert(payload):
            return {
                "status_code": status.HTTP_201_CREATED,
                "message_key": "suitabilities.create_quiz",
            }
        else:
            raise InternalServerError("common.process_issue")

    @staticmethod
    def create_profile(
        payload,
        user_repository=UserRepository(),
        suitability_repository=SuitabilityRepository(),
        suitability_user_profile_repository=SuitabilityUserProfileRepository(),
        builder_suitability_profile=SuitabilityProfileBuilder(),
    ) -> dict:
        """TODO IMPLEMENT"""
        thebes_answer = payload.get("thebes_answer")
        user_email = thebes_answer.get("email")
        suitability_submission_date = datetime.utcnow()
        answers = SuitabilityService.__get_last_suitability_answers()
        score = SuitabilityService.__get_score_for_aggressive_profile()
        (SuitabilityService
         .__update_suitability_score_and_submission_date_in_user_db(user_repository=user_repository,
                                                                    user_email=user_email,
                                                                    score=score,
                                                                    submission_date=suitability_submission_date)
         )
        (SuitabilityService
            .__insert_suitability_answers_and_submission_date_in_user_profile_db(
            suitability_user_profile_repository=suitability_user_profile_repository,
            user_email=user_email,
            answers=answers,
            submission_date=suitability_submission_date)
        )

        return {
            "status_code": status.HTTP_201_CREATED,
            "message_key": "suitabilities.create_profile",
        }
