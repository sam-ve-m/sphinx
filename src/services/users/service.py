from src.repositories.user.repository import UserRepository
from src.repositories.file.repository import FileRepository, UserFileType
from src.services.authentications.service import AuthenticationService
from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.utils.genarate_id import generate_id, hash_field
from src.utils.jwt_utils import JWTHandler
from datetime import datetime
from fastapi import status
from decouple import config


class UserService:
    @staticmethod
    def create(
        payload: dict,
        user_repository=UserRepository(),
        authentication_service=AuthenticationService,
    ) -> dict:
        payload = generate_id("email", payload, must_remove=False)
        email = payload.get("email")
        payload = hash_field(key="pin", payload=payload)
        if user_repository.find_one({"_id": payload.get("_id")}) is not None:
            raise BadRequestError("common.register_exists")

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
            }
        )

        if user_repository.insert(payload):
            authentication_service.send_authentication_email(
                email=email, payload=payload, ttl=10, body="email.body.created"
            )
            return {
                "status_code": status.HTTP_201_CREATED,
                "message_key": "user.created",
            }
        else:
            raise InternalServerError("common.process_issue")

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
        if user_repository.update_one(old=old, new=new):
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "requests.updated",
            }
        else:
            raise InternalServerError("common.process_issue")

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
        if user_repository.update_one(old=old, new=new):
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "requests.updated",
            }
        else:
            raise InternalServerError("common.process_issue")

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
        if user_repository.update_one(old=old, new=new):
            jwt = token_handler.generate_token(payload=new, ttl=525600)
            return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}
        else:
            raise InternalServerError("common.process_issue")

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
        if user_repository.update_one(old=old, new=new):
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "user.all_logged_out",
            }
        else:
            raise InternalServerError("common.process_issue")

    @staticmethod
    def add_feature(
        payload: dict, user_repository=UserRepository(), token_handler=JWTHandler
    ) -> dict:
        old = payload.get("thebes_answer")
        new = dict(old)
        new_scope = new.get("scope")
        if payload.get("feature") not in new_scope.get("features"):
            new_scope.get("features").append(payload.get("feature"))
            new.update({"scope": new_scope})
            if user_repository.update_one(old=old, new=new):
                jwt = token_handler.generate_token(payload=new, ttl=525600)
                return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}
            else:
                raise InternalServerError("common.process_issue")
        else:
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
        if payload.get("feature") in new_scope.get("features"):
            new_scope.get("features").remove(payload.get("feature"))
            new.update({"scope": new_scope})
            if user_repository.update_one(old=old, new=new):
                jwt = token_handler.generate_token(payload=new, ttl=525600)
                return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}
            else:
                raise InternalServerError("common.process_issue")
        else:
            jwt = token_handler.generate_token(payload=new, ttl=525600)
            return {
                "status_code": status.HTTP_304_NOT_MODIFIED,
                "payload": {"jwt": jwt},
            }

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
    def assign_term(
        payload: dict,
        file_repository=FileRepository(bucket_name=config("AWS_BUCKET_TERMS")),
        user_repository=UserRepository(),
        token_handler=JWTHandler,
    ) -> dict:
        thebes_answer = payload.get("thebes_answer")
        old = user_repository.find_one({"_id": thebes_answer.get("email")})
        if old:
            file_type = payload.get("file_type")
            new = dict(old)
            version = file_repository.get_term_version(file_type=file_type)
            if new.get('terms') is None:
                new["terms"] = dict()
            new["terms"][file_type.value] = {
                "version": version,
                "date": datetime.now(),
                "id_deprecated": False,
            }
            if user_repository.update_one(old=old, new=new):
                jwt = token_handler.generate_token(payload=new, ttl=525600)
                return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}
            else:
                raise InternalServerError("common.process_issue")
        raise BadRequestError("common.register_not_exists")
