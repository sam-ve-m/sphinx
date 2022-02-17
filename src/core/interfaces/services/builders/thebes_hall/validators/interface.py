# STANDARD LIBS
from abc import ABC, abstractmethod


class IValidator(ABC):
    @staticmethod
    @abstractmethod
    def run(payload: dict) -> dict:
        pass
