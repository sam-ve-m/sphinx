import pytest
from unittest.mock import MagicMock
from fastapi import status

from src.exceptions.exceptions import InternalServerError
from src.services.suitability.service import SuitabilityService
from tests.stub_classes.stub_base_repository import StubBaseRepository


class StubRepository(StubBaseRepository):
    pass


basic_payload = {
    "suitability": {
        "questions": [
            {
                "value_text": "primeira pergunta",
                "score": 20,
                "order": 1,
                "answers": [
                    {"value_text": "primeira resposta", "weight": 20},
                    {"value_text": "segunda resposta", "weight": 25},
                    {"value_text": "terceira resposta", "weight": 22},
                ],
            }
        ],
    }
}


class MySuitabilityStubRepository(StubBaseRepository):
    def find_all(self):
        return self

    def sort(self, a, b):
        return self

    def limit(self, i: int):
        pass


def test_insert_error_in_suitability_db():
    stubby_repository = StubRepository(database="", collection="")
    stubby_repository.insert = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        SuitabilityService.create_quiz(
            payload=basic_payload,
            suitability_repository=stubby_repository,
            suitability_answers_repository=stubby_repository,
        )


def test_insert_in_suitability_db():
    stubby_repository = StubRepository(database="", collection="")
    stubby_repository.insert = MagicMock(return_value=True)
    response = SuitabilityService.create_quiz(
        payload=basic_payload,
        suitability_repository=stubby_repository,
        suitability_answers_repository=stubby_repository,
    )
    assert response.get("status_code") == status.HTTP_201_CREATED
    assert response.get("message_key") == "suitability.create_quiz"


def test_create_quiz_without_suitability_payload():
    stubby_repository = StubRepository(database="", collection="")
    stubby_repository.insert = MagicMock(return_value=True)
    with pytest.raises(InternalServerError, match="suitability.error.not_found"):
        SuitabilityService.create_quiz(
            payload={},
            suitability_repository=stubby_repository,
            suitability_answers_repository=stubby_repository,
        )

    with pytest.raises(InternalServerError, match="suitability.error.not_found"):
        SuitabilityService.create_quiz(
            payload=None,
            suitability_repository=stubby_repository,
            suitability_answers_repository=stubby_repository,
        )


def test_get_suitability_version_without_suitability_version():
    stubby_repository = MySuitabilityStubRepository(database="", collection="")
    stubby_repository.limit = MagicMock(return_value=[])
    version = SuitabilityService._SuitabilityService__get_suitability_version(
        stubby_repository
    )
    assert version == 1


def test_get_suitability_version_with_invalid_mongo_error_response_none():
    stubby_repository = MySuitabilityStubRepository(database="", collection="")
    stubby_repository.find_all = MagicMock(return_value=None)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        SuitabilityService._SuitabilityService__get_suitability_version(
            stubby_repository
        )

    stubby_repository2 = MySuitabilityStubRepository(database="", collection="")
    stubby_repository2.sort = MagicMock(return_value=None)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        SuitabilityService._SuitabilityService__get_suitability_version(
            stubby_repository
        )

    stubby_repository3 = MySuitabilityStubRepository(database="", collection="")
    stubby_repository3.limit = MagicMock(return_value=None)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        SuitabilityService._SuitabilityService__get_suitability_version(
            stubby_repository
        )


def test_get_suitability_version_with_invalid_suitability_format():
    stubby_repository = MySuitabilityStubRepository(database="", collection="")
    stubby_repository.limit = MagicMock(return_value=[1])
    with pytest.raises(InternalServerError, match="suitability.error.not_found"):
        SuitabilityService._SuitabilityService__get_suitability_version(
            stubby_repository
        )


def test_get_suitability_version_with_invalid_version():
    stubby_repository = MySuitabilityStubRepository(database="", collection="")
    stubby_repository.limit = MagicMock(return_value=[{"version": "str"}])
    with pytest.raises(InternalServerError, match="common.invalid_params"):
        SuitabilityService._SuitabilityService__get_suitability_version(
            stubby_repository
        )


def test_get_suitability_version_with_valid_version():
    stubby_repository = MySuitabilityStubRepository(database="", collection="")
    stubby_repository.limit = MagicMock(return_value=[{"version": 1}])
    response = SuitabilityService._SuitabilityService__get_suitability_version(
        stubby_repository
    )

    assert response == 2


def test_insert_new_suitability_with_suitability_invalid_format():
    stubby_repository = StubRepository(database="", collection="")
    stubby_repository.insert = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.invalid_params"):
        SuitabilityService._SuitabilityService__insert_new_suitability(
            suitability_repository=stubby_repository,
            suitability=None
        )

    with pytest.raises(InternalServerError, match="common.invalid_params"):
        SuitabilityService._SuitabilityService__insert_new_suitability(
            suitability_repository=stubby_repository,
            suitability=[]
        )

    with pytest.raises(InternalServerError, match="common.invalid_params"):
        SuitabilityService._SuitabilityService__insert_new_suitability(
            suitability_repository=stubby_repository,
            suitability=1
        )


def test_insert_new_suitability_with_mongo_error():
    stubby_repository = StubRepository(database="", collection="")
    stubby_repository.insert = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        SuitabilityService._SuitabilityService__insert_new_suitability(
            suitability_repository=None,
            suitability={}
        )


def test_insert_new_suitability_with_empty_suitability():
    stubby_repository = StubRepository(database="", collection="")
    stubby_repository.insert = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        SuitabilityService._SuitabilityService__insert_new_suitability(
            suitability_repository=stubby_repository,
            suitability={}
        )

    stubby_repository2 = StubRepository(database="", collection="")
    stubby_repository2.insert = MagicMock(return_value=None)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        SuitabilityService._SuitabilityService__insert_new_suitability(
            suitability_repository=stubby_repository2,
            suitability={}
        )


def test_insert_new_suitability():
    stubby_repository = StubRepository(database="", collection="")
    stubby_repository.insert = MagicMock(return_value=True)
    response = SuitabilityService._SuitabilityService__insert_new_suitability(
            suitability_repository=stubby_repository,
            suitability={}
        )

    assert response is None


def test_insert_new_answers_with_answers_invalid_format():
    stubby_repository = StubRepository(database="", collection="")
    stubby_repository.insert = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.invalid_params"):
        SuitabilityService._SuitabilityService__insert_new_answers_suitability(
            suitability_answers_repository=stubby_repository,
            answers=None
        )

    with pytest.raises(InternalServerError, match="common.invalid_params"):
        SuitabilityService._SuitabilityService__insert_new_answers_suitability(
            suitability_answers_repository=stubby_repository,
            answers=[]
        )

    with pytest.raises(InternalServerError, match="common.invalid_params"):
        SuitabilityService._SuitabilityService__insert_new_answers_suitability(
            suitability_answers_repository=stubby_repository,
            answers=1
        )


def test_insert_new_answers_with_mongo_error():
    stubby_repository = StubRepository(database="", collection="")
    stubby_repository.insert = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        SuitabilityService._SuitabilityService__insert_new_answers_suitability(
            suitability_answers_repository=None,
            answers={}
        )


def test_insert_new_answers_with_empty_answers():
    stubby_repository = StubRepository(database="", collection="")
    stubby_repository.insert = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        SuitabilityService._SuitabilityService__insert_new_answers_suitability(
            suitability_answers_repository=stubby_repository,
            answers={}
        )

    stubby_repository2 = StubRepository(database="", collection="")
    stubby_repository2.insert = MagicMock(return_value=None)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        SuitabilityService._SuitabilityService__insert_new_answers_suitability(
            suitability_answers_repository=stubby_repository2,
            answers={}
        )


def test_insert_new_answers():
    stubby_repository = StubRepository(database="", collection="")
    stubby_repository.insert = MagicMock(return_value=True)
    response = SuitabilityService._SuitabilityService__insert_new_answers_suitability(
            suitability_answers_repository=stubby_repository,
            answers={}
        )

    assert response is None


def test_get_last_suitability_answers_metadata_with_mongo_error():
    with pytest.raises(InternalServerError, match="common.process_issue"):
        SuitabilityService._SuitabilityService__get_last_suitability_answers_metadata(
            suitability_answers_repository=None,
        )

    stubby_repository = MySuitabilityStubRepository(database="", collection="")
    stubby_repository.find_all = MagicMock(return_value=False)

    with pytest.raises(InternalServerError, match="common.process_issue"):
        SuitabilityService._SuitabilityService__get_last_suitability_answers_metadata(
            suitability_answers_repository=stubby_repository,
        )

    stubby_repository = MySuitabilityStubRepository(database="", collection="")
    stubby_repository.sort = MagicMock(return_value=None)

    with pytest.raises(InternalServerError, match="common.process_issue"):
        SuitabilityService._SuitabilityService__get_last_suitability_answers_metadata(
            suitability_answers_repository=stubby_repository,
        )

    stubby_repository = MySuitabilityStubRepository(database="", collection="")
    stubby_repository.limit = MagicMock(return_value=None)

    with pytest.raises(InternalServerError, match="common.process_issue"):
        SuitabilityService._SuitabilityService__get_last_suitability_answers_metadata(
            suitability_answers_repository=stubby_repository,
        )


def test_get_last_suitability_answers_metadata_without_answers():
    stubby_repository = MySuitabilityStubRepository(database="", collection="")
    stubby_repository.limit = MagicMock(return_value=[])

    with pytest.raises(InternalServerError, match="suitability.error.no_answers"):
        SuitabilityService._SuitabilityService__get_last_suitability_answers_metadata(
            suitability_answers_repository=stubby_repository,
        )


def test_get_last_suitability_answers_metadata_with_invalid_answers_format():
    stubby_repository = MySuitabilityStubRepository(database="", collection="")
    stubby_repository.limit = MagicMock(return_value=[1])

    with pytest.raises(InternalServerError, match="suitability.error.answers_format"):
        SuitabilityService._SuitabilityService__get_last_suitability_answers_metadata(
            suitability_answers_repository=stubby_repository,
        )

    stubby_repository = MySuitabilityStubRepository(database="", collection="")
    stubby_repository.limit = MagicMock(return_value=["string"])

    with pytest.raises(InternalServerError, match="suitability.error.answers_format"):
        SuitabilityService._SuitabilityService__get_last_suitability_answers_metadata(
            suitability_answers_repository=stubby_repository,
        )


def test_get_last_suitability_answers_metadata_with_incomplete_answers_data():
    stubby_repository = MySuitabilityStubRepository(database="", collection="")
    stubby_repository.limit = MagicMock(return_value=[{"answers": None, "score": None}])

    with pytest.raises(InternalServerError, match="suitability.error.answers_incomplete_data"):
        SuitabilityService._SuitabilityService__get_last_suitability_answers_metadata(
            suitability_answers_repository=stubby_repository,
        )

    stubby_repository = MySuitabilityStubRepository(database="", collection="")
    stubby_repository.limit = MagicMock(return_value=[{"suitability_version": None, "score": None}])

    with pytest.raises(InternalServerError, match="suitability.error.answers_incomplete_data"):
        SuitabilityService._SuitabilityService__get_last_suitability_answers_metadata(
            suitability_answers_repository=stubby_repository,
        )


def test_get_last_suitability_answers_metadata():
    stubby_repository = MySuitabilityStubRepository(database="", collection="")
    stubby_repository.limit = MagicMock(return_value=[{"answers": None, "score": None}])

    with pytest.raises(InternalServerError, match="suitability.error.answers_incomplete_data"):
        SuitabilityService._SuitabilityService__get_last_suitability_answers_metadata(
            suitability_answers_repository=stubby_repository,
        )

    stubby_repository = MySuitabilityStubRepository(database="", collection="")
    stubby_repository.limit = MagicMock(return_value=[{"suitability_version": 2, "score": 1.0, "answers": True}])

    response = SuitabilityService._SuitabilityService__get_last_suitability_answers_metadata(
        suitability_answers_repository=stubby_repository,
    )

    assert (True, 1.0, 2) == response
