# Standards
from datetime import datetime

# Third part
from pydantic import BaseModel


class FirstLevelJsonUserMergedDataValidator(BaseModel):
    _id: str
    pin: str = None
    nick_name: str
    email: str
    created_at: datetime
    scope: dict
    is_active_user: bool
    use_magic_link: bool
    token_valid_after: datetime
    terms: dict
    can_be_managed_by_third_party_operator: bool
    is_managed_by_third_party_operator: bool
    third_party_operator: dict
    suitability: dict
    cel_phone: str
    cpf: str
    is_cvm_qualified_investor: bool
    is_us_person: bool
    marital: dict
    us_tin: int
    register_analyses: str
    stone_age_contract_uuid: str
    gender: str
    name: str
    birth_date: float
    birthplace: dict
    mother_name: str
    identifier_document: dict
    address: dict
    occupation: dict
    assets: dict
    education: dict
    politically_exposed_person: dict
    connected_person: str
    person_type: str
    client_type: int
    investor_type: int
    cosif_tax_classification: int
    self_link: str
    irs_sharing: bool
    father_name: str
    midia_person: bool
    person_related_to_market_influencer: bool
    court_orders: bool
    lawsuits: bool
    fund_admin_registration: bool
    investment_fund_administrators_registration: bool
    register_auditors_securities_commission: bool
    registration_of_other_market_participants_securities_commission: bool
    foreign_investors_register_of_annex_iv_not_registered: bool
    registration_of_foreign_investors_securities_commission: bool
    registration_representative_of_nonresident_investors_securities_commission: bool


class MinimalClientTradeMetadata(BaseModel):
    cpf: str
    sinacor: bool
    sincad: bool
    solutiontech: str
    bovespa_account: str
    bmf_account: str
    last_modified_date: dict
    is_active_client: bool
