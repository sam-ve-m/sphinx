# OUTSIDE LIBRARIES
from fastapi import status

# PERSEPHONE
from src.repositories.sinacor_types.repository import SinacorTypesRepository
from src.domain.sinacor.person_gender import PersonGender
from src.domain.validators.marital_status_app_to_sphinx import (
    MaritalStatusAppToSphinxEnum,
)


class SinaCorTypes:

    @staticmethod
    def get_activity_type(sinacor_types_repository=SinacorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_activity_type()},
        }

    @staticmethod
    def get_nationality(sinacor_types_repository=SinacorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_nationality()},
        }

    @staticmethod
    def get_document_issuing_body(sinacor_types_repository=SinacorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_document_issuing_body()},
        }


    @staticmethod
    def all_in_one(sinacor_types_repository=SinacorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "activity_type": sinacor_types_repository.get_activity_type(),
                "nationality": sinacor_types_repository.get_nationality(),
                "document_issuing_body": sinacor_types_repository.get_document_issuing_body(),
                "document_type": sinacor_types_repository.get_document_type(),
                "country": sinacor_types_repository.get_country()
            },
        }

    @staticmethod
    def get_document_type(sinacor_types_repository=SinacorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_document_type()},
        }

    @staticmethod
    def get_county(payload: dict, sinacor_types_repository=SinacorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "enums": sinacor_types_repository.get_county(
                    country=payload.get("country"), state=payload.get("state")
                )
            },
        }

    @staticmethod
    def get_state(payload: dict, sinacor_types_repository=SinacorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "enums": sinacor_types_repository.get_state(
                    country=payload.get("country")
                )
            },
        }

    @staticmethod
    def get_country(sinacor_types_repository=SinacorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_country()},
        }

    @staticmethod
    def get_gender():
        genders = [
            {"code": PersonGender.MASCULINE.value, "value": "Masculino"},
            {"code": PersonGender.FEMININE.value, "value": "Feminino"},
            {"code": PersonGender.OTHERS.value, "value": "Outro"},
            {"code": PersonGender.NOT_INFORMED.value, "value": "Não desejo informar"},
        ]
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": genders},
        }

    @staticmethod
    def get_marital_status_update():
        marital_status_to_app = [
            {
                "code": MaritalStatusAppToSphinxEnum.SINGLE.value,
                "description": "Solteiro (a)",
            },
            {
                "code": MaritalStatusAppToSphinxEnum.WIDOWER.value,
                "description": "Viuvo(a)",
            },
            {
                "code": MaritalStatusAppToSphinxEnum.MARRIED_TO_BRAZILIAN.value,
                "description": "Casado(a)",
            },
            {
                "code": MaritalStatusAppToSphinxEnum.DIVORCED.value,
                "description": "Divorciado(a)",
            },
            {
                "code": MaritalStatusAppToSphinxEnum.STABLE_UNION.value,
                "description": "União Estável",
            },
        ]

        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": marital_status_to_app},
        }

    @staticmethod
    def get_nationality_update(sinacor_types_repository=SinacorTypesRepository()):
        nationalities = sinacor_types_repository.get_nationality()
        nationalities_enum = [
            {"code": nationality["code"], "value": nationality["description"].title()}
            for nationality in nationalities
        ]
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": nationalities_enum},
        }

    @staticmethod
    def get_country_update(sinacor_types_repository=SinacorTypesRepository()):
        countries = sinacor_types_repository.get_country()
        countries_enum = [
            {"code": country["code"], "value": country["description"].title()}
            for country in countries
        ]
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": countries_enum},
        }

    @staticmethod
    def get_county_update(
        payload: dict, sinacor_types_repository=SinacorTypesRepository()
    ):
        counties = sinacor_types_repository.get_county(
            country=payload.get("country"), state=payload.get("state")
        )
        counties_enum = [
            {"code": county["code"], "value": county["description"].title()}
            for county in counties
        ]
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": counties_enum},
        }

    @staticmethod
    def get_state_update(
        payload: dict, sinacor_types_repository=SinacorTypesRepository()
    ):
        states = sinacor_types_repository.get_state(country=payload.get("country"))
        states_enum = [
            {"code": state["code"], "value": state["description"].title()}
            for state in states
        ]
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": states_enum},
        }

    @staticmethod
    def get_economic_activity_update(sinacor_types_repository=SinacorTypesRepository()):
        activities = sinacor_types_repository.get_economic_activity()
        activities_enum = [
            {"code": activity["code"], "value": activity["description"].title()}
            for activity in activities
        ]
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": activities_enum},
        }

    @staticmethod
    def get_activity_type_update(sinacor_types_repository=SinacorTypesRepository()):
        activities = sinacor_types_repository.get_activity_type()
        activities_enum = [
            {"code": activity["code"], "value": activity["description"].title()}
            for activity in activities
        ]
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": activities_enum},
        }

    @staticmethod
    def get_issuing_body_update(sinacor_types_repository=SinacorTypesRepository()):
        activities = sinacor_types_repository.get_issuing_body()
        activities_enum = [
            {"code": activity["code"], "value": activity["description"].title()}
            for activity in activities
        ]
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": activities_enum},
        }
