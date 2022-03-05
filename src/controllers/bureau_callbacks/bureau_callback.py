# SPHINX
from src.services.sinacor.service import SinacorService


class BureauCallbackController:
    @staticmethod
    async def process_callback(payload: dict):
        return await SinacorService.process_callback(payload=payload)
