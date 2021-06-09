# STANDARD LIBS
from datetime import datetime

# OUTSIDE LIBRARIES
from typing import List, Tuple, Union, Optional

from fastapi import status

# SPHINX
from src.exceptions.exceptions import InternalServerError, BadRequestError
from src.repositories.base_repository import BaseRepository
from src.repositories.suitability.repository import (
    SuitabilityRepository,
    SuitabilityUserProfileRepository,
    SuitabilityAnswersRepository
)
from src.repositories.user.repository import UserRepository
from src.interfaces.services.suitability.interface import ISuitability


class SuitabilityService(ISuitability):
    @staticmethod
    def create_quiz(payload: dict, suitability_repository=SuitabilityRepository()) -> dict:
        suitability = payload.get("suitability")
        suitability.update({"date": datetime.utcnow()})

        if suitability_repository.insert(suitability):
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
    ) -> Union[dict, Exception]:
        thebes_answer: dict = payload.get("thebes_answer")
        user_email: str = thebes_answer.get("email")
        suitability_submission_date = datetime.utcnow()
        answers, score = SuitabilityService.__get_last_suitability_answers_and_score()
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

    @staticmethod
    def get_user_profile(
            payload: dict, suitability_user_profile_repository=SuitabilityUserProfileRepository()
    ) -> Union[dict, Exception]:
        thebes_answer: dict = payload.get("thebes_answer")
        user_email: str = thebes_answer.get("email")
        user_profile = SuitabilityService.__get_last_user_profile(
            suitability_user_profile_repository=suitability_user_profile_repository,
            email=user_email)
        return user_profile

    @staticmethod
    def __insert_new_suitability_answers_list():
        pass

    @staticmethod
    def __get_last_suitability_answers_and_score(
            suitability_answers_repository: BaseRepository = SuitabilityAnswersRepository()
    ) -> Union[Tuple[List[dict], int], Exception]:
        _answers = list(suitability_answers_repository.find_all().sort("_id", -1).limit(1))
        if not _answers:
            raise InternalServerError("suitability.error.no_answers")

        if type(_answers[0]) is not dict:
            raise InternalServerError("suitability.error.answers_format")

        if not ('answers' and 'score' in list(_answers[0].keys())):
            raise InternalServerError("suitability.error.answers_incomplete_data")

        score, answers = _answers[0].get("answers"), _answers[0].get("score")

        if not all([score, answers]):
            raise InternalServerError("suitability.error.no_data")

        return answers, score

    @staticmethod
    def __update_suitability_score_and_submission_date_in_user_db(
            user_repository: BaseRepository, user_email: str, score: int, submission_date: datetime
    ) -> Optional[Exception]:
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

        raise InternalServerError("suitability.error.update_error")

    @staticmethod
    def __insert_suitability_answers_and_submission_date_in_user_profile_db(
            suitability_user_profile_repository: BaseRepository,
            answers: List[dict],
            submission_date: datetime,
            user_email: str
    ) -> Optional[Exception]:
        payload = {
            "email": user_email,
            "date": submission_date,
            "answers": answers

        }
        if suitability_user_profile_repository.insert(payload):
            return

        raise InternalServerError("suitability.error.update_error")

    @staticmethod
    def __get_last_user_profile(
            suitability_user_profile_repository: BaseRepository, email: str
    ) -> Union[dict, Exception]:
        _last_user_profile = (suitability_user_profile_repository
                              .find_more_than_equal_one({"email": {"$eq": email}})
                              .sort("_id", -1)
                              .limit(1)
                              )
        last_user_profile = list(_last_user_profile)
        if not last_user_profile:
            raise BadRequestError("common.register_not_exists")

        if type(last_user_profile[0]) is not dict:
            raise InternalServerError("suitability.error.last_user_profile_format")

        if not ("email" and "date" and "answers" in list(last_user_profile[0].keys())):
            raise InternalServerError("suitability.error.last_user_profile_incomplete_data")

        return last_user_profile[0]

