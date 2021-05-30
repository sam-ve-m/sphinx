from src.repositories.user.repository import UserRepository
from src.exceptions.exceptions import InternalServerError
from src.utils.jwt_utils import JWTHandler

from fastapi import status


class PurchaseService:
    @staticmethod
    def add_feature(
        payload: dict,
        user_repository=UserRepository(),
        token_handler=JWTHandler
    ) -> dict:
        old = payload.get("thebes_answer")
        new = dict(old)
        new_scope = new.get("scope")
        if payload.get("feature") not in new_scope.get("features"):
            new_scope.get("features").append(payload.get('feature'))
            new.update({"scope": new_scope})
            if user_repository.update_one(old=old, new=new):
                jwt = token_handler.generate_token(payload=new, ttl=525600)
                return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}
            else:
                raise InternalServerError("common.process_issue")
        else:
            jwt = token_handler.generate_token(payload=new, ttl=525600)
            return {"status_code": status.HTTP_304_NOT_MODIFIED, "payload": {"jwt": jwt}}



    @staticmethod
    def delete_feature(payload: dict, user_repository=UserRepository(),token_handler=JWTHandler) -> dict:
        old = payload.get("thebes_answer")
        new = dict(old)
        new_scope = new.get("scope")
        if payload.get("feature") in new_scope.get("features"):
            new_scope.get("features").remove(payload.get('feature'))
            new.update({"scope": new_scope})
            if user_repository.update_one(old=old, new=new):
                jwt = token_handler.generate_token(payload=new, ttl=525600)
                return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}
            else:
                raise InternalServerError("common.process_issue")
        else:
            jwt = token_handler.generate_token(payload=new, ttl=525600)
            return {"status_code": status.HTTP_304_NOT_MODIFIED, "payload": {"jwt": jwt}}
