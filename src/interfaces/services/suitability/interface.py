# STANDARD LIBS
from abc import ABC, abstractmethod

# SPHINX
from src.repositories.suitability.repository import SuitabilityRepository


class ISuitability(ABC):
    @staticmethod
    @abstractmethod
    def persist(payload: dict, suitability_repository: SuitabilityRepository) -> dict:
        pass
