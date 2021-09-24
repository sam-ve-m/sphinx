from abc import ABC, abstractmethod


# SPHINX
from typing import Type

from src.services.persephone.service import PersephoneService
from src.utils.jwt_utils import JWTHandler
from src.repositories.user.repository import UserRepository
from src.services.email_sender.grid_email_sender import EmailSender as SendGridEmail
from src.services.builders.thebes_hall.thebes_hall import ThebesHall


class IAuthentication(ABC):
    @staticmethod
    @abstractmethod
    def thebes_gate(
        thebes_answer_from_request_or_error: dict,
        user_repository: UserRepository,
        token_handler: JWTHandler,
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def login(
        user_credentials: dict,
        user_repository: UserRepository,
        token_handler: JWTHandler,
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def send_authentication_email(
        email: str, payload_jwt: str, body: str, email_sender=SendGridEmail
    ) -> None:
        pass

    @staticmethod
    @abstractmethod
    def thebes_hall(
        device_and_thebes_answer_from_request: dict,
        user_repository: UserRepository,
        token_handler: JWTHandler,
    ) -> dict:
        pass
