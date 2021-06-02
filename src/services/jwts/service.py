from src.repositories.jwt.repository import JwtRepository
from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.utils.genarate_id import generate_id, hash_field
from datetime import datetime
from fastapi import status


class JwtService:
    @staticmethod
    def insert_one(jwt: str, email: str, jwt_repository=JwtRepository(),) -> dict:
        try:
            jwt_repository.insert({"jwt": jwt, "email": email})
        except Exception:
            raise InternalServerError("common.process_issue")
