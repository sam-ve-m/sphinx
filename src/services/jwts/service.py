# STANDARD LIBS
from typing import Optional
import json
from etria_logger import Gladsheim

# OUTSIDE LIBRARIES
from fastapi import Request
from jwt import JWT
from jwt.jwk import jwk_from_dict

from heimdall_client import Heimdall, HeimdallStatusResponses
from mist_client import Mist, MistStatusResponses

# SPHINX
from src.infrastructures.env_config import config
from src.repositories.jwt.repository import JwtRepository
from src.repositories.bucket.repository import Bucket
from src.exceptions.exceptions import InternalServerError, UnauthorizedError


BUCKET_NAME_KEY = config("BUCKET_NAME_KEY")


class JwtService:

    instance = JWT()
    heimdall = Heimdall
    mist = Mist
    jwt_repository = JwtRepository
    bucket = Bucket

    @classmethod
    async def insert_one(cls, jwt: str, email: str) -> None:
        try:
            await cls.jwt_repository.insert({"jwt": jwt, "email": email})
        except Exception:
            raise InternalServerError("common.process_issue")

    @classmethod
    async def generate_token(cls, jwt_payload_data: dict) -> Optional[str]:
        """The ttl value in minutes"""
        try:
            key = await cls.bucket.get_jwt_key_file(BUCKET_NAME_KEY)
            signing_key = jwk_from_dict(json.loads(key))
            compact_jws = cls.instance.encode(
                jwt_payload_data, signing_key, alg="RS256"
            )
            return compact_jws
        except Exception as e:
            Gladsheim.error(error=e)
            raise InternalServerError("common.process_issue")

    @classmethod
    async def decrypt_payload(cls, encrypted_payload: str) -> Optional[dict]:
        payload, status = await cls.heimdall.decode_payload(jwt=encrypted_payload)
        if status != HeimdallStatusResponses.SUCCESS:
            Gladsheim.error(message=str(payload))
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
            "signature_expire_time": electronic_signature.get("signature_expire_time"),
        }
        payload, status = await cls.mist.generate_jwt(jwt_values=session_dict)
        if status != MistStatusResponses.SUCCESS:
            Gladsheim.error(message=str(payload))
            raise InternalServerError("common.process_issue")
        return payload
