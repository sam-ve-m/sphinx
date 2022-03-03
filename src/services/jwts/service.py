# STANDARD LIBS
from typing import Optional
import logging
from src.infrastructures.env_config import config

# OUTSIDE LIBRARIES
from fastapi import Request
from jwt import JWT
from jwt.jwk import jwk_from_pem

from heimdall_client import Heimdall, HeimdallStatusResponses
from mist_client import Mist, MistStatusResponses

# SPHINX
from src.repositories.jwt.repository import JwtRepository
from src.exceptions.exceptions import InternalServerError, UnauthorizedError


class JwtService:

    instance = JWT()
    logger = logging.getLogger(config("LOG_NAME"))
    heimdall = Heimdall
    mist = Mist
    jwt_repository = JwtRepository()

    @classmethod
    async def insert_one(cls, jwt: str, email: str) -> None:
        try:
            await cls.jwt_repository.insert({"jwt": jwt, "email": email})
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
    async def decrypt_payload(cls, encrypted_payload: str) -> Optional[dict]:
        payload, status = await cls.heimdall.decode_payload(jwt=encrypted_payload)
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

    @classmethod
    async def get_thebes_answer_from_request(cls, request: Request) -> dict:
        jwt = JwtService.get_jwt_from_request(request=request)
        if jwt is None:
            raise UnauthorizedError("Token not supplied")
        payload = dict(await cls.decrypt_payload(jwt))
        return payload

    @classmethod
    async def generate_session_jwt(cls, electronic_signature: dict, unique_id: str):
        session_dict = {
            "unique_id": unique_id,
            "password": electronic_signature.get("signature"),
            "signatureExpireTime": electronic_signature.get("signature_expire_time"),
        }
        payload, status = await cls.mist.generate_jwt(jwt_values=session_dict)
        if status != MistStatusResponses.SUCCESS:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(str(payload), exc_info=True)
            raise InternalServerError("common.process_issue")
        return payload
