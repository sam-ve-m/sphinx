from src.services.suitability.service import SuitabilityService


class SuitabilityController:
    @staticmethod
    def persist(payload: dict):
        return SuitabilityService.persist(payload=payload)
