# NATIVE LIBRARIES
from typing import Optional

# OUTSIDE LIBRARIES
from fastapi import Request


class StubMiddlewareUtils:
    @staticmethod
    def get_valid_user_from_database(token: dict, user_repository) -> Optional[dict]:
        pass

    @staticmethod
    def is_user_token_life_time_valid(user_data: dict, token: dict) -> bool:
        pass

    @staticmethod
    def get_valid_admin_from_database(token: dict, user_repository) -> Optional[dict]:
        pass

    @staticmethod
    def validate_electronic_signature(
        request: Request, user_data: dict, jwt_handler
    ) -> bool:
        pass

    @staticmethod
    def get_token_if_token_is_valid(request: Request, jwt_handler) -> Optional[dict]:
        pass
