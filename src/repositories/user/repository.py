from src.domain.suitability.profile import SuitabilityProfile, RiskDisclaimerType
from src.infrastructures.env_config import config

from src.repositories.base_repository.mongo_db.base import MongoDbBaseRepository
from src.services.builders.thebes_hall.validators.months_past import months_past


class UserRepository(MongoDbBaseRepository):

    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    async def is_user_using_suitability_or_refuse_term(cls, unique_id: str) -> dict:
        user = await cls.find_one({"unique_id": unique_id})
        suitability = user.get("suitability")
        term_refusal = user["terms"].get("term_refusal")

        has_suitability = suitability is not None
        has_term_refusal = term_refusal is not None

        suitability_and_refusal_term = (True, True)
        only_suitability = (True, False)
        only_refusal_term = (False, True)
        nothing = (False, False)

        user_trade_match = {
            suitability_and_refusal_term: UserRepository.suitability_and_refusal_term_callback,
            only_suitability: lambda _suitability, _term_refusal: RiskDisclaimerType.SUITABILITY.value,
            only_refusal_term: lambda _suitability, _term_refusal: RiskDisclaimerType.TERM_REFUSAL.value,
            nothing: lambda _suitability, _term_refusal: None,
        }

        user_trade_profile_callback = user_trade_match.get(
            (has_suitability, has_term_refusal)
        )
        user_trade_profile = user_trade_profile_callback(suitability, term_refusal)
        user_risk_option = {"option": user_trade_profile}
        if user_trade_profile == RiskDisclaimerType.SUITABILITY.value:
            user_risk_option["suitability_profile"] = cls.__get_user_suitability_profile(suitability)
        return user_risk_option

    @classmethod
    def __get_user_suitability_profile(cls, suitability: dict) -> str:
        if suitability.get("score") == 1:
            return SuitabilityProfile.HIGH_RISK.value
        return SuitabilityProfile.LOW_RISK.value

    @staticmethod
    def suitability_and_refusal_term_callback(_suitability, _term_refusal):
        suitability_months_past = months_past(_suitability["submission_date"])
        if suitability_months_past < 24:
            return RiskDisclaimerType.SUITABILITY.value
        else:
            return RiskDisclaimerType.TERM_REFUSAL.value
