from abc import ABC, abstractmethod
from fastapi import Response, Request
from typing import Optional


class IController(ABC):
    @staticmethod
    @abstractmethod
    def run(callback: callable, payload: Optional[dict], request: Request) -> Response:
        pass

    @staticmethod
    @abstractmethod
    def create_response_payload(response_metadata: dict, lang: str) -> dict:
        pass
