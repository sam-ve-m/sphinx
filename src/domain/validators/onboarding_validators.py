# STANDARD LIBS
from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict, Any

# OUTSIDE LIBRARIES
from fastapi import Form
from pydantic import BaseModel, constr, validator, root_validator

from src.domain.drive_wealth.employed_position import EmployedPosition
from src.domain.drive_wealth.employed_status import EmployedStatus
from src.domain.drive_wealth.employed_type import EmployedType
from src.domain.validators.brazil_register_number_validator import is_cpf_valid
from src.repositories.file.enum.term_file import TermsFileType
from src.repositories.sinacor_types.repository import SinacorTypesRepository
from src.repositories.user.enum.time_experience import TimeExperienceEnum


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
    file_or_base64: constr(min_length=258)


class UserDocument(BaseModel):
    document_front: constr(min_length=258)
    document_back: constr(min_length=258)


class Weight(BaseModel):
    weight: int


class Order(BaseModel):
    order: int


class ValueText(BaseModel):
    value_text: constr(min_length=1, max_length=520)


class PoliticallyExposed(BaseModel):
    is_politically_exposed: bool
    politically_exposed_names: List[constr(min_length=1, max_length=100)]


class ExchangeMember(BaseModel):
    is_exchange_member: bool


class W8FormConfirmation(BaseModel):
    w8_confirmation: bool


class EmployForUs(BaseModel):
    user_employ_status: EmployedStatus
    user_employ_type: EmployedType
    user_employ_position: EmployedPosition
    user_employ_company_name: Optional[constr(min_length=1, max_length=100)]


class TimeExperience(BaseModel):
    time_experience: TimeExperienceEnum


class CompanyDirector(BaseModel):
    is_company_director: bool
    company_name: Optional[str]
    company_ticker: Optional[str]

    @root_validator()
    def validate_cpf(cls, values: Dict[str, Any]):
        is_company_director = values.get("is_company_director")
        company_name = values.get("company_name")
        company_ticker = values.get("company_ticker")
        if is_company_director and (not company_name or not company_ticker):
            raise ValueError(
                "need inform the field campany_name and company_ticker is you are a company director"
            )
        return values


class TermFile(BaseModel):
    file_type: TermsFileType

    @classmethod
    def as_form(cls, file_type: str = Form(...)) -> TermFile:
        return cls(file_type=file_type)


class TermsFile(BaseModel):
    file_types: List[TermsFileType]


class Cpf(BaseModel):
    cpf: str

    @validator("cpf", always=True, allow_reuse=True)
    def validate_cpf(cls, e):
        if is_cpf_valid(cpf=e):
            return e.replace(".", "").replace("-", "").replace("/", "")
        raise ValueError("invalid cpf")


class CelPhone(BaseModel):
    phone: constr(regex=r"^\+\d+", min_length=5)


class Nationality(BaseModel):
    nationality: int

    @validator("nationality", always=True, allow_reuse=True)
    def validate_value(cls, e):
        sinacor_types_repository = SinacorTypesRepository()
        if sinacor_types_repository.validate_nationality(value=e):
            return e
        raise ValueError("Nationality not exists")


class QuizQuestionOption(BaseModel):
    quiz_question_id: str
    quiz_option_id: str


class IsCvmQualifiedInvestor(BaseModel):
    is_cvm_qualified_investor: bool
