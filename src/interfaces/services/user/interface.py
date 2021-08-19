# STANDARD LIBS
from abc import ABC, abstractmethod
from persephone_client.main import Persephone

# SPHINX
from src.services.authentications.service import AuthenticationService
from src.services.persephone.service import PersephoneService

from src.repositories.user.repository import UserRepository
from src.repositories.file.repository import FileRepository

from src.utils.jwt_utils import JWTHandler
from src.utils.stone_age import StoneAge


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
    def change_view(
        payload: dict, user_repository: UserRepository, token_handler: JWTHandler
    ) -> dict:
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
    def save_user_selfie(payload: dict, file_repository: FileRepository) -> dict:
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

    @staticmethod
    @abstractmethod
    def add_user_control_metadata(payload: dict):
        pass

    @staticmethod
    @abstractmethod
    def fill_term_signed(payload: dict, file_type: str, version: int):
        pass

    @staticmethod
    @abstractmethod
    def get_signed_term(
            payload: dict,
            file_repository,
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def user_identifier_data(
        payload: dict,
        user_repository,
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def user_complementary_data(
        payload: dict,
        user_repository,
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def send_quiz_responses(
        payload: dict,
        user_repository,
        stone_age,
        persephone_client,
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def user_quiz(
        payload: dict, stone_age, user_repository
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def get_onboarding_user_current_step(
        payload: dict,
        user_repository,
        file_repository
    ) -> dict:
        pass
