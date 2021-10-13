from datetime import datetime

from src.domain.stone_age.stone_age_register_analyses import StoneAgeRegisterAnalyses


def get_x_thebes_answer_with_client_data():
    payload = {}
    payload.update({"x-thebes-answer": jwt_decoded})
    return payload


jwt_decoded = {
  "nick_name": "Sem Verificação De Email",
  "email": "ilm3@lionx.com.br",
  "scope": {
    "view_type": "default",
    "features": [
      "default"
    ]
  },
  "is_active_user": True,
  "is_blocked_electronic_signature": False,
  "terms": {
    "term_application": None,
    "term_open_account": None,
    "term_retail_liquid_provider": None,
    "term_refusal": None,
    "term_non_compliance": None
  },
  "suitability_months_past": 0,
  "last_modified_date_months_past": 0,
  "client_has_trade_allowed": True,
  "created_at": "2021-10-13 13:51:45.372674",
  "exp": 1665669105,
  "using_suitability_or_refuse_term": "suitability",
  "bovespa_account": "000000204-1",
  "bmf_account": "204",
  "register_analyses": "APROVADO"
}

onboarding_complete_client_data = {
    "_id": "ilm5@lionx.com.br",
    "pin": None,
    "nick_name": "Igão Do Onbiarding",
    "email": "ilm5@lionx.com.br",
    "created_at": {"$date": "2021-10-13T14:27:09.973Z"},
    "scope": {"view_type": "default", "features": ["default"]},
    "is_active_user": True,
    "use_magic_link": True,
    "token_valid_after": {"$date": "2021-10-13T14:27:09.973Z"},
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
        "score": 1,
        "submission_date": {"$date": "2021-10-13T16:53:11.039Z"},
        "suitability_version": 4,
    },
    "cel_phone": "11987450574",
    "cpf": "63025165014",
    "is_cvm_qualified_investor": False,
    "is_us_person": True,
    "marital": {"status": "not_married", "spouse": None},
    "us_tin": 126516515,
    "register_analyses": "APROVADO",
    "stone_age_contract_uuid": "6d6e2a04-00e4-11ec-9a03-0242ac130003",
    "electronic_signature": "8f0a62e2be8463b281db124556386c7f8dba64bce4416744f1f5c7f3bb48a405",
    "electronic_signature_wrong_attempts": 0,
    "is_blocked_electronic_signature": False,
    "address": {
        "country": "BRA",
        "street_name": "R. 2",
        "number": "126",
        "neighborhood": "Formosinha",
        "state": "GO",
        "city": "FORMOSA",
        "id_city": 968,
        "zip_code": 73813190,
        "phone_number": "11952909954",
    },
    "assets": {
        "patrimony": 5446456.44,
        "income": 5446456.44,
        "income_tax_type": 1,
        "date": {"$date": "1993-07-12T00:00:00.000Z"},
    },
    "birth_date": {"$date": "1993-07-12T00:00:00.000Z"},
    "birthplace": {
        "nationality": 1,
        "country": "BRA",
        "state": "GO",
        "city": "FORMOSA",
        "id_city": 968,
    },
    "bmf_account": "206",
    "bovespa_account": "000000206-8",
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
            "number": 310062457,
            "date": {"$date": "2018-07-12T16:31:31.000Z"},
            "state": "SP",
            "issuer": "SSP",
        },
    },
    "investment_fund_administrators_registration": False,
    "investor_type": 101,
    "irs_sharing": True,
    "is_active_client": True,
    "last_modified_date": {"concluded_at": {"$date": "2021-10-13T17:48:25.480Z"}},
    "lawsuits": False,
    "marital_update": {
        "marital_regime": 1,
        "spouse_birth_date": {"$date": "1993-07-12T00:00:00.000Z"},
    },
    "midia_person": False,
    "mother_name": "Antonia dos Santos Jr.",
    "name": "Antonio Armando Piaui",
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
    "sincad": False,
    "solutiontech": "send",
}

onboarding_unstarted_client_data = {
    "_id": "ilm5@lionx.com.br",
    "pin": None,
    "nick_name": "Igão Do Onbiarding",
    "email": "ilm5@lionx.com.br",
    "created_at": {"$date": "2021-10-13T14:27:09.973Z"},
    "scope": {"view_type": "default", "features": ["default"]},
    "is_active_user": True,
    "use_magic_link": True,
    "token_valid_after": {"$date": "2021-10-13T14:27:09.973Z"},
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
}

onboarding_suitability_step_client_data = {
    "_id": "ilm5@lionx.com.br",
    "pin": None,
    "nick_name": "Igão Do Onbiarding",
    "email": "ilm5@lionx.com.br",
    "created_at": {"$date": "2021-10-13T14:27:09.973Z"},
    "scope": {"view_type": "default", "features": ["default"]},
    "is_active_user": True,
    "use_magic_link": True,
    "token_valid_after": {"$date": "2021-10-13T14:27:09.973Z"},
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
        "score": 1,
        "submission_date": {"$date": "2021-10-13T16:53:11.039Z"},
        "suitability_version": 4,
    },
}

onboarding_user_identifier_data_step_client_data = {
    "_id": "ilm5@lionx.com.br",
    "pin": None,
    "nick_name": "Igão Do Onbiarding",
    "email": "ilm5@lionx.com.br",
    "created_at": {"$date": "2021-10-13T14:27:09.973Z"},
    "scope": {"view_type": "default", "features": ["default"]},
    "is_active_user": True,
    "use_magic_link": True,
    "token_valid_after": {"$date": "2021-10-13T14:27:09.973Z"},
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
        "score": 1,
        "submission_date": {"$date": "2021-10-13T16:53:11.039Z"},
        "suitability_version": 4,
    },
    "cel_phone": "11987450574",
    "cpf": "63025165014",
}

onboarding_user_complementary_data_step_client_data = {
    "_id": "ilm5@lionx.com.br",
    "pin": None,
    "nick_name": "Igão Do Onbiarding",
    "email": "ilm5@lionx.com.br",
    "created_at": {"$date": "2021-10-13T14:27:09.973Z"},
    "scope": {"view_type": "default", "features": ["default"]},
    "is_active_user": True,
    "use_magic_link": True,
    "token_valid_after": {"$date": "2021-10-13T14:27:09.973Z"},
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
        "score": 1,
        "submission_date": {"$date": "2021-10-13T16:53:11.039Z"},
        "suitability_version": 4,
    },
    "cel_phone": "11987450574",
    "cpf": "63025165014",
    "is_cvm_qualified_investor": False,
    "is_us_person": False,
    "marital": {"status": "not_married", "spouse": None},
    "us_tin": None,
    "register_analyses": None,
    "stone_age_contract_uuid": "6d6e2a04-00e4-11ec-9a03-0242ac130003",
}

onboarding_user_quiz_step_client_data = {
    "_id": "ilm5@lionx.com.br",
    "pin": None,
    "nick_name": "Igão Do Onbiarding",
    "email": "ilm5@lionx.com.br",
    "created_at": {"$date": "2021-10-13T14:27:09.973Z"},
    "scope": {"view_type": "default", "features": ["default"]},
    "is_active_user": True,
    "use_magic_link": True,
    "token_valid_after": {"$date": "2021-10-13T14:27:09.973Z"},
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
        "score": 1,
        "submission_date": {"$date": "2021-10-13T16:53:11.039Z"},
        "suitability_version": 4,
    },
    "cel_phone": "11987450574",
    "cpf": "63025165014",
    "is_cvm_qualified_investor": False,
    "is_us_person": False,
    "marital": {"status": "not_married", "spouse": None},
    "us_tin": None,
    "register_analyses": StoneAgeRegisterAnalyses.SEND_RESPONSES.value,
    "stone_age_contract_uuid": "6d6e2a04-00e4-11ec-9a03-0242ac130003",
}

onboarding_steps_success_status_code = 200

on_boarding_steps = {
    "finished": "finished",
    "suitability_step": "suitability_step",
    "user_identifier_data_step": "user_identifier_data_step",
    "user_selfie_step": "user_selfie_step",
    "user_complementary_step": "user_complementary_step",
    "user_quiz_step": "user_quiz_step",
    "user_electronic_signature": "user_electronic_signature",
}

stub_bucket_name = "dtvm-terms"

stub_buckets = {
    "ResponseMetadata": {
        "RequestId": "EZ86M09ZCAMZ31GC",
        "HostId": "+5r6/mUKtAUj1aiPa+s96CAbn3ndiTD/imrMm5w8neuPPgmAEGxo5dQcKUWd5TN6LVPXHx6oWPU=",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amz-id-2": "+5r6/mUKtAUj1aiPa+s96CAbn3ndiTD/imrMm5w8neuPPgmAEGxo5dQcKUWd5TN6LVPXHx6oWPU=",
            "x-amz-request-id": "EZ86M09ZCAMZ31GC",
            "date": "Wed, 13 Oct 2021 16:32:49 GMT",
            "content-type": "application/xml",
            "transfer-encoding": "chunked",
            "server": "AmazonS3",
        },
        "RetryAttempts": 0,
    },
    "Buckets": [
        {"Name": "auth-gateway", "CreationDate": datetime(2021, 6, 24, 14, 58, 6)},
        {
            "Name": "bucket-hml-sinacor-logs",
            "CreationDate": datetime(2021, 6, 10, 19, 15, 36),
        },
        {
            "Name": "cf-templates-ocofn59bu6bh-sa-east-1",
            "CreationDate": datetime(2021, 6, 14, 13, 20, 52),
        },
        {
            "Name": "dtvm-bank-statement",
            "CreationDate": datetime(2021, 9, 14, 11, 34, 33),
        },
        {
            "Name": "dtvm-custody-transfer-term",
            "CreationDate": datetime(2021, 8, 26, 14, 33, 54),
        },
        {"Name": "dtvm-terms", "CreationDate": datetime(2021, 6, 2, 20, 2, 35)},
        {"Name": "dtvm-user-self", "CreationDate": datetime(2021, 6, 22, 11, 49, 40)},
        {"Name": "dtvm-users-files", "CreationDate": datetime(2021, 6, 2, 17, 11, 2)},
        {"Name": "dump-rds-oracle", "CreationDate": datetime(2021, 8, 5, 18, 20, 1)},
        {"Name": "dumpb3", "CreationDate": datetime(2021, 6, 17, 12, 37, 29)},
        {
            "Name": "mongo-test-prod-dev-serverlessdeploymentbucket-j3ji2wtyfa8j",
            "CreationDate": datetime(2021, 5, 27, 14, 42, 35),
        },
        {
            "Name": "mongo-test-prod-dev-serverlessdeploymentbucket-ji6p2wsbkd4i",
            "CreationDate": datetime(2021, 5, 27, 15, 7, 43),
        },
        {
            "Name": "news-provider-dev-serverlessdeploymentbucket-1entzeedx2d7e",
            "CreationDate": datetime(2021, 8, 5, 18, 36, 59),
        },
        {
            "Name": "news-provider-production-serverlessdeploymentbuck-u6bu1un0uhdt",
            "CreationDate": datetime(2021, 5, 27, 17, 42, 34),
        },
        {
            "Name": "persephone-client",
            "CreationDate": datetime(2021, 6, 10, 11, 59, 44),
        },
        {"Name": "sta-tfstate", "CreationDate": datetime(2021, 6, 28, 12, 26, 38)},
        {
            "Name": "time-series-historical-c-serverlessdeploymentbuck-17316elupfp4w",
            "CreationDate": datetime(2021, 6, 28, 18, 53, 5),
        },
        {
            "Name": "time-series-historical-c-serverlessdeploymentbuck-j80yx6f7zvmw",
            "CreationDate": datetime(2021, 6, 29, 12, 21, 42),
        },
        {
            "Name": "typescript-test-lambda-d-serverlessdeploymentbuck-1xuu0ec2w562k",
            "CreationDate": datetime(2021, 6, 28, 22, 6, 51),
        },
    ],
    "Owner": {
        "DisplayName": "billing",
        "ID": "ddadb26827b39dff7bf757ada428f98b7a1f69409bd241069e1db04bf4aefd19",
    },
}
