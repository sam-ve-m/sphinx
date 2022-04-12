# Standards
from datetime import datetime
from typing import List
import json
import asyncio
from src.services.builders.client_register.us.builder import ClientRegisterBuilderUs

# Third part
from aiohttp import ClientSession, ClientResponse

# Jotunheimr
from src.infrastructures.env_config import config
from etria_logger import Gladsheim


class DWTransport:
    session = None
    token = None
    expire_at = None

    @classmethod
    async def execute_post(
        cls, url, body: dict
    ) -> ClientResponse:
        await cls.__do_authentication()
        session = await cls.__get_session()
        headers = {
            "Accept": "application/json",
            "dw-client-app-key": config("DW_APP_KEY"),
            "dw-auth-token": cls.token,
        }
        responses = await session.post(url=url, data=body, headers=headers)
        if responses.status == 200:
            return responses
        Gladsheim.error(
            message=f"DWTransportGraphicAccount::execute_get::Erros to get data from dw {responses}"
        )

    @classmethod
    async def execute_get(
        cls, url, query_params: dict
    ) -> ClientResponse:
        await cls.__do_authentication()
        session = await cls.__get_session()
        headers = {
            "Accept": "application/json",
            "dw-client-app-key": config("DW_APP_KEY"),
            "dw-auth-token": cls.token,
        }
        responses = await session.get(url=url, params=query_params, headers=headers)
        if responses.status == 200:
            return responses
        Gladsheim.error(
            message=f"DWTransportGraphicAccount::execute_get::Erros to get data from dw {responses}"
        )

    @classmethod
    async def __do_authentication(cls):
        if not cls.expire_at or cls.expire_at < datetime.utcnow():
            session = await cls.__get_session()
            payload = {
                "username": config("DW_USER"),
                "password": config("DW_PASSWORD"),
                "appTypeID": 4,
            }
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "dw-client-app-key": config("DW_APP_KEY"),
            }
            try:
                async with session.post(
                    config("DW_AUTHENTICATION_URL"), json=payload, headers=headers
                ) as response:
                    body = await response.text()
                    dict_body = json.loads(body)
                    cls.token = dict_body["authToken"]
                    cls.expire_at = datetime.fromisoformat(dict_body["expiresAt"][:-1])
            except Exception as exception:
                Gladsheim.error(
                    message=f"DWTransportGraphicAccount::get_balances::Error to authenticate:  {exception}",
                    error=exception,
                )

    @classmethod
    async def __get_session(cls) -> ClientSession:
        if cls.session is None:
            cls.session = ClientSession()
        return cls.session


class DWTransportGraphicAccount:

    @classmethod
    async def call_registry_user_post(cls, builder: ClientRegisterBuilderUs):
        pass

    @classmethod
    async def call_save_user_document_file_post(cls, user_id: str, type, document: str, side):
        pass