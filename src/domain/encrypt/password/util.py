from src.core.interfaces.utils.encrypt.password.interface import IPasswordEncrypt
from mist_client.asgard import Mist
from src.infrastructures.env_config import config
from mist_client.src.domain.enums.mist_status_responses import MistStatusResponses
from src.exceptions.exceptions import InternalServerError
import logging

logger = logging.getLogger(config("LOG_NAME"))


class PasswordEncrypt(IPasswordEncrypt):

    mist = Mist(logger)

    @classmethod
    async def encrypt_password(cls, user_password: str):
        payload, status = await cls.mist.generate_encrypted_password(
            user_password=user_password
        )
        if status != MistStatusResponses.SUCCESS:
            logger.error(str(payload), exc_info=True)
            raise InternalServerError("common.process_issue")
        return payload["encrypted_password"]
