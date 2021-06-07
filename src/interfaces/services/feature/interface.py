# STANDARD LIBS
from abc import ABC, abstractmethod


# SPHINX
from src.repositories.feature.repository import FeatureRepository


class IFeature(ABC):
    @staticmethod
    @abstractmethod
    def create(payload: dict, feature_repository: FeatureRepository) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def update(payload: dict, feature_repository: FeatureRepository) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def delete(payload: dict, feature_repository: FeatureRepository) -> dict:
        pass
