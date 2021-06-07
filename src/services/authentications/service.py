from src.repositories.user.repository import UserRepository
from src.controllers.jwts.controller import JwtController
from src.utils.jwt_utils import JWTHandler
from src.exceptions.exceptions import (
    BadRequestError,
    UnauthorizedError,
    InternalServerError,
)
from fastapi import status
from src.utils.email import HtmlModifier
from src.i18n.i18n_resolver import i18nResolver as i18n
from src.services.email_sender.grid_email_sender import EmailSender as SendGridEmail
from src.utils.genarate_id import hash_field
from decouple import config
from src.interfaces.services.authentication.interface import IAuthentication


class AuthenticationService(IAuthentication):
    @staticmethod
    def answer(
        payload: dict, user_repository=UserRepository(), token_handler=JWTHandler
    ) -> dict:
        old = user_repository.find_one({"_id": payload.get("email")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        new = dict(old)
        if old.get("is_active") is False:
            new.update(
                {
                    "is_active": True,
                    "use_magic_link": True,
                    "scope": {"view_type": "default", "features": ["default"]},
                }
            )
            if user_repository.update_one(old=old, new=new) is False:
                raise InternalServerError("common.process_issue")
        jwt = token_handler.generate_token(payload=new, ttl=525600)
        return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}

    @staticmethod
    def login(
        payload: dict, user_repository=UserRepository(), token_handler=JWTHandler
    ) -> dict:
        entity = user_repository.find_one({"_id": payload.get("email")})
        if entity is None:
            raise BadRequestError("common.register_not_exists")
        if entity.get("use_magic_link") is True:
            AuthenticationService.send_authentication_email(
                email=entity.get("email"),
                payload=entity,
                ttl=10,
                body="email.body.created",
            )
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "email.login",
            }
        else:
            pin = payload.get("pin")
            if pin is None:
                return {
                    "status_code": status.HTTP_200_OK,
                    "message_key": "user.need_pin",
                }
            if pin and hash_field(payload=pin) == entity.get("pin"):
                jwt = token_handler.generate_token(payload=entity, ttl=525600)
                JwtController.insert_one(jwt, entity.get("email"))
                return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}
            else:
                raise UnauthorizedError("user.pin_error")

    @staticmethod
    def send_authentication_email(
        email: str, payload: dict, body: str, ttl: int, email_sender=SendGridEmail
    ) -> None:
        payload_jwt = JWTHandler.generate_token(payload=payload, ttl=ttl)
        page = HtmlModifier(
            "src/services/asset",
            i18n.get_translate(key=body, locale="pt"),
            config("TARGET_LINK") + "/" + payload_jwt,
        )()
        email_sender.send_email_to(
            target_email=email,
            message=page,
            subject=i18n.get_translate(key="email.subject.created", locale="pt"),
        )

    @staticmethod
    def forgot_password(payload: dict, user_repository=UserRepository()) -> dict:
        entity = user_repository.find_one({"_id": payload.get("email")})
        if entity is None:
            raise BadRequestError("common.register_not_exists")
        AuthenticationService.send_authentication_email(
            email=entity.get("email"),
            payload=entity,
            ttl=10,
            body="email.body.forgot_password",
        )
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "user.forgot_password",
        }
