# OUTSIDE LIBRARIES
import pytest
from unittest.mock import MagicMock, patch
from fastapi import status

# SPHINX
from src.exceptions.exceptions import BadRequestError, InternalServerError
from src.services.users.service import UserService
from tests.stub_classes.stub_base_repository import StubBaseRepository
from src.repositories.file.repository import TermsFileType


class StubRepository(StubBaseRepository):
    pass


class StubAuthenticationService:
    pass


class StubAuthenticationService:
    pass


class StubPersephoneClient:
    pass


class StubJWTHandler:
    pass


payload = {"name": "lala", "email": "Lala", "pin": 1234}


def test_create_register_exists():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={})
    with pytest.raises(BadRequestError, match="^common.register_exists"):
        UserService.create(payload=payload, user_repository=stub_repository)


def test_create_process_issue():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    stub_repository.insert = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        UserService.create(payload=payload, user_repository=stub_repository)


def test_created():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    stub_repository.insert = MagicMock(return_value=True)
    stub_authentication_service = StubAuthenticationService()
    stub_authentication_service.send_authentication_email = MagicMock(return_value=True)
    stub_persephone_client = StubPersephoneClient()
    stub_persephone_client.run = MagicMock(return_value=True)
    response = UserService.create(
        payload=payload,
        user_repository=stub_repository,
        authentication_service=stub_authentication_service,
        persephone_client=stub_persephone_client,
    )
    assert response.get("status_code") == status.HTTP_201_CREATED
    assert response.get("message_key") == "user.created"


payload_change_password = {"thebes_answer": {"email": "lalal"}, "new_pin": 1234}


def test_change_password_register_exists():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="^common.register_not_exists"):
        UserService.change_password(
            payload=payload_change_password, user_repository=stub_repository
        )


def test_change_password_process_issue():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={})
    stub_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        UserService.change_password(
            payload=payload_change_password, user_repository=stub_repository
        )


def test_change_password():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={})
    stub_repository.update_one = MagicMock(return_value=True)
    response = UserService.change_password(
        payload=payload_change_password, user_repository=stub_repository
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "requests.updated"


payload_change_view = {"thebes_answer": {"email": "lalal"}, "new_view": "lite"}


def test_change_view_register_exists():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="^common.register_not_exists"):
        UserService.change_view(
            payload=payload_change_view, user_repository=stub_repository
        )


def test_change_view_process_issue():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={"scope": {"view_type": ""}})
    stub_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="^common.unable_to_process"):
        UserService.change_view(
            payload=payload_change_view, user_repository=stub_repository
        )


def test_change_view():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={"scope": {"view_type": ""}})
    stub_repository.update_one = MagicMock(return_value=True)
    stub_jwt_handler = StubJWTHandler()
    stub_jwt_handler.generate_token = MagicMock(return_value="toaskjdg1.233213.123123")
    response = UserService.change_view(
        payload=payload_change_view,
        user_repository=stub_repository,
        token_handler=stub_jwt_handler,
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert "jwt" in response.get("payload")
    assert type(response.get("payload").get("jwt")) == str


def test_delete_register_exists():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="^common.register_not_exists"):
        UserService.delete(payload=payload_change_view, user_repository=stub_repository)


def test_delete_process_issue():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={"scope": {"view_type": ""}})
    stub_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        UserService.delete(payload=payload_change_view, user_repository=stub_repository)


def test_delete():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={"scope": {"view_type": ""}})
    stub_repository.update_one = MagicMock(return_value=True)
    response = UserService.delete(
        payload=payload_change_view, user_repository=stub_repository
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "requests.updated"


def test_forgot_password_register_exists():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="^common.register_not_exists"):
        UserService.change_password(
            payload=payload_change_password, user_repository=stub_repository
        )


def test_forgot_password():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={})
    stub_repository.update_one = MagicMock(return_value=True)
    StubAuthenticationService.send_authentication_email = MagicMock(return_value=True)
    response = UserService.forgot_password(
        payload=payload_change_password,
        user_repository=stub_repository,
        authentication_service=StubAuthenticationService,
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "email.forgot_password"


def test_logout_all_not_register_exists():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="^common.register_not_exists"):
        UserService.logout_all(
            payload=payload_change_password, user_repository=stub_repository
        )


def test_logout_all_process_issue():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={"email": "lala"})
    stub_repository.update_one = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        UserService.logout_all(
            payload=payload_change_password, user_repository=stub_repository
        )


def test_logout_all():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.find_one = MagicMock(return_value={"email": "lala"})
    stub_repository.update_one = MagicMock(return_value=True)
    response = UserService.logout_all(
        payload=payload_change_password, user_repository=stub_repository
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
    payload = {
        "thebes_answer": user_data,
        "feature": "real_time_data",
    }
    stub_jwt_handler = StubJWTHandler()
    stub_jwt_handler.generate_token = MagicMock(return_value=user_data)
    stub_repository = StubRepository(database="", collection="")
    stub_repository.update_one = MagicMock(return_value=True)
    result = UserService.add_feature(
        payload=payload, user_repository=stub_repository, token_handler=stub_jwt_handler
    )
    assert result.get("status_code") == status.HTTP_304_NOT_MODIFIED


def test_add_feature_process_issue():
    copy = dict(user_data)
    copy.update({"view_type": None, "features": []},)
    payload = {
        "thebes_answer": copy,
        "feature": "real_time_data",
    }
    stub_jwt_handler = StubJWTHandler()
    stub_jwt_handler.generate_token = MagicMock(return_value=user_data)
    stub_repository = StubRepository(database="", collection="")
    stub_repository.update_one = MagicMock(return_value=True)
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        UserService.add_feature(
            payload=payload, user_repository=stub_repository, token_handler=stub_jwt_handler
        )

def test_add_feature():
    payload = {
        "thebes_answer": user_data,
        "feature": "test_feature",
    }
    stub_jwt_handler = StubJWTHandler()
    stub_jwt_handler.generate_token = MagicMock(
        return_value="jkasdh71283.12938712.1029873912"
    )
    stub_repository = StubRepository(database="", collection="")
    stub_repository.update_one = MagicMock(return_value=True)
    result = UserService.add_feature(
        payload=payload, user_repository=stub_repository, token_handler=stub_jwt_handler
    )
    assert result.get("status_code") == status.HTTP_200_OK
    assert type(result.get("payload").get("jwt")) == str


def test_delete_feature_not_exists():
    payload = {
        "thebes_answer": user_data,
        "feature": "test_feature_xxx",
    }
    stub_repository = StubRepository(database="", collection="")
    stub_repository.update_one = MagicMock(return_value=False)
    stub_jwt_handler = StubJWTHandler()
    stub_jwt_handler.generate_token = MagicMock(return_value=user_data)
    result = UserService.delete_feature(
        payload=payload, user_repository=stub_repository, token_handler=stub_jwt_handler
    )
    assert result.get("status_code") == status.HTTP_304_NOT_MODIFIED


def test_delete_feature_that_exists():
    payload = {
        "thebes_answer": user_data,
        "feature": "real_time_data",
    }
    stub_jwt_handler = StubJWTHandler()
    stub_jwt_handler.generate_token = MagicMock(
        return_value="asdkjash761.asd98y7139.123y7129h"
    )
    stub_repository = StubRepository(database="", collection="")
    stub_repository.update_one = MagicMock(return_value=True)
    result = UserService.delete_feature(
        payload=payload, user_repository=stub_repository, token_handler=stub_jwt_handler
    )
    assert result.get("status_code") == status.HTTP_200_OK
    assert type(result.get("payload").get("jwt")) == str


def test_save_user_self():
    stub_repository = StubRepository(database="", collection="")
    stub_repository.save_user_file = MagicMock(return_value=None)
    response = UserService.save_user_self(
        payload={"thebes_answer": {"email": "lala"}, "file_or_base64": ""},
        file_repository=stub_repository,
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "files.uploaded"


def test_sign_term_register_not_exists():
    stub_user_repository = StubRepository(database="", collection="")
    stub_user_repository.find_one = MagicMock(return_value=None)
    stub_file_repository = StubRepository(database="", collection="")
    with pytest.raises(BadRequestError, match="^common.register_not_exists"):
        UserService.sign_term(
            payload={"thebes_answer": {"email": "lala"}},
            file_repository=stub_file_repository,
            user_repository=stub_user_repository,
        )


def test_sign_term_process_issue():
    stub_user_repository = StubRepository(database="", collection="")
    stub_user_repository.find_one = MagicMock(return_value={"email": "lala"})
    stub_user_repository.update_one = MagicMock(return_value=False)
    stub_file_repository = StubRepository(database="", collection="")
    stub_file_repository.get_term_version = MagicMock(return_value=1)
    with pytest.raises(InternalServerError, match="^common.unable_to_process"):
        UserService.sign_term(
            payload={
                "thebes_answer": {"email": "lala"},
                "file_type": TermsFileType.TERM_REFUSAL,
            },
            file_repository=stub_file_repository,
            user_repository=stub_user_repository,
        )


def test_sign_term_process_issue_v2():
    stub_user_repository = StubRepository(database="", collection="")
    stub_user_repository.find_one = MagicMock(return_value={"email": "lala"})
    stub_user_repository.update_one = MagicMock(return_value=False)
    stub_file_repository = StubRepository(database="", collection="")
    stub_file_repository.get_term_version = MagicMock(return_value=1)
    StubPersephoneClient.run = MagicMock(return_value=True)
    with pytest.raises(InternalServerError, match="^common.unable_to_process"):
        UserService.sign_term(
            payload={
                "thebes_answer": {"email": "lala"},
                "file_type": TermsFileType.TERM_REFUSAL,
            },
            file_repository=stub_file_repository,
            user_repository=stub_user_repository,
            persephone_client=StubPersephoneClient,
        )


def test_sign_term():
    stub_user_repository = StubRepository(database="", collection="")
    stub_user_repository.find_one = MagicMock(return_value={"email": "lala"})
    stub_user_repository.update_one = MagicMock(return_value=True)

    stub_file_repository = StubRepository(database="", collection="")
    stub_file_repository.get_term_version = MagicMock(return_value=1)

    StubPersephoneClient.run = MagicMock(return_value=True)
    stub_jwt_handler = StubJWTHandler()
    stub_jwt_handler.generate_token = MagicMock(return_value=user_data)
    response = UserService.sign_term(
        payload={
            "thebes_answer": {"email": "lala"},
            "file_type": TermsFileType.TERM_REFUSAL,
        },
        file_repository=stub_file_repository,
        user_repository=stub_user_repository,
        token_handler=stub_jwt_handler,
        persephone_client=StubPersephoneClient,
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("payload").get("jwt") == user_data


def test_get_signed_term_not_signed():
    payload = {"file_type": TermsFileType.TERM_REFUSAL}
    stub_user_repository = StubRepository(database="", collection="")
    with pytest.raises(BadRequestError, match="^user.files.term_not_signed"):
        UserService.get_signed_term(
            payload=payload, file_repository=stub_user_repository
        )


def test_get_signed_term_not_signed():
    payload = {
        "file_type": TermsFileType.TERM_REFUSAL,
        "thebes_answer": {"terms": {"term_refusal": {"version": 1}}},
    }
    stub_user_repository = StubRepository(database="", collection="")
    stub_user_repository.get_term_file_by_version = MagicMock(return_value="lala")
    response = UserService.get_signed_term(
        payload=payload, file_repository=stub_user_repository
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert type(response.get("payload").get("link")) == str


def test_get_signed_term_error():
    payload = {
        "file_type": TermsFileType.TERM_REFUSAL,
        "thebes_answer": {"terms": {"term_refusal": {"version": 1}}},
    }
    stub_user_repository = StubRepository(database="", collection="")
    stub_user_repository.get_term_file_by_version = MagicMock(
        side_effect=Exception(";)")
    )
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        UserService.get_signed_term(
            payload=payload, file_repository=stub_user_repository
        )


payload_user_identifier_data = {
    "user_identifier": {"cpf": 12345678912},
    "thebes_answer": {"email": "email@net.com"},
}


class StubStoneAge:
    pass


def test_user_identifier_data_register_not_exists():
    stub_user_repository = StubRepository(database="", collection="")
    stub_user_repository.find_one = MagicMock(return_value=None)
    StubStoneAge.send_user_identifier_data = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="^common.register_not_exists"):
        UserService.user_identifier_data(
            payload=payload_user_identifier_data,
            user_repository=stub_user_repository,
            stone_age=StubStoneAge,
        )


def test_user_identifier_data_process_issue_v1():
    stub_user_repository = StubRepository(database="", collection="")
    stub_user_repository.find_one = MagicMock(return_value={"la": "la"})
    stub_user_repository.update_one = MagicMock(return_value=False)
    StubStoneAge.send_user_identifier_data = MagicMock(return_value=None)
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        UserService.user_identifier_data(
            payload=payload_user_identifier_data,
            user_repository=stub_user_repository,
            stone_age=StubStoneAge,
        )


def test_user_identifier_data_process_issue_v2():
    stub_user_repository = StubRepository(database="", collection="")
    stub_user_repository.find_one = MagicMock(return_value={"la": "la"})
    stub_user_repository.update_one = MagicMock(return_value=False)
    StubStoneAge.send_user_identifier_data = MagicMock(return_value={"a": 123})
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        UserService.user_identifier_data(
            payload=payload_user_identifier_data,
            user_repository=stub_user_repository,
            stone_age=StubStoneAge,
        )


def test_user_identifier_data():
    stub_user_repository = StubRepository(database="", collection="")
    stub_user_repository.find_one = MagicMock(return_value={"la": "la"})
    StubStoneAge.send_user_identifier_data = MagicMock(return_value={"a": 123})
    stub_user_repository.update_one = MagicMock(return_value=True)
    response = UserService.user_identifier_data(
        payload=payload_user_identifier_data,
        user_repository=stub_user_repository,
        stone_age=StubStoneAge,
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert type(response.get("payload").get("quiz")) == dict


class StubPersephoneClient:
    pass


def test_user_quiz_responses_register_not_exists():
    stub_user_repository = StubRepository(database="", collection="")
    stub_user_repository.find_one = MagicMock(return_value=None)
    StubStoneAge.send_user_quiz_responses = MagicMock(return_value=None)
    with pytest.raises(BadRequestError, match="^common.register_not_exists"):
        UserService.fill_user_data(
            payload=payload_user_identifier_data,
            user_repository=stub_user_repository,
            stone_age=StubStoneAge,
            persephone_client=StubPersephoneClient,
        )


@patch(
    "src.services.users.service.get_user_account_template_with_data",
    MagicMock(return_value={}),
)
def test_user_quiz_responses_process_issue_v1():
    stub_user_repository = StubRepository(database="", collection="")
    stub_user_repository.find_one = MagicMock(return_value={"la": "la"})
    StubStoneAge.send_user_quiz_responses = MagicMock(return_value=None)
    StubPersephoneClient.run = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        UserService.fill_user_data(
            payload=payload_user_identifier_data,
            user_repository=stub_user_repository,
            stone_age=StubStoneAge,
            persephone_client=StubPersephoneClient,
        )


@patch(
    "src.services.users.service.get_user_account_template_with_data",
    MagicMock(return_value={}),
)
def test_user_quiz_responses_process_issue_v2():
    stub_user_repository = StubRepository(database="", collection="")
    stub_user_repository.find_one = MagicMock(
        return_value={"user_account_data": {"data": "lalal"}}
    )
    stub_user_repository.update_one = MagicMock(return_value=False)
    StubStoneAge.send_user_quiz_responses = MagicMock(return_value=None)
    StubPersephoneClient.run = MagicMock(return_value=False)
    with pytest.raises(InternalServerError, match="^common.process_issue"):
        UserService.fill_user_data(
            payload=payload_user_identifier_data,
            user_repository=stub_user_repository,
            stone_age=StubStoneAge,
            persephone_client=StubPersephoneClient,
        )


@patch(
    "src.services.users.service.get_user_account_template_with_data",
    MagicMock(return_value={}),
)
def test_user_quiz_responses():
    stub_user_repository = StubRepository(database="", collection="")
    stub_user_repository.find_one = MagicMock(
        return_value={"user_account_data": {"data": "lalal"}}
    )
    stub_user_repository.update_one = MagicMock(return_value=True)
    StubPersephoneClient.run = MagicMock(return_value=True)
    stone_age = StubStoneAge()
    stone_age.send_user_quiz_responses = MagicMock(return_value={})
    response = UserService.fill_user_data(
        payload=payload_user_identifier_data,
        user_repository=stub_user_repository,
        stone_age=stone_age,
        persephone_client=StubPersephoneClient,
    )
    assert response.get("status_code") == status.HTTP_200_OK
    assert response.get("message_key") == "user.creating_account"


def test_fill_term_signed_empty_terms_on_payload():
    payload = dict()
    UserService.fill_term_signed(payload=payload, file_type="xxx", version=1)
    assert type(payload.get("terms")) == dict
    assert len(payload.get("terms")) == 1
    assert type(payload.get("terms").get("xxx")) == dict
    assert payload.get("terms").get("xxx").get("version") == 1
    assert payload.get("terms").get("xxx").get("is_deprecated") is False


def test_fill_term_signed_filled_terms_on_payload():
    payload = {"terms": {"aaa": {"version": 2, "date": None, "is_deprecated": False,}}}
    UserService.fill_term_signed(payload=payload, file_type="xxx", version=1)
    assert type(payload.get("terms")) == dict
    assert len(payload.get("terms")) == 2


def test_fill_account_data_on_user_document_without_provided_by_bureaux_field():
    payload = dict()
    stone_age_user_data = {"name": {"source": "test", "value": "Nome completo"}}
    UserService.fill_account_data_on_user_document(
        payload=payload, stone_age_user_data=stone_age_user_data
    )
    assert payload.get('provided_by_bureaux').get('name') == "Nome completo"


def test_fill_account_data_on_user_document_with_provided_by_bureaux_field():
    payload = {'provided_by_bureaux': {'year': 2012}}
    stone_age_user_data = {"name": {"source": "test", "value": "Nome completo"}}
    UserService.fill_account_data_on_user_document(
        payload=payload, stone_age_user_data=stone_age_user_data
    )
    assert payload.get('provided_by_bureaux').get('year') == 2012
