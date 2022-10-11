from enum import Enum


class TermsFileType(Enum):
    TERM_APPLICATION = "term_application"
    TERM_OPEN_ACCOUNT = "term_open_account"
    TERM_REFUSAL = "term_refusal"
    TERM_NON_COMPLIANCE = "term_non_compliance"
    TERM_RETAIL_LIQUID_PROVIDER = "term_retail_liquid_provider"

    TERM_AND_PRIVACY_POLICY_DATA_SHARING_POLICY_DL_PT = (
        "term_and_privacy_policy_data_sharing_policy_dl_pt"
    )
    TERM_AND_PRIVACY_POLICY_DATA_SHARING_POLICY_DL_US = (
        "term_and_privacy_policy_data_sharing_policy_dl_us"
    )
    TERM_OPEN_ACCOUNT_DL_PT = "term_open_account_dl_pt"
    TERM_OPEN_ACCOUNT_DL_US = "term_open_account_dl_us"
    TERM_BUSINESS_CONTINUITY_PLAN_DL_PT = "term_business_continuity_plan_dl_pt"
    TERM_BUSINESS_CONTINUITY_PLAN_DL_US = "term_business_continuity_plan_dl_us"
    TERM_CUSTOMER_RELATIONSHIP_SUMMARY_DL_PT = (
        "term_customer_relationship_summary_dl_pt"
    )
    TERM_CUSTOMER_RELATIONSHIP_SUMMARY_DL_US = (
        "term_customer_relationship_summary_dl_us"
    )
    TERM_ALL_AGREEMENT_GRINGO_DL = "term_all_agreement_gringo_dl"
    TERM_OUROINVEST = "term_ouroinvest"
    TERM_GRINGO_WORLD = "term_gringo_world"
    TERM_GRINGO_WORLD_GENERAL_ADVICES = "term_gringo_world_general_advices"
