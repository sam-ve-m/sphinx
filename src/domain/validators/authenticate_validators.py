from pydantic import BaseModel, constr, validator

from src.domain.validators.base import Email
from src.domain.validators.brazil_register_number_validator import is_cpf_valid

signature_regex = r"^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])[a-zA-Z0-9]{8,}$"


class Login(Email):
    pass


class SignatureCheck(BaseModel):
    signature: constr(regex=signature_regex)
    signature_expire_time: int = None


class Cpf(BaseModel):
    cpf: str

    @validator("cpf", always=True, allow_reuse=True)
    def validate_cpf(cls, e):
        if is_cpf_valid(cpf=e):
            return e.replace(".", "").replace("-", "").replace("/", "")
        raise ValueError("invalid cpf")


class AllowedCpf(BaseModel):
    cpf: str
