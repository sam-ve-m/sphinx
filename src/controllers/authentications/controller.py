from src.services.authentications.service import AuthenticationService


class AuthenticationController:
    @staticmethod
    def answer(payload: dict):
        return AuthenticationService.answer(payload=payload)

    @staticmethod
    def login(payload: dict):
        return AuthenticationService.login(payload=payload)
