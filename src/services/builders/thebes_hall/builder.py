# Standards
from datetime import datetime, timedelta
from typing import Tuple
import asyncio

# Third part
import nest_asyncio

from src.domain.drive_wealth.kyc_status import KycStatus
from src.repositories.file.enum.term_file import TermsFileType
from tests.src.services.builders.thebes_hall.test_thebes_hall_builder_validator import Terms

nest_asyncio.apply()

# SPHINX
from src.domain.investor_type.type import InvestorType
from src.repositories.user.repository import UserRepository
from src.services.builders.thebes_hall.validators.suitability import (
    Suitability as SuitabilityValidator,
)
from src.services.builders.thebes_hall.validators.terms import Terms as TermsValidator
from src.services.builders.thebes_hall.validators.account_data import (
    AccountData as AccountDataValidator,
)
from nidavellir import Sindri
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
        self._jwt_payload_user_data = dict()
        self._control_data = dict()
        self._user_data = user_data
        self._ttl = ttl
        self.user_repository = user_repository
        self.terms_validator = terms_validator

    def build(self) -> Tuple[dict, dict]:
        build_strategy = self._get_strategy()
        build_strategy()
        self._jwt_payload_data.update({"user": self._jwt_payload_user_data})
        Sindri.dict_to_primitive_types(obj=self._jwt_payload_data)
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

    def _get_strategy(self):
        build_strategies = self._get_build_strategies()
        is_active_user = self._user_data.get("is_active_user")
        is_active_client = self._user_data.get("is_active_client")
        build_strategy = build_strategies.get((is_active_user, is_active_client))

        if build_strategy is None:
            raise Exception("internal_error")

        return build_strategy

    def _build_user_jwt(self):
        (
            self.add_expiration_date_and_created_at()
            .add_unique_id()
            .add_scope()
            .add_nick_name()
            .add_terms()
            .add_using_suitability_or_risk_acknowledged()
            .add_last_modified_date_months_past()
            .add_has_finished_br_onboarding()
            .add_has_finished_us_onboarding()
            .add_need_validate_email()
        )

    def _build_client_jwt(self):

        # TODO: Verificar se é necessário adicionar bloquio de conta us
        # .add_client_us_account_is_blocked()

        (
            self.add_expiration_date_and_created_at()
            .add_unique_id()
            .add_nick_name()
            .add_scope()
            .add_is_blocked_electronic_signature()
            .add_register_analyses()
            .add_br_accounts()
            .add_us_accounts()
            .add_using_suitability_or_risk_acknowledged()
            .add_last_modified_date_months_past()
            .add_suitability_months_past()
            .add_suitability_remaining_months()
            .add_account_br_is_blocked()
            .add_client_is_awaiting_br_account_to_be_created()
            .add_client_has_br_trade_allowed(
                suitability_months_past=self._control_data["suitability_months_past"],
                last_modified_date_months_past=self._control_data[
                    "last_modified_date_months_past"
                ],
            )
            .add_client_has_us_trade_allowed()
            .add_client_profile()
            .add_terms()
            .add_has_finished_br_onboarding()
            .add_has_finished_us_onboarding()
        )

    def add_account_br_is_blocked(self):
        self._jwt_payload_user_data.update({"account_br_is_blocked": False})
        sinacor_account_block_status = self._user_data.get(
            "sinacor_account_block_status"
        )
        account_br_is_blocked = all([sinacor_account_block_status])
        self._jwt_payload_user_data.update(
            {"account_br_is_blocked": account_br_is_blocked}
        )

        return self

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

    def add_terms(self):
        self.terms_validator.run(user_data=self._user_data)
        terms_map = list()
        for term in TermsFileType:
            term_metadata = self._user_data["terms"].get(term.value)
            if not term_metadata:
                term_metadata = {}
            terms_map.append({"name": term.value, **term_metadata})
        self._control_data.update({"terms": terms_map})
        return self

    def add_has_finished_br_onboarding(self):
        has_electronic = bool(self._user_data.get("electronic_signature"))
        self._control_data.update({"has_finished_br_onboarding": has_electronic})
        return self

    def add_has_finished_us_onboarding(self):
        has_w8_confirmation = bool(
            self._user_data.get("external_exchange_requirements", {})
            .get("us", {})
            .get("w8_confirmation")
        )
        self._control_data.update({"has_finished_us_onboarding": has_w8_confirmation})
        return self

    def add_need_validate_email(self):
        email_validated = bool(self._user_data.get("email_validated", False))
        if not email_validated:
            self._jwt_payload_data.update(
                {"is_email_validation_token": not email_validated}
            )
        return self

    def add_suitability_months_past(self):
        SuitabilityValidator.run(user_data=self._user_data)
        suitability = self._user_data.get("suitability")
        suitability_months_past = 0
        if suitability:
            suitability_months_past = suitability.get("months_past")
        self._control_data.update({"suitability_months_past": suitability_months_past})
        return self

    def add_suitability_remaining_months(self):
        SuitabilityValidator.run(user_data=self._user_data)
        suitability = self._user_data.get("suitability")
        remaining_months = 0
        if suitability:
            remaining_months = suitability.get("remaining_months")
        self._control_data.update({"suitability_remaining_months": remaining_months})
        return self

    def add_last_modified_date_months_past(self):
        AccountDataValidator.run(user_data=self._user_data)
        last_modified_date = self._user_data.get("record_date_control", {}).get(
            "registry_updates", {}
        )
        last_modified_date_months_past = 0
        if last_modified_date:
            last_modified_date_months_past = last_modified_date.get("months_past")
        self._control_data.update(
            {"last_modified_date_months_past": last_modified_date_months_past}
        )
        return self

    def add_using_suitability_or_risk_acknowledged(self):
        current_event_loop = asyncio.get_running_loop()
        task = current_event_loop.create_task(
            self.user_repository.is_user_using_suitability_or_risk_acknowledged(
                unique_id=self._user_data.get("unique_id")
            )
        )
        value = current_event_loop.run_until_complete(task)
        self._control_data.update(
            {"using_suitability_or_risk_acknowledged": value.get("option")}
        )
        self._jwt_payload_user_data.update(
            {"using_suitability_or_risk_acknowledged": value.get("option")}
        )
        if suitability_profile := value.get("suitability_profile"):
            self._control_data.update({"suitability_profile": suitability_profile})
            self._jwt_payload_user_data.update(
                suitability={"profile": suitability_profile}
            )
        return self

    def add_nick_name(self):
        self._jwt_payload_user_data.update(
            {"nick_name": self._user_data.get("nick_name")}
        )
        return self

    def add_unique_id(self):
        self._jwt_payload_user_data.update(
            {"unique_id": self._user_data.get("unique_id")}
        )
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
        if self._jwt_payload_user_data.get("portfolios") is None:
            self._jwt_payload_user_data.update({"portfolios": dict()})
        if self._jwt_payload_user_data["portfolios"].get("br") is None:
            self._jwt_payload_user_data["portfolios"].update({"br": dict()})
        (self.add_bovespa_account().add_bmf_account())
        return self

    def add_us_accounts(self):
        if self._jwt_payload_user_data.get("portfolios") is None:
            self._jwt_payload_user_data.update({"portfolios": dict()})
        if self._jwt_payload_user_data["portfolios"].get("us") is None:
            self._jwt_payload_user_data["portfolios"].update({"us": dict()})
        (self.add_dw_account().add_dw_display_account())
        return self

    def add_bovespa_account(self):
        self._jwt_payload_user_data["portfolios"]["br"].update(
            {
                "bovespa_account": self._user_data.get("portfolios", {})
                .get("default", {})
                .get("br", {})
                .get("bovespa_account")
            }
        )
        return self

    def add_bmf_account(self):
        self._jwt_payload_user_data["portfolios"]["br"].update(
            {
                "bmf_account": self._user_data.get("portfolios", {})
                .get("default", {})
                .get("br", {})
                .get("bmf_account")
            }
        )
        return self

    def add_dw_account(self):
        dw_account = (
            self._user_data.get("portfolios", {})
            .get("default", {})
            .get("us", {})
            .get("dw_account")
        )
        if dw_account:
            self._jwt_payload_user_data["portfolios"]["us"].update(
                {"dw_account": dw_account}
            )
        return self

    def add_dw_display_account(self):
        dw_display_account = (
            self._user_data.get("portfolios", {})
            .get("default", {})
            .get("us", {})
            .get("dw_display_account")
        )
        if dw_display_account:
            self._jwt_payload_user_data["portfolios"]["us"].update(
                {"dw_display_account": dw_display_account}
            )
        return self

    def add_client_is_awaiting_br_account_to_be_created(self):
        solutiontech = self._user_data.get("solutiontech")
        sincad = self._user_data.get("sincad")
        sinacor = self._user_data.get("sinacor")
        has_all_attributes = (
            solutiontech is not None and
            sincad is not None and
            sinacor is not None
        )
        client_has_br_account = all(
            [
                solutiontech == SolutiontechClientImportStatus.SYNC.value,
                sincad,
                sinacor
            ]
        )
        self._jwt_payload_user_data.update(
            {"client_is_awaiting_br_account_to_be_created": not client_has_br_account if has_all_attributes else None}
        )
        return self

    def add_client_has_br_trade_allowed(
        self, suitability_months_past: int, last_modified_date_months_past: int
    ):
        if not self._control_data.get("using_suitability_or_risk_acknowledged"):
            self.add_using_suitability_or_risk_acknowledged()

        using_suitability_or_risk_acknowledged = self._control_data.get("using_suitability_or_risk_acknowledged")
        if using_suitability_or_risk_acknowledged == TermsFileType.TERM_REFUSAL.value:
            valid_suitability_or_risk_acknowledged_status = True
        else:
            valid_suitability_or_risk_acknowledged_status = suitability_months_past < 24

        self._jwt_payload_user_data.update({"client_has_br_trade_allowed": False})
        solutiontech = self._user_data.get("solutiontech")
        sincad = self._user_data.get("sincad")
        sinacor = self._user_data.get("sinacor")
        is_active_client = self._user_data.get("is_active_client")
        client_has_electronic_signature = self._user_data.get("electronic_signature")
        client_has_trade_allowed = all(
            [
                solutiontech == SolutiontechClientImportStatus.SYNC.value,
                sincad,
                sinacor,
                is_active_client,
                client_has_electronic_signature,
                valid_suitability_or_risk_acknowledged_status,
                last_modified_date_months_past < 24,
            ]
        )
        self._jwt_payload_user_data.update(
            {"client_has_br_trade_allowed": client_has_trade_allowed}
        )
        return self

    def add_client_has_us_trade_allowed(
        self,
    ):
        if current_dw_status := self._user_data.get("dw"):
            kyc_is_approved = current_dw_status == KycStatus.KYC_APPROVED.value
            w8_confirmation = (
                self._user_data.get("external_exchange_requirements", {})
                .get("us", {})
                .get("w8_confirmation")
            )
            has_ouroinvest_account = (
                self._user_data.get("ouro_invest", {})
                .get("account", {})
                .get("account_number")
            )
            if kyc_is_approved and w8_confirmation and has_ouroinvest_account:
                self._jwt_payload_user_data.update(
                    {"client_has_us_trade_allowed": True}
                )
            else:
                self._jwt_payload_user_data.update(
                    {"client_has_us_trade_allowed": False}
                )
        return self

    def add_client_profile(self):
        self._jwt_payload_user_data.update(
            {
                "client_profile": self._user_data.get(
                    "client_profile", InvestorType.INVESTOR
                )
            }
        )
        return self
