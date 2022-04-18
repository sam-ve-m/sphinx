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
    async def register_user(
        cls,
        user_type: str,
        nickname: str,
        unique_id: str
    ):
        social_client = cls.__get_social_client()
        social_network_operation_status, message = await social_client.create_social_network_user(
            msg={
                "user_type": user_type,
                "nickname": nickname,
                "unique_id": unique_id
            }
        )

        if social_network_operation_status is not StatusResponse.SUCCESS:
            raise InternalServerError("common.process_issue")

    @classmethod
    async def register_user_portfolio_br(cls, unique_id: str, bmf_account: str, bovespa_account: str):
        social_client = cls.__get_social_client()
        social_network_operation_status, message = await social_client.create_social_network_portfolio_default(
            msg={"unique_id": unique_id, "bmf_account": bmf_account, "bovespa_account": bovespa_account, "country": "br"}
        )

        if social_network_operation_status is not StatusResponse.SUCCESS:
            raise InternalServerError("common.process_issue")

    @classmethod
    async def register_user_portfolio_us(cls, unique_id: str, dw_account: str, dw_id: str):
        social_client = cls.__get_social_client()
        social_network_operation_status, message = await social_client.create_social_network_portfolio_default_us(
            msg={"unique_id": unique_id, "dw_account": dw_account, "dw_id": dw_id, "country": "us"}
        )

        if social_network_operation_status is not StatusResponse.SUCCESS:
            raise InternalServerError("common.process_issue")
