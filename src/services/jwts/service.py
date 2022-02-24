# STANDARD LIBS
from typing import Optional
import logging
from src.infrastructures.env_config import config

# OUTSIDE LIBRARIES
from fastapi import Request
from jwt import JWT
from jwt.jwk import jwk_from_pem

from heimdall_client.bifrost import Heimdall, HeimdallStatusResponses
from mist_client.asgard import Mist
from mist_client.src.domain.enums.mist_status_responses import MistStatusResponses

# SPHINX
from src.repositories.jwt.repository import JwtRepository
from src.exceptions.exceptions import InternalServerError, UnauthorizedError


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
    def generate_token(cls, jwt_payload_data: dict) -> Optional[str]:
        """The ttl value in minutes"""
        try:
            with open("src/keys/id_rsa", "rb") as fh:
                signing_key = jwk_from_pem(fh.read())
            compact_jws = cls.instance.encode(
                jwt_payload_data, signing_key, alg="RS256"
            )
            return compact_jws
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            raise InternalServerError("common.process_issue")

    @classmethod
    def decrypt_payload(cls, encrypted_payload: str) -> Optional[dict]:
        payload, status = cls.heimdall.decode_payload(jwt=encrypted_payload)
        if status != HeimdallStatusResponses.SUCCESS:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(str(payload), exc_info=True)
            raise InternalServerError("common.process_issue")
        return payload["decoded_jwt"]

    @staticmethod
    def get_jwt_from_request(request: Request):
        thebes_answer = None
        for header_tuple in request.headers.raw:
            if b"x-thebes-answer" in header_tuple:
                thebes_answer = header_tuple[1].decode()
                break
        return thebes_answer

    @staticmethod
    async def get_thebes_answer_from_request(request: Request) -> dict:
        jwt = JwtService.get_jwt_from_request(request=request)
        if jwt is None:
            raise UnauthorizedError("Token not supplied")
        payload = dict(JwtService.decrypt_payload(jwt))
        return payload

    @classmethod
    async def generate_session_jwt(cls, electronic_signature: dict, unique_id: str):
        session_dict = {
            "unique_id": unique_id,
            "password": electronic_signature.get("signature"),
            "signatureExpireTime": electronic_signature.get("signature_expire_time"),
        }
        payload, status = await cls.mist.generate_jwt(jwt=session_dict)
        if status != MistStatusResponses.SUCCESS:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(str(payload), exc_info=True)
            raise InternalServerError("common.process_issue")
        return payload
