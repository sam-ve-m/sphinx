from src.core.interfaces.utils.encrypt.password.interface import IPasswordEncrypt
from mist_client import Mist, MistStatusResponses
from src.exceptions.exceptions import InternalServerError


class PasswordEncrypt(IPasswordEncrypt):

    mist = Mist

    @classmethod
    async def encrypt_password(cls, user_password: str):
        payload, status = await cls.mist.generate_encrypted_password(
            user_password=user_password
        )
        if status != MistStatusResponses.SUCCESS:
            logger.error(str(payload), exc_info=True)
            raise InternalServerError("common.process_issue")
        return payload["encrypted_password"]
