# STANDARD LIBS
from datetime import datetime
import logging

# OUTSIDE LIBRARIES
from fastapi import status

# SPHINX
from src.controllers.jwts.controller import JwtController

from src.interfaces.services.user.interface import IUser

from src.services.authentications.service import AuthenticationService
from src.services.persephone.service import PersephoneService
from src.services.builders.user.on_boarding_steps_builder import OnBoardingStepBuilder

from src.repositories.suitability.repository import SuitabilityUserProfileRepository
from src.repositories.file.enum.user_file import UserFileType
from src.repositories.file.repository import FileRepository
from src.repositories.user.repository import UserRepository

from src.domain.persephone_queue import PersephoneQueue

from src.utils.genarate_id import generate_id, hash_field
from src.utils.jwt_utils import JWTHandler
from src.utils.stone_age import StoneAge
from src.utils.persephone_templates import (
    get_prospect_user_template_with_data,
    get_user_signed_term_template_with_data,
    get_user_account_template_with_data,
)
from src.utils.env_config import config

from src.exceptions.exceptions import BadRequestError, InternalServerError


class UserService(IUser):
    @staticmethod
    def create(
        payload: dict,
        user_repository=UserRepository(),
        authentication_service=AuthenticationService,
        persephone_client=PersephoneService.get_client(),
    ) -> dict:
        payload = generate_id("email", payload, must_remove=False)
        has_pin = payload.get("pin")
        if has_pin:
            payload = hash_field(key="pin", payload=payload)
        if user_repository.find_one({"_id": payload.get("_id")}) is not None:
            raise BadRequestError("common.register_exists")
        UserService.add_user_control_metadata(payload=payload)

        sent_to_persephone = persephone_client.run(
            topic=config("PERSEPHONE_TOPIC"),
            partition=PersephoneQueue.PROSPECT_USER_QUEUE.value,
            payload=get_prospect_user_template_with_data(payload=payload),
            schema_key="prospect_user_schema",
        )

        was_user_inserted = user_repository.insert(payload)

        if (sent_to_persephone and was_user_inserted) is False:
            raise InternalServerError("common.process_issue")
        authentication_service.send_authentication_email(
            email=payload.get("email"),
            payload=payload,
            ttl=10,
            body="email.body.created",
        )
        return {
            "status_code": status.HTTP_201_CREATED,
            "message_key": "user.created",
        }

    @staticmethod
    def create_admin(payload: dict) -> dict:
        payload.update({"is_admin": True})
        UserService.create(payload=payload)

    @staticmethod
    def update(payload: dict, user_repository=UserRepository()) -> None:
        pass

    @staticmethod
    def delete(
        payload: dict, user_repository=UserRepository(), token_handler=JWTHandler
    ) -> dict:
        old = user_repository.find_one({"_id": payload.get("email")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        new = dict(old)
        new.update({"deleted": True})
        if user_repository.update_one(old=old, new=new) is False:
            raise InternalServerError("common.process_issue")

        jwt = token_handler.generate_token(payload=new, ttl=525600)
        JwtController.insert_one(jwt, new.get("email"))
        return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}

    @staticmethod
    def change_password(payload: dict, user_repository=UserRepository()) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        new_pin = payload.get("new_pin")
        old = user_repository.find_one({"_id": thebes_answer.get("email")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        new = dict(old)
        new["pin"] = new_pin
        new = hash_field(key="pin", payload=new)
        if user_repository.update_one(old=old, new=new) is False:
            raise InternalServerError("common.process_issue")
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }

    @staticmethod
    def change_view(
        payload: dict, user_repository=UserRepository(), token_handler=JWTHandler
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        new_view = payload.get("new_view")
        old = user_repository.find_one({"_id": thebes_answer.get("email")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        new = dict(old)
        new["scope"] = dict(old.get("scope"))
        new["scope"]["view_type"] = new_view
        if user_repository.update_one(old=old, new=new) is False:
            raise InternalServerError("common.unable_to_process")
        jwt = token_handler.generate_token(payload=new, ttl=525600)
        return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}

    @staticmethod
    def forgot_password(
        payload: dict,
        user_repository=UserRepository(),
        authentication_service=AuthenticationService,
    ):
        entity = user_repository.find_one({"_id": payload.get("email")})
        if entity is None:
            raise BadRequestError("common.register_not_exists")
        authentication_service.send_authentication_email(
            email=entity.get("email"),
            payload=entity,
            ttl=10,
            body="email.body.forgot_password",
        )
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "email.forgot_password",
        }

    @staticmethod
    def logout_all(payload: dict, user_repository=UserRepository()):
        old = user_repository.find_one({"_id": payload.get("email")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        new = dict(old)
        new.update({"token_valid_after": datetime.now()})
        if user_repository.update_one(old=old, new=new) is False:
            raise InternalServerError("common.process_issue")
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "user.all_logged_out",
        }

    @staticmethod
    def add_feature(
        payload: dict, user_repository=UserRepository(), token_handler=JWTHandler
    ) -> dict:
        old = payload.get("x-thebes-answer")
        new = dict(old)
        new_scope = new.get("scope")
        feature = payload.get("feature")
        if feature not in new_scope.get("features"):
            new_scope.get("features").append(payload.get("feature"))
            new.update({"scope": new_scope})
            if user_repository.update_one(old=old, new=new) is False:
                raise InternalServerError("common.process_issue")
            jwt = token_handler.generate_token(payload=new, ttl=525600)
            return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}
        jwt = token_handler.generate_token(payload=new, ttl=525600)
        return {
            "status_code": status.HTTP_304_NOT_MODIFIED,
            "payload": {"jwt": jwt},
        }

    @staticmethod
    def delete_feature(
        payload: dict, user_repository=UserRepository(), token_handler=JWTHandler
    ) -> dict:
        old = payload.get("x-thebes-answer")
        new = dict(old)
        new_scope = new.get("scope")
        response = {"status_code": None, "payload": {"jwt": None}}
        if payload.get("feature") in new_scope.get("features"):
            new_scope.get("features").remove(payload.get("feature"))
            new.update({"scope": new_scope})
            if user_repository.update_one(old=old, new=new) is False:
                raise InternalServerError("common.process_issue")
            response.update({"status_code": status.HTTP_200_OK})
        else:
            response.update({"status_code": status.HTTP_304_NOT_MODIFIED})

        jwt = token_handler.generate_token(payload=new, ttl=525600)

        response.update({"jwt": jwt})

        return response

    @staticmethod
    def save_user_self(
        payload: dict,
        file_repository=FileRepository(bucket_name=config("AWS_BUCKET_USERS_SELF")),
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        file_repository.save_user_file(
            file_type=UserFileType.SELF,
            content=payload.get("file_or_base64"),
            user_email=thebes_answer.get("email"),
        )
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "files.uploaded",
        }

    @staticmethod
    def sign_term(
        payload: dict,
        file_repository=FileRepository(bucket_name=config("AWS_BUCKET_TERMS")),
        user_repository=UserRepository(),
        token_handler=JWTHandler,
        persephone_client=PersephoneService.get_client(),
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        old = user_repository.find_one({"_id": thebes_answer.get("email")})
        if type(old) is not dict:
            raise BadRequestError("common.register_not_exists")
        file_type = payload.get("file_type")
        new = dict(old)
        UserService.fill_term_signed(
            payload=new,
            file_type=file_type.value,
            version=file_repository.get_current_term_version(file_type=file_type),
        )
        sent_to_persephone = persephone_client.run(
            topic=config("PERSEPHONE_TOPIC"),
            partition=PersephoneQueue.TERM_QUEUE.value,
            payload=get_user_signed_term_template_with_data(
                payload=new, file_type=file_type.value
            ),
            schema_key="term_schema",
        )
        if (
            sent_to_persephone and user_repository.update_one(old=old, new=new)
        ) is False:
            raise InternalServerError("common.unable_to_process")
        jwt = token_handler.generate_token(payload=new, ttl=525600)
        return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}

    @staticmethod
    def add_user_control_metadata(payload: dict):
        payload.update(
            {
                "scope": {"view_type": None, "features": []},
                "is_active": False,
                "deleted": False,
                "use_magic_link": True,
                "token_valid_after": datetime.utcnow(),
                "terms": {
                    # The terms list is available in the FileRepository
                    "term_application": None,
                    "term_open_account": None,
                    "term_retail_liquid_provider": None,
                    "term_refusal": None,
                    "term_non_compliance": None,
                },
                "can_be_managed_by_third_party_operator": False,
                "is_managed_by_third_party_operator": False,
                "third_party_operator": {
                    "is_third_party_operator": False,
                    "details": {},
                    "third_party_operator_email": "string",
                },
            }
        )

    @staticmethod
    def fill_term_signed(payload: dict, file_type: str, version: int):
        if payload.get("terms") is None:
            payload["terms"] = dict()
        payload["terms"][file_type] = {
            "version": version,
            "date": datetime.now(),
            "is_deprecated": False,
        }

    @staticmethod
    def get_signed_term(
        payload: dict,
        file_repository=FileRepository(bucket_name=config("AWS_BUCKET_TERMS")),
    ) -> dict:
        file_type = payload.get("file_type")
        try:
            version = (
                payload.get("x-thebes-answer")
                .get("terms")
                .get(file_type.value)
                .get("version")
            )
        except Exception:
            raise BadRequestError("user.files.term_not_signed")
        try:
            link = file_repository.get_term_file_by_version(
                file_type=file_type, version=version
            )
            return {"status_code": status.HTTP_200_OK, "payload": {"link": link}}
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            raise InternalServerError("common.process_issue")

    @staticmethod
    def user_identifier_data(
        payload: dict,
        user_repository=UserRepository(),
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        current_user = user_repository.find_one({"_id": thebes_answer.get("email")})
        if current_user is None:
            raise BadRequestError("common.register_not_exists")
        user_identifier_data = payload.get("user_identifier")

        current_user_with_identifier_data = dict(current_user)
        UserService.add_user_identifier_data_on_current_user(
            payload=current_user_with_identifier_data,
            user_identifier_data=user_identifier_data,
        )
        if (
            user_repository.update_one(
                old=current_user, new=current_user_with_identifier_data
            )
            is False
        ):
            raise InternalServerError("common.process_issue")
        return {
            "status_code": status.HTTP_200_OK,
        }

    @staticmethod
    def add_user_identifier_data_on_current_user(
        payload: dict, user_identifier_data: dict
    ):
        payload["cpf"] = user_identifier_data.get("cpf")
        payload["cel_phone"] = user_identifier_data.get("cel_phone")

    @staticmethod
    def user_complementary_data(
        payload: dict,
        user_repository=UserRepository(),
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        current_user = user_repository.find_one({"_id": thebes_answer.get("email")})
        if current_user is None:
            raise BadRequestError("common.register_not_exists")
        user_complementary_data = payload.get("user_complementary")

        current_user_with_complementary_data = dict(current_user)
        UserService.add_user_complementary_data_on_current_user(
            payload=current_user_with_complementary_data,
            user_complementary_data=user_complementary_data,
        )

        if (
            user_repository.update_one(
                old=current_user, new=current_user_with_complementary_data
            )
            is False
        ):
            raise InternalServerError("common.process_issue")
        return {
            "status_code": status.HTTP_200_OK,
        }

    @staticmethod
    def add_user_complementary_data_on_current_user(
        payload: dict, user_complementary_data
    ):
        payload["is_us_person"] = user_complementary_data.get("is_us_person")
        payload["us_tin"] = user_complementary_data.get("us_tin")
        payload["is_cvm_qualified_investor"] = user_complementary_data.get(
            "is_cvm_qualified_investor"
        )
        payload["marital"] = {
            "status": user_complementary_data.get("marital_status"),
            "spouse": user_complementary_data.get("spouse"),
        }

    @staticmethod
    def user_quiz(
        payload: dict, stone_age=StoneAge, user_repository=UserRepository()
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        current_user = user_repository.find_one({"_id": thebes_answer.get("email")})
        current_user_marital = current_user.get("marital")

        user_identifier_data = {
            "cpf": current_user.get("cpf"),
            "cel_phone": current_user.get("cel_phone"),
            "marital_status": current_user_marital.get("marital_status"),
            "is_us_person": current_user.get("is_us_person"),
        }

        current_user_is_us_person = current_user.get("is_us_person")

        if current_user_is_us_person:
            user_identifier_data["us_tin"] = current_user.get("us_tin")

        spouse = current_user_marital.get("spouse")

        if spouse is not None:
            user_identifier_data["spouse"] = spouse

        response = stone_age.get_user_quiz(user_identifier_data)
        # TODO: SAVE UUID on user COLECTION and STATUS PERSEPHONE AND COLECTION
        quiz = response.get("output")

        return {"status_code": status.HTTP_200_OK, "payload": quiz}

    @staticmethod
    def change_user_to_client(
        payload: dict,
        user_repository=UserRepository(),
        stone_age=StoneAge,
        persephone_client=PersephoneService.get_client(),
    ) -> dict:

        thebes_answer = payload.get("x-thebes-answer")
        old = user_repository.find_one({"_id": thebes_answer.get("email")})
        if type(old) is not dict:
            raise BadRequestError("common.register_not_exists")

        stone_age_user_data = stone_age.send_user_quiz_responses(
            quiz=payload.get("quiz")
        )

        new = dict(old)
        UserService.fill_account_data_on_user_document(
            payload=new, stone_age_user_data=stone_age_user_data
        )

        if user_repository.update_one(old=old, new=new) is False:
            raise InternalServerError("common.process_issue")
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "user.creating_account",
        }

    @staticmethod
    def fill_account_data_on_user_document(
        payload: dict, stone_age_user_data: dict, stone_age=StoneAge
    ):
        if payload.get("provided_by_bureaux") is None:
            payload["provided_by_bureaux"] = dict()
        for key, value in stone_age.get_only_values_from_user_data(
            user_data=stone_age_user_data
        ).items():
            payload["provided_by_bureaux"].update({key: value})
        payload["provided_by_bureaux"]["concluded_at"] = datetime.now()

    @staticmethod
    def get_on_boarding_user_current_step(
        payload: dict,
        user_repository=UserRepository(),
        file_repository=FileRepository(bucket_name=config("AWS_BUCKET_USERS_SELF")),
        on_boarding_step_builder=OnBoardingStepBuilder(),
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        jwt_user_email = thebes_answer.get("email")

        user_file_exists = file_repository.get_user_file(file_type=UserFileType.SELF, user_email=jwt_user_email)

        current_user = user_repository.find_one({"_id": jwt_user_email})
        if current_user is None:
            raise BadRequestError("common.register_not_exists")

        user_suitability_profile = current_user.get("suitability")

        on_boarding_steps = (
            on_boarding_step_builder.user_suitability_step(
                user_suitability_profile=user_suitability_profile
            )
            .user_identifier_step(current_user=current_user)
            .user_self_step(user_file_exists=user_file_exists)
            .user_complementary_step(current_user=current_user)
            .user_quiz_step(current_user=current_user)
            .build()
        )

        return {"status_code": status.HTTP_200_OK, "payload": on_boarding_steps}
