# STANDARD LIBS
from datetime import datetime
import logging
from copy import deepcopy

# OUTSIDE LIBRARIES
from fastapi import status

# SPHINX
from src.controllers.jwts.controller import JwtController

from src.interfaces.services.user.interface import IUser

from src.services.authentications.service import AuthenticationService
from src.services.persephone.service import PersephoneService
from src.services.builders.user.onboarding_steps_builder import OnboardingStepBuilder

from src.repositories.file.enum.user_file import UserFileType
from src.repositories.file.repository import FileRepository
from src.repositories.user.repository import UserRepository

from src.domain.persephone_queue import PersephoneQueue
from src.services.sinacor.service import SinacorService

from src.utils.genarate_id import generate_id, hash_field
from src.utils.jwt_utils import JWTHandler
from src.utils.stone_age import StoneAge
from src.utils.persephone_templates import (
    get_prospect_user_template_with_data,
    get_user_signed_term_template_with_data,
)
from src.utils.env_config import config

from src.exceptions.exceptions import BadRequestError, InternalServerError


class UserService(IUser):
    @staticmethod
    def create(
        payload: dict,
        user_repository=UserRepository(),
        authentication_service=AuthenticationService,
        persephone_client=PersephoneService.get_client(),
    ) -> dict:
        payload = generate_id("email", payload, must_remove=False)
        has_pin = payload.get("pin")
        if has_pin:
            payload = hash_field(key="pin", payload=payload)
        if user_repository.find_one({"_id": payload.get("_id")}) is not None:
            raise BadRequestError("common.register_exists")
        payload.update({"created_at": datetime.now()})
        UserService.add_user_control_metadata(payload=payload)

        sent_to_persephone = persephone_client.run(
            topic=config("PERSEPHONE_TOPIC"),
            partition=PersephoneQueue.PROSPECT_USER_QUEUE.value,
            payload=get_prospect_user_template_with_data(payload=payload),
            schema_key="prospect_user_schema",
        )

        was_user_inserted = user_repository.insert(payload)

        if (sent_to_persephone and was_user_inserted) is False:
            raise InternalServerError("common.process_issue")
        authentication_service.send_authentication_email(
            email=payload.get("email"),
            payload=payload,
            ttl=10,
            body="email.body.created",
        )
        return {
            "status_code": status.HTTP_201_CREATED,
            "message_key": "user.created",
        }

    @staticmethod
    def create_admin(payload: dict) -> dict:
        payload.update({"is_admin": True})
        UserService.create(payload=payload)

    @staticmethod
    def update(payload: dict, user_repository=UserRepository()) -> None:
        pass

    @staticmethod
    def delete(
        payload: dict, user_repository=UserRepository(), token_handler=JWTHandler
    ) -> dict:
        old = user_repository.find_one({"_id": payload.get("email")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        new = deepcopy(old)
        new.update({"deleted": True})
        if user_repository.update_one(old=old, new=new) is False:
            raise InternalServerError("common.process_issue")

        jwt = token_handler.generate_token(payload=new, ttl=525600)
        JwtController.insert_one(jwt, new.get("email"))
        return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}

    @staticmethod
    def change_password(payload: dict, user_repository=UserRepository()) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        new_pin = payload.get("new_pin")
        old = user_repository.find_one({"_id": thebes_answer.get("email")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        new = deepcopy(old)
        new["pin"] = new_pin
        new = hash_field(key="pin", payload=new)
        if user_repository.update_one(old=old, new=new) is False:
            raise InternalServerError("common.process_issue")
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }

    @staticmethod
    def change_view(
        payload: dict, user_repository=UserRepository(), token_handler=JWTHandler
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        new_view = payload.get("new_view")
        old = user_repository.find_one({"_id": thebes_answer.get("email")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        new = deepcopy(old)
        new["scope"] = dict(old.get("scope"))
        new["scope"]["view_type"] = new_view
        if user_repository.update_one(old=old, new=new) is False:
            raise InternalServerError("common.unable_to_process")
        jwt = token_handler.generate_token(payload=new, ttl=525600)
        return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}

    @staticmethod
    def forgot_password(
        payload: dict,
        user_repository=UserRepository(),
        authentication_service=AuthenticationService,
    ):
        entity = user_repository.find_one({"_id": payload.get("email")})
        if entity is None:
            raise BadRequestError("common.register_not_exists")
        authentication_service.send_authentication_email(
            email=entity.get("email"),
            payload=entity,
            ttl=10,
            body="email.body.forgot_password",
        )
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "email.forgot_password",
        }

    @staticmethod
    def logout_all(payload: dict, user_repository=UserRepository()):
        old = user_repository.find_one({"_id": payload.get("email")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        new = deepcopy(old)
        new.update({"token_valid_after": datetime.now()})
        if user_repository.update_one(old=old, new=new) is False:
            raise InternalServerError("common.process_issue")
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "user.all_logged_out",
        }

    @staticmethod
    def add_feature(
        payload: dict, user_repository=UserRepository(), token_handler=JWTHandler
    ) -> dict:
        old = payload.get("x-thebes-answer")
        new = deepcopy(old)
        new_scope = new.get("scope")
        feature = payload.get("feature")
        if feature not in new_scope.get("features"):
            new_scope.get("features").append(payload.get("feature"))
            new.update({"scope": new_scope})
            if user_repository.update_one(old=old, new=new) is False:
                raise InternalServerError("common.process_issue")
            jwt = token_handler.generate_token(payload=new, ttl=525600)
            return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}
        jwt = token_handler.generate_token(payload=new, ttl=525600)
        return {
            "status_code": status.HTTP_304_NOT_MODIFIED,
            "payload": {"jwt": jwt},
        }

    @staticmethod
    def delete_feature(
        payload: dict, user_repository=UserRepository(), token_handler=JWTHandler
    ) -> dict:
        old = payload.get("x-thebes-answer")
        new = deepcopy(old)
        new_scope = new.get("scope")
        response = {"status_code": None, "payload": {"jwt": None}}
        if payload.get("feature") in new_scope.get("features"):
            new_scope.get("features").remove(payload.get("feature"))
            new.update({"scope": new_scope})
            if user_repository.update_one(old=old, new=new) is False:
                raise InternalServerError("common.process_issue")
            response.update({"status_code": status.HTTP_200_OK})
        else:
            response.update({"status_code": status.HTTP_304_NOT_MODIFIED})

        jwt = token_handler.generate_token(payload=new, ttl=525600)

        response.update({"jwt": jwt})

        return response

    @staticmethod
    def save_user_selfie(
        payload: dict,
        file_repository=FileRepository(bucket_name=config("AWS_BUCKET_USERS_SELF")),
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        file_repository.save_user_file(
            file_type=UserFileType.SELF,
            content=payload.get("file_or_base64"),
            user_email=thebes_answer.get("email"),
        )
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "files.uploaded",
        }

    @staticmethod
    def sign_term(
        payload: dict,
        file_repository=FileRepository(bucket_name=config("AWS_BUCKET_TERMS")),
        user_repository=UserRepository(),
        token_handler=JWTHandler,
        persephone_client=PersephoneService.get_client(),
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        old = user_repository.find_one({"_id": thebes_answer.get("email")})
        if type(old) is not dict:
            raise BadRequestError("common.register_not_exists")
        file_type = payload.get("file_type")
        new = deepcopy(old)
        UserService.fill_term_signed(
            payload=new,
            file_type=file_type.value,
            version=file_repository.get_current_term_version(file_type=file_type),
        )
        sent_to_persephone = persephone_client.run(
            topic=config("PERSEPHONE_TOPIC"),
            partition=PersephoneQueue.TERM_QUEUE.value,
            payload=get_user_signed_term_template_with_data(
                payload=new, file_type=file_type.value
            ),
            schema_key="term_schema",
        )
        if (
            sent_to_persephone and user_repository.update_one(old=old, new=new)
        ) is False:
            raise InternalServerError("common.unable_to_process")
        jwt = token_handler.generate_token(payload=new, ttl=525600)
        return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}

    @staticmethod
    def add_user_control_metadata(payload: dict):
        payload.update(
            {
                "scope": {"view_type": None, "features": []},
                "is_active": False,
                "deleted": False,
                "use_magic_link": True,
                "token_valid_after": datetime.utcnow(),
                "terms": {
                    # The terms list is available in the FileRepository
                    "term_application": None,
                    "term_open_account": None,
                    "term_retail_liquid_provider": None,
                    "term_refusal": None,
                    "term_non_compliance": None,
                },
                "can_be_managed_by_third_party_operator": False,
                "is_managed_by_third_party_operator": False,
                "third_party_operator": {
                    "is_third_party_operator": False,
                    "details": {},
                    "third_party_operator_email": "string",
                },
            }
        )

    @staticmethod
    def fill_term_signed(payload: dict, file_type: str, version: int):
        if payload.get("terms") is None:
            payload["terms"] = dict()
        payload["terms"][file_type] = {
            "version": version,
            "date": datetime.now(),
            "is_deprecated": False,
        }

    @staticmethod
    def get_signed_term(
        payload: dict,
        file_repository=FileRepository(bucket_name=config("AWS_BUCKET_TERMS")),
    ) -> dict:
        file_type = payload.get("file_type")
        try:
            version = (
                payload.get("x-thebes-answer")
                .get("terms")
                .get(file_type.value)
                .get("version")
            )
        except Exception:
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "user.files.term_not_signed",
            }
        try:
            link = file_repository.get_term_file_by_version(
                file_type=file_type, version=version
            )
            return {"status_code": status.HTTP_200_OK, "payload": {"link": link}}
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
            raise InternalServerError("common.process_issue")

    @staticmethod
    def user_identifier_data(
        payload: dict,
        user_repository=UserRepository(),
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        current_user = user_repository.find_one({"_id": thebes_answer.get("email")})
        if current_user is None:
            raise BadRequestError("common.register_not_exists")
        user_identifier_data = payload.get("user_identifier")

        current_user_with_identifier_data = dict(current_user)
        UserService.add_user_identifier_data_on_current_user(
            payload=current_user_with_identifier_data,
            user_identifier_data=user_identifier_data,
        )
        if (
            user_repository.update_one(
                old=current_user, new=current_user_with_identifier_data
            )
            is False
        ):
            raise InternalServerError("common.process_issue")
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }

    @staticmethod
    def add_user_identifier_data_on_current_user(
        payload: dict, user_identifier_data: dict
    ):
        payload["cpf"] = user_identifier_data.get("cpf")
        payload["cel_phone"] = user_identifier_data.get("cel_phone")

    @staticmethod
    def user_complementary_data(
        payload: dict,
        user_repository=UserRepository(),
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        current_user = user_repository.find_one({"_id": thebes_answer.get("email")})
        if current_user is None:
            raise BadRequestError("common.register_not_exists")
        user_complementary_data = payload.get("user_complementary")

        current_user_with_complementary_data = dict(current_user)
        UserService.add_user_complementary_data_on_current_user(
            payload=current_user_with_complementary_data,
            user_complementary_data=user_complementary_data,
        )

        if (
            user_repository.update_one(
                old=current_user, new=current_user_with_complementary_data
            )
            is False
        ):
            raise InternalServerError("common.process_issue")
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }

    @staticmethod
    def add_user_complementary_data_on_current_user(
        payload: dict, user_complementary_data
    ):
        payload["is_us_person"] = user_complementary_data.get("is_us_person")
        payload["us_tin"] = user_complementary_data.get("us_tin")
        payload["is_cvm_qualified_investor"] = user_complementary_data.get(
            "is_cvm_qualified_investor"
        )
        payload["marital"] = {
            "status": user_complementary_data.get("marital_status"),
            "spouse": user_complementary_data.get("spouse"),
        }

    @staticmethod
    def can_send_quiz(user_onboarding_current_step: dict):
        current_step = user_onboarding_current_step["payload"][
            "current_onboarding_step"
        ]
        quiz_step_or_finished = current_step not in ("user_quiz_step")
        all_necessary_steps = not all(
            [
                user_onboarding_current_step["payload"]["suitability_step"],
                user_onboarding_current_step["payload"]["user_identifier_data_step"],
                user_onboarding_current_step["payload"]["user_selfie_step"],
                user_onboarding_current_step["payload"]["user_complementary_step"],
            ]
        )
        return quiz_step_or_finished or all_necessary_steps

    @staticmethod
    def user_quiz(
        payload: dict, stone_age=StoneAge, user_repository=UserRepository()
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")

        user_onboarding_current_step = UserService.get_onboarding_user_current_step(
            payload=payload
        )
        if UserService.can_send_quiz(
            user_onboarding_current_step=user_onboarding_current_step
        ):
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "user.quiz.missing_steps",
            }

        current_user = user_repository.find_one({"_id": thebes_answer.get("email")})
        current_user_marital = current_user.get("marital")

        user_identifier_data = {
            "email": current_user.get("email"),
            "cpf": current_user.get("cpf"),
            "cel_phone": current_user.get("cel_phone"),
            "marital_status": current_user_marital.get("marital_status"),
            "is_us_person": current_user.get("is_us_person"),
        }

        current_user_is_us_person = current_user.get("is_us_person")

        if current_user_is_us_person:
            user_identifier_data["us_tin"] = current_user.get("us_tin")

        spouse = current_user_marital.get("spouse")

        if spouse is not None:
            user_identifier_data["spouse"] = spouse

        response = stone_age.get_user_quiz(user_identifier_data)

        output = response.get("output")
        stone_age_decision = output.get("decision")
        stone_age_contract_uuid = response.get("uuid")
        current_user_updated = deepcopy(current_user)
        current_user_updated.update(
            {"stone_age_contract_uuid": stone_age_contract_uuid}
        )

        if stone_age_decision is not None:
            current_user_updated.update({"stone_age_decision": stone_age_decision})

        if (
            user_repository.update_one(old=current_user, new=current_user_updated)
            is False
        ):
            raise InternalServerError("common.process_issue")

        return {"status_code": status.HTTP_200_OK, "payload": output}

    @staticmethod
    def change_user_to_client(
        payload: dict,
        user_repository=UserRepository(),
        stone_age=StoneAge,
        persephone_client=PersephoneService.get_client(),
    ) -> dict:

        thebes_answer = payload.get("x-thebes-answer")
        current_user = user_repository.find_one({"_id": thebes_answer.get("email")})
        if type(current_user) is not dict:
            raise BadRequestError("common.register_not_exists")

        is_dtvm_user_client = current_user.get("is_dtvm_user_client")

        if is_dtvm_user_client:
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "requests.not_modified",
            }

        stone_age_response = stone_age.send_user_quiz_responses(
            quiz=payload.get("quiz")
        )
        stone_age_decision = stone_age_response.get("decision")
        current_user_updated = deepcopy(current_user)
        if stone_age_decision is not None:
            current_user_updated.update({"stone_age_decision": stone_age_decision})
        current_user_updated.update({"is_dtvm_user_client": True})
        user_repository.update_one(old=current_user, new=current_user_updated)

        SinacorService.process_callback(
            payload=UserService.fake_stone_age_callback(
                email=thebes_answer.get("email")
            )
        )

        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "user.creating_account",
        }

    @staticmethod
    def fill_account_data_on_user_document(
        payload: dict, stone_age_user_data: dict, stone_age=StoneAge
    ):
        if payload.get("provided_by_bureaux") is None:
            payload["provided_by_bureaux"] = dict()
        for key, value in stone_age.get_only_values_from_user_data(
            user_data=stone_age_user_data
        ).items():
            payload["provided_by_bureaux"].update({key: value})
        payload["provided_by_bureaux"]["concluded_at"] = datetime.now()

    @staticmethod
    def get_onboarding_user_current_step(
        payload: dict,
        user_repository=UserRepository(),
        file_repository=FileRepository(bucket_name=config("AWS_BUCKET_USERS_SELF")),
        onboarding_step_builder=OnboardingStepBuilder(),
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        jwt_user_email = thebes_answer.get("email")

        user_file_exists = file_repository.get_user_file(
            file_type=UserFileType.SELF, user_email=jwt_user_email
        )

        current_user = user_repository.find_one({"_id": jwt_user_email})
        if current_user is None:
            raise BadRequestError("common.register_not_exists")

        user_suitability_profile = current_user.get("suitability")

        onboarding_steps = (
            onboarding_step_builder.user_suitability_step(
                user_suitability_profile=user_suitability_profile
            )
            .user_identifier_step(current_user=current_user)
            .user_selfie_step(user_file_exists=user_file_exists)
            .user_complementary_step(current_user=current_user)
            .user_user_electronic_signature(current_user=current_user)
            .user_quiz_step(current_user=current_user)
            .build()
        )

        return {"status_code": status.HTTP_200_OK, "payload": onboarding_steps}

    @staticmethod
    def set_user_electronic_signature(
        payload: dict, user_repository=UserRepository()
    ) -> dict:
        thebes_answer = payload.get("x-thebes-answer")
        electronic_signature = payload.get("electronic_signature")
        old = user_repository.find_one({"_id": thebes_answer.get("email")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        if old.get("electronic_signature"):
            raise BadRequestError("user.electronic_signature.already_set")
        new = deepcopy(old)
        new["electronic_signature"] = electronic_signature
        new = hash_field(key="electronic_signature", payload=new)
        if user_repository.update_one(old=old, new=new) is False:
            raise InternalServerError("common.process_issue")
        return {
            "status_code": status.HTTP_200_OK,
            "message_key": "requests.updated",
        }

    @staticmethod
    def fake_stone_age_callback(email: str):
        a = {
            "uuid": "21b00324-d240-4c61-a79c-9a0bd7ff6e45",
            "appName": "lionx",
            "version": "2",
            "successful": True,
            "output": {
                "decision": "APROVADO",
                "status": "OK",
                "connected_person": {"value": "N", "source": "PH3W"},
                "person_type": {"value": "F", "source": "PH3W"},
                "client_type": {"value": 1, "source": "PH3W"},
                "investor_type": {"value": 101, "source": "PH3W"},
                "cosif_tax_classification": {"value": 21, "source": "PH3W"},
                "gender": {"value": "M", "source": "PH3W"},
                "birth_date": {"value": 742446000, "source": "PH3W"},
                "birthplace": {
                    "nationality": {"value": 1, "source": "PH3W"},
                    "country": {"value": "BRA", "source": "PH3W"},
                    "state": {"value": "GO", "source": "PH3W"},
                    "city": {"value": "FORMOSA", "source": "PH3W"},
                    "id_city": {"value": 968, "source": "PH3W"},
                },
                "mother_name": {"value": "Antonia dos Santos Jr.", "source": "PH3W"},
                "identifier_document": {
                    "type": {"value": "CPF", "source": "PH3W"},
                    "document_data": {
                        "number": {"value": "13198487536", "source": "PH3W"},
                        "date": {"value": 1531423891, "source": "PH3W"},
                        "state": {"value": "SP", "source": "PH3W"},
                        "issuer": {"value": "SSP/SP", "source": "PH3W"},
                    },
                },
                "marital_update": {
                    "marital_regime": {"value": 1, "source": "PH3W"},
                    "spouse_birth_date": {"value": 742446000, "source": "PH3W"},
                },
                "address": {
                    "street_name": {"value": "R. 2", "source": "PH3W"},
                    "number": {"value": 126, "source": "PH3W"},
                    "neighborhood": {"value": "Formosinha", "source": "PH3W"},
                    "country": {"value": "BRA", "source": "PH3W"},
                    "state": {"value": "GO", "source": "PH3W"},
                    "city": {"value": "FORMOSA", "source": "PH3W"},
                    "id_city": {"value": 968, "source": "PH3W"},
                    "zip_code": {"value": 73813190, "source": "PH3W"},
                    "phone_number": {"value": "11952909954", "source": "PH3W"},
                },
                "occupation": {
                    "activity": {"value": 304, "source": "PH3W"},
                    "company": {
                        "name": {"value": "Tudo nosso .com.br", "source": "PH3W"},
                        "cpnj": {"value": "25811052000179", "source": "PH3W"},
                    },
                },
                "assets": {
                    "patrimony": {"value": 5446456.44, "source": "PH3W"},
                    "income": {"value": 5446456.44, "source": "PH3W"},
                    "date": {"value": 742446000, "source": "PH3W"},
                    "income_tax_type": {"value": 1, "source": "PH3W"},
                },
                "education": {
                    "level": {"value": "Médio incompleto", "source": "PH3W"},
                    "course": {"value": "Escola James Riwbon", "source": "PH3W"},
                },
                "politically_exposed_person": {
                    "is_politically_exposed_person": {"value": False, "source": "PH3W"}
                },
                "email": {"value": email, "source": "PH3W"},
                "name": {"value": "Antonio Armando Piaui", "source": "PH3W"},
                "cpf": {"value": "13198487536", "source": "PH3W"},
                "self_link": {"value": "http://self_user.jpg", "source": "PH3W"},
                "is_us_person": {"value": True, "source": "PH3W"},
                "us_tin": {"value": 126516515, "source": "PH3W"},
                "irs_sharing": {"value": True, "source": "PH3W"},
                "father_name": {"value": "Antonio dos Santos", "source": "PH3W"},
                "midia_person": {"value": False, "source": "PH3W"},
                "person_related_to_market_influencer": {
                    "value": False,
                    "source": "PH3W",
                },
                "court_orders": {"value": False, "source": "PH3W"},
                "lawsuits": {"value": False, "source": "PH3W"},
                "fund_admin_registration": {"value": False, "source": "PH3W"},
                "investment_fund_administrators_registration": {
                    "value": False,
                    "source": "PH3W",
                },
                "register_auditors_securities_commission": {
                    "value": False,
                    "source": "PH3W",
                },
                "registration_of_other_market_participants_securities_commission": {
                    "value": False,
                    "source": "PH3W",
                },
                "foreign_investors_register_of_annex_iv_not_reregistered": {
                    "value": False,
                    "source": "PH3W",
                },
                "registration_of_foreign_investors_securities_commission": {
                    "value": False,
                    "source": "PH3W",
                },
                "registration_representative_of_nonresident_investors_securities_commission": {
                    "value": False,
                    "source": "PH3W",
                },
                "date_of_acquisition": {"value": 1531423891, "source": "PH3W"},
            },
            "error": None,
        }
        return a
