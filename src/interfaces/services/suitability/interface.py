# STANDARD LIBS
from abc import ABC, abstractmethod

# SPHINX
from src.repositories.base_repository import BaseRepository
from src.repositories.suitability.repository import SuitabilityRepository


class ISuitability(ABC):
    @staticmethod
    @abstractmethod
    def create_quiz(
        payload: dict, suitability_repository: SuitabilityRepository
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def create_profile(
        payload: dict,
        user_repository: BaseRepository,
        suitability_repository: BaseRepository,
        suitability_user_profile_repository: BaseRepository,
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def get_user_profile(
        payload: dict, suitability_user_profile_repository: BaseRepository
    ) -> dict:
        pass
