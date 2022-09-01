from enum import Enum


class SuitabilityProfile(Enum):
    HIGH_RISK = "high_risk"
    MEDIUM_RISK = "medium_risk"
    LOW_RISK = "low_risk"


class RiskDisclaimerType(Enum):
    SUITABILITY = "suitability"
    TERM_REFUSAL = "term_refusal"
