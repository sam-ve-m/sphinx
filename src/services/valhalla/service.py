from valhalla_client.main import SocialNetworkQueue, StatusResponse, Producer
from src.exceptions.exceptions import InternalServerError
from src.infrastructures.env_config import config


class ValhallaService:
    social_client = None

    @classmethod
    def __get_social_client(cls):
        if cls.social_client is None:
            producer = Producer(host=config("VALHALLA_HOST"), port=int(config("VALHALLA_PORT")))
            cls.social_client = SocialNetworkQueue(
                producer=producer
            )
        return cls.social_client

    @classmethod
    async def register_user(cls, user_email: str, nick_name: str):
        social_client = cls.__get_social_client()
        social_network_operation_status, message = await social_client.create_social_network_user(
            msg={"email": user_email, "name": nick_name}
        )

        if social_network_operation_status is not StatusResponse.SUCCESS:
            raise InternalServerError("common.process_issue")

    @classmethod
    async def register_user_portfolio(cls, user_email: str, nick_name: str):
        # TODO: this
        social_client = cls.__get_social_client()
        social_network_operation_status, message = await social_client.create_social_network_user_portfolio(
            msg={"email": user_email, "name": nick_name}
        )

        if social_network_operation_status is not StatusResponse.SUCCESS:
            raise InternalServerError("common.process_issue")