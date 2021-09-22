from src.routers.validators.base import OptionalPIN, Email


class Login(Email, OptionalPIN):
    pass
