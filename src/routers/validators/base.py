from __future__ import annotations
from fastapi import Form
from pydantic import BaseModel, constr, validate_email, validator
from typing import Optional
from datetime import datetime


from src.repositories.view.repository import ViewRepository
from src.repositories.feature.repository import FeatureRepository
from src.repositories.file.enum.term_file import TermsFileType


class Email(BaseModel):
    email: constr(min_length=4, max_length=255)
    # TODO: DNS lib not found
    # @validator('email', always=True, allow_reuse=True)
    # def validate_email(cls, value):
    #     try:
    #         is_valid = validate_email(value)
    #         if is_valid:
    #             return True
    #     except Exception as e:
    #         logger = logging.getLogger(config("LOG_NAME"))
    #         logger.error(e, exc_info=True)
    #
    #     return False


class View(BaseModel):
    view: constr(min_length=1)

    @validator("view", always=True, allow_reuse=True)
    def validate_view(cls, e):
        view_repository = ViewRepository()
        if view_repository.find_one({"_id": e}, ttl=60):
            return e
        return False


class Feature(BaseModel):
    feature: constr(min_length=1)

    @validator("feature", always=True, allow_reuse=True)
    def validate_feature(cls, e):
        feature_repository = FeatureRepository()
        if feature_repository.find_one({"_id": e}, ttl=60):
            return e
        return False


class OptionalPIN(BaseModel):
    pin: Optional[constr(min_length=6, max_length=6)]


class PIN(BaseModel):
    pin: constr(min_length=6, max_length=6)


class Name(BaseModel):
    name: constr(min_length=1, max_length=50)


class DisplayName(BaseModel):
    display_name: constr(min_length=1, max_length=50)


class Version(BaseModel):
    version: int


class Date(BaseModel):
    date: datetime


class Score(BaseModel):
    score: int


class Weight(BaseModel):
    weight: int


class Order(BaseModel):
    order: int


class ValueText(BaseModel):
    value_text: constr(min_length=1, max_length=520)


class TermFile(BaseModel):
    file_type: TermsFileType

    @classmethod
    def as_form(cls, file_type: str = Form(...)) -> TermFile:
        return cls(file_type=file_type)
