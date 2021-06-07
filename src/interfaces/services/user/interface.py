from abc import ABC, abstractmethod


class IUser(ABC):
    @abstractmethod
    def create(payload: dict) -> dict:
        pass

    @abstractmethod
    def create_admin(payload: dict) -> dict:
        pass

    @abstractmethod
    def update(payload: dict) -> dict:
        pass

    @abstractmethod
    def delete(payload: dict) -> dict:
        pass

    @abstractmethod
    def create_admin(payload: dict) -> dict:
        pass

    @abstractmethod
    def change_password(payload: dict) -> dict:
        pass

    @abstractmethod
    def forgot_password(payload: dict) -> dict:
        pass

    @abstractmethod
    def change_view(payload: dict) -> dict:
        pass

    @abstractmethod
    def logout_all(payload: dict) -> dict:
        pass

    @abstractmethod
    def add_feature(payload: dict) -> dict:
        pass

    @abstractmethod
    def delete_feature(payload: dict) -> dict:
        pass

    @abstractmethod
    def save_user_self(payload: dict) -> dict:
        pass

    @abstractmethod
    def assign_term(payload: dict) -> dict:
        pass
