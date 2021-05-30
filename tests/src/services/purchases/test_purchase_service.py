import pytest
from unittest.mock import MagicMock
from fastapi import status

from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.services.purchases.service import PurchaseService
from src.utils.jwt_utils import JWTHandler
from tests.stubby_classes.stubby_base_repository import StubbyBaseRepository


class StubbyRepository(StubbyBaseRepository):
    pass


def test_add_feature_already_exists():
    user_data = {
        "email": "afl@lionx.com.br",
        "name": "anderson",
        "scope": {
            "view_type": None,
            "features": ["real_time_data"]
        },
        "is_active": True,
        "deleted": False,
        "use_magic_link": False,
        "token_valid_after": {
            "$date": "2021-05-29T20:00:52.571Z"
        }
    }

    jwt = JWTHandler.generate_token(payload=user_data, ttl=525600)
    payload = {
        "thebes_answer": JWTHandler.decrypt_payload(jwt),
        "feature": "real_time_data"
    }
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.update_one = MagicMock(return_value=True)
    result = PurchaseService.add_feature(payload=payload, user_repository=stubby_repository,
                                         token_handler=JWTHandler)
    assert result.get("status_code") == status.HTTP_304_NOT_MODIFIED

def test_add_feature():
    user_data = {
        "email": "afl@lionx.com.br",
        "name": "anderson",
        "scope": {
            "view_type": None,
            "features": ["real_time_data"]
        },
        "is_active": True,
        "deleted": False,
        "use_magic_link": False,
        "token_valid_after": {
            "$date": "2021-05-29T20:00:52.571Z"
        }
    }

    jwt = JWTHandler.generate_token(payload=user_data, ttl=525600)
    payload = {
        "thebes_answer": JWTHandler.decrypt_payload(jwt),
        "feature": "test_feature"
    }
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.update_one = MagicMock(return_value=True)
    result = PurchaseService.add_feature(payload=payload, user_repository=stubby_repository,
                                         token_handler=JWTHandler)
    assert result.get("status_code") == status.HTTP_200_OK

def test_delete_feature_not_exists():
    user_data = {
        "email": "afl@lionx.com.br",
        "name": "anderson",
        "scope": {
            "view_type": None,
            "features": ["real_time_data"]
        },
        "is_active": True,
        "deleted": False,
        "use_magic_link": False,
        "token_valid_after": {
            "$date": "2021-05-29T20:00:52.571Z"
        }
    }

    jwt = JWTHandler.generate_token(payload=user_data, ttl=525600)
    payload = {
        "thebes_answer": JWTHandler.decrypt_payload(jwt),
        "feature": "test_feature"
    }
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.update_one = MagicMock(return_value=True)
    result = PurchaseService.delete_feature(payload=payload, user_repository=stubby_repository,
                                         token_handler=JWTHandler)
    assert result.get("status_code") == status.HTTP_304_NOT_MODIFIED

def test_delete_feature_that_exists():
    user_data = {
        "email": "afl@lionx.com.br",
        "name": "anderson",
        "scope": {
            "view_type": None,
            "features": ["real_time_data"]
        },
        "is_active": True,
        "deleted": False,
        "use_magic_link": False,
        "token_valid_after": {
            "$date": "2021-05-29T20:00:52.571Z"
        }
    }

    jwt = JWTHandler.generate_token(payload=user_data, ttl=525600)
    payload = {
        "thebes_answer": JWTHandler.decrypt_payload(jwt),
        "feature": "real_time_data"
    }
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.update_one = MagicMock(return_value=True)
    result = PurchaseService.delete_feature(payload=payload, user_repository=stubby_repository,
                                         token_handler=JWTHandler)
    assert result.get("status_code") == status.HTTP_200_OK
