# SPHINX
from src.services.sinacor_types.service import SinaCorTypes


class ClientRegisterEnumsController:
    @staticmethod
    async def get_county(payload: dict):
        return await SinaCorTypes.get_county(payload=payload)

    @staticmethod
    async def get_state(payload: dict):
        return await SinaCorTypes.get_state(payload=payload)

    @staticmethod
    async def get_nationality(payload: dict):
        return await SinaCorTypes.get_nationality()

    @staticmethod
    async def get_document_type(payload: dict):
        return await SinaCorTypes.get_document_type()

    @staticmethod
    async def get_country(payload: dict):
        return await SinaCorTypes.get_country()

    @staticmethod
    async def get_activity_type(payload: dict):
        return await SinaCorTypes.get_activity_type()

    @staticmethod
    async def get_document_issuing_body(payload: dict):
        return await SinaCorTypes.get_document_issuing_body()

    @staticmethod
    async def all_in_one(payload: dict):
        return SinaCorTypes.all_in_one()

    @staticmethod
    async def get_gender_update(payload: dict):
        return await SinaCorTypes.get_gender()

    @staticmethod
    async def get_marital_status_update(payload: dict):
        return await SinaCorTypes.get_marital_status_update()

    @staticmethod
    async def get_nationality_update(payload: dict):
        return await SinaCorTypes.get_nationality_update()

    @staticmethod
    async def get_county_update(payload: dict):
        return await SinaCorTypes.get_county_update(payload=payload)

    @staticmethod
    async def get_state_update(payload: dict):
        return await SinaCorTypes.get_state_update(payload=payload)

    @staticmethod
    async def get_country_update(payload: dict):
        return await SinaCorTypes.get_country_update()

    @staticmethod
    async def get_economic_activity_update(payload: dict):
        return await SinaCorTypes.get_economic_activity_update()

    @staticmethod
    async def get_activity_type_update(payload: dict):
        return await SinaCorTypes.get_activity_type_update()

    @staticmethod
    async def get_issuing_body_update(payload: dict):
        return await SinaCorTypes.get_issuing_body_update()
