# SPHINX
from src.repositories.jwt.repository import JwtRepository
from src.exceptions.exceptions import InternalServerError


class JwtService:
    @staticmethod
    def insert_one(jwt: str, email: str, jwt_repository=JwtRepository()) -> None:
        try:
            jwt_repository.insert({"jwt": jwt, "email": email})
        except Exception:
            raise InternalServerError("common.process_issue")
