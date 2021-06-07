from src.services.suitability.service import SuitabilityService


class SuitabilityController:
    @staticmethod
    def create_quiz(payload: dict):
        return SuitabilityService.create_quiz(payload=payload)

    @staticmethod
    def create_profile(payload: dict):
        return SuitabilityService.create_profile(payload=payload)
