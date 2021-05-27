from src.repositories.user.repository import UserRepository
from src.utils.jwt_utils import JWTHandler
from src.exceptions.exceptions import BadRequestError, InternalServerError
from fastapi import status


class AuthenticationService:
    @staticmethod
    def answer(
        payload: dict, user_repository=UserRepository(), token_handler=JWTHandler
    ):
        old = user_repository.find_one({"_id": payload.get("email")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        new = dict(old)
        new.update(
            {
                "is_active": True,
                "scope": {"view_type": "default", "features": ["default"]},
            }
        )
        if user_repository.update_one(old=old, new=new):
            del new["pin"]
            del new["_id"]
            payload = token_handler.generate_token(payload=new, ttl=525600)
            return {"status_code": status.HTTP_200_OK, "payload": payload}
        else:
            raise InternalServerError("common.process_issue")
