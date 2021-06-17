# STANDARD LIBS
from datetime import datetime
import logging

# OUTSIDE LIBRARIES
from fastapi import status
from decouple import config

# SPHINX
from src.interfaces.services.user.interface import IUser
from src.repositories.user.repository import UserRepository
from src.repositories.file.repository import FileRepository
from src.repositories.file.enum.user_file import UserFileType
from src.services.authentications.service import AuthenticationService
from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.utils.genarate_id import generate_id, hash_field
from src.utils.jwt_utils import JWTHandler
from src.utils.stone_age import StoneAge
from src.services.persephone.service import PersephoneService
from src.utils.persephone_templates import (
    get_prospect_user_template_with_data,
    get_user_signed_term_template_with_data,
    get_table_response_template_with_data,
    get_user_account_template_with_data,
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
        payload = hash_field(key="pin", payload=payload)
        if user_repository.find_one({"_id": payload.get("_id")}) is not None:
            raise BadRequestError("common.register_exists")
        UserService.add_user_control_metadata(payload=payload)

        sent_to_persephone = persephone_client.run(
            topic="thebes.sphinx_persephone.topic",
            partition=0,
            payload=get_prospect_user_template_with_data(payload=payload),
            schema_key="prospect_user_schema",
        )

        if (sent_to_persephone and user_repository.insert(payload)) is False:
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
    def add_user_control_metadata(payload: dict):
        payload.update(
            {
                "scope": {"view_type": None, "features": []},
                "is_active": False,
                "deleted": False,
                "use_magic_link": True,
                "token_valid_after": datetime.now(),
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
    def create_admin(payload: dict) -> dict:
        payload.update({"is_admin": True})
        UserService.create(payload=payload)

    @staticmethod
    def update(payload: dict, user_repository=UserRepository()) -> None:
        pass

    @staticmethod
    def delete(payload: dict, user_repository=UserRepository()) -> dict:
        old = user_repository.find_one({"_id": payload.get("email")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        new = dict(old)
        new.update({"deleted": True})
        if user_repository.update_one(old=old, new=new) is False:
            raise InternalServerError("common.process_issue")
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }

    @staticmethod
    def change_password(payload: dict, user_repository=UserRepository()) -> dict:
        thebes_answer = payload.get("thebes_answer")
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
        thebes_answer = payload.get("thebes_answer")
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
        old = payload.get("thebes_answer")
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
        old = payload.get("thebes_answer")
        new = dict(old)
        new_scope = new.get("scope")
        response = {"status_code": None, "payload": {"jwt": None}}
        if payload.get("feature") in new_scope.get("features"):
            new_scope.get("features").remove(payload.get("feature"))
            new.update({"scope": new_scope})
            if user_repository.update_one(old=old, new=new) is False:
                raise InternalServerError("common.process_issue")
            response.update({"status_code" : status.HTTP_200_OK})
        else:
            response.update({"status_code" : status.HTTP_304_NOT_MODIFIED})

        jwt = token_handler.generate_token(payload=new, ttl=525600)

        response.update({"jwt": jwt})

        return response

    @staticmethod
    def save_user_self(
        payload: dict,
        file_repository=FileRepository(bucket_name=config("AWS_BUCKET_USERS_SELF")),
    ) -> dict:
        thebes_answer = payload.get("thebes_answer")
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
        thebes_answer = payload.get("thebes_answer")
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
            topic="thebes.sphinx_persephone.topic",
            partition=1,
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
                payload.get("thebes_answer")
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
        payload: dict, user_repository=UserRepository(), stone_age=StoneAge,
    ) -> dict:
        thebes_answer = payload.get("thebes_answer")
        old = user_repository.find_one({"_id": thebes_answer.get("email")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        user_identifier = payload.get("user_identifier")
        quiz = stone_age.send_user_identifier_data(user_identifier_data=user_identifier)
        if type(quiz) is not dict:
            raise InternalServerError("user.quiz.trouble")
        new = dict(old)
        UserService.update_user_identifier_data(
            payload=new, user_identifier=user_identifier
        )
        if user_repository.update_one(old=old, new=new) is False:
            raise InternalServerError("common.process_issue")
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"quiz": quiz},
        }

    @staticmethod
    def update_user_identifier_data(payload: dict, user_identifier: dict):
        payload["cpf"] = user_identifier.get("cpf")
        payload["is_us_person"] = user_identifier.get("is_us_person")
        payload["us_tin"] = user_identifier.get("us_tin")
        payload["is_cvm_qualified_investor"] = user_identifier.get(
            "is_cvm_qualified_investor"
        )
        payload["marital"] = {
            "status": user_identifier.get("marital_status"),
            "spouse": user_identifier.get("spouse"),
        }

    @staticmethod
    def fill_user_data(
        payload: dict,
        user_repository=UserRepository(),
        stone_age=StoneAge,
        persephone_client=PersephoneService.get_client(),
    ) -> dict:
        thebes_answer = payload.get("thebes_answer")
        old = user_repository.find_one({"_id": thebes_answer.get("email")})
        if type(old) is not dict:
            raise BadRequestError("common.register_not_exists")
        stone_age_user_data = stone_age.send_user_quiz_responses(
            quiz=payload.get("quiz")
        )
        sent_to_persephone = persephone_client.run(
            topic="thebes.sphinx_persephone.topic",
            partition=3,
            payload=get_user_account_template_with_data(
                payload={
                    "stone_age_user_data": stone_age_user_data,
                    "user_data": dict(old),
                }
            ),
            schema_key="dtvm_user_schema",
        )
        if not sent_to_persephone:
            raise InternalServerError("common.process_issue")
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
    def table_callback(
        payload: dict, persephone_client=PersephoneService.get_client(),
    ) -> dict:
        payload.update(
            {
                "uuid": "lallals-2197na-askdabskdjbaskd",
                "cpf": 43056808820,
                "email": "msa@lionx.com.br",
                "status": "aproved",
            }
        )
        table_result = persephone_client.run(
            topic="thebes.sphinx_persephone.topic",
            partition=5,
            payload=get_table_response_template_with_data(payload=payload),
            schema_key="table_schema",
        )
        if table_result is False:
            raise InternalServerError("common.process_issue")
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "ok",
        }
