# Std imports
from datetime import datetime

invalid_client_data = {}

valid_client_data = {
    "_id": "ilm@lionx.com.br",
    "pin": "7c4a8d09ca3762af61e59520943dc26494f8941b",
    "nick_name": "Igor Magro",
    "email": "ilm@lionx.com.br",
    "created_at": datetime(2021, 8, 10, 14, 1, 7, 829000),
    "scope": {"view_type": "default", "features": ["default"]},
    "is_active_user": True,
    "is_active_client": True,
    "use_magic_link": True,
    "token_valid_after": datetime(2021, 8, 10, 17, 1, 7, 829000),
    "terms": {
        "term_application": None,
        "term_open_account": None,
        "term_retail_liquid_provider": None,
        "term_refusal": None,
        "term_non_compliance": None,
    },
    "can_be_managed_by_third_party_operator": False,
    "is_managed_by_third_party_operator": False,
    "third_party_operator": {
        "is_third_party_operator": False,
        "details": {},
        "third_party_operator_email": "string",
    },
    "suitability": {
        "score": 1.0,
        "submission_date": datetime(2021, 8, 30, 23, 44, 45, 631000),
        "suitability_version": 2,
        "months_past": 1,
    },
    "cel_phone": "11987450574",
    "cpf": "46947059895",
    "is_cvm_qualified_investor": True,
    "is_us_person": True,
    "marital": {"status": 1, "spouse": "None"},
    "electronic_signature": "8f0a62e2be8463b281db124556386c7f8dba64bce4416744f1f5c7f3bb48a405",
    "register_analyses": "SEND_RESPONSES",
    "stone_age_contract_uuid": "d65a2301-330f-4fef-b314-9834df20d067",
    "address": {
        "country": "BRA",
        "street_name": "R. Sabiá Poca",
        "number": "15",
        "neighborhood": "Formosinha",
        "state": "GO",
        "city": "FORMOSA",
        "id_city": 968,
        "zip_code": 73813190,
        "phone_number": "11952909954",
    },
    "assets": {
        "patrimony": 5.0,
        "income": 5446456.44,
        "income_tax_type": 1,
        "date": datetime(1993, 7, 12, 0, 0),
    },
    "birth_date": datetime(1993, 7, 12, 0, 0),
    "birthplace": {
        "nationality": 1,
        "country": "BRA",
        "state": "GO",
        "city": "FORMOSA",
        "id_city": 968,
    },
    "bmf_account": "49",
    "bovespa_account": "000000049-9",
    "client_type": 1,
    "connected_person": "N",
    "cosif_tax_classification": 21,
    "court_orders": False,
    "education": {"level": "Médio incompleto", "course": "Escola James Riwbon"},
    "father_name": "Antonio dos Santos",
    "foreign_investors_register_of_annex_iv_not_reregistered": False,
    "fund_admin_registration": False,
    "gender": "M",
    "identifier_document": {
        "type": "RG",
        "document_data": {
            "number": 485416803,
            "date": datetime(1970, 1, 1, 0, 51, 52),
            "state": "SSP",
            "issuer": "SSP",
        },
    },
    "investment_fund_administrators_registration": False,
    "investor_type": 101,
    "irs_sharing": True,
    "last_modified_date": {
        "concluded_at": datetime(2021, 9, 24, 20, 36, 21, 580000),
        "months_past": 0,
    },
    "lawsuits": False,
    "midia_person": False,
    "mother_name": "Antonia dos Santos Jr.",
    "name": "GERTRURDES 4",
    "occupation": {
        "activity": 304,
        "company": {"cnpj": "25811052000179", "name": "Tudo nosso .com.br"},
    },
    "person_related_to_market_influencer": False,
    "person_type": "F",
    "politically_exposed_person": {"is_politically_exposed_person": False},
    "register_auditors_securities_commission": False,
    "registration_of_foreign_investors_securities_commission": False,
    "registration_of_other_market_participants_securities_commission": False,
    "registration_representative_of_nonresident_investors_securities_commission": False,
    "self_link": "http://self_user.jpg",
    "sinacor": True,
    "sincad": True,
    "solutiontech": "sync",
    "is_blocked_electronic_signature": False,
    "password": "ad243f9d63aea41fa18f85feab981049e95721f2955f74408cb437dbbe3c9018",
    "electronic_signature_wrong_attempts": 0,
    "is_admin": True,
    "stone_age_proposal_id": "cbf53b8b-bccb-4b96-a28e-43b54aa778f2",
}

sinacor_insert_client_control_data = (1, 1)
sinacor_update_client_control_data = (0, 0)

marital_married = {
    "status": 5,
    "spouse": {
        "cpf": "16746756076",
        "name": "Flavio Antobio Felicio",
        "nationality": 1,
    },
}

unemployed_occupation = {"activity": 609}

other_occupation = {
    "activity": 609,
    "company": {"cnpj": "25811052000179", "name": "Tudo nosso .com.br"},
}
