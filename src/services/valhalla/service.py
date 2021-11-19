from valhalla_client.main import SocialNetworkQueue
from kafka import KafkaProducer
import logging

from src.infrastructures.env_config import config

class ValhallaService:
        social_client = SocialNetworkQueue(
                logger=logging.getLogger(config("LOG_NAME")), 
                producer=KafkaProducer(bootstrap_servers=config("VALHALLA_QUEUE_HOST"))
        )

        @staticmethod
        def get_social_client():
                return ValhallaService.social_client