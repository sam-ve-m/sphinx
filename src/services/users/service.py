from src.repositories.user.repository import UserRepository
from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.utils.genarate_id import generate_id, hash_field
from src.utils.jwt_utils import JWTHandler
from src.services.email_sender.grid_email_sender import EmailSender as SendGridEmail
from src.i18n.i18n_resolver import i18nResolver as i18n
from fastapi import status
from decouple import config
from src.utils.email import HtmlModifier


class UserService:
    @staticmethod
    def create(
        payload: dict, user_repository=UserRepository(), email_sender=SendGridEmail
    ):
        payload = generate_id("email", payload, must_remove=False)
        email = payload.get("email")
        name = payload.get("name")
        pin = payload.get("pin")
        if (
            (len(email) < 1 or email is None)
            or (len(name) < 1 or name is None)
            or (pin is None)
        ):
            raise BadRequestError("common.invalid_params")
        payload = hash_field("pin", payload)
        if user_repository.find_one({"_id": payload.get("_id")}) is not None:
            raise BadRequestError("common.register_exists")

        payload.update(
            {"scope": {"view_type": None, "features": []}, "is_active": False}
        )

        if user_repository.insert(payload):
            del payload["pin"]
            del payload["_id"]
            payload_jwt = JWTHandler.generate_token(payload=payload, ttl=10)
            page = HtmlModifier(
                "src/services/asset",
                i18n.get_translate(key="email.body.created", locale="pt"),
                config("TARGET_LINK") + "/" + payload_jwt,
            )()
            email_sender.send_email_to(
                target_email=email,
                message=page,
                subject=i18n.get_translate(key="email.subject.created", locale="pt"),
            )
            return {
                "status_code": status.HTTP_201_CREATED,
                "message_key": "user.created",
            }
        else:
            raise InternalServerError("common.process_issue")

    @staticmethod
    def update(payload: dict, feature_repository=UserRepository()):
        pass

    @staticmethod
    def delete(payload: dict, feature_repository=UserRepository()):
        pass

    @staticmethod
    def forgot_password(payload: dict, feature_repository=UserRepository()):
        pass
