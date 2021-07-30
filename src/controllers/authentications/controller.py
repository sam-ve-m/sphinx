from src.services.authentications.service import AuthenticationService


class AuthenticationController:
    @staticmethod
    def thebes_gate(payload: dict):
        return AuthenticationService.thebes_gate(payload=payload)

    @staticmethod
    def login(payload: dict):
        return AuthenticationService.login(payload=payload)

    @staticmethod
    def thebes_hall(payload: dict):
        return AuthenticationService.thebes_hall(payload=payload)
