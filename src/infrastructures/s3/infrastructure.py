# OUTSIDE LIBRARIES
import boto3

# SPHINX
from src.infrastructures.env_config import config


class S3Infrastructure:

    client = None

    @classmethod
    def _get_client(cls):
        if cls.client is None:
            cls.client = boto3.client(
                "s3",
                aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY"),
                region_name=config("REGION_NAME"),
            )
        return cls.client
