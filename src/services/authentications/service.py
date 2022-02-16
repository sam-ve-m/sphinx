# STANDARD LIBS
from copy import deepcopy

# OUTSIDE LIBRARIES
from fastapi import status


# SPHINX
from src.domain.sincad.client_sync_status import SincadClientImportStatus
from src.domain.solutiontech.client_import_status import SolutiontechClientImportStatus
from src.infrastructures.env_config import config
from src.services.email_builder.email import HtmlModifier
from src.repositories.user.repository import UserRepository
from src.controllers.jwts.controller import JwtController
from src.services.jwts.service import JwtService
from src.exceptions.exceptions import (
    BadRequestError,
    UnauthorizedError,
    InternalServerError,
)
from src.domain.persephone_queue.persephone_queue import PersephoneQueue
from src.services.persephone.service import PersephoneService
from src.i18n.i18n_resolver import i18nResolver as i18n
from src.services.email_sender.grid_email_sender import EmailSender as SendGridEmail
from src.domain.model_decorator.generate_id import hash_field
from src.core.interfaces.services.authentication.interface import IAuthentication
from src.repositories.client_register.repository import ClientRegisterRepository
from src.services.third_part_integration.solutiontech import Solutiontech
from src.services.persephone.templates.persephone_templates import (
    get_user_thebes_hall_schema_template_with_data,
    get_create_electronic_signature_session_schema_template_with_data,
    get_user_authentication_template_with_data,
    get_user_logout_template_with_data,
)
from src.services.builders.thebes_hall.builder import ThebesHallBuilder


class AuthenticationService(IAuthentication):
    @staticmethod
    def thebes_gate(
        thebes_answer_from_request_or_error: dict,
        user_repository=UserRepository(),
        token_service=JwtService,
        persephone_client=PersephoneService.get_client(),
    ) -> dict:
        user_data = user_repository.find_one(
            {"unique_id": thebes_answer_from_request_or_error.get("unique_id")}
        )
        if user_data is None:
            raise BadRequestError("common.register_not_exists")
        is_active_user = user_data.get("is_active_user")
        response = {"status_code": None, "payload": {"jwt": None}}
        response.update({"status_code": status.HTTP_200_OK})

        if not is_active_user:
            update_data = {
                "is_active_user": True,
                "must_do_first_login": False,
                "scope": {"view_type": "default", "features": ["default", "realtime"]},
            }
            if user_repository.update_one(old=user_data, new=update_data) is False:
                raise InternalServerError("common.process_issue")
            user_data.update(update_data)

        # TODO: BACK WITH THAT
        # sent_to_persephone = persephone_client.run(
        #     topic=config("PERSEPHONE_TOPIC_AUTHENTICATION"),
        #     partition=PersephoneQueue.USER_AUTHENTICATION.value,
        #     payload=get_user_authentication_template_with_data(payload=new_user_data),
        #     schema_key="user_authentication_schema",
        # )
        # if sent_to_persephone is False:
        #     raise InternalServerError("common.process_issue")

        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=user_data, ttl=525600
        ).build()

        jwt = token_service.generate_token(jwt_payload_data=jwt_payload_data)

        response.update({"payload": {"jwt": jwt, "control_data": control_data}})

        return response

    @staticmethod
    def login(
        user_credentials: dict,
        user_repository=UserRepository(),
        token_service=JwtService,
    ) -> dict:
        user_data = user_repository.find_one({"email": user_credentials["email"]})
        if user_data is None:
            raise BadRequestError("common.register_not_exists")

        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=user_data, ttl=10
        ).build()

        is_active_user = user_data["is_active_user"]
        must_do_first_login = user_data["must_do_first_login"]
        if must_do_first_login is False and is_active_user is False:
            raise UnauthorizedError("invalid_credential")

        # TODO: add PERSEPHONE HERE

        if user_data["use_magic_link"] is True:
            jwt = token_service.generate_token(jwt_payload_data=jwt_payload_data)
            AuthenticationService.send_authentication_email(
                email=user_data["email"],
                payload_jwt=jwt,
                body="email.body.created",
            )
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "email.login",
            }
        else:
            pin = user_credentials.get("pin")
            if pin is None:
                return {
                    "status_code": status.HTTP_200_OK,
                    "message_key": "user.need_pin",
                }
            if hash_field(payload=pin) != user_data["pin"]:
                raise UnauthorizedError("user.pin_error")

            jwt = token_service.generate_token(jwt_payload_data=jwt_payload_data)
            JwtController.insert_one(jwt, user_data["email"])
            return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}

    @staticmethod
    def send_authentication_email(
        email: str, payload_jwt: str, body: str, email_sender=SendGridEmail
    ) -> None:
        page = HtmlModifier(
            "src/services/asset",
            i18n.get_translate(key=body, locale="pt"),
            config("TARGET_LINK") + "/" + payload_jwt,
        )()
        email_sender.send_email_to(
            target_email=email,
            message=page,
            subject=i18n.get_translate(key="email.subject.created", locale="pt"),
        )

    @staticmethod
    def thebes_hall(
        device_and_thebes_answer_from_request: dict,
        user_repository=UserRepository(),
        token_service=JwtService,
        persephone_client=PersephoneService.get_client(),
    ) -> dict:
        x_thebes_answer = device_and_thebes_answer_from_request["x-thebes-answer"]
        user_data = user_repository.find_one(
            {"unique_id": x_thebes_answer["unique_id"]}
        )
        if user_data is None:
            raise BadRequestError("common.register_not_exists")

        br_third_part_synchronization_status = (
            AuthenticationService._dtvm_client_has_br_trade_allowed(user=user_data)
        )

        user_data_update = {}
        must_update = False
        for key, value in br_third_part_synchronization_status.items():
            if value["status_changed"]:
                must_update = True
                user_data_update.update({key: value["status"]})

        if must_update:
            if user_repository.update_one(old=user_data, new=user_data_update) is False:
                raise InternalServerError("common.process_issue")
            user_data.update(user_data_update)

        jwt_payload_data, control_data = ThebesHallBuilder(
            user_data=user_data, ttl=525600
        ).build()
        jwt = token_service.generate_token(jwt_payload_data=jwt_payload_data)

        # TODO: BACK WITH THAT
        # sent_to_persephone = persephone_client.run(
        #     topic=config("PERSEPHONE_TOPIC_AUTHENTICATION"),
        #     partition=PersephoneQueue.USER_THEBES_HALL.value,
        #     payload=get_user_thebes_hall_schema_template_with_data(
        #         email=device_and_thebes_answer_from_request.get("email"),
        #         jwt=jwt,
        #         has_trade_allowed=client_has_trade_allowed,
        #         device_information=device_and_thebes_answer_from_request.get(
        #             "device_information"
        #         ),
        #     ),
        #     schema_key="user_thebes_hall_schema",
        # )
        # if sent_to_persephone is False:
        #     raise InternalServerError("common.process_issue")

        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"jwt": jwt, "control_data": control_data},
        }

    @staticmethod
    def _dtvm_client_has_br_trade_allowed(
        user: dict,
        client_register_repository=ClientRegisterRepository(),
        solutiontech=Solutiontech,
    ) -> dict:

        user_solutiontech_status_from_database = user.get("solutiontech")
        user_sincad_status_from_database = user.get("sincad")
        user_sinacor_status_from_database = user.get("sinacor")
        user_bmf_account_from_database = user.get("bmf_account")
        user_cpf_from_database = user.get("identifier_document", {}).get("cpf")

        if not all(
            [
                user_solutiontech_status_from_database,
                user_sincad_status_from_database,
                user_sinacor_status_from_database,
                user_bmf_account_from_database,
                user_cpf_from_database,
            ]
        ):
            return {}

        client_map_requirements_to_allow_trade_from_database = AuthenticationService._get_client_map_requirements_to_allow_trade(
            user_solutiontech_status_from_database=user_solutiontech_status_from_database,
            user_sincad_status_from_database=user_sincad_status_from_database,
            user_sinacor_status_from_database=user_sinacor_status_from_database
        )

        user_has_valid_solutiontech_status_in_database = AuthenticationService._check_if_user_has_valid_solutiontech_status_in_database(
            user_solutiontech_status_from_database=user_solutiontech_status_from_database)

        if user_has_valid_solutiontech_status_in_database:
            user_solutiontech_status_from_check_status_request = solutiontech.check_if_client_is_synced_with_solutiontech(
                user_bmf_code=int(user_bmf_account_from_database),
                user_solutiontech_status_from_database=user_solutiontech_status_from_database,
            )

            client_map_requirements_to_allow_trade_from_database = AuthenticationService._update_client_has_trade_allowed_status_with_solutiontech_status_response(
                client_map_requirements_to_allow_trade_from_database=client_map_requirements_to_allow_trade_from_database,
                user_solutiontech_status_from_database=user_solutiontech_status_from_database,
                user_solutiontech_status_from_check_status_request=user_solutiontech_status_from_check_status_request
            )

        user_is_not_already_sync_with_sincad = (
            user_sincad_status_from_database
            is SincadClientImportStatus.NOT_SYNCED.value
        )
        if user_is_not_already_sync_with_sincad:
            sincad_status_from_sinacor = (
                AuthenticationService.sinacor_is_synced_with_sincad(
                    user_cpf=user_cpf_from_database,
                    client_register_repository=client_register_repository,
                )
            )

            AuthenticationService._update_client_has_trade_allowed_status_with_sincad_status_response(
                client_has_trade_allowed_status_with_database_user=client_map_requirements_to_allow_trade_from_database,
                sincad_status_from_sinacor=sincad_status_from_sinacor,
                user_sincad_status_from_database=user_sincad_status_from_database,
            )

        sinacor_status_from_sinacor = AuthenticationService.client_sinacor_is_blocked(
            user_cpf=user_cpf_from_database,
            client_register_repository=client_register_repository,
        )

        AuthenticationService._update_client_has_trade_allowed_status_with_sinacor_status_response(
            client_has_trade_allowed_status_with_database_user=client_map_requirements_to_allow_trade_from_database,
            sinacor_status_from_sinacor=sinacor_status_from_sinacor,
            user_sinacor_status_from_database=user_sinacor_status_from_database,
        )

        return client_map_requirements_to_allow_trade_from_database

    @staticmethod
    def _get_client_map_requirements_to_allow_trade(
        user_solutiontech_status_from_database: str,
        user_sincad_status_from_database: bool,
        user_sinacor_status_from_database: bool,
    ):
        client_has_trade_allowed_status_with_database_user = {
            "solutiontech": {
                "status": user_solutiontech_status_from_database,
                "status_changed": False,
            },
            "sincad": {
                "status": user_sincad_status_from_database,
                "status_changed": False,
            },
            "sinacor": {
                "status": user_sinacor_status_from_database,
                "status_changed": False,
            },
        }

        return client_has_trade_allowed_status_with_database_user

    @staticmethod
    def _update_client_has_trade_allowed_status_with_solutiontech_status_response(
        client_map_requirements_to_allow_trade_from_database: dict,
        user_solutiontech_status_from_database: str,
        user_solutiontech_status_from_check_status_request: str,
    ):

        solutiontech_status_changed = (
            user_solutiontech_status_from_database
            != user_solutiontech_status_from_check_status_request
        )

        client_map_requirements_to_allow_trade_from_database["solutiontech"][
            "status"
        ] = user_solutiontech_status_from_check_status_request
        client_map_requirements_to_allow_trade_from_database["solutiontech"][
            "status_changed"
        ] = solutiontech_status_changed

        return client_map_requirements_to_allow_trade_from_database

    @staticmethod
    def _update_client_has_trade_allowed_status_with_sincad_status_response(
        client_has_trade_allowed_status_with_database_user: dict,
        sincad_status_from_sinacor: bool,
        user_sincad_status_from_database: bool,
    ):

        sincad_status_changed = (
            user_sincad_status_from_database != sincad_status_from_sinacor
        )
        client_has_trade_allowed_status_with_database_user["sincad"][
            "status"
        ] = sincad_status_from_sinacor
        client_has_trade_allowed_status_with_database_user["sincad"][
            "status_changed"
        ] = sincad_status_changed

        return client_has_trade_allowed_status_with_database_user

    @staticmethod
    def _update_client_has_trade_allowed_status_with_sinacor_status_response(
        client_has_trade_allowed_status_with_database_user: dict,
        sinacor_status_from_sinacor: bool,
        user_sinacor_status_from_database: bool,
    ):

        sincad_status_changed = (
            user_sinacor_status_from_database != sinacor_status_from_sinacor
        )
        client_has_trade_allowed_status_with_database_user["sinacor"][
            "status"
        ] = sinacor_status_from_sinacor
        client_has_trade_allowed_status_with_database_user["sinacor"][
            "status_changed"
        ] = sincad_status_changed

        return client_has_trade_allowed_status_with_database_user

    @staticmethod
    def _check_if_user_has_valid_solutiontech_status_in_database(
        user_solutiontech_status_from_database: str,
    ):
        user_has_valid_solutiontech_status_in_database = (
            user_solutiontech_status_from_database
            in [
                SolutiontechClientImportStatus.SEND.value,
                SolutiontechClientImportStatus.FAILED.value,
            ]
        )
        return user_has_valid_solutiontech_status_in_database

    @staticmethod
    def sinacor_is_synced_with_sincad(
        user_cpf: int, client_register_repository=ClientRegisterRepository()
    ) -> bool:
        sincad_status = client_register_repository.get_sincad_status(user_cpf=user_cpf)
        return sincad_status and sincad_status[0] in ["ACE", "ECM"]

    @staticmethod
    def client_sinacor_is_blocked(
        user_cpf: int, client_register_repository=ClientRegisterRepository()
    ) -> bool:
        sincad_status = client_register_repository.get_sinacor_status(user_cpf=user_cpf)
        return sincad_status and sincad_status[0] in ["A"]

    @staticmethod
    def create_electronic_signature_jwt(
        change_electronic_signature_request: dict,
        persephone_client=PersephoneService.get_client(),
        jwt_service=JwtService,
    ):
        jwt_mist_session = None
        allowed = None
        try:
            jwt_mist_session = jwt_service.generate_session_jwt(
                change_electronic_signature_request["electronic_signature"],
                change_electronic_signature_request["email"],
            )
            allowed = True
        except BaseException as e:
            allowed = False
            raise e
        finally:
            sent_to_persephone = persephone_client.run(
                topic=config("PERSEPHONE_TOPIC_USER"),
                partition=PersephoneQueue.USER_ELECTRONIC_SIGNATURE_SESSION.value,
                payload=get_create_electronic_signature_session_schema_template_with_data(
                    email=change_electronic_signature_request["email"],
                    mist_session=jwt_mist_session,
                    allowed=allowed,
                ),
                schema_key="create_electronic_signature_session_schema",
            )
            if sent_to_persephone is False:
                raise InternalServerError("common.process_issue")
        return {
            "status_code": status.HTTP_200_OK,
            "payload": jwt_mist_session,
        }

    @staticmethod
    def logout(
        device_jwt_and_thebes_answer_from_request: dict,
        persephone_client=PersephoneService.get_client(),
    ) -> dict:
        sent_to_persephone = persephone_client.run(
            topic=config("PERSEPHONE_TOPIC_AUTHENTICATION"),
            partition=PersephoneQueue.USER_LOGOUT.value,
            payload=get_user_logout_template_with_data(
                jwt=device_jwt_and_thebes_answer_from_request["jwt"],
                email=device_jwt_and_thebes_answer_from_request["email"],
                device_information=device_jwt_and_thebes_answer_from_request[
                    "device_information"
                ],
            ),
            schema_key="user_logout_schema",
        )
        if sent_to_persephone is False:
            raise InternalServerError("common.process_issue")

        return {"status_code": status.HTTP_200_OK, "message_key": "email.logout"}
