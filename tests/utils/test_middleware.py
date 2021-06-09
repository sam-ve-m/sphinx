# NATIVE LIBRARIES
from typing import Type
from datetime import datetime

# OUTSIDE LIBRARIES
import pytest
from fastapi import Response
from unittest.mock import MagicMock

# SPHINX
from src.utils.middleware import (
    is_public,
    need_be_admin,
    is_user_deleted,
    is_user_token_valid,
    invalidate_user,
    is_user_not_allowed,
)
from tests.stub_classes.stub_base_repository import StubBaseRepository


class StubURL:
    path = "/"


class StubHeaders:
    raw = []


class StubRequest:
    method = "POST"
    headers = StubHeaders()

    def __init__(self, url: Type[StubURL]):
        self.url = url


def test_is_public_true_post():
    stub_url = StubURL
    stub_url.path = "/user"
    request = StubRequest(url=stub_url)
    route_public = is_public(request=request)
    assert route_public


def test_is_public_true_get():
    stub_url = StubURL
    stub_url.path = "/term"
    request = StubRequest(url=stub_url)
    request.method = "GET"
    route_public = is_public(request=request)
    assert route_public


def test_is_public_false_post():
    stub_url = StubURL
    request = StubRequest(url=stub_url)
    route_public = is_public(request=request)
    assert route_public is False


def test_is_public_false_get():
    stub_url = StubURL
    stub_url.path = "/xxx"
    request = StubRequest(url=stub_url)
    request.method = "GET"
    route_public = is_public(request=request)
    assert route_public is False


def test_need_be_admin_false():
    stub_url = StubURL
    stub_url.path = "/xx"
    request = StubRequest(url=stub_url)
    is_admin_route = need_be_admin(request=request)
    assert is_admin_route is False


def test_need_be_admin_false_post():
    stub_url = StubURL
    stub_url.path = "/xxx"
    request = StubRequest(url=stub_url)
    request.method = "POST"
    is_admin_route = need_be_admin(request=request)
    assert is_admin_route is False


def test_need_be_admin_true():
    stub_url = StubURL
    stub_url.path = "/user_admin"
    request = StubRequest(url=stub_url)
    is_admin_route = need_be_admin(request=request)
    assert is_admin_route


def test_need_be_admin_true_post():
    stub_url = StubURL
    stub_url.path = "/term"
    request = StubRequest(url=stub_url)
    request.method = "POST"
    is_admin_route = need_be_admin(request=request)
    assert is_admin_route


def test_is_user_deleted_true():
    user_data = {"deleted": True}
    assert is_user_deleted(user_data=user_data)


def test_is_user_deleted_false():
    user_data = {"deleted": False}
    assert is_user_deleted(user_data=user_data) is False


def test_is_user_token_valid_error():
    user_data = {"token_valid_after": datetime.now()}
    jwt_data = {"created_at": "20-01-01"}
    token_valid = is_user_token_valid(user_data=user_data, jwt_data=jwt_data)
    assert token_valid is False


def test_is_user_token_valid_false():
    user_data = {"token_valid_after": datetime(year=2020, month=10, day=10)}
    jwt_data = {"created_at": "20-01-01"}
    token_valid = is_user_token_valid(user_data=user_data, jwt_data=jwt_data)
    assert token_valid is False


def test_is_user_token_valid_true():
    user_data = {"token_valid_after": datetime(year=2020, month=10, day=10)}
    jwt_data = {"created_at": "2020-01-01 12:10:10.0000"}
    token_valid = is_user_token_valid(user_data=user_data, jwt_data=jwt_data)
    assert token_valid


def test_invalidate_user_true():
    user_data = {
        "token_valid_after": datetime(year=2020, month=10, day=10),
        "deleted": True,
    }
    jwt_data = {"created_at": "2020-01-01 12:10:10.0000"}
    is_invalidate_user = invalidate_user(user_data=user_data, jwt_data=jwt_data)
    assert is_invalidate_user


def test_invalidate_user_false():
    user_data = {
        "token_valid_after": datetime(year=2020, month=10, day=10),
        "deleted": False,
    }
    jwt_data = {"created_at": "2020-11-01 12:10:10.0000"}
    is_invalidate_user = invalidate_user(user_data=user_data, jwt_data=jwt_data)
    assert is_invalidate_user is False


class StubRepository(StubBaseRepository):
    pass


def test_is_user_not_allowed_true():
    stub_url = StubURL
    stub_url.path = "/xxx"
    request = StubRequest(url=stub_url)
    request.method = "GET"
    user_data = {
        "token_valid_after": datetime(year=2020, month=10, day=10),
        "deleted": False,
    }
    user_repository = StubRepository(database="", collection="")
    user_repository.find_one = MagicMock(return_value=user_data)
    jwt_data = {"created_at": "2020-11-01 12:10:10.0000", "email": "test@test.com"}
    is_user_not_allowed_value = is_user_not_allowed(
        jwt_data=jwt_data, request=request, user_repository=user_repository
    )
    assert isinstance(is_user_not_allowed_value, Response) is False


def test_is_user_not_allowed_false():
    stub_url = StubURL
    stub_url.path = "/xxx"
    request = StubRequest(url=stub_url)
    request.method = "GET"
    user_data = {
        "token_valid_after": datetime(year=2020, month=10, day=10),
        "deleted": True,
    }
    user_repository = StubRepository(database="", collection="")
    user_repository.find_one = MagicMock(return_value=user_data)
    jwt_data = {"created_at": "2020-11-01 12:10:10.0000", "email": "test@test.com"}
    is_user_not_allowed_value = is_user_not_allowed(
        jwt_data=jwt_data, request=request, user_repository=user_repository
    )
    assert isinstance(is_user_not_allowed_value, Response)
