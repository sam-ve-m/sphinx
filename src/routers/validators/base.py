# STANDARD LIBS
from __future__ import annotations
from typing import Optional
from datetime import datetime
import logging

# OUTSIDE LIBRARIES
from fastapi import Form
from validate_email import validate_email
from pydantic import BaseModel, constr, validator, UUID1
from decouple import config

# SPHIX
from src.repositories.sinacor_types.repository import SinaCorTypesRepository
from src.repositories.view.repository import ViewRepository
from src.repositories.feature.repository import FeatureRepository
from src.repositories.file.enum.term_file import TermsFileType
from src.repositories.sinacor_types.enum.decision import Decisions
from src.repositories.sinacor_types.enum.status import OutputStatus
from src.utils.brazil_register_number_validator import is_cpf_valid
from src.utils.brazil_register_number_validator import is_cnpj_valid
from src.routers.validators.enum_template import MaritalStatusEnum
from src.repositories.sinacor_types.enum.person_gender import PersonGender
from src.repositories.sinacor_types.enum.document_type import DocumentTypes


class Email(BaseModel):
    email: constr(min_length=4, max_length=255)
    # TODO: DNS lib not found
    @validator("email", always=True, allow_reuse=True)
    def validate_email(cls, value):
        return value
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
    us_tin: Optional[bool]


# Bureau validators


class Uuid(BaseModel):
    uuid: str


class AppName(BaseModel):
    appName: str


class Successful(BaseModel):
    successful: bool


class Error(BaseModel):
    error: Optional[str]


class Decision(BaseModel):
    decision: Decisions


class Status(BaseModel):
    status: OutputStatus


class ClientType(BaseModel):
    client_type: str


class Country(BaseModel):
    country: str


class State(BaseModel):
    state: str


class Source(BaseModel):
    source: str


class GenderSource(Source):
    value: PersonGender


class BirthDateSource(Source):
    value: int

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        try:
            date = datetime.fromtimestamp(e)
            return date
        except:
            raise ValueError("Wrong timestamp supplied")


class NationalitySource(Source):
    value: constr(min_length=3, max_length=3)

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        sinacor_types_repository = SinaCorTypesRepository()
        if sinacor_types_repository.validate_country(value=e):
            return e
        raise ValueError("nationality not exists")


class NaturalnessSource(Source):
    value: constr(min_length=2, max_length=2)

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        sinacor_types_repository = SinaCorTypesRepository()
        if sinacor_types_repository.validate_state(value=e):
            return e
        raise ValueError("naturalness not exists")


class MotherNameSource(Source):
    value: str


class DocumentTypeSource(Source):
    value: DocumentTypes


class CpfOrCnpjSource(Source):
    value: str

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        if is_cpf_valid(cpf=e) or is_cnpj_valid(cnpj=e):
            return e
        raise ValueError("invalid cpf")


class DateSource(Source):
    value: int

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        try:
            date = datetime.fromtimestamp(e)
            return date
        except:
            raise ValueError("Wrong timestamp supplied")


class StateSource(Source):
    value: constr(min_length=2, max_length=2)

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        sinacor_types_repository = SinaCorTypesRepository()
        if sinacor_types_repository.validate_state(value=e):
            return e
        raise ValueError("state not exists")


class IssuerSource(Source):
    value: str


class StreetNameSource(Source):
    value: str


class AddressNumberSource(Source):
    value: str


class CountrySource(Source):
    value: constr(min_length=3, max_length=3)

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        sinacor_types_repository = SinaCorTypesRepository()
        if sinacor_types_repository.validate_country(value=e):
            return e
        raise ValueError("nationality not exists")


class CitySource(Source):
    value: int

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        sinacor_types_repository = SinaCorTypesRepository()
        if sinacor_types_repository.validate_city(value=e):
            return e
        raise ValueError("nationality not exists")


class ZipCodeSource(Source):
    value: str


class PhoneNumberSource(Source):
    value: str


class ActivitySource(Source):
    value: int

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        sinacor_types_repository = SinaCorTypesRepository()
        if sinacor_types_repository.validate_activity(value=e):
            return e
        raise ValueError("nationality not exists")


class CnpjSource(Source):
    value: str

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        if is_cnpj_valid(cnpj=e):
            return e
        raise ValueError("invalid cpf")


class CompanyNameSource(Source):
    value: str


class PatrimonySource(Source):
    value: float


class IncomeSource(Source):
    value: float


class EducationLevelSource(Source):
    value: str


class EducationCourseSource(Source):
    value: str


class IsPoliticallyExposedPerson(Source):
    value: bool


class DateOfAcquisition(Source):
    value: int

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        try:
            date = datetime.fromtimestamp(e)
            return date
        except:
            raise ValueError("Wrong timestamp supplied")