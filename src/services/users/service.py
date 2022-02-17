# STANDARD LIBS
from datetime import datetime
import logging
from copy import deepcopy
from typing import List

# OUTSIDE LIBRARIES
from fastapi import status

# SPHINX
from src.domain.sinacor.connected_person import ConnectedPerson
from src.domain.sinacor.person_type import PersonType
from src.core.interfaces.services.user.interface import IUser
from src.domain.enums.caf.status import CAFStatus
from src.services.authentications.service import AuthenticationService
from src.services.builders.thebes_hall.builder import ThebesHallBuilder
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

from src.domain.persephone_queue.persephone_queue import PersephoneQueue
from src.services.sinacor.service import SinacorService
from nidavellir.src.uru import Sindri

from src.domain.model_decorator.generate_id import generate_unique_id, hash_field
from src.services.jwts.service import JwtService
from src.services.persephone.templates.persephone_templates import (
    get_prospect_user_template_with_data,
    get_user_signed_term_template_with_data,
    get_user_identifier_data_schema_template_with_data,
    get_user_selfie_schema_template_with_data,
    get_user_complementary_data_schema_template_with_data,
    get_user_set_electronic_signature_schema_template_with_data,
    get_user_change_or_reset_electronic_signature_schema_template_with_data,
    get_user_update_register_schema_template_with_data,
)
from src.infrastructures.env_config import config
from src.domain.encrypt.password.util import PasswordEncrypt
from src.exceptions.exceptions import (
    BadRequestError,
    InternalServerError,
    UnauthorizedError,
)
from src.services.valhalla.service import ValhallaService


class UserService(IUser):
    @staticmethod
    def create(
        user: dict,
        user_repository=UserRepository(),
        authentication_service=AuthenticationService,
        persephone_client=PersephoneService.get_client(),
        social_client=ValhallaService.get_social_client(),
        jwt_handler=JwtService,
    ) -> dict:
        if user_repository.find_one({"email": user.get("email")}) is not None:
            raise BadRequestError("common.register_exists")
        user = generate_unique_id("email", user)
        has_pin = user.get("pin")
        if has_pin:
            user = hash_field(key="pin", payload=user)
        user.update({"created_at": datetime.utcnow()})
        UserService.add_user_control_metadata(payload=user)

        sent_to_persephone = persephone_client.run(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.PROSPECT_USER_QUEUE.value,
            payload=get_prospect_user_template_with_data(payload=user),
            schema_key="prospect_user_schema",
        )

        was_user_inserted = user_repository.insert(user)

        if (sent_to_persephone and was_user_inserted) is False:
            raise InternalServerError("common.process_issue")

        # was_user_created_on_social_network = social_client.create_social_network_user(
        #     msg={"email": user.get("email"), "name": user.get("nick_name")}
        # )
        #
        # if not was_user_created_on_social_network:
        #     raise InternalServerError("common.process_issue")

        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=user, ttl=10
        ).build()
        payload_jwt = jwt_handler.generate_token(jwt_payload_data=jwt_payload_data)
        authentication_service.send_authentication_email(
            email=user.get("email"),
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
        UserService.create(user=payload)

    @staticmethod
    def delete(
        payload: dict,
        user_repository=UserRepository(),
        token_service=JwtService,
        client_register=ClientRegisterRepository(),
    ) -> dict:
        old = user_repository.find_one({"unique_id": payload.get("unique_id")})
        if old is None:
            raise BadRequestError("common.register_not_exists")

        if (
            client_register.client_is_allowed_to_cancel_registration(
                user_cpf=int(old.get("identifier_document").get("cpf")),
                bmf_account=int(old.get("bmf_account")),
            )
            is False
        ):
            raise BadRequestError("user.cant_delete_account")

        new = deepcopy(old)
        new.update({"is_active_client": False})
        if user_repository.update_one(old=old, new=new) is False:
            raise InternalServerError("common.process_issue")

        return {"status_code": status.HTTP_200_OK, "payload": {"jwt": None}}

    @staticmethod
    def change_password(payload: dict, user_repository=UserRepository()) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        new_pin = payload.get("new_pin")
        old = user_repository.find_one({"unique_id": thebes_answer.get("unique_id")})
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
                new_state=user_from_database_to_update,
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

        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=user_from_database_to_update, ttl=525600
        ).build()
        jwt = JwtService.generate_token(jwt_payload_data=jwt_payload_data)
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
                new_state=user_from_database_to_update,
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
        payload: dict, user_repository=UserRepository(), token_service=JwtService
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        new_view = payload.get("new_view")
        old = user_repository.find_one({"unique_id": thebes_answer.get("unique_id")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        new = deepcopy(old)
        new["scope"] = dict(old.get("scope"))
        new["scope"]["view_type"] = new_view
        if user_repository.update_one(old=old, new=new) is False:
            raise InternalServerError("common.unable_to_process")
        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=new, ttl=525600
        ).build()
        jwt = token_service.generate_token(jwt_payload_data=jwt_payload_data)
        return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}

    @staticmethod
    def forgot_password(
        payload: dict,
        user_repository=UserRepository(),
        authentication_service=AuthenticationService,
        jwt_handler=JwtService,
    ) -> dict:
        entity = user_repository.find_one({"unique_id": payload.get("unique_id")})
        if entity is None:
            raise BadRequestError("common.register_not_exists")

        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=entity, ttl=10
        ).build()
        jwt_payload_data.update({"forgot_password": True})
        payload_jwt = jwt_handler.generate_token(jwt_payload_data=jwt_payload_data)
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
        old = user_repository.find_one({"unique_id": payload.get("unique_id")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        new = deepcopy(old)
        new.update({"token_valid_after": datetime.now(), "use_magic_link": True})
        if user_repository.update_one(old=old, new=new) is False:
            raise InternalServerError("common.process_issue")
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "user.all_logged_out",
        }

    @staticmethod
    def add_feature(
        payload: dict, user_repository=UserRepository(), token_service=JwtService
    ) -> dict:
        old = payload.get("x-thebes-answer")
        new = deepcopy(old)
        new_scope = new.get("scope")
        feature = payload.get("feature")
        status_code = status.HTTP_304_NOT_MODIFIED
        if feature not in new_scope.get("features"):
            new_scope.get("features").append(payload.get("feature"))
            new.update({"scope": new_scope})
            if user_repository.update_one(old=old, new=new) is False:
                raise InternalServerError("common.process_issue")
            status_code = status.HTTP_200_OK
        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=new, ttl=525600
        ).build()
        jwt = token_service.generate_token(jwt_payload_data=jwt_payload_data)
        return {
            "status_code": status_code,
            "payload": {"jwt": jwt},
        }

    @staticmethod
    def delete_feature(
        payload: dict, user_repository=UserRepository(), token_service=JwtService
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

        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=new, ttl=525600
        ).build()
        jwt = token_service.generate_token(jwt_payload_data=jwt_payload_data)

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
            payload=payload, onboard_step=["user_selfie_step"]
        )

        file_path = file_repository.save_user_file(
            file_type=UserFileType.SELFIE,
            content=payload.get("file_or_base64"),
            unique_id=thebes_answer.get("unique_id"),
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
        token_service=JwtService,
        persephone_client=PersephoneService.get_client(),
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        user_data = user_repository.find_one(
            {"unique_id": thebes_answer.get("unique_id")}
        )
        if type(user_data) is not dict:
            raise BadRequestError("common.register_not_exists")
        file_type = payload.get("file_type")
        term_update = UserService.fill_term_signed(
            file_type=file_type.value,
            version=file_repository.get_current_term_version(file_type=file_type),
        )
        # TODO: BACK WITH THAT
        # sent_to_persephone = persephone_client.run(
        #     topic=config("PERSEPHONE_TOPIC_USER"),
        #     partition=PersephoneQueue.TERM_QUEUE.value,
        #     payload=get_user_signed_term_template_with_data(
        #         payload=new, file_type=file_type.value
        #     ),
        #     schema_key="signed_term_schema",
        # )
        sent_to_persephone = True
        if (
            sent_to_persephone
            and user_repository.update_one(
                old={"unique_id": thebes_answer.get("unique_id")}, new=term_update
            )
        ) is False:
            raise InternalServerError("common.unable_to_process")
        user_data = user_repository.find_one(
            {"unique_id": thebes_answer.get("unique_id")}
        )
        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=user_data, ttl=525600
        ).build()
        jwt = token_service.generate_token(jwt_payload_data=jwt_payload_data)
        return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt, "control_data": control_data}}

    @staticmethod
    def add_user_control_metadata(payload: dict) -> None:
        payload.update(
            {
                "scope": {"view_type": "default", "features": ["default", "realtime"]},
                "is_active_user": False,
                "must_do_first_login": True,
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
            }
        )

    @staticmethod
    def fill_term_signed(file_type: str, version: int) -> dict:
        terms_update = {
            f"terms.{file_type}": {
                "version": version,
                "date": datetime.now(),
                "is_deprecated": False,
            }
        }
        return terms_update

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
        cpf = user_identifier_data.get("cpf")
        user_by_cpf = user_repository.find_one({"identifier_document.cpf": cpf})

        if user_by_cpf:
            raise BadRequestError("common.register_exists")

        UserService.onboarding_step_validator(
            payload=payload, onboard_step=["user_identifier_data_step"]
        )

        current_user = user_repository.find_one(
            {"unique_id": thebes_answer.get("unique_id")}
        )

        user_identifier_data = payload["user_identifier"]

        if current_user is None:
            raise BadRequestError("common.register_not_exists")

        current_user_with_identifier_data = dict(current_user)
        current_user_with_identifier_data.update(user_identifier_data)

        # TODO: BACK WITH THAT
        # sent_to_persephone = persephone_client.run(
        #     topic=config("PERSEPHONE_TOPIC_USER"),
        #     partition=PersephoneQueue.USER_IDENTIFIER_DATA.value,
        #     payload=get_user_identifier_data_schema_template_with_data(
        #         payload=current_user_with_identifier_data
        #     ),
        #     schema_key="user_identifier_data_schema",
        # )
        # if sent_to_persephone is False:
        #     raise InternalServerError("common.process_issue")

        del user_identifier_data["cpf"]
        user_identifier_data.update({"identifier_document": {"cpf": cpf}})

        user_updated = user_repository.update_one(
            old=current_user, new=user_identifier_data
        )
        if user_updated is False:
            raise InternalServerError("common.process_issue")

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }

    @staticmethod
    def user_complementary_data(
        payload: dict,
        user_repository=UserRepository(),
        persephone_client=PersephoneService.get_client(),
    ) -> dict:
        UserService.onboarding_step_validator(
            payload=payload, onboard_step=["user_complementary_step"]
        )
        thebes_answer = payload.get("x-thebes-answer")
        current_user = user_repository.find_one(
            {"unique_id": thebes_answer.get("unique_id")}
        )
        if current_user is None:
            raise BadRequestError("common.register_not_exists")
        user_complementary_data = payload.get("user_complementary")

        complementary_data_for_user_update = (
            UserService.get_user_complementary_data_for_user_update(
                user_complementary_data=user_complementary_data
            )
        )
        current_user_with_complementary_data = deepcopy(current_user)
        current_user_with_complementary_data.update(complementary_data_for_user_update)

        # TODO: BACK WITH THAT
        # sent_to_persephone = persephone_client.run(
        #     topic=config("PERSEPHONE_TOPIC_USER"),
        #     partition=PersephoneQueue.USER_COMPLEMENTARY_DATA.value,
        #     payload=get_user_complementary_data_schema_template_with_data(
        #         payload=current_user_with_complementary_data
        #     ),
        #     schema_key="user_complementary_data_schema",
        # )
        # if sent_to_persephone is False:
        #     raise InternalServerError("common.process_issue")

        # TODO: CREATE CONNECTED PERSON, enum and add um update ?
        # TODO: In this code chunk we will add a tag that represents the status from Bureau validation
        complementary_data_for_user_update.update(
            {
                "connected_person": False,
                "bureau_status": CAFStatus.APPROVED.value,
                "is_bureau_data_validated": False,
                "client_type": 1,
                "person_type": PersonType.PHYSICAL_PERSON.value,
                "investor_type": 101,
                "cosif_tax_classification": 21,
            }
        )

        user_was_updated = user_repository.update_one(
            old=current_user, new=complementary_data_for_user_update
        )
        if user_was_updated is False:
            raise InternalServerError("common.process_issue")

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }

    @staticmethod
    def get_user_complementary_data_for_user_update(user_complementary_data: dict):
        return {
            "marital": {
                "status": user_complementary_data.get("marital_status"),
                "spouse": user_complementary_data.get("spouse"),
            }
        }

    @staticmethod
    def fill_account_data_on_user_document(payload: dict, stone_age_user_data: dict):
        # TODO: REMOVING STONE
        if payload.get("provided_by_bureaux") is None:
            payload["provided_by_bureaux"] = dict()
        user_data = dict()
        # stone_age.get_only_values_from_user_data(
        #     user_data=stone_age_user_data, new_user_data=user_data
        # )
        for key, value in user_data.items():
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
        jwt_user_unique_id = thebes_answer["unique_id"]

        user_file_exists = file_repository.get_user_file(
            file_type=UserFileType.SELFIE, unique_id=jwt_user_unique_id
        )

        current_user = user_repository.find_one({"unique_id": jwt_user_unique_id})
        if current_user is None:
            raise BadRequestError("common.register_not_exists")

        onboarding_steps = (
            onboarding_step_builder.user_suitability_step(current_user=current_user)
            .user_identifier_step(current_user=current_user)
            .user_selfie_step(user_file_exists=user_file_exists)
            .user_complementary_step(current_user=current_user)
            .user_document_validator(current_user=current_user)
            .user_data_validation(current_user=current_user)
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
            payload=payload, onboard_step=["user_electronic_signature"]
        )
        thebes_answer = payload.get("x-thebes-answer")
        electronic_signature = payload.get("electronic_signature")
        encrypted_electronic_signature = PasswordEncrypt.encrypt_password(
            electronic_signature
        )
        old = user_repository.find_one({"unique_id": thebes_answer.get("unique_id")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        if old.get("electronic_signature"):
            raise BadRequestError("user.electronic_signature.already_set")
        new_data = {
            "electronic_signature": encrypted_electronic_signature,
            "is_blocked_electronic_signature": False,
            "electronic_signature_wrong_attempts": 0,
        }

        # TODO: BACK WITH THAT
        # sent_to_persephone = persephone_client.run(
        #     topic=config("PERSEPHONE_TOPIC_USER"),
        #     partition=PersephoneQueue.USER_SET_ELECTRONIC_SIGNATURE.value,
        #     payload=get_user_set_electronic_signature_schema_template_with_data(
        #         payload=new
        #     ),
        #     schema_key="user_set_electronic_signature_schema",
        # )
        # if sent_to_persephone is False:
        #     raise InternalServerError("common.process_issue")

        if user_repository.update_one(old=old, new=new_data) is False:
            raise InternalServerError("common.process_issue")

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
        entity = user_repository.find_one({"unique_id": thebes_answer.get("unique_id")})
        if entity is None:
            raise BadRequestError("common.register_not_exists")

        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=entity, ttl=10
        ).build()
        jwt_payload_data.update({"forgot_electronic_signature": True})

        payload_jwt = JwtService.generate_token(jwt_payload_data=jwt_payload_data)
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
    def onboarding_step_validator(payload: dict, onboard_step: List[str]):
        onboarding_steps = UserService.get_onboarding_user_current_step(payload)
        payload_from_onboarding_steps = onboarding_steps.get("payload")
        current_onboarding_step = payload_from_onboarding_steps.get(
            "current_onboarding_step"
        )
        if current_onboarding_step not in onboard_step:
            raise BadRequestError("user.invalid_on_boarding_step")

    @staticmethod
    def get_customer_registration_data(
        payload: dict,
        user_repository=UserRepository(),
    ):
        thebes_answer = payload.get("x-thebes-answer")
        unique_id = thebes_answer.get("unique_id")
        customer_registration_data = user_repository.find_one({"unique_id": unique_id})
        if customer_registration_data is None:
            raise BadRequestError("common.register_not_exists")
        customer_registration_data_built = (
            CustomerRegistrationBuilder(customer_registration_data)
            .personal_name()
            .personal_nick_name()
            .personal_birth_date()
            .personal_gender()
            .personal_parentage()
            .personal_email()
            .personal_phone()
            .personal_nationality()
            .personal_occupation_activity()
            .personal_company_name()
            .personal_company_cnpj()
            .personal_patrimony()
            .personal_income_tax_type()
            .personal_income()
            .personal_tax_residences()
            .personal_birth_place_country()
            .personal_birth_place_city()
            .personal_birth_place_state()
            .marital_status()
            .marital_spouse_name()
            .marital_spouse_cpf()
            .marital_nationality()
            .documents_cpf()
            .documents_identity_type()
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
            .address_phone()
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
        UserService.onboarding_step_validator(
            payload=payload, onboard_step=["finished", "user_data_validation"]
        )
        unique_id: str = payload.get("x-thebes-answer").get("unique_id")
        update_customer_registration_data: dict = payload.get(
            "customer_registration_data"
        )
        old_customer_registration_data = user_repository.find_one(
            {"unique_id": unique_id}
        )
        if old_customer_registration_data is None:
            raise BadRequestError("common.register_not_exists")

        new_customer_registration_data, modified_register_data = (
            UpdateCustomerRegistrationBuilder(
                old_personal_data=old_customer_registration_data,
                new_personal_data=update_customer_registration_data,
                unique_id=unique_id,
            )
            .personal_name()
            .personal_nick_name()
            .personal_phone()
            .personal_patrimony()
            .personal_income_tax_type()
            .personal_income()
            .personal_occupation_activity()
            .personal_occupation_cnpj()
            .personal_company_name()
            .personal_nationality()
            .personal_tax_residences()
            .personal_email()
            .personal_gender()
            .personal_father_name()
            .personal_mother_name()
            .personal_birth_date()
            .personal_birth_place_country()
            .personal_birth_place_city()
            .personal_birth_place_state()
            .marital_status()
            .marital_cpf()
            .marital_nationality()
            .marital_spouse_name()
            .documents_cpf()
            .documents_identity_type()
            .documents_identity_number()
            .documents_expedition_date()
            .documents_issuer()
            .documents_state()
            .address_country()
            .address_street_name()
            .address_city()
            .address_number()
            .address_zip_code()
            .address_neighborhood()
            .address_state()
            .address_phone()
        ).build()

        user_update_register_schema = (
            get_user_update_register_schema_template_with_data(
                unique_id=unique_id,
                modified_register_data=modified_register_data,
                update_customer_registration_data=update_customer_registration_data,
            )
        )

        Sindri.dict_to_primitive_types(user_update_register_schema)

        # TODO: BACK WITH THAT
        # sent_to_persephone = persephone_client.run(
        #     topic=config("PERSEPHONE_TOPIC_USER"),
        #     partition=PersephoneQueue.USER_UPDATE_REGISTER_DATA.value,
        #     payload=user_update_register_schema,
        #     schema_key="user_update_register_data_schema",
        # )
        # if sent_to_persephone is False:
        #     raise InternalServerError("common.process_issue")

        del new_customer_registration_data["_id"]

        if not user_repository.update_one(
            old={"unique_id": unique_id}, new=new_customer_registration_data
        ):
            raise InternalServerError("common.process_issue")

        SinacorService.save_or_update_client_data(
            user_data=new_customer_registration_data
        )

        if not user_repository.update_one(
            old={"unique_id": unique_id}, new={"is_bureau_data_validated": True}
        ):
            raise InternalServerError("common.process_issue")

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }
