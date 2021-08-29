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
from mist_client.asgard import Mist
from src.domain.sphinx_constants import *


def route_is_third_part_access(
    url_request: str, third_part_access_path: set, method: str = None
) -> bool:
    if url_request is None:
        raise NoPath("No path found")

    return url_request in third_part_access_path


def route_is_public(url_request: str, method: str = None) -> bool:
    if url_request is None:
        raise NoPath("No path found")

    public_route = False

    if method == "POST":
        if url_request in PUBLIC_PATHS_POST:
            public_route = True

    else:
        if url_request in PUBLIC_PATHS_GET:
            public_route = True

    return public_route


def need_be_admin(url_request: str) -> bool:
    if url_request is None:
        raise NoPath("No path found")
    must_be_admin = False
    if url_request in PRIVATE_PATHS:
        must_be_admin = True
    return must_be_admin


def need_electronic_signature(url_request: str) -> bool:
    if url_request is None:
        raise NoPath("No path found")
    must_have_electronic_signature = False
    if url_request in PATH_WITH_ELECTRONIC_SIGNATURE_REQUIRED:
        must_have_electronic_signature = True
    return must_have_electronic_signature


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
    is_signed_route = True
    is_electronic_signature_valid = False

    if user_data:
        token_is_valid = invalidate_user(user_data=user_data, jwt_data=jwt_data)
        is_admin_route = need_be_admin(url_request=request.url.path)
        is_admin = user_data.get("is_admin")
        is_signed_route = need_electronic_signature(url_request=request.url.path)
        is_electronic_signature_valid = validate_electronic_signature(
            request=request, user_data=user_data
        )

    if (
        token_is_valid is False
        or (is_admin_route and is_admin is False)
        or (is_signed_route and is_electronic_signature_valid is False)
    ):
        locale = get_language_from_request(request=request)
        message = i18n.get_translate("invalid_credential", locale=locale,)
        status_code = status.HTTP_401_UNAUTHORIZED
        content = {"detail": [{"msg": message}]}
        return Response(content=json.dumps(content), status_code=status_code)
    return True


def validate_electronic_signature(request: Request, user_data: dict) -> bool:
    mist_token = None
    for header_tuple in request.headers.raw:
        if b"x-mist" in header_tuple:
            mist_token = header_tuple[1].decode()
            break
    logger = logging.getLogger(config("LOG_NAME"))
    mist = Mist(logger)
    is_valid = mist.validate_jwt(jwt=mist_token)
    if is_valid:
        content = mist.decrypt_payload(jwt=mist_token)
    return False
    # TODO: Make Changes here


def check_if_third_party_user_is_not_allowed_to_access_route(request: Request):
    thebes_answer = None
    for header_tuple in request.headers.raw:
        if b"x-thebes-answer" in header_tuple:
            thebes_answer = header_tuple[1].decode()
            break
    if thebes_answer != config("THIRD_PARTY_TOKEN"):
        locale = get_language_from_request(request=request)
        message = i18n.get_translate("invalid_credential", locale=locale,)
        return Response(
            content=json.dumps({"detail": [{"msg": message}]}),
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    return True
