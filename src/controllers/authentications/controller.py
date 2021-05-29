from src.services.authentications.service import AuthenticationService


class AuthenticationController:
    @staticmethod
    async def answer(payload: dict):
        return await AuthenticationService.answer(payload=payload)

    @staticmethod
    async def login(payload: dict):
        return await AuthenticationService.login(payload=payload)

    @staticmethod
    async def forgot_password(payload: dict):
        return await AuthenticationService.forgot_password(payload=payload)
