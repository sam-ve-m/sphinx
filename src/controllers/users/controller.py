from src.services.users.service import UserService


class UserController:
    @staticmethod
    async def create(payload: dict):
        return await  UserService.create(payload=payload)

    @staticmethod
    async def create_admin(payload: dict):
        return await  UserService.create_admin(payload=payload)

    @staticmethod
    async def update(payload: dict):
        return await  UserService.update(payload=payload)

    @staticmethod
    async def delete(payload: dict):
        return await  UserService.delete(payload=payload)

    @staticmethod
    async def create_admin(payload: dict):
        return await  UserService.create_admin(payload=payload)

    @staticmethod
    async def create_admin(payload: dict):
        return await  UserService.create_admin(payload=payload)

    @staticmethod
    async def change_password(payload: dict):
        return await  UserService.change_password(payload=payload)

    @staticmethod
    async def forgot_password(payload: dict):
        return await  UserService.forgot_password(payload=payload)

    @staticmethod
    async def change_view(payload: dict):
        return await  UserService.change_view(payload=payload)
