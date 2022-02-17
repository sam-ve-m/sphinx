# OUTSIDE LIBRARIES
from src.infrastructures.env_config import config

# SPHINX
from src.repositories.base_repository.mongo_db.base import MongoDbBaseRepository


class UserRepository(MongoDbBaseRepository):
    def __init__(self):
        super().__init__(
            database=config("MONGODB_DATABASE_NAME"),
            collection=config("MONGODB_USER_COLLECTION"),
        )

    def is_user_using_suitability_or_refuse_term(self, unique_id: str) -> str:
        user = self.find_one({"unique_id": unique_id})
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
            only_suitability: lambda _suitability, _term_refusal: "suitability",
            only_refusal_term: lambda _suitability, _term_refusal: "term_refusal",
            nothing: lambda _suitability, _term_refusal: None,
        }

        user_trade_profile_callback = user_trade_match.get(
            (has_suitability, has_term_refusal)
        )
        user_trade_profile = user_trade_profile_callback(suitability, term_refusal)

        return user_trade_profile

    @staticmethod
    def suitability_and_refusal_term_callback(_suitability, _term_refusal):
        last_trade_profile_signed = (
            _suitability["submission_date"] > _term_refusal["date"]
        )
        return "suitability" if last_trade_profile_signed else "term_refusal"
