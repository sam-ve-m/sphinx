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
    async def delete(payload: dict):
        return await UserService.delete(payload=payload)

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
    async def save_user_document(payload: dict):
        return await UserService.save_user_document(payload=payload)

    @staticmethod
    async def sign_terms(payload: dict):
        return await UserService.sign_terms(payload=payload)

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
    async def onboarding_user_current_step_br(payload: dict):
        return await UserService.onboarding_user_current_step_br(payload=payload)

    @staticmethod
    async def onboarding_user_current_step_us(payload: dict):
        return await UserService.onboarding_user_current_step_us(payload=payload)

    @staticmethod
    async def update_politically_exposed_us(payload: dict):
        return await UserService.update_politically_exposed_us(payload=payload)

    @staticmethod
    async def update_exchange_member_us(payload: dict):
        return await UserService.update_exchange_member_us(payload=payload)

    @staticmethod
    async def update_time_experience_us(payload: dict):
        return await UserService.update_time_experience_us(payload=payload)

    @staticmethod
    async def update_company_director_us(payload: dict):
        return await UserService.update_company_director_us(payload=payload)

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
    async def get_external_fiscal_tax_residence(payload: dict):
        return await UserService.get_external_fiscal_tax_residence(payload=payload)

    @staticmethod
    async def update_external_fiscal_tax_residence(payload: dict):
        return await UserService.update_external_fiscal_tax_residence(payload=payload)

    @staticmethod
    async def get_w8_form(payload: dict):
        return await UserService.get_w8_form(payload=payload)

    @staticmethod
    async def update_w8_form_confirmation(payload: dict):
        return await UserService.update_w8_form_confirmation(payload=payload)

    @staticmethod
    async def update_employ_for_us(payload: dict):
        return await UserService.update_employ_for_us(payload=payload)

    @staticmethod
    async def update_customer_registration_data(payload: dict):
        return await UserService.update_customer_registration_data(payload=payload)
