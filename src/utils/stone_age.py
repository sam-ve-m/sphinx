# OUTSIDE LIBRARIES
from src.utils.env_config import config
import requests
import logging
from typing import Optional
import json

from src.exceptions.exceptions import InternalServerError


class StoneAge:
    @staticmethod
    def get_user_quiz(user_identifier_data: dict) -> dict:
        """this functions will send the user_identifier_data and will return a quiz"""

        # TODO: Get cpf from user identifier data
        # response = StoneAge.run_sync_stone_age_app_entry_point(
        #     entry_point="mock", body={"cpf": 123}
        # )
        response = {
            "output": dict(),
            "uuid": "1231234-asdfq34-5t-34564236",
            "decision": None,
        }
        response["output"].update(
            {
                "quiz": [
                    {
                        "questionId": "39663338-fad5-11eb-9a03-0242ac130003",
                        "question": "Qual desse números é seu?",
                        "options": [
                            {
                                "value": "+5511952896753",
                                "optionId": "428dc8b8-fad5-11eb-9a03-0242ac130003",
                            },
                            {
                                "value": "+5511952006753",
                                "optionId": "472d1fcc-fad5-11eb-9a03-0242ac130003",
                            },
                            {
                                "value": "+5511933896753",
                                "optionId": "4b502fcc-fad5-11eb-9a03-0242ac130003",
                            },
                        ],
                    },
                    {
                        "questionId": "b9e0546e-252c-4380-8ce0-df532a5e6c78",
                        "question": "Qual desses endereções é o seu?",
                        "options": [
                            {
                                "value": "R.jagunça 999, Cabrobro",
                                "optionId": "428dc8b8-fad5-11eb-9a03-0242ac130003",
                            },
                            {
                                "value": "R. jabuti aqueroso 43, Cabuti",
                                "optionId": "472d1fcc-fad5-11eb-9a03-0242ac130003",
                            },
                            {
                                "value": "R. antoni carlos 123, São Pedro",
                                "optionId": "4b502fcc-fad5-11eb-9a03-0242ac130003",
                            },
                        ],
                    },
                ]
            }
        )

        return response

    @staticmethod
    def send_user_quiz_responses(quiz: dict) -> Optional[dict]:
        # TODO: Change body to quiz
        # response = StoneAge.run_sync_stone_age_app_entry_point(
        #     entry_point="mock", body={"cpf": 123}
        # )
        response = {
            "output": dict(),
            "uuid": "1231234-asdfq34-5t-34564236",
            "decision": "MESA",
        }
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
            f"{motor_url}/api/{api_version}/RunSync/{app_name}/{entry_point}"
        )
        response = StoneAge.get_stone_age_iam()
        cookies = StoneAge.get_stone_age_auth_cookie(response)

        request_session = requests.Session()
        request_session.headers.update({"Content-type": "application/json"})
        request_session.cookies["access_token"] = cookies["access_token"]

        body_dumps = json.dumps(body)
        response = request_session.post(url=motor_app_entry_point_url, data=body_dumps)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
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
