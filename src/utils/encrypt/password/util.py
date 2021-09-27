from src.core.interfaces.utils.encrypt.password.interface import IPasswordEncrypt
from mist_client.asgard import Mist
from src.utils.env_config import config
import logging

logger = logging.getLogger(config("LOG_NAME"))


class PasswordEncrypt(IPasswordEncrypt):

    mist = Mist(logger)

    @staticmethod
    def encrypt_password(user_password: str):
        return PasswordEncrypt.mist.generate_encrypted_password(
            user_password=user_password
        )
