# NATIVE LIBRARIES
import logging
from typing import Optional
import json

# OUTSIDE LIBRARIES
from fastapi import Request, Response, status
from datetime import datetime
from decouple import config

# SPHINX
from src.repositories.user.repository import UserRepository
from src.i18n.i18n_resolver import i18nResolver as i18n
from src.utils.language_identifier import get_language_from_request


def is_public(request: Request) -> bool:
    post_method = request.method == "POST"
    get_method = request.method == "POST"
    url_path = request.path
    public_path_list = ["/user", "/user/forgot_password", "/login", "/login/admin",]
    term_path_list = ["/term",]
    if post_method and url_path in public_path_list or get_method and url_path in term_path_list :
        return True

def need_be_admin(request: Request) -> bool:
    return (
        request.url.path == "/user_admin"
        or request.url.path.startswith("/views")
        or request.url.path.startswith("/feature")
        or (request.url.path == "/term" and request.method == "POST")
    )


def is_user_deleted(user_data: dict) -> bool:
    return user_data.get("deleted")


def is_user_token_valid(user_data: dict, jwt_data: dict) -> bool:
    try:
        token_valid_after = user_data.get("token_valid_after")
        token_created_at = datetime.strptime(
            jwt_data.get("created_at"), "%Y-%m-%d %H:%M:%S.%f"
        )
        is_token_invalid = token_valid_after > token_created_at
        return is_token_invalid
    except Exception as e:
        logger = logging.getLogger(config("LOG_NAME"))
        logger.error(e, exc_info=True)
        return False


def invalidate_user(user_data: dict, jwt_data: dict) -> bool:
    is_deleted = is_user_deleted(user_data=user_data)
    is_token_invalid = is_user_token_valid(user_data=user_data, jwt_data=jwt_data)
    return is_token_invalid or is_deleted


def check_if_is_user_not_allowed_to_access_route(
    request: Request, jwt_data: dict, user_repository: UserRepository = UserRepository()
) -> Optional[Response]:
    user_data = user_repository.find_one({"email": jwt_data["email"]}, ttl=60)
    user_not_allowed = invalidate_user(user_data=user_data, jwt_data=jwt_data)
    is_user_not_admin = (
        user_data.get("is_admin") is None or user_data.get("is_admin") is False
    )
    is_admin_route = need_be_admin(request=request)
    is_not_admin_user_accessing_admin_route = is_admin_route and is_user_not_admin

    if user_not_allowed or is_not_admin_user_accessing_admin_route:
        return Response(
            content=json.dumps(
                {
                    "message": i18n.get_translate(
                        "invalid_token",
                        locale=get_language_from_request(request=request),
                    )
                }
            ),
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
