import datetime

fake_user = {
    "_id": "msa51@lionx.com.br",
    "pin": None,
    "nick_name": "John",
    "email": "msa51@lionx.com.br",
    "created_at": datetime.datetime(1993, 7, 12, 0, 0),
    "scope": {"view_type": "default", "features": ["default"]},
    "is_active_user": True,
    "use_magic_link": True,
    "token_valid_after": datetime.datetime(1993, 7, 12, 0, 0),
    "terms": {
        "term_application": None,
        "term_open_account": None,
        "term_retail_liquid_provider": None,
        "term_refusal": {
            "version": 2,
            "date": datetime.datetime(1993, 7, 12, 0, 0),
            "is_deprecated": False,
        },
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
        "score": 1,
        "submission_date": datetime.datetime(1993, 7, 12, 0, 0),
        "suitability_version": 4,
    },
    "cel_phone": "11952906652",
    "cpf": "35202904800",
    "is_cvm_qualified_investor": False,
    "marital": {"status": "not_married", "spouse": None},
    "register_analyses": "PENDING",
    "stone_age_contract_uuid": "6d6e2a04-00e4-11ec-9a03-0242ac130003",
}
