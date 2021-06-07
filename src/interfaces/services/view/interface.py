# STANDARD LIBS
from abc import ABC, abstractmethod

# SPHINX
from src.repositories.view.repository import ViewRepository


class IView(ABC):

    @staticmethod
    @abstractmethod
    def create(payload: dict, view_repository:ViewRepository) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def update(payload: dict, view_repository:ViewRepository) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def delete(payload: dict, view_repository:ViewRepository) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def link_feature(payload: dict, view_repository:ViewRepository) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def get_view(payload: dict, view_repository:ViewRepository) -> dict:
       pass
