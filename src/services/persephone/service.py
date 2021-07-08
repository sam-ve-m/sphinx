# OUTSIDE LIBRARIES
import logging

# PERSEPHONE
from persephone_client.main import Persephone

#SPHINX
from src.utils.env_config import config


class PersephoneService:

    client = Persephone(
        host=config("PERSEPHONE_QUEUE_HOST"),
        port=config("PERSEPHONE_QUEUE_PORT"),
        logger=logging.getLogger(config("LOG_NAME")),
    )

    @staticmethod
    def get_client():
        return PersephoneService.client
