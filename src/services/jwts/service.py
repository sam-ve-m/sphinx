# STANDARD LIBS
from typing import Optional
import logging
from src.infrastructures.env_config import config

# OUTSIDE LIBRARIES
from fastapi import Request
from jwt import JWT
from jwt.jwk import jwk_from_pem

from heimdall_client.bifrost import Heimdall
from mist_client.asgard import Mist

# SPHINX
from src.repositories.jwt.repository import JwtRepository
from src.exceptions.exceptions import InternalServerError, UnauthorizedError
from src.services.builders.thebes_hall.builder import ThebesHallBuilder


class JwtService:

    instance = JWT()
    logger = logging.getLogger(config("LOG_NAME"))
    heimdall = Heimdall(logger=logging.getLogger(config("LOG_NAME")))
    mist = Mist(logger=logging.getLogger(config("LOG_NAME")))

    @staticmethod
    def insert_one(jwt: str, email: str, jwt_repository=JwtRepository()) -> None:
        try:
            jwt_repository.insert({"jwt": jwt, "email": email})
        except Exception:
            raise InternalServerError("common.process_issue")

    @classmethod
    def generate_token(
        cls, user_data: dict, kwargs_to_add_on_jwt: dict = None, ttl: int = 5
    ) -> Optional[str]:
        """The ttl value in minutes"""
        try:
            with open("src/keys/id_rsa", "rb") as fh:
                signing_key = jwk_from_pem(fh.read())

            thebes_hall_builder = ThebesHallBuilder(
                user_data=user_data, kwargs_to_add_on_jwt=kwargs_to_add_on_jwt, ttl=ttl
            )
            payload_to_jwt = thebes_hall_builder.build()
            compact_jws = cls.instance.encode(payload_to_jwt, signing_key, alg="RS256")
            return compact_jws
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            raise InternalServerError("common.process_issue")

    @classmethod
    def decrypt_payload(cls, encrypted_payload: str) -> Optional[dict]:
        try:
            payload = cls.heimdall.decrypt_payload(jwt=encrypted_payload)
            return payload
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            raise InternalServerError("common.process_issue")

    @staticmethod
    def get_jwt_from_request(request: Request):
        thebes_answer = None
        for header_tuple in request.headers.raw:
            if b"x-thebes-answer" in header_tuple:
                thebes_answer = header_tuple[1].decode()
                break
        return thebes_answer

    @staticmethod
    def get_thebes_answer_from_request(request: Request) -> dict:
        jwt = JwtService.get_jwt_from_request(request=request)
        if jwt is None:
            raise UnauthorizedError("Token not supplied")
        payload = dict(JwtService.decrypt_payload(jwt))
        return payload

    @classmethod
    def generate_session_jwt(cls, electronic_signature: dict, email: str):
        session_dict = {
            "email": email,
            "password": electronic_signature.get("signature"),
            "signatureExpireTime": electronic_signature.get("signature_expire_time"),
        }
        return cls.mist.generate_jwt(jwt=session_dict)
