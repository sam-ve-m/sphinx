from src.services.features.service import FeatureService


class FeatureController:
    @staticmethod
    async def create(payload: dict):
        return await FeatureService.create(payload=payload)

    @staticmethod
    async def update(payload: dict):
        return await FeatureService.update(payload=payload)

    @staticmethod
    async def delete(payload: dict):
        return await FeatureService.delete(payload=payload)
