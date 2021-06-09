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
            "status": {"origin": "XXX", "value": "R. imbuia"},
            "userData": {
                "name": {"origin": "XXX", "value": "R. imbuia"},
                "maritalStatus": {"origin": "XXX", "value": "R. imbuia"},
                "spouse": {
                    "name": {"origin": "XXX", "value": "R. imbuia"},
                    "nationality": {"origin": "XXX", "value": "R. imbuia"},
                    "cpf": {"origin": "XXX", "value": 123},
                },
                "cpf": {"origin": "XXX", "value": 123},
                "email": {"origin": "XXX", "value": "R. imbuia"},
                "gender": {"origin": "XXX", "value": "R. imbuia"},
                "birthDate": {"origin": "XXX", "value": "123"},
                "naturalness": {"origin": "XXX", "value": "R. imbuia"},
                "nationality": {"origin": "XXX", "value": "R. imbuia"},
                "motherName": {"origin": "XXX", "value": "R. imbuia"},
                "identifierDocument": {
                    "type": {"origin": "XXX", "value": "R. imbuia"},
                    "documentData": {
                        "number": {"origin": "XXX", "value": "R. imbuia"},
                        "date": {"origin": "XXX", "value": "R. imbuia"},
                        "state": {"origin": "XXX", "value": "R. imbuia"},
                        "issuer": {"origin": "XXX", "value": "R. imbuia"},
                    },
                },
                "address": {
                    "streetName": {"origin": "XXX", "value": "R. imbuia"},
                    "number": {"origin": "XXX", "value": 123},
                    "state": {"origin": "XXX", "value": "R. imbuia"},
                    "city": {"origin": "XXX", "value": "R. imbuia"},
                    "zipCode": {"origin": "XXX", "value": "R. imbuia"},
                    "phone_number": {"origin": "XXX", "value": "R. imbuia"},
                },
                "occupation": {
                    "status": {"origin": "XXX", "value": "R. imbuia"},
                    "company": {
                        "name": {"origin": "XXX", "value": "R. imbuia"},
                        "cpnj": {"origin": "XXX", "value": 123},
                    },
                },
                "assets": {
                    "patrimony": {"origin": "XXX", "value": 123},
                    "income": {"origin": "XXX", "value": 123},
                },
                "education": {
                    "level": {"origin": "XXX", "value": "R. imbuia"},
                    "course": {"origin": "XXX", "value": "R. imbuia"},
                },
                "documentsPhotos": {
                    "identifier_document": {"origin": "XXX", "value": "R. imbuia"},
                    "address_document": {"origin": "XXX", "value": "R. imbuia"},
                },
                "politicallyExposedPerson": {"origin": "XXX", "value": True},
            },
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
            if type(value) == dict and "origin" in value and "value" in value:
                new_user_data.update({key: value.get("value")})
            elif type(value) == dict:
                new_user_data[key] = dict()
                StoneAge.get_only_values_from_user_data(
                    value, new_user_data=new_user_data[key]
                )
            else:
                new_user_data.update({key: value})
        return new_user_data
