from abc import ABC, abstractmethod

class IFeature(ABC):
    @abstractmethod
    def create(payload: dict) -> dict:
        pass

    @abstractmethod
    def update(payload: dict) -> dict:
        pass

    @abstractmethod
    def delete(payload: dict) -> dict:
        pass
