# SPHINX
from src.services.users.service import UserService


class UserController:
    @staticmethod
    async def create(user: dict):
        return await UserService.create(user=user)

    @staticmethod
    async def create_admin(payload: dict):
        return await UserService.create_admin(payload=payload)

    @staticmethod
    async def update(payload: dict):
        return await UserService.update(payload=payload)

    @staticmethod
    async def delete(payload: dict):
        return await UserService.delete(payload=payload)

    @staticmethod
    async def change_password(payload: dict):
        return await UserService.change_password(payload=payload)

    @staticmethod
    async def forgot_password(payload: dict):
        return await UserService.forgot_password(payload=payload)

    @staticmethod
    async def change_view(payload: dict):
        return await UserService.change_view(payload=payload)

    @staticmethod
    async def logout_all(payload: dict):
        return await UserService.logout_all(payload=payload)

    @staticmethod
    async def add_feature(payload: dict):
        return await UserService.add_feature(payload=payload)

    @staticmethod
    async def delete_feature(payload: dict):
        return await UserService.delete_feature(payload=payload)

    @staticmethod
    async def save_user_selfie(payload: dict):
        return await UserService.save_user_selfie(payload=payload)

    @staticmethod
    async def sign_term(payload: dict):
        return await UserService.sign_term(payload=payload)

    @staticmethod
    async def get_signed_term(payload: dict):
        return await UserService.get_signed_term(payload=payload)

    @staticmethod
    async def user_identifier_data(payload: dict):
        return await UserService.user_identifier_data(payload=payload)

    @staticmethod
    async def user_complementary_data(payload: dict):
        return await UserService.user_complementary_data(payload=payload)

    @staticmethod
    async def user_quiz(payload: dict):
        return await UserService.user_quiz(payload=payload)

    @staticmethod
    async def send_quiz_responses(payload: dict):
        return await UserService.send_quiz_responses(payload=payload)

    @staticmethod
    async def get_onboarding_user_current_step(payload: dict):
        return await UserService.get_onboarding_user_current_step(payload=payload)

    @staticmethod
    async def set_user_electronic_signature(payload: dict):
        return await UserService.set_user_electronic_signature(payload=payload)

    @staticmethod
    async def forgot_electronic_signature(payload: dict):
        return await UserService.forgot_electronic_signature(payload=payload)

    @staticmethod
    async def reset_electronic_signature(payload: dict):
        return await UserService.reset_electronic_signature(payload=payload)

    @staticmethod
    async def change_electronic_signature(payload: dict):
        return await UserService.change_electronic_signature(payload=payload)

    @staticmethod
    async def get_customer_registration_data(payload: dict):
        return await UserService.get_customer_registration_data(payload=payload)

    @staticmethod
    async def update_customer_registration_data(payload: dict):
        return await UserService.update_customer_registration_data(payload=payload)
