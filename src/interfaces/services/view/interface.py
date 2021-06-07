from abc import ABC, abstractmethod


class IView(ABC):

    @abstractmethod
    def create(payload: dict) -> dict:
        pass

    @abstractmethod
    def update(payload: dict) -> dict:
        pass

    @abstractmethod
    def delete(payload: dict) -> dict:
        pass

    @abstractmethod
    def link_feature(payload: dict) -> dict:
        pass

    @abstractmethod
    def get_view(payload: dict) -> dict:
       pass
