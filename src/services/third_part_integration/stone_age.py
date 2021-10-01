# OUTSIDE LIBRARIES
from src.core.interfaces.repositories.file_repository.interface import IFile
from src.repositories.file.enum.user_file import UserFileType
from src.infrastructures.env_config import config
import requests
import logging
from typing import Optional
import json

from src.exceptions.exceptions import InternalServerError


class StoneAge:
    @staticmethod
    def get_user_quiz(user_identifier_data: dict) -> dict:
        """this functions will send the user_identifier_data and will return a quiz"""
        response = StoneAge.run_sync_stone_age_app_entry_point(
            entry_point="onbPfP1Post", body=user_identifier_data
        )
        return response

    @staticmethod
    def send_user_quiz_responses(send_quiz_request: dict) -> Optional[dict]:
        response = StoneAge.run_sync_stone_age_app_entry_point(
            entry_point="onbPfP2Post", body=send_quiz_request
        )
        return response

    @staticmethod
    def get_only_values_from_user_data(user_data: dict, new_user_data=dict()) -> dict:
        for key, value in user_data.items():
            if type(value) == dict and "source" in value and "value" in value:
                new_user_data.update({key: value.get("value")})
            elif type(value) == dict:
                new_user_data[key] = dict()
                StoneAge.get_only_values_from_user_data(
                    value, new_user_data=new_user_data[key]
                )
            else:
                new_user_data.update({key: value})
        return new_user_data

    @staticmethod
    def run_sync_stone_age_app_entry_point(entry_point: str, body: dict):

        motor_url = config("STONE_AGE_MOTOR_URL")
        app_name = config("STONE_AGE_MOTOR_APP_NAME")
        api_version = config("STONE_AGE_MOTOR_VERSION")

        motor_app_entry_point_url = (
            f"{motor_url}/api/{api_version}/RunSync/{app_name}/{entry_point}?dev=true"
        )
        response = StoneAge.get_stone_age_iam()
        cookies = StoneAge.get_stone_age_auth_cookie(response)

        request_session = requests.Session()
        request_session.headers.update({"Content-type": "application/json"})
        request_session.cookies["access_token"] = cookies["access_token"]

        # TODO: remove this
        # if body.get('marital_status'):
        #     body['marital_status'] = 1

        body_dumps = json.dumps(body)
        response = request_session.post(url=motor_app_entry_point_url, data=body_dumps)

        if response.status_code == 200:
            data = response.json()
            if data["successful"]:
                return data

        logger = logging.getLogger(config("LOG_NAME"))
        response_error_stone_age = f"Stone age return status code: {response.status_code}, error response: {response}"
        logger.info(msg=response_error_stone_age)
        raise InternalServerError("common.process_issue")

    @staticmethod
    def list_stone_age_apps():

        motor_url = config("STONE_AGE_MOTOR_URL")
        api_version = config("STONE_AGE_MOTOR_VERSION")
        list_app_end_point_url = f"{motor_url}/api/{api_version}/apps"

        response = StoneAge.get_stone_age_iam()
        cookies = StoneAge.get_stone_age_auth_cookie(response)

        request_session = requests.Session()
        request_session.headers.update({"Content-type": "application/json"})

        request_session.cookies["access_token"] = cookies["access_token"]
        response = request_session.get(url=list_app_end_point_url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            logger = logging.getLogger(config("LOG_NAME"))
            response_error_stone_age = f"Stone age return status code: {response.status_code}, error response: {response.text}"
            logger.info(msg=response_error_stone_age)

    @staticmethod
    def get_stone_age_app_by_name(app_name: str):

        motor_url = config("STONE_AGE_MOTOR_URL")
        api_version = config("STONE_AGE_MOTOR_VERSION")
        get_app_by_name_end_point_url = f"{motor_url}/api/{api_version}/apps/{app_name}"

        response = StoneAge.get_stone_age_iam()
        cookies = StoneAge.get_stone_age_auth_cookie(response)

        request_session = requests.Session()
        request_session.headers.update({"Content-type": "application/json"})

        request_session.cookies["access_token"] = cookies["access_token"]
        response = request_session.get(url=get_app_by_name_end_point_url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            logger = logging.getLogger(config("LOG_NAME"))
            response_error_stone_age = f"Stone age return status code: {response.status_code}, error response: {response.text}"
            logger.info(msg=response_error_stone_age)

    @staticmethod
    def get_stone_age_iam():

        iam_url = config("STONE_AGE_IAM_URL")
        iam_token_end_point = f"{iam_url}/api/token"

        stone_age_user_name = config("STONE_AGE_USERNAME")
        stone_age_user_password = config("STONE_AGE_PASSWORD")
        stone_age_credentials = {
            "username": stone_age_user_name,
            "password": stone_age_user_password,
        }

        response = requests.post(url=iam_token_end_point, data=stone_age_credentials)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            logger = logging.getLogger(config("LOG_NAME"))
            error_response = response.json()
            response_error_stone_age = f"Stone age return status code: {response.status_code}, error response: {error_response}"
            logger.info(msg=response_error_stone_age)

    @staticmethod
    def get_stone_age_auth_cookie(iam_response: dict):

        access_token = iam_response["access_token"]
        refresh_token = iam_response["refresh_token"]
        has_refresh = iam_response["has_refresh"]
        user_info = iam_response["user_info"]
        app_info = iam_response["app_info"]

        headers = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "has_refresh": has_refresh,
            "user_info": user_info,
            "app_info": app_info,
        }

        return headers

    @staticmethod
    def get_stone_age_auth_header():

        bearer_token = config("STONE_AGE_BEARER_TOKEN")

        headers = {
            "Bearer": bearer_token,
        }

        return headers

    @staticmethod
    def get_user_identifier_data(
        payload: dict,
        current_user: dict,
        current_user_marital: dict,
        file_repository: IFile,
    ):
        user_identifier_data = {
            "email": current_user.get("email"),
            "cpf": current_user.get("cpf"),
            "cel_phone": current_user.get("cel_phone"),
            "marital_status": current_user_marital.get("status"),
            "is_us_person": current_user.get("is_us_person"),
            "uri_selfie": file_repository.get_user_selfie(
                file_type=UserFileType.SELF, user_email=current_user.get("email")
            ),
            "device": payload.get("device_information"),
        }

        current_user_is_us_person = current_user.get("is_us_person")

        if current_user_is_us_person:
            user_identifier_data["us_tin"] = current_user.get("us_tin")

        spouse = current_user_marital.get("spouse")

        if spouse is not None:
            user_identifier_data["spouse"] = spouse

        return user_identifier_data

    @staticmethod
    def get_user_send_quiz_request(payload: dict, current_user: dict):
        send_quiz_request = {
            "proposalId": current_user.get("stone_age_proposal_id"),
            "email": current_user.get("email"),
            "cpf": current_user.get("cpf"),
            "cel_phone": current_user.get("cel_phone"),
            "responses": payload.get("quiz"),
            "device": payload.get("device_information"),
        }

        return send_quiz_request
