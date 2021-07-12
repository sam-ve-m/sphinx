# STANDARD LIBS
from datetime import datetime


def get_prospect_user_template_with_data(payload: dict) -> dict:
    return {
        "user_email": payload.get("email"),
        "name": payload.get("name"),
        "create_user_time_stamp": int(datetime.utcnow().timestamp()),
    }


def get_user_signed_term_template_with_data(payload: dict, file_type: str) -> dict:
    version = payload.get("terms").get(file_type).get("version")
    return {
        "metadata": {
            "user_email": payload.get("email"),
        },
        "term_type": file_type,
        "term_version": f"v{version}",
        "user_accept": True,
        "term_answer_time_stamp": int(datetime.utcnow().timestamp()),
    }


def get_table_response_template_with_data(payload: dict) -> dict:
    return {
        "stone_age_id": payload.get("uuid"),
        "user_id": payload.get("email"),
        "status": payload.get("status"),
        "cpf": payload.get("cpf"),
    }


def get_user_suitability_template_with_data(payload: dict) -> dict:
    return {
        "metadata": {
            "user_email": payload.get("email"),
        },
        "form": _normalize_form_helper(payload.get("answers")),
        "version": payload.get("suitability_version"),
        "score": payload.get("score"),
        "profile": "Agressivo",
        "create_suitability_time_stamp": payload.get("suitability_submission_date"),
    }


def _normalize_form_helper(form: list) -> list:
    new_list = list()
    for item in form:
        new_list.append(
            {"question_id": item.get("question_id"), "answer": item.get("answer")}
        )
    return new_list


def get_user_account_template_with_data(payload: dict) -> dict:
    user_data = payload.get("user_data")
    marital = user_data.get("marital")
    return {
        "metadata": {
            "user_email": user_data.get("email"),
        },
        "user_registry_data": {
            "provided_by_user": {
                "name": user_data.get("name"),
                "marital": {
                    "status": marital.get("status"),
                    "spouse": {
                        "spouse_name": marital.get("spouse").get("name"),
                        "nationality": marital.get("spouse").get("nationality"),
                        "cpf": marital.get("spouse").get("cpf"),
                    },
                },
                "cpf": user_data.get("cpf"),
                "email": user_data.get("email"),
                "can_be_managed_by_third_party_operator": user_data.get(
                    "can_be_managed_by_third_party_operator"
                ),
                "is_managed_by_third_party_operator": user_data.get(
                    "is_managed_by_third_party_operator"
                ),
                "third_party_operator": {
                    "is_third_party_operator": user_data.get(
                        "third_party_operator"
                    ).get("is_third_party_operator"),
                    "details": {},
                    "third_party_operator_email": "",
                },
                "is_cvm_qualified_investor": user_data.get("is_cvm_qualified_investor"),
                "us_person": {
                    "is_us_person": user_data.get("is_us_person"),
                    "us_tin": user_data.get("us_tin"),
                },
            },
            "provided_by_bureaux": payload.get("stone_age_user_data"),
        },
        "create_user_time_stamp": int(datetime.utcnow().timestamp()),
        "create_digital_signature_time_stamp": int(datetime.utcnow().timestamp()),
    }
