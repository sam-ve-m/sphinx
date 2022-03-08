from src.infrastructures.env_config import config
import aiohttp
from etria_logger import Gladsheim
import json

from src.domain.solutiontech.client_import_status import SolutiontechClientImportStatus


class Solutiontech:

    response_message_map = {
        "Cliente encontrado!": SolutiontechClientImportStatus.SYNC.value,
    }

    @staticmethod
    async def check_if_client_is_synced_with_solutiontech(
        user_bmf_code: int, user_solutiontech_status_from_database: str
    ) -> str:
        base_url_solutiontech = config("SOLUTIONTECH_BASE_URL")
        solutiontech_verify_dtvm_client = config("SOLUTIONTECH_VERIFY_DTVM_CLIENT")
        response_message = None

        Solutiontech.response_message_map.update(
            {"Cliente não encontrado!": user_solutiontech_status_from_database}
        )
        try:
            async with aiohttp.ClientSession() as session:
                # TODO: THis must be with ssl
                async with session.get(
                    f"{base_url_solutiontech}{solutiontech_verify_dtvm_client}",
                    params={"codCliente": user_bmf_code},
                    ssl=False
                ) as response:
                    if response.status == 200:
                        response_message = await response.text()
                        maped_response = Solutiontech.response_message_map.get(
                            response_message
                        )
                        if maped_response:
                            return maped_response
        except Exception as e:
            Gladsheim.error(
                error=e,
                message=f"user_bmf_code {user_bmf_code} - response  = {response_message} -  error = {str(e)}",
            )

        return user_solutiontech_status_from_database

    @staticmethod
    async def request_client_sync(user_bmf_code: int):
        base_url_solutiontech = config("SOLUTIONTECH_BASE_URL")
        solutiontech_sync_dtvm_client = config("SOLUTIONTECH_SYNC_DTVM_CLIENT")
        response_message = None
        try:
            headers = {"content-type": "application/json"}
            async with aiohttp.ClientSession() as session:
                # TODO: THis must be with ssl
                async with session.post(
                    f"{base_url_solutiontech}{solutiontech_sync_dtvm_client}",
                    params={"codCliente": user_bmf_code},
                    data=json.dumps({"codCliente": user_bmf_code}),
                    headers=headers,
                    ssl=False
                ) as response:
                    if response.status == 200:
                        response_json = json.loads(await response.text())
                        status = response_json.get("message")
                        if status == "OK":
                            return True
        except Exception as e:
            Gladsheim.error(
                error=e,
                message=f"user_bmf_code: {user_bmf_code} - Solution Tech Response  = {response_message} -  error = {str(e)}",
            )

        return False
