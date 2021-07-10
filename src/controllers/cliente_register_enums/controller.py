# SPHINX
from src.services.sinacor_types.service import SinaCorTypes


class ClientRegisterEnumsController:
    @staticmethod
    def get_type_of_income_tax(payload: dict):
        return SinaCorTypes.get_type_of_income_tax()

    @staticmethod
    def get_client_type(payload: dict):
        return SinaCorTypes.get_client_type(payload=payload)

    @staticmethod
    def get_investor_type(payload: dict):
        return SinaCorTypes.get_investor_type(payload=payload)

    @staticmethod
    def get_activity_type(payload: dict):
        return SinaCorTypes.get_activity_type(payload=payload)

    @staticmethod
    def get_type_ability_person(payload: dict):
        return SinaCorTypes.get_type_ability_person(payload=payload)

    @staticmethod
    def get_customer_qualification_type(payload: dict):
        return SinaCorTypes.get_customer_qualification_type(payload=payload)

    @staticmethod
    def get_cosif_tax_classification(payload: dict):
        return SinaCorTypes.get_cosif_tax_classification(payload=payload)

    @staticmethod
    def get_marital_status(payload: dict):
        return SinaCorTypes.get_marital_status(payload=payload)

    @staticmethod
    def get_nationality(payload: dict):
        return SinaCorTypes.get_nationality(payload=payload)

    @staticmethod
    def get_document_issuing_body(payload: dict):
        return SinaCorTypes.get_document_issuing_body(payload=payload)

    @staticmethod
    def get_document_type(payload: dict):
        return SinaCorTypes.get_document_type(payload=payload)

    @staticmethod
    def get_county(payload: dict):
        return SinaCorTypes.get_county(payload=payload)

    @staticmethod
    def get_state(payload: dict):
        return SinaCorTypes.get_state(payload=payload)

    @staticmethod
    def get_country(payload: dict):
        return SinaCorTypes.get_country(payload=payload)

    @staticmethod
    def get_marriage_regime(payload: dict):
        return SinaCorTypes.get_marriage_regime(payload=payload)

    @staticmethod
    def get_customer_origin(payload: dict):
        return SinaCorTypes.get_customer_origin(payload=payload)

    @staticmethod
    def get_customer_status(payload: dict):
        return SinaCorTypes.get_customer_status(payload=payload)

    @staticmethod
    def get_bmf_customer_type(payload: dict):
        return SinaCorTypes.get_bmf_customer_type(payload=payload)

    @staticmethod
    def get_economic_activity(payload: dict):
        return SinaCorTypes.get_economic_activity(payload=payload)

    @staticmethod
    def get_account_type(payload: dict):
        return SinaCorTypes.get_account_type(payload=payload)
