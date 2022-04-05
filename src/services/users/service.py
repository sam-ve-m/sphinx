# STANDARD LIBS
from etria_logger import Gladsheim
from copy import deepcopy
from datetime import datetime
from typing import List
from uuid import uuid4

# OUTSIDE LIBRARIES
from fastapi import status
from nidavellir import Sindri

# SPHINX
from src.core.interfaces.services.user.interface import IUser
from src.domain.caf.status import CAFStatus
from src.domain.encrypt.password.util import PasswordEncrypt
from src.domain.persephone_queue.persephone_queue import PersephoneQueue
from src.domain.user_level.enum import UserLevel
from src.exceptions.exceptions import (
    BadRequestError,
    InternalServerError,
    UnauthorizedError,
)
from src.infrastructures.env_config import config
from src.repositories.client_register.repository import ClientRegisterRepository
from src.repositories.file.enum.user_file import UserFileType
from src.repositories.file.repository import FileRepository
from src.repositories.user.repository import UserRepository
from src.services.authentications.service import AuthenticationService
from src.services.builders.thebes_hall.builder import ThebesHallBuilder
from src.services.builders.user.customer_registration import CustomerRegistrationBuilder
from src.services.builders.user.customer_registration_update import (
    UpdateCustomerRegistrationBuilder,
)
from src.services.builders.user.onboarding_steps_builder import OnboardingStepBuilder
from src.services.jwts.service import JwtService
from persephone_client import Persephone
from src.services.persephone.templates.persephone_templates import (
    get_prospect_user_template_with_data,
    get_user_selfie_schema_template_with_data,
    get_user_change_or_reset_electronic_signature_schema_template_with_data,
    get_user_update_register_schema_template_with_data,
    get_user_signed_term_template_with_data,
    get_user_identifier_data_schema_template_with_data,
    get_user_complementary_data_schema_template_with_data,
    get_user_set_electronic_signature_schema_template_with_data,
)
from src.services.sinacor.service import SinacorService
from src.services.valhalla.service import ValhallaService


class UserService(IUser):

    persephone_client = Persephone

    @staticmethod
    async def create(
        user: dict,
        user_repository=UserRepository,
        authentication_service=AuthenticationService,
        valhalla_service=ValhallaService,
        jwt_handler=JwtService,
    ) -> dict:
        user_from_database = await user_repository.find_one(
            {"email": user.get("email")}
        )
        is_email_in_use = user_from_database is not None
        if is_email_in_use:
            raise BadRequestError("common.register_exists")

        await UserService._add_user_control_metadata(payload=user)

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await UserService.persephone_client.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.PROSPECT_USER_QUEUE.value,
            message=get_prospect_user_template_with_data(payload=user),
            schema_name="prospect_user_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        was_user_inserted = await user_repository.insert(user)
        if was_user_inserted is False:
            raise InternalServerError("common.process_issue")

        await valhalla_service.register_user(
            user_email=user.get("email"), nick_name=user.get("nick_name")
        )

        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=user, ttl=10
        ).build()
        jwt = await jwt_handler.generate_token(jwt_payload_data=jwt_payload_data)
        authentication_service.send_authentication_email(
            email=user.get("email"),
            payload_jwt=jwt,
            body="email.body.created",
        )
        return {
            "status_code": status.HTTP_201_CREATED,
            "message_key": "user.created",
        }

    @staticmethod
    async def create_admin(payload: dict) -> None:
        payload.update({"is_admin": True})
        await UserService.create(user=payload)

    @staticmethod
    async def delete(
        payload: dict,
        user_repository=UserRepository,
        token_service=JwtService,
        client_register=ClientRegisterRepository(),
    ) -> dict:
        unique_id = payload["user"]["unique_id"]
        old = await user_repository.find_one({"unique_id": unique_id})
        if old is None:
            raise BadRequestError("common.register_not_exists")

        if (
            await client_register.client_is_allowed_to_cancel_registration(
                user_cpf=int(old.get("identifier_document").get("cpf")),
                bmf_account=int(old.get("bmf_account")),
            )
            is False
        ):
            raise BadRequestError("user.cant_delete_account")

        if (
            await user_repository.update_one(
                old={"unique_id": unique_id}, new={"is_active_client": False}
            )
            is False
        ):
            raise InternalServerError("common.process_issue")

        return {"status_code": status.HTTP_200_OK, "payload": {"jwt": None}}

    @staticmethod
    async def reset_electronic_signature(
        payload: dict, user_repository=UserRepository
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        forgot_electronic_signature = thebes_answer.get("forgot_electronic_signature")

        if not forgot_electronic_signature:
            raise UnauthorizedError("invalid_credential")

        new_electronic_signature = payload.get("new_electronic_signature")

        unique_id = thebes_answer["user"]["unique_id"]

        user_from_database = await user_repository.find_one({"unique_id": unique_id})
        if user_from_database is None:
            raise BadRequestError("common.register_not_exists")

        user_from_database_to_update = {
            "electronic_signature": await PasswordEncrypt.encrypt_password(
                new_electronic_signature
            ),
            "is_blocked_electronic_signature": False,
            "electronic_signature_wrong_attempts": 0,
        }

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await UserService.persephone_client.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_CHANGE_OR_RESET_ELECTRONIC_SIGNATURE.value,
            message=get_user_change_or_reset_electronic_signature_schema_template_with_data(
                previous_state=user_from_database,
                new_state=user_from_database_to_update,
            ),
            schema_name="user_change_or_reset_electronic_signature_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        if (
            await user_repository.update_one(
                old={"unique_id": unique_id}, new=user_from_database_to_update
            )
            is False
        ):
            raise InternalServerError("common.process_issue")

        user_from_database.update(user_from_database_to_update)

        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=user_from_database, ttl=525600
        ).build()
        jwt = await JwtService.generate_token(jwt_payload_data=jwt_payload_data)
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"jwt": jwt, "control_data": control_data},
            "message_key": "requests.updated",
        }

    @staticmethod
    async def change_electronic_signature(
        payload: dict, user_repository=UserRepository
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        current_electronic_signature = payload.get("current_electronic_signature")
        new_electronic_signature = payload.get("new_electronic_signature")
        unique_id = thebes_answer["user"]["unique_id"]
        user_from_database = await user_repository.find_one({"unique_id": unique_id})
        if user_from_database is None:
            raise BadRequestError("common.register_not_exists")

        user_has_electronic_signature_blocked = user_from_database.get(
            "is_blocked_electronic_signature"
        )
        if user_has_electronic_signature_blocked:
            raise UnauthorizedError("user.electronic_signature_is_blocked")
        encrypted_current_electronic_signature = await PasswordEncrypt.encrypt_password(
            current_electronic_signature
        )
        encrypted_new_electronic_signature = await PasswordEncrypt.encrypt_password(
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

        user_from_database_to_update = {
            "electronic_signature": encrypted_new_electronic_signature,
            "is_blocked_electronic_signature": user_from_database.get(
                "is_blocked_electronic_signature"
            ),
            "electronic_signature_wrong_attempts": user_from_database.get(
                "electronic_signature_wrong_attempts"
            ),
        }

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await UserService.persephone_client.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_CHANGE_OR_RESET_ELECTRONIC_SIGNATURE.value,
            message=get_user_change_or_reset_electronic_signature_schema_template_with_data(
                previous_state=user_from_database,
                new_state=user_from_database_to_update,
            ),
            schema_name="user_change_or_reset_electronic_signature_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        user_was_updated = await user_repository.update_one(
            old={"unique_id": unique_id}, new=user_from_database_to_update
        )

        if user_was_updated is False:
            raise InternalServerError("common.process_issue")

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }

    @staticmethod
    async def change_view(
        payload: dict, user_repository=UserRepository, token_service=JwtService
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        new_view = payload.get("new_view")
        old = await user_repository.find_one(
            {"unique_id": thebes_answer["user"].get("unique_id")}
        )
        if old is None:
            raise BadRequestError("common.register_not_exists")
        new = deepcopy(old)
        new["scope"] = dict(old.get("scope"))
        new["scope"]["view_type"] = new_view
        if await user_repository.update_one(old=old, new=new) is False:
            raise InternalServerError("common.unable_to_process")
        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=new, ttl=525600
        ).build()
        jwt = await token_service.generate_token(jwt_payload_data=jwt_payload_data)
        return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}

    @staticmethod
    async def logout_all(payload: dict, user_repository=UserRepository) -> dict:
        old = await user_repository.find_one(
            {"unique_id": payload["user"].get("unique_id")}
        )
        if old is None:
            raise BadRequestError("common.register_not_exists")
        if "_id" in old:
            del old["_id"]
        new = deepcopy(old)
        new.update({"token_valid_after": datetime.utcnow(), "use_magic_link": True})
        if await user_repository.update_one(old=old, new=new) is False:
            raise InternalServerError("common.process_issue")
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "user.all_logged_out",
        }

    @staticmethod
    async def add_feature(
        payload: dict, user_repository=UserRepository, token_service=JwtService
    ) -> dict:
        old = payload.get("x-thebes-answer")
        new = deepcopy(old)
        new_scope = new.get("scope")
        feature = payload.get("feature")
        # status_code = status.HTTP_304_NOT_MODIFIED
        status_code = status.HTTP_200_OK
        if feature not in new_scope.get("features"):
            new_scope.get("features").append(payload.get("feature"))
            new.update({"scope": new_scope})
            if await user_repository.update_one(old=old, new=new) is False:
                raise InternalServerError("common.process_issue")
            status_code = status.HTTP_200_OK
        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=new, ttl=525600
        ).build()
        jwt = await token_service.generate_token(jwt_payload_data=jwt_payload_data)
        return {
            "status_code": status_code,
            "payload": {"jwt": jwt},
        }

    @staticmethod
    async def delete_feature(
        payload: dict, user_repository=UserRepository, token_service=JwtService
    ) -> dict:
        old = payload.get("x-thebes-answer")
        new = deepcopy(old)
        new_scope = new.get("scope")
        response = {"status_code": None, "payload": {"jwt": None}}
        if payload.get("feature") in new_scope.get("features"):
            new_scope.get("features").remove(payload.get("feature"))
            new.update({"scope": new_scope})
            if await user_repository.update_one(old=old, new=new) is False:
                raise InternalServerError("common.process_issue")
            response.update({"status_code": status.HTTP_200_OK})
        else:
            response.update(
                {
                    # "status_code": status.HTTP_304_NOT_MODIFIED,
                    "status_code": status.HTTP_200_OK,
                }
            )

        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=new, ttl=525600
        ).build()
        jwt = await token_service.generate_token(jwt_payload_data=jwt_payload_data)

        response.update({"jwt": jwt})

        return response

    @staticmethod
    async def save_user_selfie(payload: dict, file_repository=FileRepository) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        await UserService.onboarding_step_validator(
            payload=payload, onboard_step=["user_selfie_step"]
        )

        file_path = await file_repository.save_user_file(
            file_type=UserFileType.SELFIE,
            content=payload.get("file_or_base64"),
            unique_id=thebes_answer["user"].get("unique_id"),
            bucket_name=config("AWS_BUCKET_USERS_SELF"),
        )

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await UserService.persephone_client.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_SELFIE.value,
            message=get_user_selfie_schema_template_with_data(
                file_path=file_path, unique_id=thebes_answer["user"]["unique_id"]
            ),
            schema_name="user_selfie_schema",
        )

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "files.uploaded",
        }

    @staticmethod
    async def sign_term(
        payload: dict,
        file_repository=FileRepository,
        user_repository=UserRepository,
        token_service=JwtService,
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        user_data = await user_repository.find_one(
            {"unique_id": thebes_answer["user"]["unique_id"]}
        )
        if type(user_data) is not dict:
            raise BadRequestError("common.register_not_exists")
        file_type = payload.get("file_type")
        term_version = await file_repository.get_current_term_version(
            file_type=file_type, bucket_name=config("AWS_BUCKET_TERMS")
        )
        term_update = await UserService.fill_term_signed(
            file_type=file_type.value,
            version=term_version,
        )
        thebes_answer_user = thebes_answer["user"]
        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await UserService.persephone_client.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.TERM_QUEUE.value,
            message=get_user_signed_term_template_with_data(
                term_version=term_version,
                payload=thebes_answer_user,
                file_type=file_type.value,
            ),
            schema_name="signed_term_schema",
        )
        if not sent_to_persephone:
            raise InternalServerError("common.unable_to_process")

        was_updated = await user_repository.update_one(
            old={"unique_id": thebes_answer_user["unique_id"]}, new=term_update
        )
        if not was_updated:
            raise InternalServerError("common.unable_to_process")

        user_data = await user_repository.find_one(
            {"unique_id": thebes_answer["user"]["unique_id"]}
        )
        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=user_data, ttl=525600
        ).build()
        jwt = await token_service.generate_token(jwt_payload_data=jwt_payload_data)
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"jwt": jwt, "control_data": control_data},
        }

    @staticmethod
    async def _add_user_control_metadata(payload: dict) -> None:
        payload.update(
            {
                "unique_id": str(uuid4()),
                "created_at": datetime.utcnow(),
                "scope": {
                    "user_level": UserLevel.PROSPECT.value,
                    "view_type": "default",
                    "features": ["default"],
                },
                "is_active_user": False,
                "must_do_first_login": True,
                "use_magic_link": True,
                "token_valid_after": datetime.utcnow(),
                "terms": {
                    "term_application": None,
                    "term_open_account": None,
                    "term_retail_liquid_provider": None,
                    "term_refusal": None,
                    "term_non_compliance": None,
                },
            }
        )

    @staticmethod
    async def fill_term_signed(file_type: str, version: int) -> dict:
        terms_update = {
            f"terms.{file_type}": {
                "version": version,
                "date": datetime.utcnow(),
                "is_deprecated": False,
            }
        }
        return terms_update

    @staticmethod
    async def get_signed_term(
        payload: dict,
        file_repository=FileRepository,
        user_repository=UserRepository,
    ) -> dict:
        try:
            file_type = payload.get("file_type")
            thebes_answer = payload.get("x-thebes-answer")
            user_data = await user_repository.find_one(
                {"unique_id": thebes_answer["user"].get("unique_id")}
            )
            version = user_data["terms"][file_type.value]["version"]
        except Exception:
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "user.files.term_not_signed",
            }
        try:
            link = await file_repository.get_term_file_by_version(
                file_type=file_type,
                version=version,
                bucket_name=config("AWS_BUCKET_TERMS"),
            )
            return {"status_code": status.HTTP_200_OK, "payload": {"link": link}}
        except Exception as e:
            Gladsheim.error(error=e)
            raise InternalServerError("common.process_issue")

    @staticmethod
    async def user_identifier_data(
        payload: dict, user_repository=UserRepository
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        unique_id = thebes_answer["user"]["unique_id"]

        user_identifier_data = payload.get("user_identifier")

        user_cpf = user_identifier_data.get("cpf")
        user_by_cpf = await user_repository.find_one(
            {"identifier_document.cpf": user_cpf}
        )
        if user_by_cpf:
            raise BadRequestError("common.register_exists")

        await UserService.onboarding_step_validator(
            payload=payload, onboard_step=["user_identifier_data_step"]
        )

        current_user = await user_repository.find_one({"unique_id": unique_id})

        user_identifier_data.update({"unique_id": unique_id})

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await UserService.persephone_client.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_IDENTIFIER_DATA.value,
            message=get_user_identifier_data_schema_template_with_data(
                payload=user_identifier_data
            ),
            schema_name="user_identifier_data_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        del user_identifier_data["cpf"]
        user_identifier_data.update({"identifier_document": {"cpf": user_cpf}})

        user_updated = await user_repository.update_one(
            old={"unique_id": unique_id}, new=user_identifier_data
        )
        if user_updated is False:
            raise InternalServerError("common.process_issue")

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }

    @staticmethod
    async def user_complementary_data(
        payload: dict, user_repository=UserRepository
    ) -> dict:
        await UserService.onboarding_step_validator(
            payload=payload, onboard_step=["user_complementary_step"]
        )
        thebes_answer = payload.get("x-thebes-answer")
        unique_id = thebes_answer["user"]["unique_id"]
        current_user = await user_repository.find_one({"unique_id": unique_id})
        if current_user is None:
            raise BadRequestError("common.register_not_exists")
        user_complementary_data = payload.get("user_complementary")

        complementary_data_for_user_update = (
            await UserService.get_user_complementary_data_for_user_update(
                user_complementary_data=user_complementary_data
            )
        )

        if (
            complementary_data_for_user_update.get("marital")
            and complementary_data_for_user_update.get("marital", {}).get("spouse")
            and current_user["identifier_document"]["cpf"]
            == complementary_data_for_user_update.get("marital", {})
            .get("spouse", {})
            .get("cpf")
        ):
            raise BadRequestError("user.you_cant_be_your_spouse")

        current_user_with_complementary_data = deepcopy(current_user)
        current_user_with_complementary_data.update(complementary_data_for_user_update)

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await UserService.persephone_client.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_COMPLEMENTARY_DATA.value,
            message=get_user_complementary_data_schema_template_with_data(
                payload=current_user_with_complementary_data
            ),
            schema_name="user_complementary_data_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        # TODO: CREATE CONNECTED PERSON, enum and add um update ?
        # TODO: In this code chunk we will add a tag that represents the status from Bureau validation
        complementary_data_for_user_update.update(
            {
                "bureau_status": CAFStatus.APPROVED.value,
                "is_bureau_data_validated": False,
            }
        )

        user_was_updated = await user_repository.update_one(
            old={"unique_id": unique_id}, new=complementary_data_for_user_update
        )
        if user_was_updated is False:
            raise InternalServerError("common.process_issue")

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }

    @staticmethod
    async def get_user_complementary_data_for_user_update(
        user_complementary_data: dict,
    ):
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
        payload["provided_by_bureaux"]["concluded_at"] = datetime.utcnow()

    @staticmethod
    async def get_onboarding_user_current_step(
        payload: dict,
        user_repository=UserRepository,
        file_repository=FileRepository,
    ) -> dict:
        onboarding_step_builder = OnboardingStepBuilder()
        x_thebes_answer = payload.get("x-thebes-answer")
        user_unique_id = x_thebes_answer["user"]["unique_id"]

        user_file_exists = await file_repository.user_file_exists(
            file_type=UserFileType.SELFIE,
            unique_id=user_unique_id,
            bucket_name=config("AWS_BUCKET_USERS_SELF"),
        )

        current_user = await user_repository.find_one({"unique_id": user_unique_id})
        if current_user is None:
            raise BadRequestError("common.register_not_exists")

        onboarding_steps = await (
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
    async def set_user_electronic_signature(
        payload: dict, user_repository=UserRepository
    ) -> dict:
        await UserService.onboarding_step_validator(
            payload=payload, onboard_step=["user_electronic_signature"]
        )
        thebes_answer = payload.get("x-thebes-answer")
        electronic_signature = payload.get("electronic_signature")
        encrypted_electronic_signature = await PasswordEncrypt.encrypt_password(
            electronic_signature
        )
        unique_id = thebes_answer["user"].get("unique_id")
        old = await user_repository.find_one({"unique_id": unique_id})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        if old.get("electronic_signature"):
            raise BadRequestError("user.electronic_signature.already_set")
        new_data = {
            "electronic_signature": encrypted_electronic_signature,
            "is_blocked_electronic_signature": False,
            "electronic_signature_wrong_attempts": 0,
        }

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await UserService.persephone_client.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_SET_ELECTRONIC_SIGNATURE.value,
            message=get_user_set_electronic_signature_schema_template_with_data(
                payload=new_data, unique_id=unique_id
            ),
            schema_name="user_set_electronic_signature_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        if await user_repository.update_one(old=old, new=new_data) is False:
            raise InternalServerError("common.process_issue")

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }

    @staticmethod
    async def forgot_electronic_signature(
        payload: dict,
        user_repository=UserRepository,
        authentication_service=AuthenticationService,
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        entity = await user_repository.find_one(
            {"unique_id": thebes_answer["user"].get("unique_id")}
        )
        if entity is None:
            raise BadRequestError("common.register_not_exists")

        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=entity, ttl=10
        ).build()
        jwt_payload_data.update({"forgot_electronic_signature": True})

        jwt = await JwtService.generate_token(jwt_payload_data=jwt_payload_data)

        authentication_service.send_authentication_email(
            email=entity.get("email"),
            payload_jwt=jwt,
            body="email.body.forgot_electronic_signature",
        )
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "email.forgot_electronic_signature",
        }

    @staticmethod
    async def onboarding_step_validator(payload: dict, onboard_step: List[str]):
        onboarding_steps = await UserService.get_onboarding_user_current_step(payload)
        payload_from_onboarding_steps = onboarding_steps.get("payload")
        current_onboarding_step = payload_from_onboarding_steps.get(
            "current_onboarding_step"
        )
        if current_onboarding_step not in onboard_step:
            raise BadRequestError("user.invalid_on_boarding_step")

    @staticmethod
    async def get_customer_registration_data(
        payload: dict,
        user_repository=UserRepository,
    ):
        thebes_answer = payload.get("x-thebes-answer")
        unique_id = thebes_answer["user"]["unique_id"]
        customer_registration_data = await user_repository.find_one(
            {"unique_id": unique_id}
        )
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
    async def update_customer_registration_data(
        payload: dict, user_repository=UserRepository
    ):
        await UserService.onboarding_step_validator(
            payload=payload, onboard_step=["finished", "user_data_validation"]
        )
        unique_id: str = payload["x-thebes-answer"]["user"]["unique_id"]
        update_customer_registration_data: dict = payload.get(
            "customer_registration_data"
        )
        old_customer_registration_data = await user_repository.find_one(
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

        (
            sent_to_persephone,
            status_sent_to_persephone,
        ) = await UserService.persephone_client.send_to_persephone(
            topic=config("PERSEPHONE_TOPIC_USER"),
            partition=PersephoneQueue.USER_UPDATE_REGISTER_DATA.value,
            message=user_update_register_schema,
            schema_name="user_update_register_data_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        del new_customer_registration_data["_id"]

        if not await user_repository.update_one(
            old={"unique_id": unique_id}, new=new_customer_registration_data
        ):
            raise InternalServerError("common.process_issue")

        await SinacorService.save_or_update_client_data(
            user_data=new_customer_registration_data
        )

        if not await user_repository.update_one(
            old={"unique_id": unique_id},
            new={
                "scope.user_level": UserLevel.CLIENT.value,
                "is_bureau_data_validated": True,
            },
        ):
            raise InternalServerError("common.process_issue")

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }
