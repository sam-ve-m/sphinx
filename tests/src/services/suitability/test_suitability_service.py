import pytest
from unittest.mock import MagicMock
from fastapi import status

from src.exceptions.exceptions import InternalServerError
from src.services.suitability.service import SuitabilityService
from tests.stubby_classes.stubby_base_repository import StubbyBaseRepository


class StubbyRepository(StubbyBaseRepository):
    pass


basic_payload = {
    "version": 1,
    "questions": [
        {
            "value_text": "primeira pergunta",
            "score": 20,
            "order": 1,
            "answers": [
                {
                    "value_text": "primeira resposta",
                    "weight": 20
                },
                {
                    "value_text": "segunda resposta",
                    "weight": 25
                },
                {
                    "value_text": "terceira resposta",
                    "weight": 22
                }
            ]
        }
    ]
}


def test_insert_error_in_suitability_db():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.insert = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        SuitabilityService.persist(payload=basic_payload, suitability_repository=stubby_repository)


def test_insert_in_suitability_db():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.insert = MagicMock(return_value=True)
    response = SuitabilityService.persist(payload=basic_payload, suitability_repository=stubby_repository)
    assert response.get('status_code') == status.HTTP_201_CREATED
    assert response.get('message_key') == "suitability.persisted"
