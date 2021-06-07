from src.services.authentications.service import AuthenticationService


class AuthenticationController:
    @staticmethod
    def answer(payload: dict):
        return AuthenticationService.answer(payload=payload)

    @staticmethod
    def login(payload: dict):
        return AuthenticationService.login(payload=payload)

    @staticmethod
    def forgot_password(payload: dict):
        return AuthenticationService.forgot_password(payload=payload)

    @staticmethod
    def hall(payload: dict):
        return AuthenticationService.hall(payload=payload)
