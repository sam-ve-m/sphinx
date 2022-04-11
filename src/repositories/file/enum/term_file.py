from enum import Enum


class TermsFileType(Enum):
    TERM_APPLICATION = "term_application"
    TERM_OPEN_ACCOUNT = "term_open_account"
    TERM_REFUSAL = "term_refusal"
    TERM_NON_COMPLIANCE = "term_non_compliance"
    TERM_RETAIL_LIQUID_PROVIDER = "term_retail_liquid_provider"
    TERM_OPEN_ACCOUNT_DW = "term_open_account_dw"
    TERM_APPLICATION_DW = "term_application_dw"
    TERM_PRIVACY_POLICY_DW = "term_privacy_policy_dw"
    TERM_DATA_SHARING_POLICY_DW = "term_data_sharing_policy_dw"
