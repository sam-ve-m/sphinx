from src.services.authentications.service import AuthenticationService


class AuthenticationController:
    @staticmethod
    def answer(payload: dict):
        return AuthenticationService.answer(payload=payload)
