from fastapi import Request, Response, status
import json
from jwt import JWT, jwk_from_dict, jwk_from_pem
from jwt.utils import get_int_from_datetime
from datetime import datetime, timezone
from src.exceptions.exceptions import InternalServerError, UnauthorizedError
import logging
from datetime import timedelta
from decouple import config


from src.i18n.i18n_resolver import i18nResolver as i18n
from src.utils.language_identifier import get_language_from_request


class JWTHandler:

    instance = JWT()

    @staticmethod
    def generate_token(payload: dict, ttl: int = 5):
        """The ttl value in minutes"""
        payload.update(
            {
                "exp": get_int_from_datetime(
                    datetime.now(timezone.utc) + timedelta(minutes=ttl)
                ),
                "created_at": datetime.now(),
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
    def decrypt_payload(encrypted_payload: str):
        try:
            with open("src/keys/id_rsa.json", "r") as fh:
                verifying_key = jwk_from_dict(json.load(fh))
            payload = JWTHandler.instance.decode(
                encrypted_payload, verifying_key, do_time_check=True
            )
            return payload
        except:
            raise InternalServerError("common.process_issue")

    @staticmethod
    def filter_payload_to_jwt(payload: dict):
        new_payload = {
            "name": payload.get("name"),
            "email": payload.get("email"),
            "scope": payload.get("scope"),
            "is_active": payload.get("is_active"),
            "created_at": str(payload.get("created_at")),
            "deleted": payload.get("deleted"),
        }
        if payload.get("is_admin"):
            new_payload.update({"is_admin": payload.get("is_admin")})
        return new_payload

    @staticmethod
    def get_payload_from_request(request: Request):
        thebes_answer = None
        for header_tuple in request.headers.raw:
            if b"thebes_answer" in header_tuple:
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
