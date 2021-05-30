from fastapi import Request, Response
from datetime import datetime

from src.repositories.user.repository import UserRepository
from src.utils.jwt_utils import JWTHandler


def is_public(request: Request):
    return request.method == "POST" and request.url.path in [
        "/user",
        "/user/forgot_password",
        "/login",
        "/login/admin",
    ]


def need_be_admin(request: Request):
    return (
        request.url.path == "/user_admin"
        or request.url.path.startswith("/view")
        or request.url.path.startswith("/feature")
    )


def need_be_admin(request: Request):
    return (
        request.url.path == "/user_admin"
        or request.url.path.startswith("/view")
        or request.url.path.startswith("/feature")
    )


def user_not_allowed(user_data: dict, jwt_data: dict) -> bool:
    try:
        is_deleted = user_data.get("deleted")
        token_valid_after = user_data.get("token_valid_after")
        token_created_at = datetime.strptime(jwt_data.get("created_at"), '%Y-%m-%d %H:%M:%S.%f')
        is_token_invalid = token_valid_after > token_created_at
        return is_token_invalid or is_deleted
    except Exception as e:
        print(e)
        return False


def validate_user(request: Request):
    user_repository = UserRepository()
    jwt_data = JWTHandler.get_payload_from_request(request=request)
    if user_not_allowed(
            user_data=user_repository.find_one({"email": jwt_data["email"]}),
            jwt_data=jwt_data
    ):
        return "invalid_token"
    return None
