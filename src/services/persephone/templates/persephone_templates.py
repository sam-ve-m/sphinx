# STANDARD LIBS
from datetime import datetime
from typing import List


def get_prospect_user_template_with_data(payload: dict) -> dict:
    return {
        "unique_id": payload.get("unique_id"),
        "email": payload.get("email"),
        "nick_name": payload.get("nick_name"),
        "create_user_time_stamp": int(datetime.utcnow().timestamp()),
    }


def get_user_identifier_data_schema_template_with_data(payload: dict) -> dict:
    return {
        "unique_id": payload["unique_id"],
        "cpf": payload["cpf"],
        "cel_phone": payload["phone"],
        "tax_residences": payload["tax_residences"],
    }


def get_user_selfie_schema_template_with_data(file_path: str, unique_id: str) -> dict:
    return {
        "unique_id": unique_id,
        "file_path": file_path,
    }


def get_user_politically_exposed_schema_template_with_data(
    politically_exposed: bool, unique_id: str, politically_exposed_names: List[str]
) -> dict:
    return {
        "unique_id": unique_id,
        "politically_exposed": politically_exposed,
        "politically_exposed_names": politically_exposed_names,
    }


def get_user_exchange_member_schema_template_with_data(
    exchange_member: bool, unique_id: str
) -> dict:
    return {
        "unique_id": unique_id,
        "exchange_member": exchange_member,
    }


def get_user_time_experience_schema_template_with_data(
    time_experience: str, unique_id: str
) -> dict:
    return {
        "unique_id": unique_id,
        "time_experience": time_experience,
    }


def get_user_tax_residences_schema_template_with_data(
    tax_residences: str, unique_id: str
) -> dict:
    return {
        "unique_id": unique_id,
        "tax_residences": tax_residences,
    }


def get_w8_form_confirmation_schema_template_with_data(
    w8_form_confirmation: str, unique_id: str
) -> dict:
    return {
        "unique_id": unique_id,
        "w8_form_confirmation": w8_form_confirmation,
    }


def get_user_employ_for_schema_template_with_data(
    employ_status: str,
    employ_type: str,
    employ_position: str,
    employ_company_name: str,
    unique_id: str,
) -> dict:
    return {
        "unique_id": unique_id,
        "employ_status": employ_status,
        "employ_type": employ_type,
        "employ_position": employ_position,
        "employ_company_name": employ_company_name,
    }


def get_user_company_director_schema_template_with_data(
    company_director: bool,
    user_is_company_director_of: str,
    unique_id: str,
    company_ticker_that_user_is_director_of: str,
) -> dict:
    return {
        "unique_id": unique_id,
        "company_director": company_director,
        "user_is_company_director_of": user_is_company_director_of,
        "company_ticker_that_user_is_director_of": company_ticker_that_user_is_director_of,
    }


def get_user_document_schema_template_with_data(
    path_document_front: str, path_document_back: str, unique_id: str
) -> dict:
    return {
        "unique_id": unique_id,
        "path_document_front": path_document_front,
        "path_document_back": path_document_back,
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


def unique_id(output: dict, email: str, device_information: dict) -> dict:
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
        "unique_id": previous_state.get("unique_id"),
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


def get_user_set_electronic_signature_schema_template_with_data(
    payload: dict, unique_id: str
) -> dict:
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


def get_user_signed_terms_template_with_data(
    terms_update: dict, payload: dict, files_type: List[str]
) -> dict:
    return {
        "unique_id": payload.get("unique_id"),
        "terms_type": files_type,
        "terms_update": terms_update,
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


def get_user_fill_suitability(
    answers: dict, score: float, suitability_version: int, unique_id: str
) -> dict:
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
    return {
        "unique_id": unique_id,
        "jwt": jwt,
        "device_information": device_information,
    }
