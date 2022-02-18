# SPHINX
from src.services.sinacor_types.service import SinaCorTypes


class ClientRegisterEnumsController:
    @staticmethod
    def get_type_of_income_tax(payload: dict):
        return SinaCorTypes.get_type_of_income_tax()

    @staticmethod
    def get_activity_type(payload: dict):
        return SinaCorTypes.get_activity_type()

    @staticmethod
    def get_nationality(payload: dict):
        return SinaCorTypes.get_nationality()

    @staticmethod
    def get_document_issuing_body(payload: dict):
        return SinaCorTypes.get_document_issuing_body()

    @staticmethod
    def get_document_type(payload: dict):
        return SinaCorTypes.get_document_type()

    @staticmethod
    def get_county(payload: dict):
        return SinaCorTypes.get_county(payload=payload)

    @staticmethod
    def get_state(payload: dict):
        return SinaCorTypes.get_state(payload=payload)

    @staticmethod
    def get_country(payload: dict):
        return SinaCorTypes.get_country()

    @staticmethod
    def get_gender_update(payload: dict):
        return SinaCorTypes.get_gender()

    @staticmethod
    def get_marital_status_update(payload: dict):
        return SinaCorTypes.get_marital_status_update()

    @staticmethod
    def get_nationality_update(payload: dict):
        return SinaCorTypes.get_nationality_update()

    @staticmethod
    def get_county_update(payload: dict):
        return SinaCorTypes.get_county_update(payload=payload)

    @staticmethod
    def get_state_update(payload: dict):
        return SinaCorTypes.get_state_update(payload=payload)

    @staticmethod
    def get_country_update(payload: dict):
        return SinaCorTypes.get_country_update()

    @staticmethod
    def get_economic_activity_update(payload: dict):
        return SinaCorTypes.get_economic_activity_update()

    @staticmethod
    def get_activity_type_update(payload: dict):
        return SinaCorTypes.get_activity_type_update()

    @staticmethod
    def get_issuing_body_update(payload: dict):
        return SinaCorTypes.get_issuing_body_update()
