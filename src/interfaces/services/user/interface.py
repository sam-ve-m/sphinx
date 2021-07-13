# STANDARD LIBS
from abc import ABC, abstractmethod

# SPHINX
from src.services.authentications.service import AuthenticationService
from src.repositories.user.repository import UserRepository
from src.repositories.file.repository import FileRepository
from src.utils.jwt_utils import JWTHandler
from src.utils.stone_age import StoneAge

from persephone_client.main import Persephone


class IUser(ABC):
    @staticmethod
    @abstractmethod
    def create(
        payload: dict,
        user_repository: UserRepository,
        authentication_service: AuthenticationService,
        persephone_client: Persephone,
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def create_admin(payload: dict) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def update(payload: dict, user_repository: UserRepository) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def delete(payload: dict, user_repository: UserRepository) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def change_password(payload: dict, user_repository: UserRepository) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def forgot_password(
        payload: dict,
        user_repository: UserRepository,
        authentication_service: AuthenticationService,
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def change_view(
        payload: dict, user_repository: UserRepository, token_handler: JWTHandler
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def change_user_to_client(
        payload: dict,
        user_repository: UserRepository,
        stone_age: StoneAge,
        persephone_client: Persephone,
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def logout_all(payload: dict, user_repository: UserRepository) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def add_feature(
        payload: dict, user_repository: UserRepository, token_handler: JWTHandler
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def delete_feature(
        payload: dict, user_repository: UserRepository, token_handler: JWTHandler
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def save_user_self(payload: dict, file_repository: FileRepository) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def sign_term(
        payload: dict,
        user_repository: UserRepository,
        token_handler: JWTHandler,
        file_repository: FileRepository,
    ) -> dict:
        pass
