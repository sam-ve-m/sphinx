from src.services.users.service import UserService


class UserController:
    @staticmethod
    def create(payload: dict):
        return UserService.create(payload=payload)

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
    def save_user_self(payload: dict):
        return UserService.save_user_self(payload=payload)

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
    def user_quiz_responses(payload: dict):
        return UserService.quiz_responses(payload=payload)

    @staticmethod
    def change_user_to_client(payload: dict):
        return UserService.change_user_to_client(payload=payload)

    @staticmethod
    def table_callback(payload: dict):
        return UserService.table_callback(payload=payload)
