from enum import Enum


class TermsFileType(Enum):
    TERM_APPLICATION = "term_application"
    TERM_OPEN_ACCOUNT = "term_open_account"
    TERM_REFUSAL = "term_refusal"
    TERM_NON_COMPLIANCE = "term_non_compliance"
    TERM_RETAIL_LIQUID_PROVIDER = "term_retail_liquid_provider"
