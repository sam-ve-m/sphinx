import logging
from datetime import datetime
from typing import Optional

from email_validator import validate_email
from pydantic import BaseModel, validator, constr

from src.repositories.sinacor_types.enum.connected_person import ConnectedPerson
from src.repositories.sinacor_types.enum.decision import Decisions
from src.repositories.sinacor_types.enum.document_type import DocumentTypes
from src.repositories.sinacor_types.enum.person_gender import PersonGender
from src.repositories.sinacor_types.enum.person_type import PersonType
from src.repositories.sinacor_types.enum.status import OutputStatus
from src.repositories.sinacor_types.repository import SinaCorTypesRepository
from src.routers.validators.enum_template import MaritalStatusEnum
from src.utils.brazil_register_number_validator import is_cpf_valid, is_cnpj_valid
from src.utils.env_config import config


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
        except Exception:
            raise ValueError("Wrong timestamp supplied")


class CelPhoneSource(Source):
    value: constr(min_length=11, max_length=11)


class MaritalRegime(BaseModel):
    marital_status: int

    @validator("marital_status", always=True, allow_reuse=True)
    def validate_value(cls, e):
        sinacor_types_repository = SinaCorTypesRepository()
        if sinacor_types_repository.validate_marital_regime(value=e):
            return e
        raise ValueError("marital not exists")


class MotherNameSource(Source):
    value: str


class DocumentTypeSource(Source):
    value: DocumentTypes


class DocumentNumber(Source):
    value: str

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        return e.replace(".", "").replace("-", "").replace("/", "")


class CpfOrCnpjSource(Source):
    value: str

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        if is_cpf_valid(cpf=e) or is_cnpj_valid(cnpj=e):
            return e.replace(".", "").replace("-", "").replace("/", "")
        raise ValueError("invalid cpf")


class CpfSource(Source):
    value: str

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        if is_cpf_valid(cpf=e):
            return e.replace(".", "").replace("-", "").replace("/", "")
        raise ValueError("invalid cpf")


class DateSource(Source):
    value: int

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        try:
            date = datetime.fromtimestamp(e)
            return date
        except Exception:
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


class NationalitySource(Source):
    value: int

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        sinacor_types_repository = SinaCorTypesRepository()
        if sinacor_types_repository.validate_nationality(value=e):
            return e
        raise ValueError("nationality not exists")


class CitySource(Source):
    value: str


class IdCitySource(Source):
    value: int


class ZipCodeSource(Source):
    value: int


class PhoneNumberSource(Source):
    value: str


class ActivitySource(Source):
    value: int

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        sinacor_types_repository = SinaCorTypesRepository()
        if sinacor_types_repository.validate_activity(value=e):
            return e
        raise ValueError("Activity not exists")


class CnpjSource(Source):
    value: str

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        if is_cnpj_valid(cnpj=e):
            return e.replace(".", "").replace("-", "").replace("/", "")
        raise ValueError("invalid cnpj")


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
        except Exception:
            raise ValueError("Wrong timestamp supplied")


class IncomeTaxTypeSource(Source):
    value: int

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        sinacor_types_repository = SinaCorTypesRepository()
        if sinacor_types_repository.validate_income_tax_type(value=e):
            return e
        raise ValueError("Income tax type not exists")


class ConnectedPersonSource(Source):
    value: ConnectedPerson


class ClientTypeSource(Source):
    value: int

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        sinacor_types_repository = SinaCorTypesRepository()
        if sinacor_types_repository.validate_client_type(value=e):
            return e
        raise ValueError("Client type not exists")


class PersonTypeSource(Source):
    value: PersonType


class InvestorTypeTypeSource(Source):
    value: int

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        sinacor_types_repository = SinaCorTypesRepository()
        if sinacor_types_repository.validate_investor_type(value=e):
            return e
        raise ValueError("Investor type not exists")


class CosifTaxClassificationSource(Source):
    value: int

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        sinacor_types_repository = SinaCorTypesRepository()
        if sinacor_types_repository.validate_cosif_tax_classification(value=e):
            return e
        raise ValueError("Cosif tax classification not exists")


class CountySource(Source):
    value: int


class MaritalRegimeSource(Source):
    value: int

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        sinacor_types_repository = SinaCorTypesRepository()
        if sinacor_types_repository.validate_marital_regime(value=e):
            return e
        raise ValueError("Martial Regime not exists")


class MaritalStatusSource(BaseModel):
    value: MaritalStatusEnum


class NeighborhoodSource(Source):
    value: str


class AssetsDateSource(Source):
    value: int

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        try:
            date = datetime.fromtimestamp(e)
            return date
        except Exception:
            raise ValueError("Wrong timestamp supplied")


class EmailSource(Source):
    value: str

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, value):
        # return value
        try:
            is_valid = validate_email(value)
            if is_valid:
                return value
            raise ValueError("The given email is invalid")
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
        raise ValueError("The given email is invalid")


class NameSource(Source):
    value: str


class SelfLinkSource(Source):
    value: str


class IsUsPersonSource(Source):
    value: bool


class UsTinSource(Source):
    value: int


class IrsSharingSource(Source):
    value: bool


class FatherNameSource(Source):
    value: str


class MidiaPersonSource(Source):
    value: bool


class PersonRelatedToMarketInfluencerSource(Source):
    value: bool


class CourtOrdersSource(Source):
    value: bool


class IdentityDocumentNumber(Source):
    value: int


class LawsuitsSource(Source):
    value: bool


class FundAdminRegistrationSource(Source):
    value: bool


class InvestmentFundAdministratorsRegistrationSource(Source):
    value: bool


class RegisterAuditorsSecuritiesCommissionSource(Source):
    value: bool


class RegistrationOfOtherMarketParticipantsSecuritiesCommissionSource(Source):
    value: bool


class ForeignInvestorsRegisterOfAnnexIvNotReregisteredSource(Source):
    value: bool


class RegistrationOfForeignInvestorsSecuritiesCommissionSource(Source):
    value: bool
