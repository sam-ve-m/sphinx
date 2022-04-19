# Standards
from datetime import datetime
from typing import List, Tuple
import json
from nidavellir import Sindri

from src.domain.drive_wealth.account import (
    DriveWealthAccountType,
    DriveWealthAccountManagementType,
    DriveWealthAccountTradingType,
)
from src.domain.drive_wealth.file_type import (
    DriveWealthFileType,
    DriveWealthFileSide,
)

# Third part
from aiohttp import ClientSession, ClientResponse

# Jotunheimr
from src.infrastructures.env_config import config
from mepho import DWApiTransport


class DWTransport:

    dw_caller_transport = DWApiTransport

    @classmethod
    async def _build_response(cls, http_response: ClientResponse) -> Tuple[bool, dict]:
        status = False
        if http_response.status in [200, 201]:
            status = True
        body = await http_response.text()
        dict_body = json.loads(body)
        return status, dict_body

    @classmethod
    async def call_registry_user_post(cls, user_register_data: dict):
        url = config("DW_CREATE_USER_URL")
        http_response = await cls.dw_caller_transport.execute_post(
            url=url, body=user_register_data
        )
        response = await cls._build_response(http_response=http_response)
        return response

    @classmethod
    async def call_kyc_status_get(
        cls,
        user_id: str,
    ):
        url = config("DW_KYC_USER_URL")
        formatted_url = url.format(user_id)
        http_response = await cls.dw_caller_transport.execute_get(
            url=formatted_url, query_params={}
        )
        response = await cls._build_response(http_response=http_response)
        return response

    @classmethod
    async def call_registry_user_patch(cls, user_register_data: dict, user_dw_id: str):
        url = config("DW_UPDATE_USER_URL")
        formatted_url = url.format(user_dw_id)
        http_response = await cls.dw_caller_transport.execute_patch(
            url=formatted_url, body=user_register_data
        )
        response = await cls._build_response(http_response=http_response)
        return response

    @classmethod
    async def call_registry_account_post(
        cls,
        user_id: str,
        account_type: DriveWealthAccountType,
        account_management_type: DriveWealthAccountManagementType,
        trading_type: DriveWealthAccountTradingType,
        ignore_buying_power: bool,
    ):
        body = {
            "userID": user_id,
            "accountType": account_type.value,
            "accountManagementType": account_management_type.value,
            "tradingType": trading_type.value,
            "ignoreBuyingPower": ignore_buying_power,
            "ignoreMarketHoursForTest": bool(
                eval(config("DW_IGNORE_MARKET_HOURS_FOR_TEST"))
            ),
        }
        url = config("DW_CREATE_ACCOUNT_URL")
        http_response = await cls.dw_caller_transport.execute_post(url=url, body=body)
        response = await cls._build_response(http_response=http_response)
        return response

    @classmethod
    async def call_save_user_document_file_post(
        cls,
        user_id: str,
        document_type: DriveWealthFileType,
        document: str,
        side: DriveWealthFileSide,
    ):
        url = config("DW_USER_FILE_UPLOAD_URL")
        body = {
            "userID": user_id,
            "type": document_type.value,
            "document": document,
            "side": side.value,
        }
        http_response = await cls.dw_caller_transport.execute_post(url=url, body=body)
        response = await cls._build_response(http_response=http_response)
        return response
