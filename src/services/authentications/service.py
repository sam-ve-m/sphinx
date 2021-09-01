# STANDARD LIBS
from copy import deepcopy

# OUTSIDE LIBRARIES
from fastapi import status

from src.domain.sincad.client_sync_status import SincadClientImportStatus
from src.domain.solutiontech.client_import_status import SolutiontechClientImportStatus
from src.utils.env_config import config

# SPHINX
from src.utils.email import HtmlModifier
from src.repositories.user.repository import UserRepository
from src.controllers.jwts.controller import JwtController
from src.utils.jwt_utils import JWTHandler
from src.exceptions.exceptions import (
    BadRequestError,
    UnauthorizedError,
    InternalServerError,
)
from src.i18n.i18n_resolver import i18nResolver as i18n
from src.services.email_sender.grid_email_sender import EmailSender as SendGridEmail
from src.utils.genarate_id import hash_field
from src.interfaces.services.authentication.interface import IAuthentication
from src.repositories.client_register.repository import ClientRegisterRepository
from src.utils.solutiontech import Solutiontech


class AuthenticationService(IAuthentication):
    @staticmethod
    def thebes_gate(
        payload: dict, user_repository=UserRepository(), token_handler=JWTHandler
    ) -> dict:
        old = user_repository.find_one({"_id": payload.get("email")})
        if old is None:
            raise BadRequestError("common.register_not_exists")
        new = deepcopy(old)
        is_active_user = old.get("is_active_user")
        response = {"status_code": None, "payload": {"jwt": None}}
        response.update({"status_code": status.HTTP_200_OK})

        if not is_active_user:
            new.update(
                {
                    "is_active_user": True,
                    "scope": {"view_type": "default", "features": ["default"]},
                }
            )
            if user_repository.update_one(old=old, new=new) is False:
                raise InternalServerError("common.process_issue")

        jwt = token_handler.generate_token(payload=new, ttl=525600)

        response.update({"payload": {"jwt": jwt}})

        return response

    @staticmethod
    def login(
        payload: dict, user_repository=UserRepository(), token_handler=JWTHandler
    ) -> dict:
        entity = user_repository.find_one({"_id": payload.get("email")})
        if entity is None:
            raise BadRequestError("common.register_not_exists")
        ########################################################################### ADICIONAR ESSA VERIFICAÇAO QUANDO DELETAR USUARIO/CLIENTE ####################################################################
        # if entity.get("is_active_client") is False:
        #     raise UnauthorizedError("invalid_credential")
        if entity.get("use_magic_link") is True:
            payload_jwt = JWTHandler.generate_token(payload=entity, ttl=10)
            AuthenticationService.send_authentication_email(
                email=entity.get("email"),
                payload_jwt=payload_jwt,
                body="email.body.created",
            )
            return {
                "status_code": status.HTTP_200_OK,
                "message_key": "email.login",
            }
        else:
            pin = payload.get("pin")
            if pin is None:
                return {
                    "status_code": status.HTTP_200_OK,
                    "message_key": "user.need_pin",
                }
            if hash_field(payload=pin) != entity.get("pin"):
                raise UnauthorizedError("user.pin_error")

            jwt = token_handler.generate_token(payload=entity, ttl=525600)
            JwtController.insert_one(jwt, entity.get("email"))
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
        payload: dict, user_repository=UserRepository(), token_handler=JWTHandler
    ) -> dict:
        user_old = user_repository.find_one({"_id": payload.get("email")})
        if user_old is None:
            raise BadRequestError("common.register_not_exists")

        user_new = deepcopy(user_old)
        client_has_trade_allowed = AuthenticationService._dtvm_client_has_trade_allowed(
            user=user_old
        )
        must_update = False
        for key, value in client_has_trade_allowed.items():
            if value["status_changed"]:
                must_update = True
                user_new.update({key: value["status"]})

        if must_update:
            if user_repository.update_one(old=user_old, new=user_new) is False:
                raise InternalServerError("common.process_issue")

        jwt = token_handler.generate_token(payload=user_new, ttl=525600)
        return {"status_code": status.HTTP_200_OK, "payload": {"jwt": jwt}}

    @staticmethod
    def _dtvm_client_has_trade_allowed(user: dict) -> dict:

        user_solutiontech_status_from_database = user.get("solutiontech")
        user_sincad_status_from_database = user.get("sincad")
        user_bmf_account_from_database = user.get("bmf_account")
        user_cpf_from_database = user.get("cpf")

        client_has_trade_allowed_status_with_database_user = AuthenticationService._get_client_has_trade_allowed_status_with_database_user(
            user_solutiontech_status_from_database=user_solutiontech_status_from_database,
            user_sincad_status_from_database=user_sincad_status_from_database,
        )

        user_has_valid_solutiontech_status_in_database = AuthenticationService.check_if_user_has_valid_solutiontech_status_in_database(
            user_solutiontech_status_from_database=user_solutiontech_status_from_database
        )

        if user_has_valid_solutiontech_status_in_database:
            user_solutiontech_status_from_check_status_request = Solutiontech.check_if_client_is_synced_with_solutiontech(
                    user_bmf_code=int(user_bmf_account_from_database),
                    user_solutiontech_status_from_database=user_solutiontech_status_from_database
                )

            client_has_trade_allowed_status_with_database_user = AuthenticationService._update_client_has_trade_allowed_status_with_solutiontech_status_response(
                client_has_trade_allowed_status_with_database_user=client_has_trade_allowed_status_with_database_user,
                user_solutiontech_status_from_database=user_solutiontech_status_from_database,
                user_solutiontech_status_from_check_status_request=user_solutiontech_status_from_check_status_request,
            )

        user_is_already_sync_with_sincad = (
            user_sincad_status_from_database
            is SincadClientImportStatus.NOT_SYNCED.value
        )
        if user_is_already_sync_with_sincad:
            sincad_status_from_sinacor = AuthenticationService.sinacor_is_synced_with_sincad(
                user_cpf=user_cpf_from_database
            )

            AuthenticationService._update_client_has_trade_allowed_status_with_sincad_status_response(
                client_has_trade_allowed_status_with_database_user=client_has_trade_allowed_status_with_database_user,
                sincad_status_from_sinacor=sincad_status_from_sinacor,
                user_sincad_status_from_database=user_sincad_status_from_database,
            )

        return client_has_trade_allowed_status_with_database_user

    @staticmethod
    def _get_client_has_trade_allowed_status_with_database_user(
        user_solutiontech_status_from_database: str,
        user_sincad_status_from_database: str,
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
        }

        return client_has_trade_allowed_status_with_database_user

    @staticmethod
    def _update_client_has_trade_allowed_status_with_solutiontech_status_response(
        client_has_trade_allowed_status_with_database_user: dict,
        user_solutiontech_status_from_database: str,
        user_solutiontech_status_from_check_status_request: str,
    ):

        solutiontech_status_changed = (
            user_solutiontech_status_from_database
            != user_solutiontech_status_from_check_status_request
        )

        client_has_trade_allowed_status_with_database_user["solutiontech"][
            "status"
        ] = user_solutiontech_status_from_check_status_request
        client_has_trade_allowed_status_with_database_user["solutiontech"][
            "status_changed"
        ] = solutiontech_status_changed

        return client_has_trade_allowed_status_with_database_user

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
    def check_if_user_has_valid_solutiontech_status_in_database(
        user_solutiontech_status_from_database: str,
    ):
        user_has_valid_solutiontech_status_in_database = (
            user_solutiontech_status_from_database
            == SolutiontechClientImportStatus.SEND.value
            or user_solutiontech_status_from_database
            == SolutiontechClientImportStatus.FAILED.value
        )

        return user_has_valid_solutiontech_status_in_database

    @staticmethod
    def sinacor_is_synced_with_sincad(
        user_cpf: int, client_register_repository=ClientRegisterRepository()
    ) -> bool:
        sincad_status = client_register_repository.get_sincad_status(user_cpf=user_cpf)
        return sincad_status and sincad_status[0] in ["ACE", "ECM"]

    @staticmethod
    def create_electronic_signature_jwt(payload: dict):
        jwt_mist_session = JWTHandler.generate_session_jwt(payload.get('electronic_signature'), payload.get("email"))
        return {
            "status_code": status.HTTP_200_OK,
            "payload": jwt_mist_session[0],
        }
