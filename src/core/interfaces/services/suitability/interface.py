# STANDARD LIBS
from abc import ABC, abstractmethod

# SPHINX
from typing import Type

from src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure
from src.repositories.suitability.repository import SuitabilityRepository
from src.services.persephone.service import PersephoneService
from src.utils.jwt_utils import JWTHandler


class ISuitability(ABC):
    @staticmethod
    @abstractmethod
    def create_quiz(
        payload: dict,
        suitability_repository: SuitabilityRepository,
        suitability_answers_repository: Type[MongoDBInfrastructure] = None,
        suitability_answers_profile_builder=None,
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def create_profile(
        payload: dict,
        user_repository: MongoDBInfrastructure,
        suitability_repository: MongoDBInfrastructure,
        suitability_user_profile_repository: MongoDBInfrastructure,
        persephone_client: Type[PersephoneService] = None,
        token_handler: Type[JWTHandler] = None,
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def get_user_profile(
        payload: dict, suitability_user_profile_repository: MongoDBInfrastructure
    ) -> dict:
        pass
