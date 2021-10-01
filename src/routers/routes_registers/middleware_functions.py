# NATIVE LIBRARIES
import logging
from typing import Optional

# OUTSIDE LIBRARIES
from fastapi import Request


# SPHINX
from src.infrastructures.env_config import config
from src.repositories.user.repository import UserRepository
from src.utils.jwt_utils import JWTHandler


class MiddlewareUtils:

    @staticmethod
    def get_valid_user_from_database(
        token: dict, user_repository=UserRepository()
    ) -> Optional[dict]:
        user_data = user_repository.find_one(query={"_id": token["email"]})
        if user_data and user_data.get("is_active_user"):
            return user_data

    @staticmethod
    def is_user_token_life_time_valid(user_data: dict, token: dict) -> bool:
        try:
            user_created = str(user_data["token_valid_after"])
            jwt_created_at = token["created_at"]
            is_token_valid = jwt_created_at >= user_created
            return is_token_valid
        except ValueError:
            return False
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            return False

    @staticmethod
    def get_valid_admin_from_database(
        token: dict, user_repository=UserRepository()
    ) -> Optional[dict]:
        user_data = user_repository.find_one(query={"_id": token["email"]})
        if user_data and user_data["is_active_user"] and user_data.get("is_admin"):
            return user_data

    @staticmethod
    def validate_electronic_signature(
        request: Request, user_data: dict, jwt_handler=JWTHandler
    ) -> bool:
        mist_token = None
        for header_tuple in request.headers.raw:
            if b"x-mist" in header_tuple:
                mist_token = header_tuple[1].decode()
                break
        is_valid = jwt_handler.mist.validate_jwt(jwt=mist_token)
        if is_valid:
            mist_content = jwt_handler.mist.decrypt_payload(jwt=mist_token)
            if user_data["email"] == mist_content["email"]:
                return True
        return False

    @staticmethod
    def get_token_if_token_is_valid(
        request: Request, jwt_handler=JWTHandler
    ) -> Optional[dict]:
        try:
            return jwt_handler.get_thebes_answer_from_request(request=request)
        except BaseException as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
