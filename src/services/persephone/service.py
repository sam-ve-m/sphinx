# OUTSIDE LIBRARIES
from decouple import config
import logging

# PERSEPHONE
from persephone_client.main import Persephone


class PersephoneService:

    client = Persephone(
        host=config("PERSEPHONE_QUEUE_HOST"),
        port=config("PERSEPHONE_QUEUE_PORT"),
        logger=logging.getLogger(config("LOG_NAME")),
    )

    @staticmethod
    def get_client():
        return PersephoneService.client
