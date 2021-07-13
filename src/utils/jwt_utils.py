# STANDARD LIBS
import os.path
from typing import Union, Optional
from datetime import datetime, timezone, timedelta
import logging
from src.utils.env_config import config
import json
from pathlib import Path

# OUTSIDE LIBRARIES
from fastapi import Request, Response, status
from jwt import JWT, jwk_from_dict, jwk_from_pem
from jwt.utils import get_int_from_datetime

# SPHINX
from src.i18n.i18n_resolver import i18nResolver as i18n
from src.utils.language_identifier import get_language_from_request
from src.exceptions.exceptions import InternalServerError
from src.services.builders.thebes_hall.thebes_hall import ThebesHall


class JWTHandler:
    # TODO change this method to use heimdall to validate the given jwt and this to generate the jwt only
    instance = JWT()

    @staticmethod
    def generate_token(payload: dict, ttl: int = 5) -> Optional[str]:
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
            compact_jws = JWTHandler.instance.encode(
                JWTHandler.filter_payload_to_jwt(payload), signing_key, alg="RS256"
            )
            return compact_jws
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            raise InternalServerError("common.process_issue")

    @staticmethod
    def decrypt_payload(encrypted_payload: str) -> Optional[dict]:
        try:
            base_path = Path(__file__).parents[1]
            path = os.path.join(base_path, "keys", "id_rsa.json")
            with open(path, "r") as fh:
                verifying_key = jwk_from_dict(json.load(fh))
            payload = JWTHandler.instance.decode(
                encrypted_payload, verifying_key, do_time_check=True
            )
            return payload
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            raise InternalServerError("common.process_issue")

    @staticmethod
    def filter_payload_to_jwt(payload: dict) -> dict:
        new_payload = JWTHandler.filter_payload_helper(payload=payload)
        JWTHandler.convert_datetime_field_in_str(payload=new_payload)
        if payload.get("is_admin"):
            new_payload.update({"is_admin": payload.get("is_admin")})
        return new_payload

    @staticmethod
    def filter_payload_helper(payload: dict) -> dict:
        ThebesHall.validate(payload=payload)
        suitability = payload.get("suitability")
        suitability_months_past = None
        if suitability:
            suitability_months_past = suitability.get("months_past")
        user_account_data = payload.get("user_account_data")
        user_account_data_months_past = None
        if user_account_data:
            user_account_data_months_past = user_account_data.get("months_past")
        new_payload = {
            "name": payload.get("name"),
            "email": payload.get("email"),
            "scope": payload.get("scope"),
            "is_active": payload.get("is_active"),
            "terms": payload.get("terms"),
            "suitability_months_past": suitability_months_past,
            "user_account_data_months_past": user_account_data_months_past,
            "exp": payload.get("exp"),
            "created_at": payload.get("created_at"),
            "on_boarding_steps": {},
        }
        return new_payload

    @staticmethod
    def convert_datetime_field_in_str(payload: dict) -> None:
        for key in payload:
            if isinstance(payload[key], dict):
                JWTHandler.convert_datetime_field_in_str(payload[key])
            elif isinstance(payload[key], datetime):
                payload[key] = str(payload[key])

    @staticmethod
    def get_payload_from_request(request: Request) -> Union[dict, Response]:
        thebes_answer = None
        for header_tuple in request.headers.raw:
            if b"x-thebes-answer" in header_tuple:
                thebes_answer = header_tuple[1].decode()
                break
        try:
            payload = dict(JWTHandler.decrypt_payload(thebes_answer))
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            lang = get_language_from_request(request=request)
            return Response(
                content=json.dumps(
                    {"message": i18n.get_translate(str(e), locale=lang)}
                ),
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        return payload
