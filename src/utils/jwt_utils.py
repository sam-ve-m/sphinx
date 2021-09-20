# STANDARD LIBS
import os.path
from typing import Union, Optional
from datetime import datetime, timezone, timedelta
import logging

from src.domain.solutiontech.client_import_status import SolutiontechClientImportStatus
from src.utils.env_config import config
import json
from pathlib import Path

# OUTSIDE LIBRARIES
from fastapi import Request, Response, status
from jwt import JWT, jwk_from_dict, jwk_from_pem
from jwt.utils import get_int_from_datetime
from heimdall_client.bifrost import Heimdall
from mist_client.asgard import Mist

# SPHINX
from src.i18n.i18n_resolver import i18nResolver as i18n
from src.utils.language_identifier import get_language_from_request
from src.exceptions.exceptions import InternalServerError
from src.services.builders.thebes_hall.thebes_hall import ThebesHall
from src.repositories.user.repository import UserRepository


class JWTHandler:
    # TODO change this method to use heimdall to validate the given jwt and this to generate the jwt only
    instance = JWT()
    logger = logging.getLogger(config("LOG_NAME"))
    heimdall = Heimdall(logger=logging.getLogger(config("LOG_NAME")))
    mist = Mist(logger=logging.getLogger(config("LOG_NAME")))

    @staticmethod
    def generate_token(payload: dict, args: dict = None, ttl: int = 5) -> Optional[str]:
        """The ttl value in minutes"""
        payload.update(
            {
                "exp": get_int_from_datetime(
                    datetime.utcnow() + timedelta(minutes=ttl)
                ),
                "created_at": datetime.utcnow(),
            }
        )
        try:
            with open("src/keys/id_rsa", "rb") as fh:
                signing_key = jwk_from_pem(fh.read())
            user_metadata_to_add_into_jwt = JWTHandler.filter_payload_to_jwt(
                payload, args=args
            )
            compact_jws = JWTHandler.instance.encode(
                user_metadata_to_add_into_jwt, signing_key, alg="RS256"
            )
            return compact_jws
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            raise InternalServerError("common.process_issue")

    @staticmethod
    def decrypt_payload(encrypted_payload: str) -> Optional[dict]:
        try:
            payload = JWTHandler.heimdall.decrypt_payload(jwt=encrypted_payload)
            return payload
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            raise InternalServerError("common.process_issue")

    @staticmethod
    def filter_payload_to_jwt(payload: dict, args: dict) -> dict:
        new_payload = JWTHandler.filter_payload_helper(payload=payload, args=args)
        JWTHandler.convert_datetime_field_in_str(payload=new_payload)
        if payload.get("is_admin"):
            new_payload.update({"is_admin": payload.get("is_admin")})
        return new_payload

    @staticmethod
    def filter_payload_helper(payload: dict, args: dict) -> dict:
        ThebesHall.validate(payload=payload)
        suitability_months_past = 0
        last_modified_date_months_past = 0
        suitability = payload.get("suitability")
        last_modified_date = payload.get("last_modified_date")

        if suitability:
            suitability_months_past = suitability.get("months_past")

        if last_modified_date:
            last_modified_date_months_past = last_modified_date.get("months_past")

        user_repository = UserRepository()

        new_payload = {
            "nick_name": payload.get("nick_name"),
            "email": payload.get("email"),
            "scope": payload.get("scope"),
            "is_active_user": payload.get("is_active_user"),
            "is_blocked_electronic_signature": payload.get(
                "is_blocked_electronic_signature"
            ),
            "terms": payload.get("terms"),
            "suitability_months_past": suitability_months_past,
            "last_modified_date_months_past": last_modified_date_months_past,
            "client_has_trade_allowed": False,
            "created_at": payload.get("created_at"),
            "exp": payload.get("exp"),
            "using_suitability_or_refuse_term": user_repository.is_user_using_suitability_or_refuse_term(
                user_email=payload.get("email")
            ),
        }

        if args is not None:
            new_payload.update(args)

        register_analyses = payload.get("register_analyses")
        bovespa_account = payload.get("bovespa_account")
        bmf_account = payload.get("bmf_account")

        if bmf_account and bovespa_account:
            new_payload.update(
                {"bovespa_account": bovespa_account, "bmf_account": bmf_account}
            )

        if register_analyses:
            new_payload.update({"register_analyses": register_analyses})

        solutiontech = payload.get("solutiontech")
        sincad = payload.get("sincad")
        sinacor = payload.get("sinacor")
        is_active_client = payload.get("is_active_client")

        client_has_trade_allowed = (
            solutiontech == SolutiontechClientImportStatus.SYNC.value
            and sincad
            and sinacor
            and is_active_client
            and suitability_months_past < 24
            and last_modified_date_months_past < 24
        )
        new_payload.update({"client_has_trade_allowed": client_has_trade_allowed})

        return new_payload

    @staticmethod
    def convert_datetime_field_in_str(payload: dict) -> None:
        for key in payload:
            if isinstance(payload[key], dict):
                JWTHandler.convert_datetime_field_in_str(payload[key])
            elif isinstance(payload[key], datetime):
                payload[key] = str(payload[key])

    @staticmethod
    def get_jwt_from_request(request: Request):
        thebes_answer = None
        for header_tuple in request.headers.raw:
            if b"x-thebes-answer" in header_tuple:
                thebes_answer = header_tuple[1].decode()
                break
        return thebes_answer

    @staticmethod
    def get_payload_from_request(request: Request) -> Union[dict, Response]:
        thebes_answer = JWTHandler.get_jwt_from_request(request=request)
        lang = get_language_from_request(request=request)
        if thebes_answer is None:
            return Response(
                content=json.dumps(
                    {
                        "detail": [
                            {"msg": i18n.get_translate("token_not_find", locale=lang)}
                        ]
                    }
                ),
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            payload = dict(JWTHandler.decrypt_payload(thebes_answer))
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            return Response(
                content=json.dumps(
                    {
                        "detail": [
                            {"msg": i18n.get_translate("invalid_token", locale=lang)}
                        ]
                    }
                ),
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        return payload

    @staticmethod
    def generate_session_jwt(electronic_signature: dict, email: str):
        session_dict = {
            "email": email,
            "password": electronic_signature.get("signature"),
            "signatureExpireTime": electronic_signature.get("signature_expire_time"),
        }
        return JWTHandler.mist.generate_jwt(jwt=session_dict)
