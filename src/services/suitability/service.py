# STANDARD LIBS
from datetime import datetime

# OUTSIDE LIBRARIES
from fastapi import status

# SPHINX
from src.exceptions.exceptions import InternalServerError
from src.repositories.base_repository import BaseRepository
from src.repositories.suitability.repository import SuitabilityRepository, SuitabilityUserProfileRepository
from src.repositories.user.repository import UserRepository
from src.services.builders.suitability.builder import SuitabilityProfileBuilder
from src.interfaces.services.suitability.interface import ISuitability

ASCENDING_ORDER = 1


class SuitabilityService(ISuitability):
    @staticmethod
    def __get_current_suitability(suitability_repository: BaseRepository) -> dict:
        suitability = suitability_repository.find_more_than_equal_one({}).sort("date", ASCENDING_ORDER).limit(1)
        return suitability

    @staticmethod
    def __update_score_and_suitability_submission_date_in_db(
            user_data: BaseRepository, score: int, date: datetime
    ) -> None or Exception:
        """TODO IMPLEMENT"""
        pass

    @staticmethod
    def __insert_suitability_answers_and_submission_date_in_db(
            suitability_user_profile: BaseRepository, answers: dict, date: datetime
    ) -> None or Exception:
        """TODO IMPLEMENT"""
        pass

    @staticmethod
    def create_quiz(payload: dict, suitability_repository=SuitabilityRepository()) -> dict:
        payload.update({"date": datetime.utcnow()})

        if suitability_repository.insert(payload):
            return {
                "status_code": status.HTTP_201_CREATED,
                "message_key": "suitabilities.persisted",
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
        # suitability_submission_date = datetime.utcnow()
        # current_suitability = SuitabilityService.__get_current_suitability(suitability_repository)
        # user_profile = (builder_suitability_profile
        #                 .set_user_data({})
        #                 .set_current_suitability(current_suitability)
        #                 .get_profile())
        # answers = user_profile.get("answers")
        # score = user_profile.get("score")
        # SuitabilityService.__update_score_and_suitability_submission_date_in_db(
        #     user_repository,
        #     int(),
        #     suitability_submission_date
        # )
        # SuitabilityService.__insert_suitability_answers_and_submission_date_in_db(
        #     suitability_user_profile_repository,
        #     {},
        #     suitability_submission_date
        # )
        pass
