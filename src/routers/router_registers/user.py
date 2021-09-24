from fastapi import APIRouter


class UserRouter:

    _instance = None

    def __init__(self):
        raise Exception("You are using Sphinx ways (routers) wrong!")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = APIRouter()
        return cls._instance
