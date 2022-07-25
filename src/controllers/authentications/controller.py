from src.services.authentications.service import AuthenticationService


class AuthenticationController:
    @staticmethod
    async def thebes_nock(data: dict):
        return await AuthenticationService.thebes_nock(data)

    @staticmethod
    async def thebes_gate(thebes_answer: dict):
        return await AuthenticationService.thebes_gate(thebes_answer=thebes_answer)

    @staticmethod
    async def login(user_credentials: dict):
        return await AuthenticationService.login(user_credentials=user_credentials)

    @staticmethod
    async def validate_cpf(cpf: str):
        return await AuthenticationService.validate_cpf(cpf=cpf)

    @staticmethod
    async def thebes_hall(device_and_thebes_answer_from_request: dict):
        return await AuthenticationService.thebes_hall(
            device_and_thebes_answer_from_request=device_and_thebes_answer_from_request
        )

    @staticmethod
    async def validate_electronic_signature(change_electronic_signature_request: dict):
        return await AuthenticationService.create_electronic_signature_jwt(
            change_electronic_signature_request=change_electronic_signature_request
        )

    @staticmethod
    async def logout(device_jwt_and_thebes_answer_from_request: dict):
        return await AuthenticationService.logout(
            device_jwt_and_thebes_answer_from_request=device_jwt_and_thebes_answer_from_request
        )
