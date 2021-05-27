import pytest
from unittest.mock import MagicMock
from fastapi import status

from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.services.authentications.service import AuthenticationService
from tests.stubby_classes.stubby_base_repository import StubbyBaseRepository


class StubbyRepository(StubbyBaseRepository):
    pass


class StubbyTokenHandler(StubbyBaseRepository):
    @staticmethod
    def generate_token(paylod: dict, ttl: int):
        pass


payload = {"email": ""}


def test_answer_register_exists():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        AuthenticationService.answer(
            payload=payload,
            user_repository=stubby_repository,
            token_handler=StubbyTokenHandler,
        )


def test_answer_process_issue():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={})
    stubby_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        AuthenticationService.answer(
            payload=payload,
            user_repository=stubby_repository,
            token_handler=StubbyTokenHandler,
        )


def test_answer():
    generate_token_value = 'lalala'
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={
        "pin": '',
        "_id": '',
    })
    stubby_repository.update_one = MagicMock(return_value=True)
    StubbyTokenHandler.generate_token = MagicMock(return_value=generate_token_value)
    response = AuthenticationService.answer(
        payload=payload,
        user_repository=stubby_repository,
        token_handler=StubbyTokenHandler,
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("payload") == generate_token_value
