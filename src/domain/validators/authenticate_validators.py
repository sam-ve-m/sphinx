from pydantic import BaseModel, constr

from src.domain.validators.base import OptionalPIN, Email

signature_regex = r"^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])[a-zA-Z0-9]{8,}$"


class Login(Email, OptionalPIN):
    pass


class SignatureCheck(BaseModel):
    signature: constr(regex=signature_regex)
    signature_expire_time: int = None
