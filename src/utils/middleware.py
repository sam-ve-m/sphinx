# NATIVE LIBRARIES
import logging
from typing import Union
import json

# OUTSIDE LIBRARIES
from fastapi import Request, Response, status
from datetime import datetime

# SPHINX
from src.utils.env_config import config
from src.repositories.user.repository import UserRepository
from src.i18n.i18n_resolver import i18nResolver as i18n
from src.utils.language_identifier import get_language_from_request
from src.exceptions.exceptions import NoPath


def route_is_third_part_access(url_request: str, method: str = None) -> bool:
    if url_request is None:
        raise NoPath("No path found")
    third_part_access_path = [
        "/client_register_enums/type_of_income_tax",
        "/client_register_enums/client_type",
        "/client_register_enums/investor_type",
        "/client_register_enums/activity_type",
        "/client_register_enums/type_ability_person",
        "/client_register_enums/customer_qualification_type",
        "/client_register_enums/cosif_tax_classification",
        "/client_register_enums/marital_status",
        "/client_register_enums/nationality",
        "/client_register_enums/document_issuing_body",
        "/client_register_enums/document_type",
        "/client_register_enums/county",
        "/client_register_enums/state",
        "/client_register_enums/country",
        "/client_register_enums/marriage_regime",
        "/client_register_enums/customer_origin",
        "/client_register_enums/customer_status",
        "/client_register_enums/bmf_customer_type",
        "/client_register_enums/economic_activity",
        "/client_register_enums/account_type",
        "/bureau_callback",
    ]
    return url_request in third_part_access_path


def route_is_public(url_request: str, method: str = None) -> bool:
    if url_request is None:
        raise NoPath("No path found")

    public_route = False
    public_paths_get = [
        "/term",
        "/terms",
        "/docs",
        "/openapi.json",
        "/thebes_gate",
        "/user/forgot_password",
    ]

    public_paths_post = [
        "/user",
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
    private_paths = ["/user/admin", "/views", "/feature", "/term", "/suitability/quiz"]
    if url_request in private_paths:
        need_admin = True

    return need_admin


def is_user_active(user_data: dict) -> bool:
    return user_data.get("is_active_user")


def is_user_token_valid(user_data: dict, jwt_data: dict) -> bool:
    try:
        user_created = str(user_data.get("token_valid_after"))
        jwt_created_at = jwt_data.get("created_at")
        is_token_valid = jwt_created_at >= user_created
        return is_token_valid
    except ValueError:
        return False
    except Exception as e:
        logger = logging.getLogger(config("LOG_NAME"))
        logger.error(e, exc_info=True)
        return False


def invalidate_user(user_data: dict, jwt_data: dict) -> bool:
    is_active_user = is_user_active(user_data=user_data)
    if is_active_user:
        return is_user_token_valid(user_data=user_data, jwt_data=jwt_data)
    return False


def check_if_is_user_not_allowed_to_access_route(
    request: Request, jwt_data: dict, user_repository: UserRepository = UserRepository()
) -> Union[Response, bool]:
    user_data = user_repository.find_one({"_id": jwt_data["email"]}, ttl=60)

    token_is_valid = False
    is_admin_route = True
    is_admin = False

    if user_data:
        token_is_valid = invalidate_user(user_data=user_data, jwt_data=jwt_data)
        is_admin_route = need_be_admin(url_request=request.url.path)
        is_admin = user_data.get("is_admin")

    if token_is_valid is False or (is_admin_route and is_admin is False):
        locale = get_language_from_request(request=request)
        message = i18n.get_translate(
            "invalid_credential",
            locale=locale,
        )
        status_code = status.HTTP_401_UNAUTHORIZED
        content = {"detail": [{"msg": message}]}
        return Response(content=json.dumps(content), status_code=status_code)
    return True


def check_if_third_party_user_is_not_allowed_to_access_route(request: Request):
    thebes_answer = None
    for header_tuple in request.headers.raw:
        if b"x-thebes-answer" in header_tuple:
            thebes_answer = header_tuple[1].decode()
            break
    if thebes_answer != config("THIRD_PARTY_TOKEN"):
        locale = get_language_from_request(request=request)
        message = i18n.get_translate(
            "invalid_credential",
            locale=locale,
        )
        return Response(
            content=json.dumps({"detail": [{"msg": message}]}),
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    return True
