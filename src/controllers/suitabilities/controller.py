from src.services.suitability.service import SuitabilityService


class SuitabilityController:
    @staticmethod
    async def create_quiz(payload: dict):
        return await SuitabilityService.create_quiz(payload=payload)

    @staticmethod
    async def create_profile(payload: dict):
        return await SuitabilityService.create_profile(payload=payload)

    @staticmethod
    async def get_user_profile(payload: dict):
        return await SuitabilityService.get_user_profile(payload=payload)
