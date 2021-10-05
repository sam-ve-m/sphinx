# Standards
from datetime import datetime, timedelta

# SPHINX
from src.repositories.user.repository import UserRepository
from src.services.builders.thebes_hall.validators.suitability import (
    Suitability as SuitabilityValidator,
)
from src.services.builders.thebes_hall.validators.terms import Terms as TermsValidator
from src.services.builders.thebes_hall.validators.account_data import (
    AccountData as AccountDataValidator,
)
from nidavellir.src.uru import Sindri
from jwt.utils import get_int_from_datetime
from src.domain.solutiontech.client_import_status import SolutiontechClientImportStatus


class ThebesHallBuilder:
    def __init__(
        self,
        user_data: dict,
        kwargs_to_add_on_jwt: dict,
        ttl: int,
        user_repository=UserRepository(),
        terms_validator=TermsValidator(),
    ):
        self._jwt_payload_data = dict()
        self._user_data = user_data
        self._kwargs_to_add_on_jwt = kwargs_to_add_on_jwt
        self._ttl = ttl
        self.user_repository = user_repository
        self.terms_validator = terms_validator

    def _get_build_strategies(self) -> dict:
        is_not_active_user = (False, None)
        is_active_user = (True, None)
        is_not_active_client = (True, False)
        is_active_client = (True, True)

        build_strategies = {
            is_not_active_user: self._build_user_jwt,
            is_active_user: self._build_user_jwt,
            is_not_active_client: self._build_user_jwt,
            is_active_client: self._build_client_jwt,
        }

        return build_strategies

    def _get_strategy(self):
        build_strategies = self._get_build_strategies()
        is_active_user = self._user_data.get("is_active_user")
        is_active_client = self._user_data.get("is_active_client")
        build_strategy = build_strategies.get((is_active_user, is_active_client))

        if build_strategy is None:
            raise Exception("internal_error")

        return build_strategy

    def build(self) -> dict:
        build_strategy = self._get_strategy()
        build_strategy()

        Sindri.dict_to_primitive_types(values=self._jwt_payload_data)
        return self._jwt_payload_data

    def _build_user_jwt(self):
        (
            self.add_expiration_date_and_created_at()
            .add_nick_name()
            .add_email()
            .add_scope()
            .add_is_active_user()
            .add_terms()
            .add_last_modified_date()
            .add_extra_kwargs()
        )

    def _build_client_jwt(self):
        (
            self.add_expiration_date_and_created_at()
            .add_extra_kwargs()
            .add_suitability_months_past()
            .add_terms()
            .add_last_modified_date()
            .add_is_admin()
            .add_nick_name()
            .add_email()
            .add_scope()
            .add_is_active_user()
            .add_is_blocked_electronic_signature()
            .add_register_analyses()
            .add_bovespa_account()
            .add_bmf_account()
            .add_using_suitability_or_refuse_term()
            .add_client_has_trade_allowed(
                suitability_months_past=self._jwt_payload_data[
                    "suitability_months_past"
                ],
                last_modified_date_months_past=self._jwt_payload_data[
                    "last_modified_date_months_past"
                ],
            )
        )

    def add_expiration_date_and_created_at(self):
        self._jwt_payload_data.update(
            {
                "exp": get_int_from_datetime(
                    datetime.utcnow() + timedelta(minutes=self._ttl)
                ),
                "created_at": datetime.utcnow(),
            }
        )
        return self

    def add_extra_kwargs(self):
        if self._kwargs_to_add_on_jwt:
            self._jwt_payload_data.update(self._kwargs_to_add_on_jwt)
        return self

    def add_terms(self):
        self.terms_validator.run(user_data=self._user_data)
        self._jwt_payload_data.update({"terms": self._user_data["terms"]})
        return self

    def add_suitability_months_past(self):
        SuitabilityValidator.run(user_data=self._user_data)
        suitability = self._user_data.get("suitability")
        suitability_months_past = 0
        if suitability:
            suitability_months_past = suitability.get("months_past")
        self._jwt_payload_data.update(
            {"suitability_months_past": suitability_months_past}
        )
        return self

    def add_last_modified_date(self):
        AccountDataValidator.run(user_data=self._user_data)
        last_modified_date = self._user_data.get("last_modified_date")
        last_modified_date_months_past = 0
        if last_modified_date:
            last_modified_date_months_past = last_modified_date.get("months_past")
        self._jwt_payload_data.update(
            {"last_modified_date_months_past": last_modified_date_months_past}
        )
        return self

    def add_using_suitability_or_refuse_term(self):
        self._jwt_payload_data.update(
            {
                "using_suitability_or_refuse_term": self.user_repository.is_user_using_suitability_or_refuse_term(
                    user_email=self._user_data.get("email")
                )
            }
        )
        return self

    def add_is_admin(self):
        if self._user_data.get("is_admin"):
            self._jwt_payload_data.update({"is_admin": self._user_data.get("is_admin")})
        return self

    def add_nick_name(self):
        self._jwt_payload_data.update({"nick_name": self._user_data.get("nick_name")})
        return self

    def add_email(self):
        self._jwt_payload_data.update({"email": self._user_data.get("email")})
        return self

    def add_scope(self):
        self._jwt_payload_data.update({"scope": self._user_data.get("scope")})
        return self

    def add_is_active_user(self):
        self._jwt_payload_data.update(
            {"is_active_user": self._user_data.get("is_active_user")}
        )
        return self

    def add_is_blocked_electronic_signature(self):
        self._jwt_payload_data.update(
            {
                "is_blocked_electronic_signature": self._user_data.get(
                    "is_blocked_electronic_signature"
                )
            }
        )
        return self

    def add_register_analyses(self):
        if register_analyses := self._user_data.get("register_analyses"):
            self._jwt_payload_data.update({"register_analyses": register_analyses})
        return self

    def add_bovespa_account(self):
        if bovespa_account := self._user_data.get("bovespa_account"):
            self._jwt_payload_data.update({"bovespa_account": bovespa_account})
        return self

    def add_bmf_account(self):
        if bmf_account := self._user_data.get("bmf_account"):
            self._jwt_payload_data.update({"bmf_account": bmf_account})
        return self

    def add_client_has_trade_allowed(
        self, suitability_months_past: int, last_modified_date_months_past: int
    ):
        self._jwt_payload_data.update({"client_has_trade_allowed": False})
        solutiontech = self._user_data.get("solutiontech")
        sincad = self._user_data.get("sincad")
        sinacor = self._user_data.get("sinacor")
        is_active_client = self._user_data.get("is_active_client")
        client_has_trade_allowed = all([
            solutiontech == SolutiontechClientImportStatus.SYNC.value,
            sincad,
            sinacor,
            is_active_client,
            suitability_months_past < 24,
            last_modified_date_months_past < 24
        ])
        self._jwt_payload_data.update(
            {"client_has_trade_allowed": client_has_trade_allowed}
        )
        return self
