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
    def create_admin(payload: dict):
        return UserService.create_admin(payload=payload)

    @staticmethod
    def create_admin(payload: dict):
        return UserService.create_admin(payload=payload)

    @staticmethod
    def change_password(payload: dict):
        return UserService.change_password(payload=payload)

    @staticmethod
    def forgot_password(payload: dict):
        return UserService.forgot_password(payload=payload)

    @staticmethod
    def change_view(payload: dict):
        return UserService.change_view(payload=payload)
