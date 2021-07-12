# STANDARD LIBS
from __future__ import annotations
from typing import Optional
from datetime import datetime
import logging

# OUTSIDE LIBRARIES
from fastapi import Form
from validate_email import validate_email
from pydantic import BaseModel, constr, validator, UUID1
from src.utils.env_config import config

# SPHIX
from src.repositories.view.repository import ViewRepository
from src.repositories.feature.repository import FeatureRepository
from src.repositories.file.enum.term_file import TermsFileType
from src.utils.brazil_register_number_validator import is_cpf_valid
from src.routers.validators.enum_template import MaritalStatusEnum


class Email(BaseModel):
    email: constr(min_length=4, max_length=255)
    # TODO: DNS lib not found
    @validator("email", always=True, allow_reuse=True)
    def validate_email(cls, value):
        try:
            is_valid = validate_email(value)
            if is_valid:
                return value
            raise ValueError("The given email is invalid")
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
        raise ValueError("The given email is invalid")


class View(BaseModel):
    view: constr(min_length=1)

    @validator("view", always=True, allow_reuse=True)
    def validate_view(cls, e):
        view_repository = ViewRepository()
        if view_repository.find_one({"_id": e}, ttl=60):
            return e
        raise ValueError("view not exists")


class Feature(BaseModel):
    feature: constr(min_length=1)

    @validator("feature", always=True, allow_reuse=True)
    def validate_feature(cls, e):
        feature_repository = FeatureRepository()
        if feature_repository.find_one({"_id": e}, ttl=60):
            return e
        raise ValueError("feature not exists")


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


class Cpf(BaseModel):
    cpf: int

    @validator("cpf", always=True, allow_reuse=True)
    def validate_cpf(cls, e):
        if is_cpf_valid(cpf=e):
            return e
        raise ValueError("invalid cpf")


class CelPhone(BaseModel):
    cel_phone: constr(min_length=11, max_length=11)


class MaritalStatus(BaseModel):
    marital_status: MaritalStatusEnum


class Nationality(BaseModel):
    nationality: str


class QuizQuestionOption(BaseModel):
    quiz_question_id: UUID1
    quiz_option_id: UUID1


class IsCvmQualifiedInvestor(BaseModel):
    is_cvm_qualified_investor: bool


class IsUsPerson(BaseModel):
    is_us_person: bool


class UsTin(BaseModel):
    us_tin: Optional[int]
