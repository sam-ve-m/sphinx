from src.services.authentications.service import AuthenticationService


class AuthenticationController:
    @staticmethod
    def thebes_gate(thebes_answer_from_request_or_error: dict):
        return AuthenticationService.thebes_gate(
            thebes_answer_from_request_or_error=thebes_answer_from_request_or_error
        )

    @staticmethod
    def login(user_credentials: dict):
        return AuthenticationService.login(user_credentials=user_credentials)

    @staticmethod
    def thebes_hall(device_and_thebes_answer_from_request: dict):
        return AuthenticationService.thebes_hall(
            device_and_thebes_answer_from_request=device_and_thebes_answer_from_request
        )

    @staticmethod
    def validate_electronic_signature(change_electronic_signature_request: dict):
        return AuthenticationService.create_electronic_signature_jwt(
            change_electronic_signature_request=change_electronic_signature_request
        )

    @staticmethod
    def logout(device_jwt_and_thebes_answer_from_request: dict):
        return AuthenticationService.logout(
            device_jwt_and_thebes_answer_from_request=device_jwt_and_thebes_answer_from_request
        )
