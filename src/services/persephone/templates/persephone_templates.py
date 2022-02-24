# STANDARD LIBS
from datetime import datetime


def get_prospect_user_template_with_data(payload: dict) -> dict:
    return {
        "unique_id": payload.get("unique_id"),
        "email": payload.get("email"),
        "nick_name": payload.get("nick_name"),
        "create_user_time_stamp": int(datetime.utcnow().timestamp()),
    }


def get_user_identifier_data_schema_template_with_data(payload: dict) -> dict:
    return {
        "unique_id": payload.get("unique_id"),
        "cpf": payload.get("cpf"),
        "cel_phone": payload.get("phone"),
        "tax_residences": payload.get("tax_residences")
    }


def get_user_selfie_schema_template_with_data(file_path: str, unique_id: str) -> dict:
    return {
        "unique_id": unique_id,
        "file_path": file_path,
    }


def get_user_authentication_template_with_data(payload: dict) -> dict:
    return {
        "unique_id": payload.get("unique_id"),
        "is_active_user": payload.get("is_active_user"),
        "scope": payload.get("scope"),
    }


def get_user_complementary_data_schema_template_with_data(payload: dict) -> dict:
    return {
        "unique_id": payload.get("unique_id"),
        "marital": payload.get("marital"),
    }


def unique_id(
    output: dict, email: str, device_information: dict
) -> dict:
    return {
        "unique_id": unique_id,
        "output": output,
        "device_information": device_information,
    }


def get_user_quiz_response_from_stoneage_schema_template_with_data(
    quiz: dict, response: dict, unique_id: str, device_information: dict
) -> dict:
    return {
        "unique_id": unique_id,
        "quiz": quiz,
        "response": response,
        "device_information": device_information,
    }


def get_user_change_or_reset_electronic_signature_schema_template_with_data(
    previous_state: dict, new_state: dict
) -> dict:
    return {
        "unique_id": new_state.get("unique_id"),
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


def get_user_set_electronic_signature_schema_template_with_data(payload: dict, unique_id: str) -> dict:
    return {
        "unique_id": unique_id,
        "electronic_signature": payload.get("electronic_signature"),
        "is_blocked_electronic_signature": payload.get(
            "is_blocked_electronic_signature"
        ),
        "electronic_signature_wrong_attempts": payload.get(
            "electronic_signature_wrong_attempts"
        ),
    }


def get_user_update_register_schema_template_with_data(
    unique_id: str,
    modified_register_data: dict,
    update_customer_registration_data: dict,
) -> dict:
    return {
        "unique_id": unique_id,
        "modified_register_data": modified_register_data,
        "update_customer_registration_data": update_customer_registration_data,
    }


def get_user_thebes_hall_schema_template_with_data(
    jwt: str, unique_id: str, jwt_payload_data: dict, device_information: dict
) -> dict:
    return {
        "unique_id": unique_id,
        "jwt": jwt,
        "jwt_payload_data": jwt_payload_data,
        "device_information": device_information,
    }


def get_create_electronic_signature_session_schema_template_with_data(
    mist_session: str, unique_id: str, allowed: bool
) -> dict:
    return {
        "unique_id": unique_id,
        "mist_session": mist_session,
        "allowed": allowed,
    }


def get_user_signed_term_template_with_data(term_version: int, payload: dict, file_type: str) -> dict:
    return {
        "unique_id": payload.get("unique_id"),
        "term_type": file_type,
        "term_version": f"v{term_version}",
        "user_accept": True,
        "term_answer_time_stamp": int(datetime.utcnow().timestamp()),
    }


def get_table_response_template_with_data(payload: dict) -> dict:
    return {
        "stone_age_id": payload.get("proposal_id"),
        "unique_id": payload.get("unique_id"),
        "status": payload.get("status"),
        "cpf": payload.get("identifier_document").get("cpf"),
    }


def get_user_suitability_template_with_data(payload: dict) -> dict:
    return {
        "unique_id": payload.get("unique_id"),
        "form": _normalize_form_helper(payload.get("answers")),
        "version": payload.get("suitability_version"),
        "score": payload.get("score"),
        "profile": "Agressivo",
        "create_suitability_time_stamp": payload.get("suitability_submission_date"),
    }


def get_user_fill_suitability(answers: dict, score: float, suitability_version: int, unique_id: str) -> dict:
    return {
        "answers": answers,
        "score": score,
        "suitability_version": suitability_version,
        "suitability_submission_date": int(datetime.utcnow().timestamp()),
        "unique_id": unique_id,
    }


def _normalize_form_helper(form: list) -> list:
    new_list = list()
    for item in form:
        new_list.append(
            {"question_id": item.get("question_id"), "answer": item.get("answer")}
        )
    return new_list


def get_user_account_template_with_data(payload: dict, unique_id: str) -> dict:
    return {"unique_id": unique_id, "bureau_data": payload}


def get_user_logout_template_with_data(
    jwt: dict, unique_id: str, device_information: dict
) -> dict:
    return {"unique_id": unique_id, "jwt": jwt, "device_information": device_information}
