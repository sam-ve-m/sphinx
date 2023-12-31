from src.services.features.service import FeatureService


class FeatureController:
    @staticmethod
    def create(payload: dict):
        return FeatureService.create(payload=payload)

    @staticmethod
    def update(payload: dict):
        return FeatureService.update(payload=payload)

    @staticmethod
    def delete(payload: dict):
        return FeatureService.delete(payload=payload)

    @staticmethod
    def get(payload: dict):
        return FeatureService.get()
