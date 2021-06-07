from abc import ABC, abstractmethod


# SPHINX
from src.utils.jwt_utils import JWTHandler
from src.repositories.user.repository import UserRepository
from src.services.email_sender.grid_email_sender import EmailSender as SendGridEmail


class IAuthentication(ABC):
    @staticmethod
    @abstractmethod
    def answer(payload: dict, user_repository: UserRepository, token_handler: JWTHandler) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def login(payload: dict, user_repository: UserRepository, token_handler: JWTHandler) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def forgot_password(payload: dict, user_repository: UserRepository) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def forgot_password(email: str, payload: dict, body: str, ttl: int, email_sender: SendGridEmail) -> None:
        pass