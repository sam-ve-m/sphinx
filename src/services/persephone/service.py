# OUTSIDE LIBRARIES
import logging

# PERSEPHONE
from persephone_client.main import Persephone

# SPHINX
from src.infrastructures.env_config import config


class PersephoneService:

    client = None

    @classmethod
    def get_client(cls):
        if cls.client is None:
            cls.client = Persephone(
                host=config("PERSEPHONE_QUEUE_HOST"),
                port=config("PERSEPHONE_QUEUE_PORT"),
                logger=logging.getLogger(config("LOG_NAME")),
            )
        return cls.client
