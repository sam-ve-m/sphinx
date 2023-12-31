# STANDARD LIBS
from datetime import datetime
from typing import List, Tuple, Union

# OUTSIDE LIBRARIES
from fastapi import status

from src.core.interfaces.services.suitability.interface import ISuitability
from src.domain.persephone_queue.persephone_queue import PersephoneQueue

# SPHINX
from src.exceptions.exceptions import InternalServerError, BadRequestError
from src.infrastructures.env_config import config
from src.repositories.base_repository.mongo_db.base import MongoDbBaseRepository
from src.repositories.suitability.repository import (
    SuitabilityRepository,
    SuitabilityUserProfileRepository,
    SuitabilityAnswersRepository,
)
from src.repositories.user.repository import UserRepository
from src.services.builders.suitability.builder import SuitabilityAnswersProfileBuilder
from src.services.builders.thebes_hall.builder import ThebesHallBuilder
from src.services.jwts.service import JwtService
from persephone_client import Persephone
from src.services.persephone.templates.persephone_templates import (
    get_user_suitability_template_with_data,
    get_user_fill_suitability,
)


class SuitabilityService(ISuitability):

    persephone_client = Persephone

    @staticmethod
    async def create_quiz(
        payload: dict,
        suitability_repository: MongoDbBaseRepository = SuitabilityRepository(),
        suitability_answers_repository: MongoDbBaseRepository = SuitabilityAnswersRepository(),
        suitability_answers_profile_builder=SuitabilityAnswersProfileBuilder(),
    ) -> dict:

        if payload is None:
            raise InternalServerError("suitability.error.not_found")

        suitability = payload.get("suitability")

        if not suitability:
            raise InternalServerError("suitability.error.not_found")

        version = await SuitabilityService.__get_suitability_version()
        suitability_submission_date = datetime.utcnow()
        suitability.update({"date": suitability_submission_date, "version": version})
        await SuitabilityService.__insert_new_suitability(
            suitability_repository=suitability_repository, suitability=suitability
        )

        suitability_answers_profile_builder.suitability = suitability
        answers = suitability_answers_profile_builder.profile
        await SuitabilityService.__insert_new_answers_suitability(
            suitability_answers_repository=suitability_answers_repository,
            answers=answers,
        )
        return {
            "status_code": status.HTTP_201_CREATED,
            "message_key": "suitability.create_quiz",
        }

    @staticmethod
    async def create_profile(
        payload,
        user_repository=UserRepository(),
        suitability_repository=SuitabilityRepository(),
        suitability_user_profile_repository=SuitabilityUserProfileRepository(),
        token_service=JwtService,
    ) -> dict:
        thebes_answer: dict = payload.get("x-thebes-answer")
        unique_id: str = thebes_answer["user"].get("unique_id")
        suitability_submission_date = datetime.utcnow()
        (
            answers,
            score,
            suitability_version,
        ) = await SuitabilityService.__get_last_suitability_answers_metadata()
        sent_to_persephone = (
            await SuitabilityService.persephone_client.send_to_persephone(
                topic=config("PERSEPHONE_TOPIC_USER"),
                partition=PersephoneQueue.SUITABILITY_QUEUE.value,
                message=get_user_suitability_template_with_data(
                    payload=get_user_fill_suitability(
                        answers=answers,
                        score=score,
                        unique_id=unique_id,
                        suitability_version=suitability_version,
                    )
                ),
                schema_name="suitability_schema",
            )
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")
        (
            await SuitabilityService.__update_suitability_score_and_submission_date_in_user_db(
                user_repository=user_repository,
                unique_id=unique_id,
                score=score,
                suitability_version=suitability_version,
                submission_date=suitability_submission_date,
            )
        )
        (
            await SuitabilityService.__insert_suitability_answers_in_user_profile_db(
                suitability_user_profile_repository=suitability_user_profile_repository,
                unique_id=unique_id,
                user_score=score,
                suitability_version=suitability_version,
                answers=answers,
                submission_date=suitability_submission_date,
            )
        )
        user_data = await user_repository.find_one({"unique_id": unique_id})

        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=user_data, ttl=525600
        ).build()

        jwt = await token_service.generate_token(jwt_payload_data=jwt_payload_data)

        return {
            "status_code": status.HTTP_201_CREATED,
            "payload": {"jwt": jwt, "control_data": control_data},
        }

    @staticmethod
    async def get_user_profile(
        payload: dict,
        suitability_user_profile_repository=SuitabilityUserProfileRepository(),
    ) -> dict:
        thebes_answer: dict = payload.get("x-thebes-answer")
        user_email: str = thebes_answer.get("email")
        user_profile = await SuitabilityService.__get_last_user_profile(
            suitability_user_profile_repository=suitability_user_profile_repository,
            email=user_email,
        )
        del user_profile["_id"]
        user_profile["date"] = str(user_profile["date"])
        return {
            "status_code": status.HTTP_200_OK,
            "payload": user_profile,
        }

    @staticmethod
    async def __get_suitability_version(
        suitability_repository=SuitabilityRepository(),
    ) -> int:
        try:
            last_suitability = await suitability_repository.find_all(
                {}, sort=("_id", -1), limit=1
            )

        except (TypeError, AttributeError):
            raise InternalServerError("common.process_issue")

        if not last_suitability:
            return 1

        if type(last_suitability) is not list:
            raise InternalServerError("suitability.error.not_found")

        if len(last_suitability) != 1:
            raise InternalServerError("suitability.error.not_found")

        if type(last_suitability[0]) is not dict:
            raise InternalServerError("suitability.error.not_found")

        last_version = last_suitability[0].get("version")

        if type(last_version) is not int:
            raise InternalServerError("common.invalid_params")

        new_version = last_version + 1
        return new_version

    @staticmethod
    async def __insert_new_suitability(
        suitability_repository: MongoDbBaseRepository, suitability: dict
    ) -> None:
        if type(suitability) is not dict:
            raise InternalServerError("common.invalid_params")
        try:
            inserted = await suitability_repository.insert(suitability)
        except AttributeError:
            raise InternalServerError("common.process_issue")
        else:
            if not inserted:
                raise InternalServerError("common.process_issue")
            else:
                return

    @staticmethod
    async def __insert_new_answers_suitability(
        suitability_answers_repository: MongoDbBaseRepository,
        answers: dict,
    ) -> None:
        if type(answers) is not dict:
            raise InternalServerError("common.invalid_params")
        try:
            inserted = await suitability_answers_repository.insert(answers)
        except AttributeError:
            raise InternalServerError("common.process_issue")
        else:
            if not inserted:
                raise InternalServerError("common.process_issue")
            else:
                return

    @staticmethod
    async def __get_last_suitability_answers_metadata(
        suitability_answers_repository: MongoDbBaseRepository = SuitabilityAnswersRepository(),
    ) -> Union[Tuple[List[dict], int, int], Exception]:
        try:
            _answers = list(
                await suitability_answers_repository.find_all(
                    {}, sort=("_id", -1), limit=1
                )
            )
        except (TypeError, AttributeError) as e:
            raise InternalServerError("common.process_issue")

        if type(_answers) is not list:
            raise InternalServerError("suitability.error.no_answers")

        if len(_answers) != 1:
            raise InternalServerError("suitability.error.no_answers")

        if type(_answers[0]) is not dict:
            raise InternalServerError("suitability.error.answers_format")

        answers = _answers[0].get("answers")
        score = _answers[0].get("score")
        suitability_version = _answers[0].get("suitability_version")

        if not all([score, answers, suitability_version]):
            raise InternalServerError("suitability.error.answers_incomplete_data")

        return answers, score, suitability_version

    @staticmethod
    async def __update_suitability_score_and_submission_date_in_user_db(
        user_repository: MongoDbBaseRepository,
        unique_id: str,
        score: int,
        suitability_version: int,
        submission_date: datetime,
    ) -> None:
        try:
            old = await user_repository.find_one({"unique_id": unique_id})
        except AttributeError:
            raise InternalServerError("common.process_issue")

        if type(old) is not dict:
            raise BadRequestError("common.register_not_exists")

        if not all(
            [
                unique_id,
                score,
                suitability_version,
                submission_date,
            ]
        ):
            raise InternalServerError("common.process_issue")

        suitability_data = {
            "suitability": {
                "score": score,
                "submission_date": submission_date,
                "suitability_version": suitability_version,
            }
        }
        try:
            updated = await user_repository.update_one(old=old, new=suitability_data)
        except AttributeError:
            raise InternalServerError("common.process_issue")
        else:
            if not updated:
                raise BadRequestError("suitability.error.update_error")
        return

    @staticmethod
    async def __insert_suitability_answers_in_user_profile_db(
        suitability_user_profile_repository: MongoDbBaseRepository,
        answers: List[dict],
        suitability_version: int,
        unique_id: str,
        user_score: int,
        submission_date: datetime,
    ) -> None:
        if not all(
            [
                answers,
                suitability_version,
                unique_id,
                user_score,
                submission_date,
            ]
        ):
            raise InternalServerError("common.process_issue")

        payload = {
            "unique_id": unique_id,
            "date": submission_date,
            "user_score": user_score,
            "answers": answers,
            "suitability_version": suitability_version,
        }
        try:
            inserted = await suitability_user_profile_repository.insert(payload)
        except AttributeError:
            raise InternalServerError("common.process_issue")
        else:
            if not inserted:
                raise InternalServerError("suitability.error.update_error")
        return

    @staticmethod
    async def __get_last_user_profile(
        suitability_user_profile_repository: MongoDbBaseRepository, email: str
    ) -> dict:
        if not email:
            raise InternalServerError("common.process_issue")

        try:
            _last_user_profile = (
                await suitability_user_profile_repository.find_more_than_equal_one(
                    {"email": email}
                )
                .sort("_id", -1)
                .limit(1)
            )
        except (TypeError, AttributeError):
            raise InternalServerError("common.process_issue")

        if not _last_user_profile:
            raise BadRequestError("common.register_not_exists")

        last_user_profile = list(_last_user_profile)

        if not last_user_profile:
            raise BadRequestError("common.register_not_exists")

        if type(last_user_profile[0]) is not dict:
            raise InternalServerError("suitability.error.last_user_profile_format")

        if not ("email" and "date" and "answers" in list(last_user_profile[0].keys())):
            raise InternalServerError(
                "suitability.error.last_user_profile_incomplete_data"
            )

        return last_user_profile[0]
