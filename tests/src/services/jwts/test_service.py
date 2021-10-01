# OUTSIDE LIBRARIES
import pytest
from unittest.mock import MagicMock, patch

# SPHINX
from tests.stub_classes.stub_request import (
    StubURL,
    StubRequest
)
from tests.stub_classes.stub_jwt_service_composition import StubJwtService
from src.exceptions.exceptions import UnauthorizedError, InternalServerError


@pytest.fixture
def get_new_stub_jwt_service():
    stub_jwt_service = StubJwtService()
    return stub_jwt_service


@pytest.fixture
def get_new_stub_request_with_thebes_answer_header():
    stub_url = StubURL
    stub_url.path = "/"
    stub_request = StubRequest(url=stub_url)
    stub_request.headers.set_headers([(b"x-thebes-answer", b"lala")])
    return stub_request


@pytest.fixture
def get_new_stub_request_with_thebes_answer_header_wrong_encode():
    stub_url = StubURL
    stub_url.path = "/"
    stub_request = StubRequest(url=stub_url)
    stub_request.headers.set_headers([(b"x-thebes-answer", "lala")])
    return stub_request


@pytest.fixture
def get_new_stub_request_with_out_thebes_answer_header():
    stub_url = StubURL
    stub_url.path = "/"
    stub_request = StubRequest(url=stub_url)
    return stub_request


def test_get_jwt_from_request_with_header_with_wrong_encode(
    get_new_stub_jwt_service,
    get_new_stub_request_with_thebes_answer_header_wrong_encode
):
    stub_request = get_new_stub_request_with_thebes_answer_header_wrong_encode
    stub_jwt_service = get_new_stub_jwt_service
    with pytest.raises(AttributeError):
        stub_jwt_service.get_jwt_from_request(request=stub_request)


def test_get_jwt_from_request_with_out_header(
    get_new_stub_jwt_service,
    get_new_stub_request_with_out_thebes_answer_header
):
    stub_request = get_new_stub_request_with_out_thebes_answer_header
    stub_jwt_service = get_new_stub_jwt_service
    assert stub_jwt_service.get_jwt_from_request(request=stub_request) is None


def test_get_jwt_from_request_with_header(
    get_new_stub_jwt_service,
    get_new_stub_request_with_thebes_answer_header
):
    stub_request = get_new_stub_request_with_thebes_answer_header
    stub_jwt_service = get_new_stub_jwt_service
    assert stub_jwt_service.get_jwt_from_request(request=stub_request) == "lala"


def test_get_thebes_answer_from_request_fail_to_get_jwt(
    get_new_stub_request_with_out_thebes_answer_header,
    get_new_stub_jwt_service
):
    stub_request = get_new_stub_request_with_out_thebes_answer_header
    stub_jwt_service = get_new_stub_jwt_service
    with pytest.raises(UnauthorizedError):
        stub_jwt_service.get_thebes_answer_from_request(request=stub_request)


@patch('src.services.jwts.service.JwtService.decrypt_payload')
def test_get_thebes_answer_from_request(
    mock_decrypt_payload,
    get_new_stub_request_with_thebes_answer_header,
    get_new_stub_jwt_service
):
    stub_request = get_new_stub_request_with_thebes_answer_header
    stub_jwt_service = get_new_stub_jwt_service
    decrypted_payload = {"a": 1}
    mock_decrypt_payload.return_value = decrypted_payload
    assert stub_jwt_service.get_thebes_answer_from_request(request=stub_request) == decrypted_payload


def test_decrypt_payload_error_raised(
    get_new_stub_jwt_service
):
    stub_jwt_service = get_new_stub_jwt_service
    stub_jwt_service.heimdall.decrypt_payload = MagicMock(side_effect=Exception())
    with pytest.raises(InternalServerError):
        stub_jwt_service.decrypt_payload(encrypted_payload='')


def test_decrypt_payload(
    get_new_stub_jwt_service
):
    stub_jwt_service = get_new_stub_jwt_service
    decrypted_payload = {"a": 1}
    stub_jwt_service.heimdall.decrypt_payload = MagicMock(return_value=decrypted_payload)
    assert stub_jwt_service.decrypt_payload(encrypted_payload='') == decrypted_payload

