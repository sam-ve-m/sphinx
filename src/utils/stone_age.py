# OUTSIDE LIBRARIES
from decouple import config
import requests
import logging
from typing import Optional


class StoneAge:
    @staticmethod
    def send_user_identifier_data(
        user_identifier_data: dict, requests=requests
    ) -> Optional[list]:
        """this functions will send the user_identifier_data and will return a quiz"""
        return [
            {
                "questionId": "b9e0546e-252c-4380-8ce0-df532a5e6c77",
                "question": "Qual desse números é seu?",
                "options": [
                    {
                        "value": "+5511952896753",
                        "optionId": "b9e1541e-252c-4380-8ce0-df532a5e6c77",
                    },
                    {
                        "value": "+5511952006753",
                        "optionId": "b9e1546e-252c-4480-8ce0-df532a5e6c77",
                    },
                    {
                        "value": "+5511933896753",
                        "optionId": "b9e1546e-252c-4380-8ce0-df532a5y6c77",
                    },
                ],
            },
            {
                "questionId": "b9e0546e-252c-4380-8ce0-df532a5e6c78",
                "question": "Qual desses endereções é o seu?",
                "options": [
                    {
                        "value": "R.jagunça 999, Cabrobro",
                        "optionId": "b9e1541e-252c-4380-8ce0-df532a5e6c77",
                    },
                    {
                        "value": "R. jabuti aqueroso 43, Cabuti",
                        "optionId": "b9e1546e-252c-4480-8ce0-df532a5e6c77",
                    },
                    {
                        "value": "R. antoni carlos 123, São Pedro",
                        "optionId": "b9e1546e-252c-4380-8ce0-df532a5y6c77",
                    },
                ],
            },
        ]
        # try:
        #     response = requests.post(url=config('STONE_AGE_RUN_ENDPOINT'), data=user_identifier_data)
        #     if response.status_code == 200:
        #         data = response.json()
        #         if data.get('successful') and data.get('error') is not True:
        #             return data.get('output').get('quiz')
        # except Exception as e:
        #     logger = logging.getLogger(config("LOG_NAME"))
        #     logger.error(e, exc_info=True)
        # return None

    @staticmethod
    def send_user_quiz_responses(quiz: dict, requests=requests) -> Optional[dict]:
        """this functions will send the user_identifier_data and will return a quiz"""
        return {
            "gender": {"value": "string", "source": "string"},
            "birthDate": {"value": 5465465456456456, "source": "string"},
            "naturalness": {"value": "string", "source": "string"},
            "nationality": {"value": "string", "source": "string"},
            "mother_name": {"value": "string", "source": "string"},
            "identifier_document": {
                "type": {"value": "string", "source": "string"},
                "document_data": {
                    "number": {"value": "string", "source": "string"},
                    "date": {"value": 5456456, "source": "string"},
                    "state": {"value": "string", "source": "string"},
                    "issuer": {"value": "string", "source": "string"},
                },
            },
            "address": {
                "street_name": {"value": "string", "source": "string"},
                "number": {"value": 5464564, "source": "string"},
                "state": {"value": "string", "source": "string"},
                "city": {"value": "string", "source": "string"},
                "zipCode": {"value": "string", "source": "string"},
                "phone_number": {"value": "string", "source": "string"},
            },
            "occupation": {
                "status": {"value": "Assalariado", "source": "string"},
                "company": {
                    "name": {"value": "string", "source": "string"},
                    "cpnj": {"value": 46564564564656544, "source": "string"},
                },
            },
            "assets": {
                "patrimony": {"value": 5446456.44, "source": "string"},
                "income": {"value": 5446456.44, "source": "string"},
            },
            "education": {
                "level": {"value": "Médio incompleto", "source": "string"},
                "course": {"value": "string", "source": "string"},
            },
            "documents_photos": {
                "identifier_document": {"value": "string", "source": "string"},
                "address_document": {"value": "string", "source": "string"},
            },
            "politically_exposed_person": {
                "is_politically_exposed_person": {"value": False, "source": "string"}
            },
            "date_of_acquisition": {"value": 5465465456456456, "source": "string"},
        }
        # try:
        #     response = requests.post(url=config('STONE_AGE_RESPONSE_ENDPOINT'), data=quiz)
        #     if response.status_code == 200:
        #         data = response.json()
        #         if data.get('successful') and data.get('error') is not True:
        #             return data.get('output').get('user_data')
        # except Exception as e:
        #     logger = logging.getLogger(config("LOG_NAME"))
        #     logger.error(e, exc_info=True)
        # return None

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
