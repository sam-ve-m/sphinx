# STANDARD LIBS
from datetime import datetime
import logging
from copy import deepcopy
import json

# OUTSIDE LIBRARIES
from fastapi import status
from fordev.generators import rg

# SPHINX
from src.controllers.jwts.controller import JwtController
from src.utils.json_encoder.date_encoder import DateEncoder
from src.interfaces.services.user.interface import IUser

from src.services.authentications.service import AuthenticationService
from src.services.builders.user.customer_registration import CustomerRegistrationBuilder
from src.services.builders.user.customer_registration_update import (
    UpdateCustomerRegistrationBuilder,
)
from src.services.persephone.service import PersephoneService
from src.services.builders.user.onboarding_steps_builder import OnboardingStepBuilder
from src.repositories.client_register.repository import ClientRegisterRepository

from src.repositories.file.enum.user_file import UserFileType
from src.repositories.file.repository import FileRepository
from src.repositories.user.repository import UserRepository

from src.domain.persephone_queue import PersephoneQueue
from src.services.sinacor.service import SinacorService
from src.utils.base_model_normalizer import normalize_enum_types

from src.utils.genarate_id import generate_id, hash_field
from src.utils.jwt_utils import JWTHandler
from src.utils.stone_age import StoneAge
from src.utils.persephone_templates import (
    get_prospect_user_template_with_data,
    get_user_signed_term_template_with_data,
    get_user_identifier_data_schema_template_with_data,
    get_user_selfie_schema_template_with_data,
    get_user_complementary_data_schema_template_with_data,
    get_user_quiz_from_stoneage_schema_template_with_data,
    get_user_quiz_response_from_stoneage_schema_template_with_data,
    get_user_set_electronic_signature_schema_template_with_data,
    get_user_change_or_reset_electronic_signature_schema_template_with_data,
    get_user_update_register_schema_template_with_data
)
from src.utils.env_config import config
from src.utils.encrypt.password.util import PasswordEncrypt
from src.exceptions.exceptions import (
    BadRequestError,
    InternalServerError,
    UnauthorizedError,
)


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
        payload.update({"created_at": datetime.now()})
        UserService.add_user_control_metadata(payload=payload)

        sent_to_persephone = persephone_client.run(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.PROSPECT_USER_QUEUE.value,
            payload=get_prospect_user_template_with_data(payload=payload),
            schema_key="prospect_user_schema",
        )

        was_user_inserted = user_repository.insert(payload)

        if (sent_to_persephone and was_user_inserted) is False:
            raise InternalServerError("common.process_issue")

        payload_jwt = JWTHandler.generate_token(payload=payload, ttl=10)
        authentication_service.send_authentication_email(
            email=payload.get("email"),
            payload_jwt=payload_jwt,
            body="email.body.created",
        )
        return {
            "status_code": status.HTTP_201_CREATED,
            "message_key": "user.created",
        }

    @staticmethod
    def create_admin(payload: dict) -> None:
        payload.update({"is_admin": True})
        UserService.create(payload=payload)

    @staticmethod
    def update(payload: dict, user_repository=UserRepository()) -> None:
        pass

    @staticmethod
    def delete(
        payload: dict,
        user_repository=UserRepository(),
        token_handler=JWTHandler,
        client_register=ClientRegisterRepository(),
    ) -> dict:
        old = user_repository.find_one({"_id": payload.get("email")})
        if old is None:
            raise BadRequestError("common.register_not_exists")

        if (
            client_register.client_is_allowed_to_cancel_registration(
                user_cpf=int(old.get("cpf")), bmf_account=int(old.get("bmf_account"))
            )
            is False
        ):
            raise BadRequestError("user.cant_delete_account")

        new = deepcopy(old)
        new.update({"is_active_client": False})
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
        new = deepcopy(old)
        new["pin"] = new_pin
        new = hash_field(key="pin", payload=new)
        if user_repository.update_one(old=old, new=new) is False:
            raise InternalServerError("common.process_issue")
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }

    @staticmethod
    def reset_electronic_signature(
        payload: dict,
        user_repository=UserRepository(),
        persephone_client=PersephoneService.get_client(),
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        forgot_electronic_signature = thebes_answer.get("forgot_electronic_signature")

        if not forgot_electronic_signature:
            raise UnauthorizedError("invalid_credential")

        new_electronic_signature = payload.get("new_electronic_signature")

        user_from_database = user_repository.find_one(
            {"_id": thebes_answer.get("email")}
        )
        if user_from_database is None:
            raise BadRequestError("common.register_not_exists")

        encrypted_electronic_signature = PasswordEncrypt.encrypt_password(
            new_electronic_signature
        )
        user_from_database_to_update = deepcopy(user_from_database)
        user_from_database_to_update[
            "electronic_signature"
        ] = encrypted_electronic_signature
        user_from_database_to_update["is_blocked_electronic_signature"] = False
        user_from_database_to_update["electronic_signature_wrong_attempts"] = 0

        sent_to_persephone = persephone_client.run(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_CHANGE_OR_RESET_ELECTRONIC_SIGNATURE.value,
            payload=get_user_change_or_reset_electronic_signature_schema_template_with_data(
                previous_state=user_from_database,
                new_state=user_from_database_to_update
            ),
            schema_key="user_change_or_reset_electronic_signature_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        if (
            user_repository.update_one(
                old=user_from_database, new=user_from_database_to_update
            )
            is False
        ):
            raise InternalServerError("common.process_issue")

        jwt = JWTHandler.generate_token(
            payload=user_from_database_to_update, ttl=525600
        )

        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"jwt": jwt},
            "message_key": "requests.updated",
        }

    @staticmethod
    def change_electronic_signature(
        payload: dict,
        user_repository=UserRepository(),
        persephone_client=PersephoneService.get_client(),
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        current_electronic_signature = payload.get("current_electronic_signature")
        new_electronic_signature = payload.get("new_electronic_signature")

        user_from_database = user_repository.find_one(
            {"_id": thebes_answer.get("email")}
        )
        if user_from_database is None:
            raise BadRequestError("common.register_not_exists")

        is_blocked_electronic_signature = user_from_database.get(
            "is_blocked_electronic_signature"
        )
        user_has_electronic_signature_blocked = is_blocked_electronic_signature is True
        if user_has_electronic_signature_blocked:
            raise UnauthorizedError("user.electronic_signature_is_blocked")
        encrypted_current_electronic_signature = PasswordEncrypt.encrypt_password(
            current_electronic_signature
        )
        encrypted_new_electronic_signature = PasswordEncrypt.encrypt_password(
            new_electronic_signature
        )
        encrypted_electronic_signature_from_database = user_from_database.get(
            "electronic_signature"
        )

        is_correct_electronic_signature_typed = (
            encrypted_current_electronic_signature
            == encrypted_electronic_signature_from_database
        )

        if not is_correct_electronic_signature_typed:
            raise UnauthorizedError("user.wrong_electronic_signature")

        user_from_database_to_update = deepcopy(user_from_database)
        user_from_database_to_update[
            "electronic_signature"
        ] = encrypted_new_electronic_signature

        sent_to_persephone = persephone_client.run(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_CHANGE_OR_RESET_ELECTRONIC_SIGNATURE.value,
            payload=get_user_change_or_reset_electronic_signature_schema_template_with_data(
                previous_state=user_from_database,
                new_state=user_from_database_to_update
            ),
            schema_key="user_change_or_reset_electronic_signature_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        user_was_updated = user_repository.update_one(
            old=user_from_database, new=user_from_database_to_update
        )

        if user_was_updated is False:
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
        new = deepcopy(old)
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
    ) -> dict:
        entity = user_repository.find_one({"_id": payload.get("email")})
        if entity is None:
            raise BadRequestError("common.register_not_exists")
        to_add_into_jwt = {"forgot_password": True}
        payload_jwt = JWTHandler.generate_token(
            payload=entity, args=to_add_into_jwt, ttl=10
        )
        authentication_service.send_authentication_email(
            email=entity.get("email"),
            payload_jwt=payload_jwt,
            body="email.body.forgot_password",
        )
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "email.forgot_password",
        }

    @staticmethod
    def logout_all(payload: dict, user_repository=UserRepository()) -> dict:
        old = user_repository.find_one({"_id": payload.get("email")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        new = deepcopy(old)
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
        new = deepcopy(old)
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
        new = deepcopy(old)
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
    def save_user_selfie(
        payload: dict,
        file_repository=FileRepository(bucket_name=config("AWS_BUCKET_USERS_SELF")),
        persephone_client=PersephoneService.get_client(),
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        UserService.onboarding_step_validator(
            payload=payload, on_board_step="user_selfie_step"
        )

        file_path = file_repository.save_user_file(
            file_type=UserFileType.SELF,
            content=payload.get("file_or_base64"),
            user_email=thebes_answer.get("email"),
        )

        sent_to_persephone = persephone_client.run(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_SELFIE.value,
            payload=get_user_selfie_schema_template_with_data(
                file_path=file_path, email=thebes_answer.get("email")
            ),
            schema_key="user_selfie_schema",
        )

        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")
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
        new = deepcopy(old)
        UserService.fill_term_signed(
            payload=new,
            file_type=file_type.value,
            version=file_repository.get_current_term_version(file_type=file_type),
        )
        sent_to_persephone = persephone_client.run(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.TERM_QUEUE.value,
            payload=get_user_signed_term_template_with_data(
                payload=new, file_type=file_type.value
            ),
            schema_key="signed_term_schema",
        )
        if (
            sent_to_persephone and user_repository.update_one(old=old, new=new)
        ) is False:
            raise InternalServerError("common.unable_to_process")
        jwt = token_handler.generate_token(payload=new, ttl=525600)
        return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}

    @staticmethod
    def add_user_control_metadata(payload: dict) -> None:
        payload.update(
            {
                "scope": {"view_type": "default", "features": ["default", "realtime"]},
                "is_active_user": False,
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
    def fill_term_signed(payload: dict, file_type: str, version: int) -> None:
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
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "user.files.term_not_signed",
            }
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
        persephone_client=PersephoneService.get_client(),
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        user_identifier_data = payload.get("user_identifier")

        user_by_cpf = user_repository.find_one({"cpf": user_identifier_data.get("cpf")})

        if user_by_cpf is not None:
            raise BadRequestError("common.register_exists")

        UserService.onboarding_step_validator(
            payload=payload, on_board_step="user_identifier_data_step"
        )

        current_user = user_repository.find_one({"_id": thebes_answer.get("email")})

        if current_user is None:
            raise BadRequestError("common.register_not_exists")

        current_user_with_identifier_data = dict(current_user)

        UserService.add_user_identifier_data_on_current_user(
            payload=current_user_with_identifier_data,
            user_identifier_data=user_identifier_data,
        )

        sent_to_persephone = persephone_client.run(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_IDENTIFIER_DATA.value,
            payload=get_user_identifier_data_schema_template_with_data(payload=current_user_with_identifier_data),
            schema_key="user_identifier_data_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        user_updated = user_repository.update_one(
            old=current_user, new=current_user_with_identifier_data
        )
        if user_updated is False:
            raise InternalServerError("common.process_issue")

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }

    @staticmethod
    def add_user_identifier_data_on_current_user(
        payload: dict, user_identifier_data: dict
    ) -> None:
        payload["cpf"] = user_identifier_data.get("cpf")
        payload["cel_phone"] = user_identifier_data.get("cel_phone")

    @staticmethod
    def user_complementary_data(
        payload: dict,
        user_repository=UserRepository(),
        persephone_client=PersephoneService.get_client(),
    ) -> dict:
        UserService.onboarding_step_validator(
            payload=payload, on_board_step="user_complementary_step"
        )
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

        sent_to_persephone = persephone_client.run(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_COMPLEMENTARY_DATA.value,
            payload=get_user_complementary_data_schema_template_with_data(
                payload=current_user_with_complementary_data
            ),
            schema_key="user_complementary_data_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        user_was_updated = user_repository.update_one(
            old=current_user, new=current_user_with_complementary_data
        )
        if user_was_updated is False:
            raise InternalServerError("common.process_issue")

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
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
    def can_send_quiz(user_onboarding_current_step: dict):
        current_step = user_onboarding_current_step["payload"][
            "current_onboarding_step"
        ]
        quiz_step_or_finished = current_step not in ("user_quiz_step")
        all_necessary_steps = not all(
            [
                user_onboarding_current_step["payload"]["suitability_step"],
                user_onboarding_current_step["payload"]["user_identifier_data_step"],
                user_onboarding_current_step["payload"]["user_selfie_step"],
                user_onboarding_current_step["payload"]["user_complementary_step"],
            ]
        )
        return quiz_step_or_finished or all_necessary_steps

    @staticmethod
    def user_quiz(
        payload: dict, stone_age=StoneAge, user_repository=UserRepository()
    ) -> dict:
        UserService.onboarding_step_validator(
            payload=payload, on_board_step="user_quiz_step"
        )
        thebes_answer = payload.get("x-thebes-answer")

        user_onboarding_current_step = UserService.get_onboarding_user_current_step(
            payload=payload
        )
        if UserService.can_send_quiz(
            user_onboarding_current_step=user_onboarding_current_step
        ):
            return {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message_key": "user.quiz.missing_steps",
            }

        current_user = user_repository.find_one({"_id": thebes_answer.get("email")})
        current_user_marital = current_user.get("marital")

        user_identifier_data = {
            "email": current_user.get("email"),
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

        output = response.get("output")
        stone_age_contract_uuid = response.get("uuid")
        current_user_updated = deepcopy(current_user)
        current_user_updated.update(
            {"stone_age_contract_uuid": stone_age_contract_uuid}
        )

        current_user_updated.update({"register_analyses": output.get("decision")})

        if (
            user_repository.update_one(old=current_user, new=current_user_updated)
            is False
        ):
            raise InternalServerError("common.process_issue")

        return {"status_code": status.HTTP_200_OK, "payload": output}

    @staticmethod
    def user_quiz_put(
        payload: dict,
        stone_age=StoneAge,
        user_repository=UserRepository(),
        persephone_client=PersephoneService.get_client(),
    ) -> dict:
        UserService.onboarding_step_validator(
            payload=payload, on_board_step="user_quiz_step"
        )
        thebes_answer = payload.get("x-thebes-answer")

        user_onboarding_current_step = UserService.get_onboarding_user_current_step(
            payload=payload
        )
        if UserService.can_send_quiz(
            user_onboarding_current_step=user_onboarding_current_step
        ):
            return {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message_key": "user.quiz.missing_steps",
            }

        current_user = user_repository.find_one({"_id": thebes_answer.get("email")})
        current_user_marital = current_user.get("marital")

        user_identifier_data = {
            "email": current_user.get("email"),
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

        output = response.get("output")
        stone_age_contract_uuid = response.get("uuid")
        current_user_updated = deepcopy(current_user)
        current_user_updated.update(
            {"stone_age_contract_uuid": stone_age_contract_uuid}
        )

        current_user_updated.update({"register_analyses": output.get("decision")})

        sent_to_persephone = persephone_client.run(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_GET_QUIZ_FROM_STONEAGE.value,
            payload=get_user_quiz_from_stoneage_schema_template_with_data(
                output=output, device_information=payload.get('device_information'), email=current_user.get('email')
            ),
            schema_key="user_get_quiz_from_stoneage_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        user_was_updated = user_repository.update_one(
            old=current_user, new=current_user_updated
        )
        if user_was_updated is False:
            raise InternalServerError("common.process_issue")

        return {"status_code": status.HTTP_200_OK, "payload": output}

    @staticmethod
    def send_quiz_responses(
        payload: dict,
        user_repository=UserRepository(),
        stone_age=StoneAge,
        persephone_client=PersephoneService.get_client(),
    ) -> dict:

        thebes_answer = payload.get("x-thebes-answer")
        current_user = user_repository.find_one({"_id": thebes_answer.get("email")})
        if type(current_user) is not dict:
            raise BadRequestError("common.register_not_exists")

        current_user_updated = deepcopy(current_user)
        must_send_quiz = current_user_updated.get("register_analyses") is None

        if must_send_quiz is False:
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "requests.not_modified",
            }
        # NAO SABEMOS O QUE A STONE AGE IRA RETORNAR AO ENVIARMOS AS RESPOSTAS DO QUIZ, VERIFICAR O QUE FAZER COM ESSE RETORNO
        stone_age_response = stone_age.send_user_quiz_responses(
            quiz=payload.get("quiz")
        )

        sent_to_persephone = persephone_client.run(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_SEND_QUIZ_FROM_STONEAGE.value,
            payload=get_user_quiz_response_from_stoneage_schema_template_with_data(
                quiz=payload.get("quiz"),
                response=stone_age_response,
                device_information=payload.get('device_information'),
                email=thebes_answer.get("email"),
            ),
            schema_key="user_send_quiz_from_stoneage_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        if must_send_quiz:
            current_user_updated.update({"register_analyses": "PENDING"})
            if (
                user_repository.update_one(old=current_user, new=current_user_updated)
                is False
            ):
                raise InternalServerError("common.process_issue")

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "user.quiz.send",
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
    def get_onboarding_user_current_step(
        payload: dict,
        user_repository=UserRepository(),
        file_repository=FileRepository(bucket_name=config("AWS_BUCKET_USERS_SELF")),
    ) -> dict:
        onboarding_step_builder = OnboardingStepBuilder()
        thebes_answer = payload.get("x-thebes-answer")
        jwt_user_email = thebes_answer.get("email")

        user_file_exists = file_repository.get_user_file(
            file_type=UserFileType.SELF, user_email=jwt_user_email
        )

        current_user = user_repository.find_one({"_id": jwt_user_email})
        if current_user is None:
            raise BadRequestError("common.register_not_exists")

        onboarding_steps = (
            onboarding_step_builder.user_suitability_step(current_user=current_user)
            .user_identifier_step(current_user=current_user)
            .user_selfie_step(user_file_exists=user_file_exists)
            .user_complementary_step(current_user=current_user)
            .user_quiz_step(current_user=current_user)
            .user_electronic_signature(current_user=current_user)
            .build()
        )

        return {"status_code": status.HTTP_200_OK, "payload": onboarding_steps}

    @staticmethod
    def set_user_electronic_signature(
        payload: dict,
        user_repository=UserRepository(),
        persephone_client=PersephoneService.get_client(),
    ) -> dict:
        UserService.onboarding_step_validator(
            payload=payload, on_board_step="user_electronic_signature"
        )
        thebes_answer = payload.get("x-thebes-answer")
        electronic_signature = payload.get("electronic_signature")
        encrypted_electronic_signature = PasswordEncrypt.encrypt_password(
            electronic_signature
        )
        old = user_repository.find_one({"_id": thebes_answer.get("email")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        if old.get("electronic_signature"):
            raise BadRequestError("user.electronic_signature.already_set")
        new = deepcopy(old)
        new["electronic_signature"] = encrypted_electronic_signature
        new["is_blocked_electronic_signature"] = False
        new["electronic_signature_wrong_attempts"] = 0

        sent_to_persephone = persephone_client.run(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_SET_ELECTRONIC_SIGNATURE.value,
            payload=get_user_set_electronic_signature_schema_template_with_data(payload=new),
            schema_key="user_set_electronic_signature_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        if user_repository.update_one(old=old, new=new) is False:
            raise InternalServerError("common.process_issue")

        payload = UserService.fake_stone_age_callback(
            email=thebes_answer.get("email"), cpf=new.get("cpf")
        )
        SinacorService.process_callback(payload=payload)

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }

    @staticmethod
    def forgot_electronic_signature(
        payload: dict,
        user_repository=UserRepository(),
        authentication_service=AuthenticationService,
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        entity = user_repository.find_one({"_id": thebes_answer.get("email")})
        if entity is None:
            raise BadRequestError("common.register_not_exists")
        to_add_into_jwt = {"forgot_electronic_signature": True}
        payload_jwt = JWTHandler.generate_token(
            payload=entity, args=to_add_into_jwt, ttl=10
        )
        authentication_service.send_authentication_email(
            email=entity.get("email"),
            payload_jwt=payload_jwt,
            body="email.body.forgot_electronic_signature",
        )
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "email.forgot_electronic_signature",
        }

    @staticmethod
    def fake_stone_age_callback(email: str, cpf: str):

        fake_response = {
            "error": None,
            "successful": True,
            "appName": "lionx",
            "uuid": "21b00324-d240-4c61-a79c-9a0bd7ff6e45",
            "output": {
                "status": "OK",
                "decision": "APROVADO",
                "gender": {"source": "PH3W", "value": "M"},
                "email": {"source": "PH3W", "value": email},
                "name": {"source": "PH3W", "value": "Antonio Armando Piaui"},
                "birth_date": {"source": "PH3W", "value": datetime(1993, 7, 12, 0, 0)},
                "birthplace": {
                    "nationality": {"source": "PH3W", "value": 1},
                    "country": {"source": "PH3W", "value": "BRA"},
                    "state": {"source": "PH3W", "value": "GO"},
                    "city": {"source": "PH3W", "value": "FORMOSA"},
                    "id_city": {"source": "PH3W", "value": 968},
                },
                "mother_name": {"source": "PH3W", "value": "Antonia dos Santos Jr."},
                "identifier_document": {
                    "type": {"source": "PH3W", "value": "RG"},
                    "document_data": {
                        # GENERATE
                        "number": {
                            "source": "PH3W",
                            "value": int(rg().replace(".", "").replace("-", "")),
                        },
                        "date": {
                            "source": "PH3W",
                            "value": datetime(2018, 7, 12, 16, 31, 31),
                        },
                        "state": {"source": "PH3W", "value": "SP"},
                        "issuer": {"source": "PH3W", "value": "SSP"},
                    },
                },
                "address": {
                    "country": {"source": "PH3W", "value": "BRA"},
                    "street_name": {"source": "PH3W", "value": "R. 2"},
                    "number": {"source": "PH3W", "value": "126"},
                    "neighborhood": {"source": "PH3W", "value": "Formosinha"},
                    "state": {"source": "PH3W", "value": "GO"},
                    "city": {"source": "PH3W", "value": "FORMOSA"},
                    "id_city": {"source": "PH3W", "value": 968},
                    "zip_code": {"source": "PH3W", "value": 73813190},
                    "phone_number": {"source": "PH3W", "value": "11952909954"},
                },
                "occupation": {
                    "activity": {"source": "PH3W", "value": 304},
                    "company": {
                        "cnpj": {"source": "PH3W", "value": "25811052000179"},
                        "name": {"source": "PH3W", "value": "Tudo nosso .com.br"},
                    },
                },
                "assets": {
                    "patrimony": {"source": "PH3W", "value": 5446456.44},
                    "income": {"source": "PH3W", "value": 5446456.44},
                    "income_tax_type": {"source": "PH3W", "value": 1},
                    "date": {"source": "PH3W", "value": datetime(1993, 7, 12, 0, 0)},
                },
                "education": {
                    "level": {"source": "PH3W", "value": "Médio incompleto"},
                    "course": {"source": "PH3W", "value": "Escola James Riwbon"},
                },
                "politically_exposed_person": {
                    "is_politically_exposed_person": {"source": "PH3W", "value": False}
                },
                "date_of_acquisition": {
                    "source": "PH3W",
                    "value": datetime(2018, 7, 12, 16, 31, 31),
                },
                "connected_person": {"source": "PH3W", "value": "N"},
                "person_type": {"source": "PH3W", "value": "F"},
                "client_type": {"source": "PH3W", "value": 1},
                "investor_type": {"source": "PH3W", "value": 101},
                "cosif_tax_classification": {"source": "PH3W", "value": 21},
                "marital_update": {
                    "marital_regime": {"source": "PH3W", "value": 1},
                    "spouse_birth_date": {
                        "source": "PH3W",
                        "value": datetime(1993, 7, 12, 0, 0),
                    },
                },
                "cpf": {"source": "PH3W", "value": cpf},
                "self_link": {"source": "PH3W", "value": "http://self_user.jpg"},
                "is_us_person": {"source": "PH3W", "value": True},
                "us_tin": {"source": "PH3W", "value": 126516515},
                "irs_sharing": {"source": "PH3W", "value": True},
                "father_name": {"source": "PH3W", "value": "Antonio dos Santos"},
                "midia_person": {"source": "PH3W", "value": False},
                "person_related_to_market_influencer": {
                    "source": "PH3W",
                    "value": False,
                },
                "court_orders": {"source": "PH3W", "value": False},
                "lawsuits": {"source": "PH3W", "value": False},
                "fund_admin_registration": {"source": "PH3W", "value": False},
                "investment_fund_administrators_registration": {
                    "source": "PH3W",
                    "value": False,
                },
                "register_auditors_securities_commission": {
                    "source": "PH3W",
                    "value": False,
                },
                "registration_of_other_market_participants_securities_commission": {
                    "source": "PH3W",
                    "value": False,
                },
                "foreign_investors_register_of_annex_iv_not_reregistered": {
                    "source": "PH3W",
                    "value": False,
                },
                "registration_of_foreign_investors_securities_commission": {
                    "source": "PH3W",
                    "value": False,
                },
                "registration_representative_of_nonresident_investors_securities_commission": {
                    "source": "PH3W",
                    "value": False,
                },
            },
        }

        return fake_response

    @staticmethod
    def onboarding_step_validator(payload: dict, on_board_step: str):
        onboarding_steps = UserService.get_onboarding_user_current_step(payload)
        payload_from_onboarding_steps = onboarding_steps.get("payload")
        current_onboarding_step = payload_from_onboarding_steps.get(
            "current_onboarding_step"
        )
        if current_onboarding_step != on_board_step:
            raise BadRequestError("user.invalid_on_boarding_step")

    @staticmethod
    def get_customer_registration_data(
        payload: dict,
        user_repository=UserRepository(),
    ):
        thebes_answer = payload.get("x-thebes-answer")
        email = thebes_answer.get("email")
        customer_registration_data = user_repository.find_one({"_id": email})
        if customer_registration_data is None:
            raise BadRequestError("common.register_not_exists")

        customer_registration_data_built = (
            CustomerRegistrationBuilder(customer_registration_data)
            .personal_name()
            .personal_birth_date()
            .personal_parentage()
            .personal_gender()
            .personal_email()
            .personal_phone()
            .personal_patrimony()
            .personal_us_tin()
            .personal_occupation_activity()
            .personal_company_name()
            .marital_status()
            .marital_spouse_name()
            .marital_spouse_cpf()
            .marital_cpf()
            .marital_nationality()
            .documents_cpf()
            .documents_identity_number()
            .documents_expedition_date()
            .documents_issuer()
            .documents_state()
            .address_country()
            .address_number()
            .address_street_name()
            .address_city()
            .address_neighborhood()
            .address_zip_code()
            .address_state()
        ).build()

        return {
            "status_code": status.HTTP_200_OK,
            "payload": customer_registration_data_built,
        }

    @staticmethod
    def update_customer_registration_data(
        payload: dict,
        user_repository=UserRepository(),
        persephone_client=PersephoneService.get_client(),
    ):
        email: str = payload.get("x-thebes-answer", {}).get("email")
        update_customer_registration_data: dict = payload.get(
            "customer_registration_data"
        )
        old_customer_registration_data = user_repository.find_one({"_id": email})
        if old_customer_registration_data is None:
            raise BadRequestError("common.register_not_exists")

        new_customer_registration_data, modified_register_data = (
            UpdateCustomerRegistrationBuilder(
                old_personal_data=old_customer_registration_data,
                new_personal_data=update_customer_registration_data,
                email=email,
            )
            .personal_name()
            .person_us_tin()
            .personal_phone()
            .personal_patrimony()
            .personal_occupation_activity()
            .personal_occupation_cnpj()
            .personal_company_name()
            .marital_status()
            .marital_cpf()
            .marital_nationality()
            .marital_spouse_name()
            .documents_cpf()
            .documents_identity_number()
            .documents_expedition_date()
            .documents_issuer()
            .documents_state()
            .address_country()
            .address_street_name()
            .address_city()
            .address_number()
            .address_id_city()
            .address_zip_code()
            .address_neighborhood()
            .address_state()
        ).build()

        user_update_register_schema = get_user_update_register_schema_template_with_data(
                email=email,
                modified_register_data=modified_register_data,
                update_customer_registration_data=update_customer_registration_data
            )

        normalize_enum_types(user_update_register_schema)

        sent_to_persephone = persephone_client.run(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_UPDATE_REGISTER_DATA.value,
            payload=json.loads(json.dumps(user_update_register_schema, cls=DateEncoder)),
            schema_key="user_update_register_data_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        SinacorService.save_or_update_client_data(
            user_data=new_customer_registration_data
        )

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }
