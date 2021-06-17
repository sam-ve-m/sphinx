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
    check_if_is_user_not_allowed_to_access_route,
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


def test_forgort_password_post_is_public():
    stub_url = StubURL
    stub_url.path = "/user/forgot_password"
    request = StubRequest(url=stub_url)
    route_public = is_public(request=request)
    assert route_public


def test_login_post_is_public():
    stub_url = StubURL
    stub_url.path = "/login"
    request = StubRequest(url=stub_url)
    route_public = is_public(request=request)
    assert route_public


def test_login_admin_post_is_public():
    stub_url = StubURL
    stub_url.path = "/login/admin"
    request = StubRequest(url=stub_url)
    route_public = is_public(request=request)
    assert route_public


def test_any_post_is_public():
    stub_url = StubURL
    stub_url.path = "/ANY_POST_METHOD"
    request = StubRequest(url=stub_url)
    route_public = is_public(request=request)
    assert route_public is False


def test_any_get_is_public():
    stub_url = StubURL
    stub_url.path = "ANY_GET_METHOD"
    request = StubRequest(url=stub_url)
    request.method = "GET"
    route_public = is_public(request=request)
    assert route_public is False


def test_none_url_path_is_public():
    stub_url = StubURL
    request = StubRequest(url=stub_url)
    request.method = "GET"
    route_public = is_public(request=request)
    assert route_public is False


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


def test_feature_need_be_admin_true():
    stub_url = StubURL
    stub_url.path = "/feature"
    request = StubRequest(url=stub_url)
    is_admin_route = need_be_admin(request=request)
    assert is_admin_route is True


def test_term_need_be_admin_true_post():
    stub_url = StubURL
    stub_url.path = "/term"
    request = StubRequest(url=stub_url)
    request.method = "POST"
    is_admin_route = need_be_admin(request=request)
    assert is_admin_route is True


def test_views_need_be_admin_true_post():
    stub_url = StubURL
    stub_url.path = "/views"
    request = StubRequest(url=stub_url)
    request.method = "POST"
    is_admin_route = need_be_admin(request=request)
    assert is_admin_route is True


def test_user_admin_need_be_admin_true_post():
    stub_url = StubURL
    stub_url.path = "/user_admin"
    request = StubRequest(url=stub_url)
    request.method = "POST"
    is_admin_route = need_be_admin(request=request)
    assert is_admin_route is True


def test_is_user_deleted_true():
    user_data = {"deleted": True}
    assert is_user_deleted(user_data=user_data)


def test_is_user_deleted_false():
    user_data = {"deleted": False}
    assert is_user_deleted(user_data=user_data) is False


def test_is_user_token_valid_error():
    user_data = {"token_valid_after": "2020-12-01"}
    jwt_data = {"created_at": datetime.now().strftime("%Y-%m-%d")}
    token_valid = is_user_token_valid(user_data=user_data, jwt_data=jwt_data)
    assert token_valid is False


def test_is_user_token_valid_false_because_created_at_date_is_invalid():
    user_data = {
        "token_valid_after": datetime(
            year=2020, month=10, day=10, hour=0, minute=0, second=0
        )
    }
    jwt_data = {"created_at": "2020-01-01"}
    token_valid = is_user_token_valid(user_data=user_data, jwt_data=jwt_data)
    assert token_valid is False


def test_is_user_token_valid_false_because_token_is_expired():
    user_data = {
        "token_valid_after": datetime(
            year=2020, month=10, day=10, hour=0, minute=0, second=0
        )
    }
    jwt_data = {"created_at": "2020-10-10"}
    token_valid = is_user_token_valid(user_data=user_data, jwt_data=jwt_data)
    assert token_valid is False


def test_is_user_token_valid_true():
    user_data = {
        "token_valid_after": datetime(
            year=2020, month=10, day=10, hour=0, minute=0, second=0
        ).strftime("%Y-%m-%d")
    }
    jwt_data = {"created_at": "2020-01-01"}
    token_valid = is_user_token_valid(user_data=user_data, jwt_data=jwt_data)
    assert token_valid


def test_invalidate_user_true():
    user_data = {
        "token_valid_after": datetime(year=2020, month=10, day=10),
        "deleted": True,
    }
    jwt_data = {"created_at": "2020-01-01"}
    is_invalidate_user = invalidate_user(user_data=user_data, jwt_data=jwt_data)
    assert is_invalidate_user


def test_invalidate_user_false():
    user_data = {
        "token_valid_after": datetime(year=2020, month=10, day=10),
        "deleted": False,
    }
    jwt_data = {"created_at": "2020-11-01"}
    is_invalidate_user = invalidate_user(user_data=user_data, jwt_data=jwt_data)
    assert is_invalidate_user is False


class StubRepository(StubBaseRepository):
    pass


def test_check_if_is_user_not_allowed_to_access_route_expect_request_because_user_not_is_admin_accessing_admin_route():
    stub_url = StubURL
    stub_url.path = "/views"
    request = StubRequest(url=stub_url)
    request.method = "GET"
    user_data = {
        "token_valid_after": "2020-11-01",
        "deleted": False,
        "is_admin": False,
    }
    user_repository = StubRepository(database="", collection="")
    user_repository.find_one = MagicMock(return_value=user_data)
    jwt_data = {"created_at": "2020-06-01", "email": "test@test.com"}
    is_user_not_allowed_value = check_if_is_user_not_allowed_to_access_route(
        request=request, jwt_data=jwt_data, user_repository=user_repository
    )
    assert is_user_not_allowed_value.status_code == 401


def test_check_if_is_user_not_allowed_to_access_route_expect_none_because_user_not_is_admin_accessing_not_admin_route():
    stub_url = StubURL
    stub_url.path = "/not_admin_route"
    request = StubRequest(url=stub_url)
    request.method = "GET"
    user_data = {
        "token_valid_after": "2020-11-01",
        "deleted": False,
        "is_admin": False,
    }
    user_repository = StubRepository(database="", collection="")
    user_repository.find_one = MagicMock(return_value=user_data)
    jwt_data = {"created_at": "2020-06-01", "email": "test@test.com"}
    is_user_not_allowed_value = check_if_is_user_not_allowed_to_access_route(
        request=request, jwt_data=jwt_data, user_repository=user_repository
    )
    assert is_user_not_allowed_value.status_code == 200


def test_check_if_is_user_not_allowed_to_access_route_expect_none_because_user_is_admin_accessing_admin_route():
    stub_url = StubURL
    stub_url.path = "/views"
    request = StubRequest(url=stub_url)
    request.method = "GET"
    user_data = {
        "token_valid_after": datetime(year=2020, month=10, day=10),
        "deleted": False,
        "is_admin": True,
    }
    user_repository = StubRepository(database="", collection="")
    user_repository.find_one = MagicMock(return_value=user_data)
    jwt_data = {"created_at": "2020-11-01", "email": "test@test.com"}
    is_user_not_allowed_value = check_if_is_user_not_allowed_to_access_route(
        request=request, jwt_data=jwt_data, user_repository=user_repository
    )
    assert is_user_not_allowed_value.status_code == 200


def test_check_if_is_user_not_allowed_to_access_route_expect_request_because_admin_user_is_not_allowed():
    stub_url = StubURL
    stub_url.path = "/views"
    request = StubRequest(url=stub_url)
    request.method = "GET"
    user_data = {
        "token_valid_after": datetime(year=2020, month=10, day=10),
        "deleted": True,
        "is_admin": False,
    }
    user_repository = StubRepository(database="", collection="")
    user_repository.find_one = MagicMock(return_value=user_data)
    jwt_data = {"created_at": "2020-11-01 12:10:10.0000", "email": "test@test.com"}
    is_user_not_allowed_value = check_if_is_user_not_allowed_to_access_route(
        request=request, jwt_data=jwt_data, user_repository=user_repository
    )
    assert isinstance(is_user_not_allowed_value, Response) is True


def test_check_if_is_user_not_allowed_to_access_route_expect_request_because_not_admin_user_is_not_allowed():
    stub_url = StubURL
    stub_url.path = "/views"
    request = StubRequest(url=stub_url)
    request.method = "GET"
    user_data = {
        "token_valid_after": datetime(year=2020, month=10, day=10),
        "deleted": True,
        "is_admin": True,
    }
    user_repository = StubRepository(database="", collection="")
    user_repository.find_one = MagicMock(return_value=user_data)
    jwt_data = {"created_at": "2020-11-01 12:10:10.0000", "email": "test@test.com"}
    is_user_not_allowed_value = check_if_is_user_not_allowed_to_access_route(
        request=request, jwt_data=jwt_data, user_repository=user_repository
    )
    assert isinstance(is_user_not_allowed_value, Response) is True
