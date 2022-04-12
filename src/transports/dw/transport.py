# Standards
from datetime import datetime
from typing import List, Tuple
import json
import asyncio

from src.domain.drive_wealth.file_type import DriveWealthFileType, DriveWealthFileSide
from src.services.builders.client_register.us.builder import ClientRegisterBuilderUs

# Third part
from aiohttp import ClientSession, ClientResponse

# Jotunheimr
from src.infrastructures.env_config import config
from etria_logger import Gladsheim


class DWCaller:
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
        if responses.status != 200:
            Gladsheim.error(
                message=f"DWTransportGraphicAccount::execute_get::Erros to get data from dw {responses}"
            )
        return responses

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
        if responses.status != 200:
            Gladsheim.error(
                message=f"DWTransportGraphicAccount::execute_get::Erros to get data from dw {responses}"
            )
        return responses


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


class DWTransport:

    dw_caller_transport = DWCaller

    @classmethod
    def _build_response(cls, http_response: ClientResponse) -> Tuple[bool, dict]:
        status = False
        if http_response.status == 200:
            status = True
        body = await http_response.text()
        dict_body = json.loads(body)
        return status, dict_body

    @classmethod
    async def call_registry_user_post(cls, builder: ClientRegisterBuilderUs):
        url = config("DW_CREATE_USER_URL")
        body = builder.build()
        http_response = await cls.dw_caller_transport.execute_post(url=url, body=body)
        response = cls._build_response(http_response=http_response)
        return response

    @classmethod
    async def call_save_user_document_file_post(
        cls,
        user_id: str,
        document_type: DriveWealthFileType,
        document: str,
        side: DriveWealthFileSide
    ):
        url = config("DW_USER_FILE_UPLOAD_URL")
        body = {
            "userID": user_id,
            "type": document_type.value,
            "document": document,
            "side": side.value,
        }
        http_response = await cls.dw_caller_transport.execute_post(url=url, body=body)
        response = cls._build_response(http_response=http_response)
        return response
