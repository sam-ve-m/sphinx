# STANDARD LIBS
from __future__ import annotations
from typing import Optional
from datetime import datetime

# OUTSIDE LIBRARIES
from fastapi import Form
from pydantic import BaseModel, constr, validator, UUID1

from src.repositories.file.enum.term_file import TermsFileType
from src.repositories.sinacor_types.repository import SinaCorTypesRepository
from src.domain.validators.enum_template import MaritalStatusEnum
from src.domain.validators.brazil_register_number_validator import is_cpf_valid


class Name(BaseModel):
    name: constr(min_length=1, max_length=100)


class NickName(BaseModel):
    nick_name: constr(min_length=1, max_length=50)


class DisplayName(BaseModel):
    display_name: constr(min_length=1, max_length=50)


class Version(BaseModel):
    version: int


class DeviceInformation(BaseModel):
    device_name: str
    device_model: str
    is_emulator: bool
    device_operating_system_name: str
    os_sdk_version: str
    device_is_in_root_mode: bool
    device_network_interfaces: str
    public_ip: str
    access_ip: str = None
    phone_wifi_ip: str = None
    geolocation: str = None


class DeviceInformationOptional(BaseModel):
    device_name: str = None
    device_model: str = None
    is_emulator: bool = None
    device_operating_system_name: str = None
    os_sdk_version: str = None
    device_is_in_root_mode: bool = None
    device_network_interfaces: str = None
    public_ip: str = None
    access_ip: str = None
    phone_wifi_ip: str = None
    geolocation: str = None


class Date(BaseModel):
    date: datetime


class Score(BaseModel):
    score: int


class FileBase64(BaseModel):
    file_or_base64: str


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
    cpf: str

    @validator("cpf", always=True, allow_reuse=True)
    def validate_cpf(cls, e):
        if is_cpf_valid(cpf=e):
            return e.replace(".", "").replace("-", "").replace("/", "")
        raise ValueError("invalid cpf")


class CelPhone(BaseModel):
    cel_phone: constr(min_length=11, max_length=11)


class MaritalStatus(BaseModel):
    marital_status: MaritalStatusEnum


class Nationality(BaseModel):
    nationality: str

    @validator("nationality", always=True, allow_reuse=True)
    def validate_value(cls, e):
        sinacor_types_repository = SinaCorTypesRepository()
        if sinacor_types_repository.validate_nationality(value=e):
            return e
        raise ValueError("Nationality not exists")


class QuizQuestionOption(BaseModel):
    quiz_question_id: str
    quiz_option_id: str


class IsCvmQualifiedInvestor(BaseModel):
    is_cvm_qualified_investor: bool


class IsUsPerson(BaseModel):
    is_us_person: bool


class UsTin(BaseModel):
    us_tin: Optional[int]
