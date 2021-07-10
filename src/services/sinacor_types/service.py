# OUTSIDE LIBRARIES
from fastapi import status

# PERSEPHONE
from src.repositories.sinacor_types.repository import SinaCorTypesRepository


class SinaCorTypes:
    @staticmethod
    def get_type_of_income_tax(sinacor_types_repository=SinaCorTypesRepository()):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_type_of_income_tax()},
        }

    @staticmethod
    def get_client_type(
        sinacor_types_repository=SinaCorTypesRepository()
    ):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_client_type()},
        }

    @staticmethod
    def get_investor_type(
        sinacor_types_repository=SinaCorTypesRepository()
    ):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_investor_type()},
        }

    @staticmethod
    def get_activity_type(
        sinacor_types_repository=SinaCorTypesRepository()
    ):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_activity_type()},
        }

    @staticmethod
    def get_type_ability_person(
        sinacor_types_repository=SinaCorTypesRepository()
    ):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_type_ability_person()},
        }

    @staticmethod
    def get_customer_qualification_type(
        sinacor_types_repository=SinaCorTypesRepository()
    ):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "enums": sinacor_types_repository.get_customer_qualification_type()
            },
        }

    @staticmethod
    def get_cosif_tax_classification(
        sinacor_types_repository=SinaCorTypesRepository()
    ):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "enums": sinacor_types_repository.get_cosif_tax_classification()
            },
        }

    @staticmethod
    def get_marital_status(
        sinacor_types_repository=SinaCorTypesRepository()
    ):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_marital_status()},
        }

    @staticmethod
    def get_nationality(
        sinacor_types_repository=SinaCorTypesRepository()
    ):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_nationality()},
        }

    @staticmethod
    def get_document_issuing_body(
        sinacor_types_repository=SinaCorTypesRepository()
    ):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_document_issuing_body()},
        }

    @staticmethod
    def get_document_type(
        sinacor_types_repository=SinaCorTypesRepository()
    ):
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
    def get_marriage_regime(
        sinacor_types_repository=SinaCorTypesRepository()
    ):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_marriage_regime()},
        }

    @staticmethod
    def get_customer_origin(
        sinacor_types_repository=SinaCorTypesRepository()
    ):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_customer_origin()},
        }

    @staticmethod
    def get_customer_status(
        sinacor_types_repository=SinaCorTypesRepository()
    ):
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
    def get_economic_activity(
        sinacor_types_repository=SinaCorTypesRepository()
    ):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_economic_activity()},
        }

    @staticmethod
    def get_account_type(
        sinacor_types_repository=SinaCorTypesRepository()
    ):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": sinacor_types_repository.get_account_type()},
        }
