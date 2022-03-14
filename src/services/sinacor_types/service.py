# OUTSIDE LIBRARIES
from typing import List

from fastapi import status

# PERSEPHONE
from src.repositories.sinacor_types.repository import SinacorTypesRepository
from src.domain.sinacor.person_gender import PersonGender
from src.domain.validators.marital_status_app_to_sphinx import (
    MaritalStatusAppToSphinxEnum,
)


class SinaCorTypes:
    @staticmethod
    async def get_activity_type(sinacor_types_repository=SinacorTypesRepository):
        activities = await sinacor_types_repository.get_activity_type()
        activities_enum = SinaCorTypes.convert_description_to_title(activities)
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": activities_enum},
        }

    @staticmethod
    async def get_nationality(sinacor_types_repository=SinacorTypesRepository):
        nationalities = await sinacor_types_repository.get_nationality()
        nationalities_enum = SinaCorTypes.convert_description_to_title(nationalities)
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": nationalities_enum},
        }

    @staticmethod
    async def get_document_issuing_body(
        sinacor_types_repository=SinacorTypesRepository,
    ):
        issuing_body = await sinacor_types_repository.get_issuing_body()
        issuing_body_enum = SinaCorTypes.convert_description_to_title(issuing_body)
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": issuing_body_enum},
        }

    @staticmethod
    async def all_in_one(sinacor_types_repository=SinacorTypesRepository):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "activity_type": await sinacor_types_repository.get_activity_type(),
                "nationality": await sinacor_types_repository.get_nationality(),
                "document_issuing_body": await sinacor_types_repository.get_issuing_body(),
                "document_type": await sinacor_types_repository.get_document_type(),
                "country": await sinacor_types_repository.get_country(),
            },
        }

    @staticmethod
    async def get_document_type(sinacor_types_repository=SinacorTypesRepository):
        document_types = await sinacor_types_repository.get_document_type()
        document_types_enum = SinaCorTypes.convert_description_to_title(document_types)
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": document_types_enum},
        }

    @staticmethod
    async def get_city(payload: dict, sinacor_types_repository=SinacorTypesRepository):
        cities = await sinacor_types_repository.get_county(
            country=payload.get("country"), state=payload.get("state")
        )
        cities_enum = SinaCorTypes.convert_description_to_title(cities)
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": cities_enum},
        }

    @staticmethod
    async def get_state(payload: dict, sinacor_types_repository=SinacorTypesRepository):
        states = await sinacor_types_repository.get_state(
            country=payload.get("country")
        )
        states_enum = SinaCorTypes.convert_description_to_title(states)
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": states_enum},
        }

    @staticmethod
    async def get_country(sinacor_types_repository=SinacorTypesRepository):
        countries = await sinacor_types_repository.get_country()
        countries_enum = SinaCorTypes.convert_description_to_title(countries)
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": countries_enum},
        }

    @staticmethod
    async def get_gender(sinacor_types_repository=SinacorTypesRepository):
        genders = await sinacor_types_repository.get_gender()
        gender_enum = SinaCorTypes.convert_description_to_title(genders)
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": gender_enum},
        }

    @staticmethod
    async def get_marital_status(sinacor_types_repository=SinacorTypesRepository):
        marital_status = await sinacor_types_repository.get_marital_status()
        marital_status_enum = SinaCorTypes.convert_description_to_title(marital_status)
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": marital_status_enum},
        }

    @staticmethod
    def convert_description_to_title(enum: List[dict]) -> List[dict]:
        titled_enum = [
            {"code": item["code"], "value": item["description"].title()}
            for item in enum
        ]
        return titled_enum
