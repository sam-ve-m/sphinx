from abc import ABC, abstractmethod


class ISuitability(ABC):

    @abstractmethod
    def persist(payload: dict) -> dict:
        pass
