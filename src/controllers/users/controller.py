# SPHINX
from src.services.users.service import UserService


class UserController:
    @staticmethod
    def create(user: dict):
        return UserService.create(user=user)

    @staticmethod
    def create_admin(payload: dict):
        return UserService.create_admin(payload=payload)

    @staticmethod
    def update(payload: dict):
        return UserService.update(payload=payload)

    @staticmethod
    def delete(payload: dict):
        return UserService.delete(payload=payload)

    @staticmethod
    def change_password(payload: dict):
        return UserService.change_password(payload=payload)

    @staticmethod
    def forgot_password(payload: dict):
        return UserService.forgot_password(payload=payload)

    @staticmethod
    def change_view(payload: dict):
        return UserService.change_view(payload=payload)

    @staticmethod
    def logout_all(payload: dict):
        return UserService.logout_all(payload=payload)

    @staticmethod
    def add_feature(payload: dict):
        return UserService.add_feature(payload=payload)

    @staticmethod
    def delete_feature(payload: dict):
        return UserService.delete_feature(payload=payload)

    @staticmethod
    def save_user_selfie(payload: dict):
        return UserService.save_user_selfie(payload=payload)

    @staticmethod
    def sign_term(payload: dict):
        return UserService.sign_term(payload=payload)

    @staticmethod
    def get_signed_term(payload: dict):
        return UserService.get_signed_term(payload=payload)

    @staticmethod
    def user_identifier_data(payload: dict):
        return UserService.user_identifier_data(payload=payload)

    @staticmethod
    def user_complementary_data(payload: dict):
        return UserService.user_complementary_data(payload=payload)

    @staticmethod
    def user_quiz(payload: dict):
        return UserService.user_quiz(payload=payload)

    @staticmethod
    def user_quiz_put(payload: dict):
        return UserService.user_quiz_put(payload=payload)

    @staticmethod
    def send_quiz_responses(payload: dict):
        return UserService.send_quiz_responses(payload=payload)

    @staticmethod
    def get_onboarding_user_current_step(payload: dict):
        return UserService.get_onboarding_user_current_step(payload=payload)

    @staticmethod
    def set_user_electronic_signature(payload: dict):
        return UserService.set_user_electronic_signature(payload=payload)

    @staticmethod
    def forgot_electronic_signature(payload: dict):
        return UserService.forgot_electronic_signature(payload=payload)

    @staticmethod
    def reset_electronic_signature(payload: dict):
        return UserService.reset_electronic_signature(payload=payload)

    @staticmethod
    def change_electronic_signature(payload: dict):
        return UserService.change_electronic_signature(payload=payload)

    @staticmethod
    def get_customer_registration_data(payload: dict):
        return UserService.get_customer_registration_data(payload=payload)

    @staticmethod
    def update_customer_registration_data(payload: dict):
        return UserService.update_customer_registration_data(payload=payload)
