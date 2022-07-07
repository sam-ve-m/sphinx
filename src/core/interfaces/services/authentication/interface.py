from abc import ABC, abstractmethod


# SPHINX
from src.domain.email.templates.enum import EmailTemplate
from src.services.jwts.service import JwtService
from src.repositories.user.repository import UserRepository
from src.services.email_sender.grid_email_sender import EmailSender as SendGridEmail


class IAuthentication(ABC):
    @staticmethod
    @abstractmethod
    async def thebes_gate(
        thebes_answer_from_request_or_error: dict,
        user_repository: UserRepository,
        token_service: JwtService,
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def login(
        user_credentials: dict,
        user_repository: UserRepository,
        token_service: JwtService,
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def send_authentication_email(
        email_template: EmailTemplate, email: str, payload_jwt: str, body: str, email_sender=SendGridEmail
    ) -> None:
        pass

    @staticmethod
    @abstractmethod
    def thebes_hall(
        device_and_thebes_answer_from_request: dict,
        user_repository: UserRepository,
        token_service: JwtService,
    ) -> dict:
        pass
