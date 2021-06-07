from abc import ABC, abstractmethod

class ITerm:
    
    @abstractmethod
    def save_term(payload: dict) -> dict:
        pass
    @abstractmethod
    def get_term(payload: dict) -> dict:
        pass
