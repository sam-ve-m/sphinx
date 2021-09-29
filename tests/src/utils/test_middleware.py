# NATIVE LIBRARIES
from datetime import datetime

# OUTSIDE LIBRARIES
import pytest
from unittest.mock import MagicMock

# SPHINX
from src.utils.middleware import (
    get_valid_user_from_database,
    is_user_token_life_time_valid,
    get_valid_admin_from_database,
    validate_electronic_signature,
    get_token_if_token_is_valid,
)
from tests.stub_classes.stub_base_repository import StubBaseRepository
from tests.stub_classes.stub_request import (
    StubURL,
    StubRequest
)
from tests.stub_classes.stub_jwt_handler_composition import StubJWTHandler


class StubRepository(StubBaseRepository):
    pass


@pytest.fixture
def get_new_stubby_repository():
    return StubRepository(database="", collection="")


@pytest.fixture
def get_new_stub_jwt_handler():
    stub_jwt_handler = StubJWTHandler()
    return stub_jwt_handler


@pytest.fixture
def get_new_stub_request_user_with_mist_header():
    stub_url = StubURL
    stub_url.path = "/user"
    stub_request = StubRequest(url=stub_url)
    stub_request.headers.set_headers([(b"x-mist", b"lala")])
    return stub_request


@pytest.fixture
def get_new_stub_request_user_with_mist_header_wrong():
    stub_url = StubURL
    stub_url.path = "/user"
    stub_request = StubRequest(url=stub_url)
    stub_request.headers.set_headers([(b"x-mist", "lala")])
    return stub_request


def test_is_user_token_valid_error():
    user_data = {"token_valid_after": datetime.now().strftime("%Y-%m-%d")}
    jwt_data = {"created_at": "2020-12-01"}
    token_valid = is_user_token_life_time_valid(user_data=user_data, token=jwt_data)
    assert token_valid is False


def test_is_user_token_valid_false_because_created_at_date_is_invalid():
    user_data = {
        "token_valid_after": datetime(year=2020, month=10, day=10).strftime("%Y-%m-%d")
    }
    jwt_data = {"created_at": "2020-01-01"}
    token_valid = is_user_token_life_time_valid(user_data=user_data, token=jwt_data)
    assert token_valid is False


def test_is_user_token_valid_false_because_token_is_expired():
    user_data = {
        "token_valid_after": datetime(year=2020, month=10, day=11).strftime("%Y-%m-%d")
    }
    jwt_data = {"created_at": "2020-10-10"}
    token_valid = is_user_token_life_time_valid(user_data=user_data, token=jwt_data)
    assert token_valid is False


def test_is_user_token_valid_true():
    user_data = {
        "token_valid_after": datetime(year=2020, month=10, day=10).strftime("%Y-%m-%d")
    }
    jwt_data = {"created_at": "2020-11-01"}
    token_valid = is_user_token_life_time_valid(user_data=user_data, token=jwt_data)
    assert token_valid


def test_get_valid_user_from_database_repository_does_not_fid_user(
    get_new_stubby_repository,
):
    user_repository = get_new_stubby_repository
    user_repository.find_one = MagicMock(return_value=None)
    token = {"email": ""}
    assert (
        get_valid_user_from_database(token=token, user_repository=user_repository)
        is None
    )


def test_get_valid_user_from_database_user_is_not_active():
    user_repository = get_new_stubby_repository
    user_repository.find_one = MagicMock(return_value={"is_active_user": False})
    token = {"email": ""}
    assert (
        get_valid_user_from_database(token=token, user_repository=user_repository)
        is None
    )


def test_get_valid_user_from_database():
    user_repository = get_new_stubby_repository
    user_stub_data = {"is_active_user": True}
    user_repository.find_one = MagicMock(return_value=user_stub_data)
    token = {"email": ""}
    assert (
        get_valid_user_from_database(token=token, user_repository=user_repository)
        == user_stub_data
    )


def test_get_valid_admin_from_database_repository_does_not_fid_user(
    get_new_stubby_repository,
):
    user_repository = get_new_stubby_repository
    user_repository.find_one = MagicMock(return_value=None)
    token = {"email": ""}
    assert (
        get_valid_admin_from_database(token=token, user_repository=user_repository)
        is None
    )


def test_get_valid_admin_from_database_user_is_not_active(get_new_stubby_repository):
    user_repository = get_new_stubby_repository
    user_repository.find_one = MagicMock(return_value={"is_active_user": False})
    token = {"email": ""}
    assert (
        get_valid_admin_from_database(token=token, user_repository=user_repository)
        is None
    )


def test_get_valid_admin_from_database_dont_have_admin_key(get_new_stubby_repository):
    user_repository = get_new_stubby_repository
    user_stub_data = {"is_active_user": True}
    user_repository.find_one = MagicMock(return_value=user_stub_data)
    token = {"email": ""}
    assert (
        get_valid_admin_from_database(token=token, user_repository=user_repository)
        is None
    )


def test_get_valid_admin_from_database_is_not_admin(get_new_stubby_repository):
    user_repository = get_new_stubby_repository
    user_stub_data = {"is_active_user": True, "is_admin": False}
    user_repository.find_one = MagicMock(return_value=user_stub_data)
    token = {"email": ""}
    assert (
        get_valid_admin_from_database(token=token, user_repository=user_repository)
        is None
    )


def test_get_valid_admin_from_database(get_new_stubby_repository):
    user_repository = get_new_stubby_repository
    user_stub_data = {"is_active_user": True, "is_admin": True}
    user_repository.find_one = MagicMock(return_value=user_stub_data)
    token = {"email": ""}
    assert (
        get_valid_admin_from_database(token=token, user_repository=user_repository)
        == user_stub_data
    )


def test_validate_electronic_signature_with_token(
    get_new_stub_request_user_with_mist_header, get_new_stub_jwt_handler
):
    stub_request = get_new_stub_request_user_with_mist_header
    stub_jwt_handler = get_new_stub_jwt_handler

    stub_jwt_handler.mist.validate_jwt = MagicMock(return_value=False)

    assert (
        validate_electronic_signature(
            request=stub_request, user_data={}, jwt_handler=stub_jwt_handler
        )
        is False
    )


def test_validate_electronic_signature_with_token_not_encoded(
    get_new_stub_request_user_with_mist_header_wrong, get_new_stub_jwt_handler
):
    stub_request = get_new_stub_request_user_with_mist_header_wrong
    stub_jwt_handler = get_new_stub_jwt_handler

    stub_jwt_handler.mist.validate_jwt = MagicMock(return_value=False)
    with pytest.raises(AttributeError):
        validate_electronic_signature(
            request=stub_request, user_data={}, jwt_handler=stub_jwt_handler
        )


def test_validate_electronic_signature_with_token_and_is_valid_but_email_does_not_match(
    get_new_stub_request_user_with_mist_header, get_new_stub_jwt_handler
):
    stub_request = get_new_stub_request_user_with_mist_header
    stub_jwt_handler = get_new_stub_jwt_handler

    stub_jwt_handler.mist.validate_jwt = MagicMock(return_value=False)
    stub_jwt_handler.mist.decrypt_payload = MagicMock(return_value={"email": "lalala"})

    assert (
        validate_electronic_signature(
            request=stub_request,
            user_data={"email": "lala"},
            jwt_handler=stub_jwt_handler,
        )
        is False
    )


def test_validate_electronic_signature_with_token_and_is_valid_but_email_does_match(
    get_new_stub_request_user_with_mist_header, get_new_stub_jwt_handler
):
    stub_request = get_new_stub_request_user_with_mist_header
    stub_jwt_handler = get_new_stub_jwt_handler

    stub_jwt_handler.mist.validate_jwt = MagicMock(return_value=False)
    stub_jwt_handler.mist.decrypt_payload = MagicMock(return_value={"email": "lala"})

    assert (
        validate_electronic_signature(
            request=stub_request,
            user_data={"email": "lala"},
            jwt_handler=stub_jwt_handler,
        )
        is False
    )


def test_get_token_if_token_is_valid(
    get_new_stub_request_user_with_mist_header, get_new_stub_jwt_handler
):
    value = "lala"
    stub_jwt_handler = get_new_stub_jwt_handler
    stub_request = get_new_stub_request_user_with_mist_header
    stub_jwt_handler.get_thebes_answer_from_request = MagicMock(return_value=value)
    assert value == get_token_if_token_is_valid(
        request=stub_request, jwt_handler=stub_jwt_handler
    )


def test_get_token_if_token_is_valid_raise_error(
    get_new_stub_request_user_with_mist_header, get_new_stub_jwt_handler
):
    stub_jwt_handler = get_new_stub_jwt_handler
    stub_request = get_new_stub_request_user_with_mist_header
    stub_jwt_handler.get_thebes_answer_from_request = MagicMock(
        name="get_thebes_answer_from_request", side_effect=BaseException()
    )

    assert (
        get_token_if_token_is_valid(request=stub_request, jwt_handler=stub_jwt_handler)
        is None
    )
