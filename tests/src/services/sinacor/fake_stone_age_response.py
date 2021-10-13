import datetime

fake_response = {
    "proposal_id": "21b00324-d240-4c61-a79c-9a0bd7ff6e45",
    "data": {
        "status": "OK",
        "decision": "APROVADO",
        "gender": {"source": "PH3W", "value": "M"},
        "email": {"source": "PH3W", "value": "lala@l.com.br"},
        "name": {"source": "PH3W", "value": "Antonio Armando Piaui"},
        "birth_date": {
            "source": "PH3W",
            "value": datetime.datetime(1993, 7, 12, 0, 0),
        },
        "birthplace": {
            "nationality": {"source": "PH3W", "value": 1},
            "country": {"source": "PH3W", "value": "BRA"},
            "state": {"source": "PH3W", "value": "GO"},
            "city": {"source": "PH3W", "value": "FORMOSA"},
            "id_city": {"source": "PH3W", "value": 968},
        },
        "mother_name": {"source": "PH3W", "value": "Antonia dos Santos Jr."},
        "identifier_document": {
            "type": {"source": "PH3W", "value": "RG"},
            "document_data": {
                # GENERATE
                "number": {
                    "source": "PH3W",
                    "value": int("37.059.072-7".replace(".", "").replace("-", "")),
                },
                "date": {
                    "source": "PH3W",
                    "value": datetime.datetime(2018, 7, 12, 16, 31, 31),
                },
                "state": {"source": "PH3W", "value": "SP"},
                "issuer": {"source": "PH3W", "value": "SSP"},
            },
        },
        "address": {
            "country": {"source": "PH3W", "value": "BRA"},
            "street_name": {"source": "PH3W", "value": "R. 2"},
            "number": {"source": "PH3W", "value": "126"},
            "neighborhood": {"source": "PH3W", "value": "Formosinha"},
            "state": {"source": "PH3W", "value": "GO"},
            "city": {"source": "PH3W", "value": "FORMOSA"},
            "id_city": {"source": "PH3W", "value": 968},
            "zip_code": {"source": "PH3W", "value": 73813190},
            "phone_number": {"source": "PH3W", "value": "11952909954"},
        },
        "occupation": {
            "activity": {"source": "PH3W", "value": 304},
            "company": {
                "cnpj": {"source": "PH3W", "value": "25811052000179"},
                "name": {"source": "PH3W", "value": "Tudo nosso .com.br"},
            },
        },
        "assets": {
            "patrimony": {"source": "PH3W", "value": 5446456.44},
            "income": {"source": "PH3W", "value": 5446456.44},
            "income_tax_type": {"source": "PH3W", "value": 1},
            "date": {
                "source": "PH3W",
                "value": datetime.datetime(1993, 7, 12, 0, 0),
            },
        },
        "education": {
            "level": {"source": "PH3W", "value": "Médio incompleto"},
            "course": {"source": "PH3W", "value": "Escola James Riwbon"},
        },
        "politically_exposed_person": {
            "is_politically_exposed_person": {"source": "PH3W", "value": False}
        },
        "date_of_acquisition": {
            "source": "PH3W",
            "value": datetime.datetime(2018, 7, 12, 16, 31, 31),
        },
        "connected_person": {"source": "PH3W", "value": "N"},
        "person_type": {"source": "PH3W", "value": "F"},
        "client_type": {"source": "PH3W", "value": 1},
        "investor_type": {"source": "PH3W", "value": 101},
        "cosif_tax_classification": {"source": "PH3W", "value": 21},
        "marital": {
            "status": {"source": "PH3W", "value": 5},
            "spouse": {
                "cpf": {"value": "16746756076", "source": "REQUEST"},
                "name": {
                    "value": "Flavio Antobio Felicio",
                    "source": "REQUEST",
                },
                "nationality": {"value": 1, "source": "REQUEST"},
            },
        },
        "cpf": {"source": "PH3W", "value": "43056808820"},
        "self_link": {"source": "PH3W", "value": "http://self_user.jpg"},
        "is_us_person": {"source": "PH3W", "value": True},
        "us_tin": {"source": "PH3W", "value": 126516515},
        "irs_sharing": {"source": "PH3W", "value": True},
        "father_name": {"source": "PH3W", "value": "Antonio dos Santos"},
        "midia_person": {"source": "PH3W", "value": False},
        "person_related_to_market_influencer": {
            "source": "PH3W",
            "value": False,
        },
        "court_orders": {"source": "PH3W", "value": False},
        "lawsuits": {"source": "PH3W", "value": False},
        "fund_admin_registration": {"source": "PH3W", "value": False},
        "investment_fund_administrators_registration": {
            "source": "PH3W",
            "value": False,
        },
        "register_auditors_securities_commission": {
            "source": "PH3W",
            "value": False,
        },
        "registration_of_other_market_participants_securities_commission": {
            "source": "PH3W",
            "value": False,
        },
        "foreign_investors_register_of_annex_iv_not_registered": {
            "source": "PH3W",
            "value": False,
        },
        "registration_of_foreign_investors_securities_commission": {
            "source": "PH3W",
            "value": False,
        },
        "registration_representative_of_nonresident_investors_securities_commission": {
            "source": "PH3W",
            "value": False,
        },
    },
}
