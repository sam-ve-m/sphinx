# STANDARD LIBS
from datetime import datetime


def get_prospect_user_template_with_data(payload: dict) -> dict:
    return {
        "user_email": payload.get("email"),
        "nick_name": payload.get("nick_name"),
        "create_user_time_stamp": int(datetime.utcnow().timestamp()),
    }


def get_user_identifier_data_schema_template_with_data(payload: dict) -> dict:
    return {
        "user_email": payload.get("email"),
        "cpf": payload.get("cpf"),
        "cel_phone": payload.get("cel_phone"),
    }


def get_user_selfie_schema_template_with_data(file_path: str, email: str) -> dict:
    return {
        "user_email": email,
        "file_path": file_path,
    }


def get_user_authentication_template_with_data(payload: dict) -> dict:
    return {
        "user_email": payload.get("email"),
        "is_active_user": payload.get("is_active_user"),
        "scope": payload.get("scope"),
    }


def get_user_complementary_data_schema_template_with_data(payload: dict) -> dict:
    payload["marital"]["status"] = payload["marital"]["status"].value
    return {
        "user_email": payload.get("email"),
        "is_us_person": payload.get("is_us_person"),
        "us_tin": payload.get("us_tin"),
        "is_cvm_qualified_investor": payload.get("is_cvm_qualified_investor"),
        "marital": payload.get("marital"),
    }


def get_user_quiz_from_stoneage_schema_template_with_data(
    output: dict, email: str, device_information: dict
) -> dict:
    return {
        "user_email": email,
        "output": output,
        "device_information": device_information,
    }


def get_user_quiz_response_from_stoneage_schema_template_with_data(
    quiz: dict, response: dict, email: str, device_information: dict
) -> dict:
    return {
        "user_email": email,
        "quiz": quiz,
        "response": response,
        "device_information": device_information,
    }


def get_user_change_or_reset_electronic_signature_schema_template_with_data(
    previous_state: dict, new_state: dict
) -> dict:
    return {
        "user_email": new_state.get("email"),
        "previous_electronic_signature": previous_state.get("electronic_signature"),
        "previous_is_blocked_electronic_signature": previous_state.get(
            "is_blocked_electronic_signature"
        ),
        "previous_electronic_signature_wrong_attempts": previous_state.get(
            "electronic_signature_wrong_attempts"
        ),
        "new_electronic_signature": new_state.get("electronic_signature"),
        "new_is_blocked_electronic_signature": new_state.get(
            "is_blocked_electronic_signature"
        ),
        "new_electronic_signature_wrong_attempts": new_state.get(
            "electronic_signature_wrong_attempts"
        ),
    }


def get_user_set_electronic_signature_schema_template_with_data(payload: dict) -> dict:
    return {
        "user_email": payload.get("email"),
        "electronic_signature": payload.get("electronic_signature"),
        "is_blocked_electronic_signature": payload.get(
            "is_blocked_electronic_signature"
        ),
        "electronic_signature_wrong_attempts": payload.get(
            "electronic_signature_wrong_attempts"
        ),
    }


def get_user_update_register_schema_template_with_data(
    email: str, modified_register_data: dict, update_customer_registration_data: dict
) -> dict:
    return {
        "user_email": email,
        "modified_register_data": modified_register_data,
        "update_customer_registration_data": update_customer_registration_data,
    }


def get_user_thebes_hall_schema_template_with_data(
    jwt: str, email: str, has_trade_allowed: dict, device_information: dict
) -> dict:
    return {
        "user_email": email,
        "jwt": jwt,
        "has_trade_allowed": has_trade_allowed,
        "device_information": device_information,
    }


def get_create_electronic_signature_session_schema_template_with_data(
    mist_session: str, email: str, allowed: bool
) -> dict:
    return {
        "user_email": email,
        "mist_session": mist_session,
        "allowed": allowed,
    }


def get_user_signed_term_template_with_data(payload: dict, file_type: str) -> dict:
    version = payload.get("terms").get(file_type).get("version")
    return {
        "user_email": payload.get("email"),
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
        "user_email": payload.get("email"),
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


def get_user_account_template_with_data(payload: dict, email: str) -> dict:
    return {"user_email": email, "bureau_data": payload}


def get_user_logout_template_with_data(
    jwt: dict, email: str, device_information: dict
) -> dict:
    return {"user_email": email, "jwt": jwt, "device_information": device_information}
