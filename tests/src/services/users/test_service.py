import pytest
from unittest.mock import MagicMock
from fastapi import status

from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.utils.jwt_utils import JWTHandler
from src.services.users.service import UserService
from tests.stubby_classes.stubby_base_repository import StubbyBaseRepository
from src.repositories.file.repository import TermsFileType


class StubbyRepository(StubbyBaseRepository):
    pass


class StubbyAuthenticationService:
    pass


class StubbyAuthenticationService:
    pass


payload = {"name": "lala", "email": "Lala", "pin": 1234}


def test_create_register_exists():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={})
    with pytest.raises(BadRequestError, match="common.register_exists"):
        UserService.create(payload=payload, user_repository=stubby_repository)


def test_create_process_issue():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value=None)
    stubby_repository.insert = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        UserService.create(payload=payload, user_repository=stubby_repository)


def test_created():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value=None)
    stubby_repository.insert = MagicMock(return_value=True)
    StubbyAuthenticationService.send_authentication_email = MagicMock(return_value=True)
    response = UserService.create(
        payload=payload,
        user_repository=stubby_repository,
        authentication_service=StubbyAuthenticationService,
    )
    assert response.get("status_code") == status.HTTP_201_CREATED
    assert response.get("message_key") == "user.created"


payload_change_password = {"thebes_answer": {"email": "lalal"}, "new_pin": 1234}


def test_change_password_register_exists():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        UserService.change_password(
            payload=payload_change_password, user_repository=stubby_repository
        )


def test_change_password_process_issue():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={})
    stubby_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        UserService.change_password(
            payload=payload_change_password, user_repository=stubby_repository
        )


def test_change_password():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={})
    stubby_repository.update_one = MagicMock(return_value=True)
    response = UserService.change_password(
        payload=payload_change_password, user_repository=stubby_repository
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "requests.updated"


payload_change_view = {"thebes_answer": {"email": "lalal"}, "new_view": "lite"}


def test_change_view_register_exists():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        UserService.change_view(
            payload=payload_change_view, user_repository=stubby_repository
        )


def test_change_view_process_issue():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={"scope": {"view_type": ""}})
    stubby_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        UserService.change_view(
            payload=payload_change_view, user_repository=stubby_repository
        )


def test_change_view():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={"scope": {"view_type": ""}})
    stubby_repository.update_one = MagicMock(return_value=True)
    response = UserService.change_view(
        payload=payload_change_view, user_repository=stubby_repository
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert "jwt" in response.get("payload")


def test_delete_register_exists():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        UserService.delete(
            payload=payload_change_view, user_repository=stubby_repository
        )


def test_delete_process_issue():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={"scope": {"view_type": ""}})
    stubby_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        UserService.delete(
            payload=payload_change_view, user_repository=stubby_repository
        )


def test_delete():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={"scope": {"view_type": ""}})
    stubby_repository.update_one = MagicMock(return_value=True)
    response = UserService.delete(
        payload=payload_change_view, user_repository=stubby_repository
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "requests.updated"


def test_forgot_password_register_exists():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        UserService.change_password(
            payload=payload_change_password, user_repository=stubby_repository
        )


def test_forgot_password():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={})
    stubby_repository.update_one = MagicMock(return_value=True)
    StubbyAuthenticationService.send_authentication_email = MagicMock(return_value=True)
    response = UserService.forgot_password(
        payload=payload_change_password,
        user_repository=stubby_repository,
        authentication_service=StubbyAuthenticationService,
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "email.forgot_password"


def test_logout_all_not_register_exists():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        UserService.logout_all(
            payload=payload_change_password, user_repository=stubby_repository
        )


def test_logout_all_process_issue():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={"email": "lala"})
    stubby_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="common.process_issue"):
        UserService.logout_all(
            payload=payload_change_password, user_repository=stubby_repository
        )


def test_logout_all():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.find_one = MagicMock(return_value={"email": "lala"})
    stubby_repository.update_one = MagicMock(return_value=True)
    response = UserService.logout_all(
        payload=payload_change_password, user_repository=stubby_repository
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "user.all_logged_out"


user_data = {
    "email": "afl@lionx.com.br",
    "name": "anderson",
    "scope": {"view_type": None, "features": ["real_time_data"]},
    "is_active": True,
    "deleted": False,
    "use_magic_link": False,
    "token_valid_after": {"$date": "2021-05-29T20:00:52.571Z"},
}


def test_add_feature_already_exists():

    jwt = JWTHandler.generate_token(payload=user_data, ttl=525600)
    payload = {
        "thebes_answer": JWTHandler.decrypt_payload(jwt),
        "feature": "real_time_data",
    }
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.update_one = MagicMock(return_value=True)
    result = UserService.add_feature(
        payload=payload, user_repository=stubby_repository, token_handler=JWTHandler
    )
    assert result.get("status_code") == status.HTTP_304_NOT_MODIFIED


def test_add_feature():
    jwt = JWTHandler.generate_token(payload=user_data, ttl=525600)
    payload = {
        "thebes_answer": JWTHandler.decrypt_payload(jwt),
        "feature": "test_feature",
    }
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.update_one = MagicMock(return_value=True)
    result = UserService.add_feature(
        payload=payload, user_repository=stubby_repository, token_handler=JWTHandler
    )
    assert result.get("status_code") == status.HTTP_200_OK


def test_delete_feature_not_exists():
    jwt = JWTHandler.generate_token(payload=user_data, ttl=525600)
    payload = {
        "thebes_answer": JWTHandler.decrypt_payload(jwt),
        "feature": "test_feature",
    }
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.update_one = MagicMock(return_value=True)
    result = UserService.delete_feature(
        payload=payload, user_repository=stubby_repository, token_handler=JWTHandler
    )
    assert result.get("status_code") == status.HTTP_304_NOT_MODIFIED


def test_delete_feature_that_exists():
    jwt = JWTHandler.generate_token(payload=user_data, ttl=525600)
    payload = {
        "thebes_answer": JWTHandler.decrypt_payload(jwt),
        "feature": "real_time_data",
    }
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.update_one = MagicMock(return_value=True)
    result = UserService.delete_feature(
        payload=payload, user_repository=stubby_repository, token_handler=JWTHandler
    )
    assert result.get("status_code") == status.HTTP_200_OK


def test_save_user_self():
    stubby_repository = StubbyRepository(database="", collection="")
    stubby_repository.save_user_file = MagicMock(return_value=None)
    response = UserService.save_user_self(
        payload={"thebes_answer": {"email": "lala"}, "file_or_base64": ""},
        file_repository=stubby_repository,
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "files.uploaded"


def test_sign_term_register_not_exists():
    stubby_user_repository = StubbyRepository(database="", collection="")
    stubby_user_repository.find_one = MagicMock(return_value=None)
    stubby_file_repository = StubbyRepository(database="", collection="")
    with pytest.raises(BadRequestError, match="common.register_not_exists"):
        UserService.sign_term(
            payload={"thebes_answer": {"email": "lala"}},
            file_repository=stubby_file_repository,
            user_repository=stubby_user_repository,
        )


def test_sign_term_process_issue():
    stubby_user_repository = StubbyRepository(database="", collection="")
    stubby_user_repository.find_one = MagicMock(return_value={"email": "lala"})
    stubby_user_repository.update_one = MagicMock(return_value=False)
    stubby_file_repository = StubbyRepository(database="", collection="")
    stubby_file_repository.get_term_version = MagicMock(return_value=1)
    with pytest.raises(InternalServerError, match="common.process_issu"):
        UserService.sign_term(
            payload={
                "thebes_answer": {"email": "lala"},
                "file_type": TermsFileType.TERM_REFUSAL,
            },
            file_repository=stubby_file_repository,
            user_repository=stubby_user_repository,
        )


def test_sign_term():
    stubby_user_repository = StubbyRepository(database="", collection="")
    stubby_user_repository.find_one = MagicMock(return_value={"email": "lala"})
    stubby_user_repository.update_one = MagicMock(return_value=True)
    stubby_file_repository = StubbyRepository(database="", collection="")
    stubby_file_repository.get_term_version = MagicMock(return_value=1)
    response = UserService.sign_term(
        payload={
            "thebes_answer": {"email": "lala"},
            "file_type": TermsFileType.TERM_REFUSAL,
        },
        file_repository=stubby_file_repository,
        user_repository=stubby_user_repository,
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert type(response.get("payload").get("jwt")) == str


def test_get_signed_term_not_signed():
    payload = {"file_type": TermsFileType.TERM_REFUSAL}
    stubby_user_repository = StubbyRepository(database="", collection="")
    with pytest.raises(BadRequestError, match="user.files.term_not_signed"):
        UserService.get_signed_term(
            payload=payload, file_repository=stubby_user_repository
        )


def test_get_signed_term_not_signed():
    payload = {
        "file_type": TermsFileType.TERM_REFUSAL,
        "thebes_answer": {"terms": {"term_refusal": {"version": 1}}},
    }
    stubby_user_repository = StubbyRepository(database="", collection="")
    stubby_user_repository.get_term_file_by_version = MagicMock(return_value="lala")
    response = UserService.get_signed_term(
        payload=payload, file_repository=stubby_user_repository
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert type(response.get("payload").get("link")) == str


def test_get_signed_term_error():
    payload = {
        "file_type": TermsFileType.TERM_REFUSAL,
        "thebes_answer": {"terms": {"term_refusal": {"version": 1}}},
    }
    stubby_user_repository = StubbyRepository(database="", collection="")
    stubby_user_repository.get_term_file_by_version = MagicMock(
        side_effect=Exception(";)")
    )
    with pytest.raises(InternalServerError, match="common.process_issue"):
        UserService.get_signed_term(
            payload=payload, file_repository=stubby_user_repository
        )
