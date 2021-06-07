from fastapi import status
from datetime import datetime

from src.exceptions.exceptions import InternalServerError
from src.repositories.suitability.repository import SuitabilityRepository
from src.interfaces.services.suitability.interface import ISuitability


class SuitabilityService(ISuitability):

    @staticmethod
    def persist(payload: dict, suitability_repository=SuitabilityRepository()) -> dict:
        payload.update({"date": str(datetime.utcnow())})

        if suitability_repository.insert(payload):
            return {
                "status_code": status.HTTP_201_CREATED,
                "message_key": "suitabilities.persisted",
            }
        else:
            raise InternalServerError("common.process_issue")
