from src.repositories.user.repository import UserRepository
from src.utils.jwt_utils import JWTHandler
from src.exceptions.exceptions import (
    BadRequestError,
    UnauthorizedError,
    InternalServerError,
)
from fastapi import status
from src.utils.genarate_id import hash_field


class AuthenticationService:
    @staticmethod
    def answer(
        payload: dict, user_repository=UserRepository(), token_handler=JWTHandler
    ):
        old = user_repository.find_one({"_id": payload.get("email")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        new = dict(old)
        if old.get("is_active") is False:
            new.update(
                {
                    "is_active": True,
                    "use_magic_link": True,
                    "scope": {"view_type": "default", "features": ["default"]},
                }
            )
            if user_repository.update_one(old=old, new=new) is False:
                raise InternalServerError("common.process_issue")
        jwt = token_handler.generate_token(payload=new, ttl=525600)
        return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}

    @staticmethod
    def login(
        payload: dict, user_repository=UserRepository(), token_handler=JWTHandler
    ):
        entity = user_repository.find_one({"_id": payload.get("email")})
        if entity is None:
            raise BadRequestError("common.register_not_exists")
        if entity.get("use_magic_link") is True:
            # TODO: ENVIAR EMAIL, AVISAR Q ELE PRECVISA VE RO EMAIL
            pass
        else:
            pin = payload.get("pin")
            if pin is None:
                return {
                    "status_code": status.HTTP_200_OK,
                    "message_key": "user.need_pin",
                }
            if pin and hash_field(payload=pin) == entity.get("pin"):
                jwt = token_handler.generate_token(payload=entity, ttl=525600)
                return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}
            else:
                raise UnauthorizedError("user.pin_error")
