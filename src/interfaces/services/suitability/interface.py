# STANDARD LIBS
from abc import ABC, abstractmethod

# SPHINX
from src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure
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
        user_repository: MongoDBInfrastructure,
        suitability_repository: MongoDBInfrastructure,
        suitability_user_profile_repository: MongoDBInfrastructure,
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def get_user_profile(
        payload: dict, suitability_user_profile_repository: MongoDBInfrastructure
    ) -> dict:
        pass
