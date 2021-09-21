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

    @staticmethod
    def get_thebes_hall(payload: dict):
        return AuthenticationService.get_thebes_hall(payload=payload)

    @staticmethod
    def validate_electronic_signature(payload: dict):
        return AuthenticationService.create_electronic_signature_jwt(payload=payload)

    @staticmethod
    def logout(payload: dict):
        return AuthenticationService.logout(payload=payload)
