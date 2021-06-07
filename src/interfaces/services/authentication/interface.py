from abc import ABC, abstractmethod


class IAuthentication(ABC):
    @abstractmethod
    def answer(payload: dict) -> dict:
        pass

    @abstractmethod
    def login(payload: dict) -> dict:
        pass

    @abstractmethod
    def forgot_password(payload: dict) -> dict:
        pass
