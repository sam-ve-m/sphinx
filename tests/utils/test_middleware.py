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


class StubRepository(StubBaseRepository):
    pass


@pytest.fixture
def get_new_stubby_repository():
    return StubRepository(database="", collection="")


@pytest.fixture
def get_new_stubby_request_user():
    stub_url = StubURL
    stub_url.path = "/user"
    return StubRequest(url=stub_url)


@pytest.fixture
def get_new_stubby_request_forgot_password():
    stub_url = StubURL
    stub_url.path = "/user/forgot_password"
    return StubRequest(url=stub_url)


@pytest.fixture
def get_new_stubby_request_login():
    stub_url = StubURL
    stub_url.path = "/login"
    return StubRequest(url=stub_url)


@pytest.fixture
def get_new_stubby_request_login_admin():
    stub_url = StubURL
    stub_url.path = "/login/admin"
    return StubRequest(url=stub_url)


@pytest.fixture
def get_new_stubby_request_none_path():
    stub_url = StubURL
    stub_url.path = None
    return StubRequest(url=stub_url)


@pytest.fixture
def get_new_stubby_request_random_path():
    stub_url = StubURL
    stub_url.path = "/xx"
    return StubRequest(url=stub_url)


@pytest.fixture
def get_new_stubby_request_feature():
    stub_url = StubURL
    stub_url.path = "/feature"
    return StubRequest(url=stub_url)


@pytest.fixture
def get_new_stubby_request_term():
    stub_url = StubURL
    stub_url.path = "/term"
    return StubRequest(url=stub_url)


@pytest.fixture
def get_new_stubby_request_views():
    stub_url = StubURL
    stub_url.path = "/views"
    return StubRequest(url=stub_url)


@pytest.fixture
def get_new_stubby_request_user_admin():
    stub_url = StubURL
    stub_url.path = "/user/admin"
    return StubRequest(url=stub_url)


def test_is_public_true_user(get_new_stubby_request_user):
    route_public = is_public(request=get_new_stubby_request_user)
    assert route_public is True

def test_is_public_false(get_new_stubby_request_feature):
    route_public = is_public(request=get_new_stubby_request_feature)
    assert route_public is False


def test_forgot_password_post_is_public(get_new_stubby_request_forgot_password):
    route_public = is_public(request=get_new_stubby_request_forgot_password)
    assert route_public is True


def test_login_is_public(get_new_stubby_request_login):
    route_public = is_public(request=get_new_stubby_request_login)
    assert route_public is True


def test_login_admin_is_public(get_new_stubby_request_login_admin):
    route_public = is_public(request=get_new_stubby_request_login_admin)
    assert route_public is True


def test_none_url_path_is_public(get_new_stubby_request_none_path):
    route_public = is_public(request=get_new_stubby_request_none_path)
    assert route_public is False


def test_is_public_true(get_new_stubby_request_random_path):
    route_public = is_public(request=get_new_stubby_request_random_path)
    assert route_public is True


def test_need_be_admin_false(get_new_stubby_request_random_path):
    is_admin_route = need_be_admin(request=get_new_stubby_request_random_path)
    assert is_admin_route is False


def test_feature_need_be_admin_true(get_new_stubby_request_feature):
    is_admin_route = need_be_admin(request=get_new_stubby_request_feature)
    assert is_admin_route is True


def test_term_need_be_admin_true(get_new_stubby_request_term):
    is_admin_route = need_be_admin(request=get_new_stubby_request_term)
    assert is_admin_route is True


def test_views_need_be_admin_true(get_new_stubby_request_views):
    is_admin_route = need_be_admin(request=get_new_stubby_request_views)
    assert is_admin_route is True


def test_user_admin_need_be_admin(get_new_stubby_request_user_admin):
    is_admin_route = need_be_admin(request=get_new_stubby_request_user_admin)
    assert is_admin_route is True


def test_is_user_deleted_true():
    user_data = {"deleted": True}
    assert is_user_deleted(user_data=user_data)


def test_is_user_deleted_false():
    user_data = {"deleted": False}
    assert is_user_deleted(user_data=user_data) is False


def test_is_user_token_valid_error():
    user_data = {"token_valid_after": datetime.now().strftime("%Y-%m-%d")}
    jwt_data = {"created_at": "2020-12-01"}
    token_valid = is_user_token_valid(user_data=user_data, jwt_data=jwt_data)
    assert token_valid is False


def test_is_user_token_valid_false_because_created_at_date_is_invalid():
    user_data = {
        "token_valid_after": datetime(year=2020, month=10, day=10).strftime("%Y-%m-%d")
    }
    jwt_data = {"created_at": "2020-01-01"}
    token_valid = is_user_token_valid(user_data=user_data, jwt_data=jwt_data)
    assert token_valid is False


def test_is_user_token_valid_false_because_token_is_expired():
    user_data = {
        "token_valid_after": datetime(year=2020, month=10, day=10).strftime("%Y-%m-%d")
    }
    jwt_data = {"created_at": "2020-10-10"}
    token_valid = is_user_token_valid(user_data=user_data, jwt_data=jwt_data)
    assert token_valid is False


def test_is_user_token_valid_true():
    user_data = {
        "token_valid_after": datetime(year=2020, month=10, day=10).strftime("%Y-%m-%d")
    }
    jwt_data = {"created_at": "2020-11-01"}
    token_valid = is_user_token_valid(user_data=user_data, jwt_data=jwt_data)
    assert token_valid


def test_invalidate_user_true():
    user_data = {
        "token_valid_after": datetime(year=2020, month=10, day=10).strftime("%Y-%m-%d"),
        "deleted": True,
    }
    jwt_data = {"created_at": "2020-01-01"}
    is_invalidate_user = invalidate_user(user_data=user_data, jwt_data=jwt_data)
    assert is_invalidate_user is False


def test_invalidate_user_false():
    user_data = {
        "token_valid_after": datetime(year=2020, month=10, day=10),
        "deleted": False,
    }
    jwt_data = {"created_at": "2020-11-01"}
    is_invalidate_user = invalidate_user(user_data=user_data, jwt_data=jwt_data)
    assert is_invalidate_user is False


def test_check_if_user_is_allowed_to_access_route_user_is_admin(get_new_stubby_request_random_path,
                                                                get_new_stubby_repository):
    request = get_new_stubby_request_random_path
    user_data = {
        "token_valid_after": "2020-06-01",
        "deleted": False,
        "is_admin": True,
    }
    user_repository = get_new_stubby_repository
    user_repository.find_one = MagicMock(return_value=user_data)
    jwt_data = {"created_at": "2020-07-01", "email": "test@test.com"}
    is_user_not_allowed_value = check_if_is_user_not_allowed_to_access_route(
        request=request, jwt_data=jwt_data, user_repository=user_repository
    )
    assert is_user_not_allowed_value.status_code == 200


def test_check_if_is_user_not_allowed_to_access_route_user_not_admin(get_new_stubby_request_views,
                                                                     get_new_stubby_repository):
    request = get_new_stubby_request_views
    user_data = {
        "token_valid_after": datetime(year=2020, month=10, day=10).strftime("%Y-%m-%d"),
        "deleted": False,
        "is_admin": False,
    }
    user_repository = get_new_stubby_repository
    user_repository.find_one = MagicMock(return_value=user_data)
    jwt_data = {"created_at": "2020-11-01", "email": "test@test.com"}
    is_user_not_allowed_value = check_if_is_user_not_allowed_to_access_route(
        request=request, jwt_data=jwt_data, user_repository=user_repository
    )
    assert is_user_not_allowed_value.status_code == 401


def test_check_if_is_user_not_allowed_to_access_route_user_not_admin_and_user_is_deleted(get_new_stubby_request_views,
                                                                                         get_new_stubby_repository):
    request = get_new_stubby_request_views
    user_data = {
        "token_valid_after": datetime(year=2020, month=11, day=10).strftime("%Y-%m-%d"),
        "deleted": True,
        "is_admin": False,
    }
    user_repository = get_new_stubby_repository
    user_repository.find_one = MagicMock(return_value=user_data)
    jwt_data = {"created_at": "2020-11-01", "email": "test@test.com"}
    is_user_not_allowed_value = check_if_is_user_not_allowed_to_access_route(
        request=request, jwt_data=jwt_data, user_repository=user_repository
    )
    assert is_user_not_allowed_value.status_code == 401


def test_check_if_is_user_not_allowed_to_access_route_user_is_admin_and_user_is_deleted(get_new_stubby_request_views,
                                                                                        get_new_stubby_repository):
    request = get_new_stubby_request_views
    user_data = {
        "token_valid_after": datetime(year=2020, month=11, day=10).strftime("%Y-%m-%d"),
        "deleted": True,
        "is_admin": True,
    }
    user_repository = get_new_stubby_repository
    user_repository.find_one = MagicMock(return_value=user_data)
    jwt_data = {"created_at": "2020-11-01", "email": "test@test.com"}
    is_user_not_allowed_value = check_if_is_user_not_allowed_to_access_route(
        request=request, jwt_data=jwt_data, user_repository=user_repository
    )
    assert is_user_not_allowed_value.status_code == 401
