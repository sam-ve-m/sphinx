# Standards
from datetime import datetime, timedelta
from typing import Tuple

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
        ttl: int,
        user_repository=UserRepository(),
        terms_validator=TermsValidator(),
    ):
        self._jwt_payload_data = dict()
        self._control_data = dict()
        self._user_data = user_data
        self._ttl = ttl
        self.user_repository = user_repository
        self.terms_validator = terms_validator

    async def build(self) -> Tuple[dict, dict]:
        build_strategy = await self._get_strategy()
        build_strategy()

        Sindri.dict_to_primitive_types(values=self._jwt_payload_data)
        return self._jwt_payload_data, self._control_data

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

    async def _get_strategy(self):
        build_strategies = await self._get_build_strategies()
        is_active_user = self._user_data.get("is_active_user")
        is_active_client = self._user_data.get("is_active_client")
        build_strategy = build_strategies.get((is_active_user, is_active_client))

        if build_strategy is None:
            raise Exception("internal_error")

        return build_strategy

    async def _build_user_jwt(self):
        (
            self.add_expiration_date_and_created_at()
            .add_unique_id()
            .add_scope()
            .add_nick_name()
            .add_terms()
            .add_last_modified_date_months_past()
        )

    def _build_client_jwt(self):
        (
            self.add_expiration_date_and_created_at()
            .add_unique_id()
            .add_nick_name()
            .add_scope()
            .add_is_blocked_electronic_signature()
            .add_register_analyses()
            .add_br_accounts()
            .add_us_accounts()
            .add_using_suitability_or_refuse_term()
            .add_last_modified_date_months_past()
            .add_suitability_months_past()
            .add_client_has_br_trade_allowed(
                suitability_months_past=self._control_data["suitability_months_past"],
                last_modified_date_months_past=self._control_data[
                    "last_modified_date_months_past"
                ],
            )
            .add_client_has_us_trade_allowed()
            .add_client_profile()
            .add_terms()
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

    async def add_terms(self):
        self.terms_validator.run(user_data=self._user_data)
        self._control_data.update({"terms": self._user_data["terms"]})
        return self

    def add_suitability_months_past(self):
        SuitabilityValidator.run(user_data=self._user_data)
        suitability = self._user_data.get("suitability")
        suitability_months_past = 0
        if suitability:
            suitability_months_past = suitability.get("months_past")
        self._control_data.update({"suitability_months_past": suitability_months_past})
        return self

    def add_last_modified_date_months_past(self):
        AccountDataValidator.run(user_data=self._user_data)
        last_modified_date = self._user_data.get("last_modified_date")
        last_modified_date_months_past = 0
        if last_modified_date:
            last_modified_date_months_past = last_modified_date.get("months_past")
        self._control_data.update(
            {"last_modified_date_months_past": last_modified_date_months_past}
        )
        return self

    def add_using_suitability_or_refuse_term(self):
        self._control_data.update(
            {
                "using_suitability_or_refuse_term": self.user_repository.is_user_using_suitability_or_refuse_term(
                    unique_id=self._user_data.get("unique_id")
                )
            }
        )
        return self

    def add_nick_name(self):
        self._jwt_payload_data.update({"nick_name": self._user_data.get("nick_name")})
        return self

    def add_unique_id(self):
        self._jwt_payload_data.update({"unique_id": self._user_data.get("unique_id")})
        return self

    def add_scope(self):
        self._jwt_payload_data.update({"scope": self._user_data.get("scope")})
        return self

    def add_is_blocked_electronic_signature(self):
        self._control_data.update(
            {
                "is_blocked_electronic_signature": self._user_data.get(
                    "is_blocked_electronic_signature"
                )
            }
        )
        return self

    def add_register_analyses(self):
        if register_analyses := self._user_data.get("register_analyses"):
            self._control_data.update({"register_analyses": register_analyses})
        return self

    def add_br_accounts(self):
        if self._jwt_payload_data.get("accounts") is None:
            self._jwt_payload_data.update({"accounts": dict()})
        if self._jwt_payload_data["accounts"].get("br") is None:
            self._jwt_payload_data["accounts"].update({"br": dict()})
        (self.add_bovespa_account().add_bmf_account())
        return self

    def add_us_accounts(self):
        if self._jwt_payload_data.get("accounts") is None:
            self._jwt_payload_data.update({"accounts": dict()})
        if self._jwt_payload_data["accounts"].get("us") is None:
            self._jwt_payload_data["accounts"].update({"us": dict()})
        self._jwt_payload_data["accounts"]["us"].update({"dw_account": None})
        return self

    def add_bovespa_account(self):
        if bovespa_account := self._user_data.get("bovespa_account"):
            self._jwt_payload_data["accounts"]["br"].update(
                {"bovespa_account": bovespa_account}
            )
        return self

    def add_bmf_account(self):
        if bmf_account := self._user_data.get("bmf_account"):
            self._jwt_payload_data["accounts"]["br"].update(
                {"bmf_account": bmf_account}
            )
        return self

    def add_client_has_br_trade_allowed(
        self, suitability_months_past: int, last_modified_date_months_past: int
    ):
        self._jwt_payload_data.update({"client_has_br_trade_allowed": False})
        solutiontech = self._user_data.get("solutiontech")
        sincad = self._user_data.get("sincad")
        sinacor = self._user_data.get("sinacor")
        is_active_client = self._user_data.get("is_active_client")
        client_has_trade_allowed = all(
            [
                solutiontech == SolutiontechClientImportStatus.SYNC.value,
                sincad,
                sinacor,
                is_active_client,
                suitability_months_past < 24,
                last_modified_date_months_past < 24,
            ]
        )
        self._jwt_payload_data.update(
            {"client_has_br_trade_allowed": client_has_trade_allowed}
        )
        return self

    def add_client_has_us_trade_allowed(
        self,
    ):
        self._jwt_payload_data.update({"client_has_us_trade_allowed": False})
        return self

    def add_client_profile(self):
        self._jwt_payload_data.update({"client_profile": self._user_data.get("client_profile", 0)})
        return self
