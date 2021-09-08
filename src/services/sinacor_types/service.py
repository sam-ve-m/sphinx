# OUTSIDE LIBRARIES
from fastapi import status

# PERSEPHONE
from src.repositories.sinacor_types.repository import SinaCorTypesRepository
from src.repositories.sinacor_types.enum.person_gender import PersonGender


class SinaCorTypes:
    @staticmethod
    def get_type_of_income_tax(sinacor_types_repository=SinaCorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_type_of_income_tax()},
        }

    @staticmethod
    def get_client_type(sinacor_types_repository=SinaCorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_client_type()},
        }

    @staticmethod
    def get_investor_type(sinacor_types_repository=SinaCorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_investor_type()},
        }

    @staticmethod
    def get_activity_type(sinacor_types_repository=SinaCorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_activity_type()},
        }

    @staticmethod
    def get_type_ability_person(sinacor_types_repository=SinaCorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_type_ability_person()},
        }

    @staticmethod
    def get_customer_qualification_type(
        sinacor_types_repository=SinaCorTypesRepository(),
    ):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "enums": sinacor_types_repository.get_customer_qualification_type()
            },
        }

    @staticmethod
    def get_cosif_tax_classification(sinacor_types_repository=SinaCorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "enums": sinacor_types_repository.get_cosif_tax_classification()
            }
        }

    @staticmethod
    def get_marital_status(sinacor_types_repository=SinaCorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_marital_status()},
        }

    @staticmethod
    def get_nationality(sinacor_types_repository=SinaCorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_nationality()},
        }

    @staticmethod
    def get_document_issuing_body(sinacor_types_repository=SinaCorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_document_issuing_body()},
        }

    @staticmethod
    def get_document_type(sinacor_types_repository=SinaCorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_document_type()},
        }

    @staticmethod
    def get_county(payload: dict, sinacor_types_repository=SinaCorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "enums": sinacor_types_repository.get_county(
                    country=payload.get("country"), state=payload.get("state")
                )
            },
        }

    @staticmethod
    def get_state(payload: dict, sinacor_types_repository=SinaCorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "enums": sinacor_types_repository.get_state(
                    country=payload.get("country")
                )
            },
        }

    @staticmethod
    def get_country(sinacor_types_repository=SinaCorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_country()},
        }

    @staticmethod
    def get_marriage_regime(sinacor_types_repository=SinaCorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_marriage_regime()},
        }

    @staticmethod
    def get_customer_origin(sinacor_types_repository=SinaCorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_customer_origin()},
        }

    @staticmethod
    def get_customer_status(sinacor_types_repository=SinaCorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_customer_status()},
        }

    @staticmethod
    def get_bmf_customer_type(
        payload: dict, sinacor_types_repository=SinaCorTypesRepository()
    ):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "enums": sinacor_types_repository.get_bmf_customer_type(
                    client_type=payload.get("client_type")
                )
            },
        }

    @staticmethod
    def get_economic_activity(sinacor_types_repository=SinaCorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_economic_activity()},
        }

    @staticmethod
    def get_account_type(sinacor_types_repository=SinaCorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_account_type()},
        }

    @staticmethod
    def get_gender():
        genders = [{"code": gender.value, "value": gender.name.title()} for gender in list(PersonGender)]
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": genders},
        }

    @staticmethod
    def get_marital_status_update(sinacor_types_repository=SinaCorTypesRepository()):
        sinacor_marital_status_list = sinacor_types_repository.get_marital_status()
        sinacor_marital_status_list_max_len = len(sinacor_marital_status_list)

        for sinacor_marital_status_list_index in range(sinacor_marital_status_list_max_len):
            marital_status_description = sinacor_marital_status_list[sinacor_marital_status_list_index].get("description")
            marital_status_description_lower_case = marital_status_description.title()
            marital_status_description_lower_case = marital_status_description_lower_case.replace("(A)", "(a)")
            sinacor_marital_status_list[sinacor_marital_status_list_index].update({"description": marital_status_description_lower_case})

        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_marital_status_list},
        }

    @staticmethod
    def get_nationality_update(sinacor_types_repository=SinaCorTypesRepository()):
        nationalities = sinacor_types_repository.get_nationality()
        nationalities_enum = [{"code": nationality['code'], "value": nationality['description'].title()} for nationality in nationalities]
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": nationalities_enum},
        }

    @staticmethod
    def get_country_update(sinacor_types_repository=SinaCorTypesRepository()):
        countries = sinacor_types_repository.get_country()
        countries_enum = [{"code": country['initials'], "value": country['description'].title()} for country in
                          countries]
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": countries_enum},
        }

    @staticmethod
    def get_county_update(payload: dict, sinacor_types_repository=SinaCorTypesRepository()):
        counties = sinacor_types_repository.get_county(
                    country=payload.get("country"), state=payload.get("state")
        )
        counties_enum = [{"code": county['code'], "value": county['description'].title()} for county in
                          counties]
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "enums": counties_enum
            },
        }

    @staticmethod
    def get_state_update(payload: dict, sinacor_types_repository=SinaCorTypesRepository()):
        states = sinacor_types_repository.get_state(country=payload.get("country"))
        states_enum = [{"code": state['initials'], "value": state['description'].title()} for state in
                         states]
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "enums": states_enum
            },
        }

    @staticmethod
    def get_economic_activity_update(sinacor_types_repository=SinaCorTypesRepository()):
        activities = sinacor_types_repository.get_economic_activity()
        activities_enum = [{"code": activity['code'], "value": activity['description'].title()} for activity in
                         activities]
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": activities_enum},
        }