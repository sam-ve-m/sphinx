from abc import ABC, abstractmethod


class IPasswordEncrypt(ABC):
    @staticmethod
    @abstractmethod
    def encrypt_password(user_password: str):
        pass
