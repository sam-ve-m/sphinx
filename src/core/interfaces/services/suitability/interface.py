# STANDARD LIBS
from abc import ABC, abstractmethod

# SPHINX
from typing import Type


from src.repositories.base_repository.mongo_db.base import MongoDbBaseRepository
from src.repositories.suitability.repository import SuitabilityRepository
from src.services.persephone.service import PersephoneService
from src.services.jwts.service import JwtService


class ISuitability(ABC):
    @staticmethod
    @abstractmethod
    def create_quiz(
        payload: dict,
        suitability_repository: SuitabilityRepository,
        suitability_answers_repository: Type[MongoDbBaseRepository] = None,
        suitability_answers_profile_builder=None,
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def create_profile(
        payload: dict,
        user_repository: MongoDbBaseRepository,
        suitability_repository: MongoDbBaseRepository,
        suitability_user_profile_repository: MongoDbBaseRepository,
        persephone_client: Type[PersephoneService] = None,
        token_service: Type[JwtService] = None,
    ) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def get_user_profile(
        payload: dict, suitability_user_profile_repository: MongoDbBaseRepository
    ) -> dict:
        pass
