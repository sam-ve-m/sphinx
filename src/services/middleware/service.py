# NATIVE LIBRARIES
from etria_logger import Gladsheim
from typing import Optional

# OUTSIDE LIBRARIES
from fastapi import Request


# SPHINX
from datetime import timezone
from src.repositories.user.repository import UserRepository
from src.services.jwts.service import JwtService
from mist_client import MistStatusResponses


class MiddlewareService:
    @staticmethod
    async def get_valid_user_from_database(
        token: dict, user_repository=UserRepository()
    ) -> Optional[dict]:
        user_data = await user_repository.find_one(
            query={"unique_id": token["user"]["unique_id"]}
        )
        if user_data and user_data.get("is_active_user"):
            return user_data



    @staticmethod
    def is_user_token_life_time_valid(user_data: dict, token: dict) -> bool:
        try:
            token_valid_after = user_data["token_valid_after"]
            token_valid_after = token_valid_after.replace(tzinfo=timezone.utc)
            user_created = token_valid_after.timestamp()
            jwt_created_at = token["created_at"]
            is_token_valid = jwt_created_at >= user_created
            return is_token_valid
        except ValueError:
            return False
        except AttributeError as e:
            Gladsheim.error(
                error=e,
                message="Hey they joke with you probably token_valid_after from user_data isn't a datetime.datetime object.",
            )
        except Exception as e:
            Gladsheim.error(error=e)
            return False

    @staticmethod
    async def get_valid_admin_from_database(
        token: dict, user_repository=UserRepository()
    ) -> Optional[dict]:
        user_data = await user_repository.find_one(
            query={"unique_id": token["unique_id"]}
        )
        if user_data and user_data["is_active_user"] and user_data.get("is_admin"):
            return user_data

    @staticmethod
    async def validate_electronic_signature(
        request: Request, user_data: dict, jwt_handler=JwtService
    ) -> bool:
        mist_token = None
        for header_tuple in request.headers.raw:
            if b"x-mist" in header_tuple:
                mist_token = header_tuple[1].decode()
                break
        is_valid = await jwt_handler.mist.validate_jwt(jwt=mist_token)
        if is_valid:
            mist_content, status = await jwt_handler.mist.decode_payload(jwt=mist_token)
            if (
                status == MistStatusResponses.SUCCESS
                and user_data["unique_id"] == mist_content["decoded_jwt"]["unique_id"]
            ):
                return True
        return False

    @staticmethod
    async def get_token_if_token_is_valid(
        request: Request, jwt_handler=JwtService
    ) -> Optional[dict]:
        try:
            return await jwt_handler.get_thebes_answer_from_request(request=request)
        except BaseException as e:
            Gladsheim.error(error=e)
