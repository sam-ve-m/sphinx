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
    post_method = "POST" in request.method
    get_method = "GET" in request.method
    url_path = request.url.path
    public_path_list = ["/user", "/user/forgot_password", "/login", "/login/admin", ]
    term_path_list = ["/term", ]
    if post_method and url_path in public_path_list or get_method and url_path in term_path_list:
        return True
    return False


def need_be_admin(request: Request) -> bool:
    need_admin = False
    starts_with_user_admin = request.url.path.startswith("/user_admin")
    starts_with_views = request.url.path.startswith("/views")
    starts_with_feature = request.url.path.startswith("/feature")
    starts_with_term = request.url.path.startswith("/term")

    if starts_with_user_admin:
        need_admin = True
    elif starts_with_views:
        need_admin = True
    elif starts_with_feature:
        need_admin = True
    elif starts_with_term:
        need_admin = True
    return need_admin


def is_user_deleted(user_data: dict) -> bool:
    return user_data.get("deleted")


def is_user_token_valid(user_data: dict, jwt_data: dict) -> bool:
    try:
        token_valid_after = user_data.get("token_valid_after")
        user_created_at = jwt_data.get("created_at")
        is_token_invalid = token_valid_after > user_created_at
        return is_token_invalid
    except ValueError:
        return False
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
    token_is_valid = invalidate_user(user_data=user_data, jwt_data=jwt_data)
    is_admin_route = need_be_admin(request=request)
    is_admin = user_data.get("is_admin")
    content = {"message": None}
    locale = get_language_from_request(request=request)
    message = i18n.get_translate("valid_credential", locale=locale, )
    status_code = 200

    if not token_is_valid:
        status_code = status.HTTP_401_UNAUTHORIZED
    elif is_admin_route:
        if is_admin:
            message = i18n.get_translate("valid_credential", locale=locale, )
            status_code = status.HTTP_200_OK
        else:
            message = i18n.get_translate("invalid_credential", locale=locale, )
            status_code = status.HTTP_401_UNAUTHORIZED

    content.update({"message": message})
    return Response(content=json.dumps(content), status_code=status_code)