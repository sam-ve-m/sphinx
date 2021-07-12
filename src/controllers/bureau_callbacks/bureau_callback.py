# SPHINX
from src.services.sinacor.service import SinacorService


class BureauCallbackController:
    @staticmethod
    def process_callback(payload: dict):
        return SinacorService.process_callback(payload=payload)
