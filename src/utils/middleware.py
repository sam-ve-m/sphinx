# NATIVE LIBRARIES
import logging
from typing import Union
import json

# OUTSIDE LIBRARIES
from fastapi import Request, Response, status
from datetime import datetime
from decouple import config

# SPHINX
from src.repositories.user.repository import UserRepository
from src.i18n.i18n_resolver import i18nResolver as i18n
from src.utils.language_identifier import get_language_from_request
from src.exceptions.exceptions import NoPath


def route_is_public(url_request: str, method: str = None) -> bool:
    if url_request is None:
        raise NoPath("No path found")

    public_route = False
    public_paths_get = [
        "/term",
        "/docs",
        "/openapi.json",
        "/thebes_gate",
        "/thebes_hall",
    ]

    public_paths_post = [
        "/user",
        "/user/forgot_password",
        "/login",
        "/login/admin",
    ]
    if method == "POST":
        if url_request in public_paths_post:
            public_route = True

    else:
        if url_request in public_paths_get:
            public_route = True

    return public_route


def need_be_admin(url_request: str) -> bool:
    if url_request is None:
        raise NoPath("No path found")

    need_admin = False
    private_paths = ["/user/admin", "/views", "/feature", "/term"]
    if url_request in private_paths:
        need_admin = True

    return need_admin


def is_user_deleted(user_data: dict) -> bool:
    return user_data.get("deleted")


def is_user_active(user_data: dict) -> bool:
    return user_data.get("is_active")


def is_user_token_valid(user_data: dict, jwt_data: dict) -> bool:
    try:
        user_created = str(user_data.get("token_valid_after"))
        jwt_created_at = jwt_data.get("created_at")
        is_token_valid = jwt_created_at > user_created
        return is_token_valid
    except ValueError:
        return False
    except Exception as e:
        logger = logging.getLogger(config("LOG_NAME"))
        logger.error(e, exc_info=True)
        return False


def invalidate_user(user_data: dict, jwt_data: dict) -> bool:
    is_deleted = is_user_deleted(user_data=user_data)
    is_active = is_user_active(user_data=user_data)
    if not is_deleted and is_active:
        return is_user_token_valid(user_data=user_data, jwt_data=jwt_data)
    return False


def check_if_is_user_not_allowed_to_access_route(
    request: Request, jwt_data: dict, user_repository: UserRepository = UserRepository()
) -> Union[Response, bool]:
    user_data = user_repository.find_one({"_id": jwt_data["email"]}, ttl=60)
    token_is_valid = invalidate_user(user_data=user_data, jwt_data=jwt_data)
    is_admin_route = need_be_admin(url_request=request.url.path)
    is_admin = user_data.get("is_admin")
    content = {"message": None}
    locale = get_language_from_request(request=request)
    message = i18n.get_translate(
        "valid_credential",
        locale=locale,
    )
    status_code = 200
    return_response = False
    if not token_is_valid:
        message = i18n.get_translate(
            "invalid_credential",
            locale=locale,
        )
        status_code = status.HTTP_401_UNAUTHORIZED
        return_response = True
    elif is_admin_route:
        if not is_admin:
            message = i18n.get_translate(
                "invalid_credential",
                locale=locale,
            )
            status_code = status.HTTP_401_UNAUTHORIZED
            return_response = True
    if return_response:
        content.update({"message": message})
        return Response(content=json.dumps(content), status_code=status_code)
    return True
