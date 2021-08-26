from src.utils.env_config import config
import requests
import logging
import json

from src.exceptions.exceptions import InternalServerError
from src.domain.solutiontech.client_import_status import SolutiontechClientImportStatus


class Solutiontech:

    response_message_map = {
        "Cliente encontrado!": SolutiontechClientImportStatus.SYNC.value,
        "Cliente não encontrado!": SolutiontechClientImportStatus.SEND.value,
    }

    @staticmethod
    def check_if_client_is_synced_with_solutiontech(user_bmf_code: int, user_solutiontech_status_from_database: str) -> str:
        base_url_solutiontech = config("SOLUTIONTECH_BASE_URL")
        solutiontech_verify_dtvm_client = config("SOLUTIONTECH_VERIFY_DTVM_CLIENT")
        response_message = None
        try:
            # Verificar necessidade de retirar o verify=False
            response = requests.get(
                url=f"{base_url_solutiontech}{solutiontech_verify_dtvm_client}",
                params={"codCliente": user_bmf_code},
                verify=False,
            )
            if response.status_code == 200:
                response_message = response.text
                maped_response = Solutiontech.response_message_map.get(response_message)
                if maped_response:
                    return maped_response
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(
                msg=f"user_bmf_code {user_bmf_code} - response  = {response_message} -  error = {str(e)}", exc_info=e
            )

        return user_solutiontech_status_from_database

    @staticmethod
    def request_client_sync(user_bmf_code: int):
        base_url_solutiontech = config("SOLUTIONTECH_BASE_URL")
        solutiontech_sync_dtvm_client = config("SOLUTIONTECH_SYNC_DTVM_CLIENT")
        response_message = None
        try:
            # Verificar necessidade de retirar o verify=False
            headers = {"content-type": "application/json"}
            response = requests.post(
                url=f"{base_url_solutiontech}{solutiontech_sync_dtvm_client}",
                data=json.dumps({"codCliente": user_bmf_code}),
                verify=False,
                headers=headers,
            )
            if response.status_code == 200:
                response_json = json.loads(response.text)
                status = response_json.get("message")
                if status == "OK":
                    return True
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(
                msg=f"user_bmf_code: {user_bmf_code} - Solution Tech Response  = {response_message} -  error = {str(e)}", exc_info=e
            )

        return False
