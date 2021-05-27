import json
from jwt import JWT, jwk_from_dict, jwk_from_pem
from jwt.utils import get_int_from_datetime
from datetime import datetime, timezone
from src.exceptions.exceptions import InternalServerError

from datetime import timedelta


class JWTHandler:

    instance = JWT()

    @staticmethod
    def generate_token(payload: dict, ttl: int = 5):
        """The ttl value in minutes"""
        payload.update(
            {
                "exp": get_int_from_datetime(
                    datetime.now(timezone.utc) + timedelta(minutes=ttl)
                )
            }
        )
        try:
            with open("src/keys/id_rsa", "rb") as fh:
                signing_key = jwk_from_pem(fh.read())
            compact_jws = JWTHandler.instance.encode(
                JWTHandler.filter_payload_to_jwt(payload), signing_key, alg="RS256"
            )
            print(compact_jws)
            return compact_jws
        except:
            raise InternalServerError("common.process_issue")

    @staticmethod
    def decrpty_to_paylod(crypted_payload: str):
        try:
            with open("src/keys/id_rsa.json", "r") as fh:
                verifying_key = jwk_from_dict(json.load(fh))
            payload = JWTHandler.instance.decode(
                crypted_payload, verifying_key, do_time_check=True
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
        }
        return new_payload
