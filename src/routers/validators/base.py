from pydantic import BaseModel, constr, validator
from typing import Optional


class Email(BaseModel):
    email: str

    # @validator('email', always=True)
    # def validate_email(self, e):
    #     is_valid = validate_email(e, check_mx=True)
    #     if is_valid:
    #         return True
    #     return False


class View(BaseModel):
    view: str
    #
    # @validator('view', always=True)
    # def validate_email(self, e):
    #     # TODO: VALIDATR COM MODEL
    #     is_valid = validate_email(e, check_mx=True)
    #     if is_valid:
    #         return True
    #     return False


class Feature(BaseModel):
    feature: str

    # @validator('feature', always=True)
    # def validate_email(self, e):
    #     # TODO: VALIDATR COM MODEL
    #     is_valid = validate_email(e, check_mx=True)
    #     if is_valid:
    #         return True
    #     return False


class OptionalPIN(BaseModel):
    pin: Optional[constr(min_length=6, max_length=6)]


class PIN(BaseModel):
    pin: constr(min_length=6, max_length=6)


class Name(BaseModel):
    name: constr(min_length=1, max_length=50)


class DisplayName(BaseModel):
    display_name: constr(min_length=1, max_length=50)
