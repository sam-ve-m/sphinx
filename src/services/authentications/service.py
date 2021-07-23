# STANDARD LIBS
from copy import deepcopy

# OUTSIDE LIBRARIES
from fastapi import status
from src.utils.env_config import config

# SPHINX
from src.utils.email import HtmlModifier
from src.repositories.user.repository import UserRepository
from src.services.builders.thebes_hall.thebes_hall import ThebesHall
from src.controllers.jwts.controller import JwtController
from src.utils.jwt_utils import JWTHandler
from src.exceptions.exceptions import (
    BadRequestError,
    UnauthorizedError,
    InternalServerError,
)
from src.i18n.i18n_resolver import i18nResolver as i18n
from src.services.email_sender.grid_email_sender import EmailSender as SendGridEmail
from src.utils.genarate_id import hash_field
from src.interfaces.services.authentication.interface import IAuthentication


class AuthenticationService(IAuthentication):
    @staticmethod
    def thebes_gate(
        payload: dict, user_repository=UserRepository(), token_handler=JWTHandler
    ) -> dict:
        old = user_repository.find_one({"_id": payload.get("email")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        new = deepcopy(old)
        is_active = old.get("is_active")
        has_pin = old.get("pin")
        response = {"status_code": None, "payload": {"jwt": None}}
        response.update({"status_code": status.HTTP_200_OK})

        if not is_active:
            if not has_pin:
                new.update(
                    {
                        "is_active": True,
                        "use_magic_link": True,
                        "scope": {"view_type": "default", "features": ["default"]},
                    }
                )
            else:
                new.update(
                    {
                        "is_active": True,
                        "use_magic_link": False,
                        "scope": {"view_type": "default", "features": ["default"]},
                    }
                )
            if user_repository.update_one(old=old, new=new) is False:
                raise InternalServerError("common.process_issue")

        jwt = token_handler.generate_token(payload=new, ttl=525600)

        response.update({"payload": {"jwt": jwt}})

        return response

    @staticmethod
    def login(
        payload: dict, user_repository=UserRepository(), token_handler=JWTHandler
    ) -> dict:
        entity = user_repository.find_one({"_id": payload.get("email")})
        if entity is None:
            raise BadRequestError("common.register_not_exists")
        if entity.get("deleted"):
            raise UnauthorizedError("invalid_credential")
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
            if hash_field(payload=pin) != entity.get("pin"):
                raise UnauthorizedError("user.pin_error")

            jwt = token_handler.generate_token(payload=entity, ttl=525600)
            JwtController.insert_one(jwt, entity.get("email"))
            return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}

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
    def thebes_hall(
        payload: dict,
        user_repository=UserRepository(),
        token_handler=JWTHandler,
        thebes_hall=ThebesHall,
    ) -> dict:
        user = user_repository.find_one({"_id": payload.get("email")})
        if user is None:
            raise BadRequestError("common.register_not_exists")
        jwt = token_handler.generate_token(payload=user, ttl=525600)
        return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}
