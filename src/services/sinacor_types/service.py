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
    async def get_activity_type(sinacor_types_repository=SinacorTypesRepository):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": await sinacor_types_repository.get_activity_type()},
        }

    @staticmethod
    async def get_nationality(sinacor_types_repository=SinacorTypesRepository):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": await sinacor_types_repository.get_nationality()},
        }

    @staticmethod
    async def get_document_issuing_body(
        sinacor_types_repository=SinacorTypesRepository,
    ):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "enums": await sinacor_types_repository.get_document_issuing_body()
            },
        }

    @staticmethod
    async def all_in_one(sinacor_types_repository=SinacorTypesRepository):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "activity_type": await sinacor_types_repository.get_activity_type(),
                "nationality": await sinacor_types_repository.get_nationality(),
                "document_issuing_body": await sinacor_types_repository.get_document_issuing_body(),
                "document_type": await sinacor_types_repository.get_document_type(),
                "country": await sinacor_types_repository.get_country(),
            },
        }

    @staticmethod
    async def get_document_type(sinacor_types_repository=SinacorTypesRepository):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": await sinacor_types_repository.get_document_type()},
        }

    @staticmethod
    async def get_county(
        payload: dict, sinacor_types_repository=SinacorTypesRepository
    ):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "enums": await sinacor_types_repository.get_county(
                    country=payload.get("country"), state=payload.get("state")
                )
            },
        }

    @staticmethod
    async def get_state(payload: dict, sinacor_types_repository=SinacorTypesRepository):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "enums": await sinacor_types_repository.get_state(
                    country=payload.get("country")
                )
            },
        }

    @staticmethod
    async def get_country(sinacor_types_repository=SinacorTypesRepository):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": await sinacor_types_repository.get_country()},
        }

    @staticmethod
    async def get_gender():
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
    async def get_marital_status_update():
        marital_status_to_app = [
            {
                "code": MaritalStatusAppToSphinxEnum.SINGLE.value,
                "value": "Solteiro (a)",
            },
            {
                "code": MaritalStatusAppToSphinxEnum.WIDOWER.value,
                "value": "Viuvo(a)",
            },
            {
                "code": MaritalStatusAppToSphinxEnum.MARRIED_TO_BRAZILIAN.value,
                "value": "Casado(a)",
            },
            {
                "code": MaritalStatusAppToSphinxEnum.DIVORCED.value,
                "value": "Divorciado(a)",
            },
            {
                "code": MaritalStatusAppToSphinxEnum.STABLE_UNION.value,
                "value": "União Estável",
            },
        ]

        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": marital_status_to_app},
        }

    @staticmethod
    async def get_nationality_update(sinacor_types_repository=SinacorTypesRepository):
        nationalities = await sinacor_types_repository.get_nationality()
        nationalities_enum = [
            {"code": nationality["code"], "value": nationality["description"].title()}
            for nationality in nationalities
        ]
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": nationalities_enum},
        }

    @staticmethod
    async def get_country_update(sinacor_types_repository=SinacorTypesRepository):
        countries = await sinacor_types_repository.get_country()
        countries_enum = [
            {"code": country["code"], "value": country["description"].title()}
            for country in countries
        ]
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": countries_enum},
        }

    @staticmethod
    async def get_county_update(
        payload: dict, sinacor_types_repository=SinacorTypesRepository
    ):
        counties = await sinacor_types_repository.get_county(
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
    async def get_state_update(
        payload: dict, sinacor_types_repository=SinacorTypesRepository
    ):
        states = await sinacor_types_repository.get_state(
            country=payload.get("country")
        )
        states_enum = [
            {"code": state["code"], "value": state["description"].title()}
            for state in states
        ]
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": states_enum},
        }

    @staticmethod
    async def get_economic_activity_update(
        sinacor_types_repository=SinacorTypesRepository,
    ):
        activities = await sinacor_types_repository.get_economic_activity()
        activities_enum = [
            {"code": activity["code"], "value": activity["description"].title()}
            for activity in activities
        ]
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": activities_enum},
        }

    @staticmethod
    async def get_activity_type_update(sinacor_types_repository=SinacorTypesRepository):
        activities = await sinacor_types_repository.get_activity_type()
        activities_enum = [
            {"code": activity["code"], "value": activity["description"].title()}
            for activity in activities
        ]
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": activities_enum},
        }

    @staticmethod
    async def get_issuing_body_update(sinacor_types_repository=SinacorTypesRepository):
        activities = await sinacor_types_repository.get_issuing_body()
        activities_enum = [
            {"code": activity["code"], "value": activity["description"].title()}
            for activity in activities
        ]
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": activities_enum},
        }
