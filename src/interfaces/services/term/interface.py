# STANDARD LIBS
from abc import ABC, abstractmethod

# SPHINX
from src.repositories.file.repository import FileRepository


class ITerm(ABC):
    @staticmethod
    @abstractmethod
    def save_term(payload: dict, file_repository: FileRepository) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def get_term(payload: dict, file_repository: FileRepository) -> dict:
        pass
