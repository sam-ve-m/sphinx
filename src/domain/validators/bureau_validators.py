from etria_logger import Gladsheim
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from email_validator import validate_email
from pydantic import BaseModel, validator, constr, root_validator

from src.domain.sinacor.decision import Decisions
from src.domain.sinacor.document_type import DocumentTypes
from src.domain.sinacor.person_gender import PersonGender
from src.domain.sinacor.person_type import PersonType
from src.domain.sinacor.status import OutputStatus
from src.domain.validators.base import Email
from src.domain.validators.brazil_register_number_validator import (
    is_cpf_valid,
    is_cnpj_valid,
)
from src.domain.validators.user_validators import TaxResidence, Spouse
from src.repositories.sinacor_types.repository import SinacorTypesRepository


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
            date = datetime.fromtimestamp(e, tz=timezone.utc)
            return date
        except Exception:
            raise ValueError("Wrong timestamp supplied")


class CelPhoneSource(Source):
    value: constr(min_length=11, max_length=12)


class PhoneSource(Source):
    value: constr(min_length=10, max_length=10)


class EmailSource(Source):
    value: Email


class MaritalStatus(BaseModel):
    marital_status: int

    @validator("marital_status", always=True, allow_reuse=True)
    def validate_value(cls, e):
        sinacor_types_repository = SinacorTypesRepository()
        if sinacor_types_repository.validate_marital_regime(value=e):
            return e
        raise ValueError("marital not exists")


class MotherNameSource(Source):
    value: str


class DocumentTypeSource(Source):
    value: DocumentTypes


class DocumentNumberSource(Source):
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
        e = e.replace(".", "").replace("-", "").replace("/", "")
        if is_cpf_valid(cpf=e):
            return e
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
        sinacor_types_repository = SinacorTypesRepository()
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
        sinacor_types_repository = SinacorTypesRepository()
        if sinacor_types_repository.validate_country(value=e):
            return e
        raise ValueError("nationality not exists")


class NationalitySource(Source):
    value: int

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        sinacor_types_repository = SinacorTypesRepository()
        if sinacor_types_repository.validate_nationality(value=e):
            return e
        raise ValueError("nationality not exists")


class CitySource(Source):
    value: str


class IdCitySource(Source):
    value: int


class ZipCodeSource(Source):
    value: str


class PhoneNumberSource(Source):
    value: str


class ActivitySource(Source):
    value: int

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        sinacor_types_repository = SinacorTypesRepository()
        if sinacor_types_repository.validate_activity(value=e):
            return e
        raise ValueError("Activity not exists")


class CnpjSource(Source):
    value: str

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        e = e.replace(".", "").replace("-", "").replace("/", "")
        if is_cnpj_valid(cnpj=e):
            return e
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


class ConnectedPersonSource(Source):
    value: bool


class PersonTypeSource(Source):
    value: PersonType


class CountySource(Source):
    value: int


class MaritalStatusSource(Source):
    value: int

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, e):
        sinacor_types_repository = SinacorTypesRepository()
        if sinacor_types_repository.validate_marital_regime(value=e):
            return e
        raise ValueError("Martial Status not exists")


class NeighborhoodSource(Source):
    value: str


class TaxResidenceSource(Source):
    value: List[TaxResidence]


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
            Gladsheim.error(error=e)
        raise ValueError("The given email is invalid")


class NameSource(Source):
    value: str


class SelfLinkSource(Source):
    value: str


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


class IdentityDocumentType(Source):
    value: int


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


class RegistrationRepresentativeOfNonresidentInvestorsSecuritiesCommissionSource(
    Source
):
    value: bool


class SpouseSource(BaseModel):
    name: NameSource
    cpf: CpfSource
    nationality: NationalitySource


class DocumentTypesSource(Source):
    value: DocumentTypes


class UserMaritalData(MaritalStatus):
    spouse: Optional[Spouse]


class UserMaritalDataSource(BaseModel):
    status: MaritalStatusSource
    spouse: Optional[SpouseSource]


class UserPersonalDataValidation(BaseModel):
    name: NameSource
    nick_name: NameSource
    birth_date: BirthDateSource
    gender: GenderSource
    father_name: Optional[NameSource]
    mother_name: NameSource
    email: EmailSource
    cel_phone: CelPhoneSource
    nationality: NationalitySource
    occupation_activity: ActivitySource
    company_name: Optional[CompanyNameSource]
    company_cnpj: Optional[CnpjSource]
    patrimony: PatrimonySource
    income: IncomeSource
    tax_residences: Optional[TaxResidenceSource]
    birth_place_country: CountrySource
    birth_place_state: StateSource
    birth_place_city: CountySource


class UserDocumentsDataValidation(BaseModel):
    cpf: CpfSource
    identity_type: DocumentTypesSource
    identity_number: DocumentNumberSource
    expedition_date: DateSource
    issuer: IssuerSource
    state: StateSource


class UserAddressDataValidation(BaseModel):
    country: CountrySource
    state: StateSource
    city: CountySource
    neighborhood: NeighborhoodSource
    street_name: StreetNameSource
    number: AddressNumberSource
    zip_code: ZipCodeSource
    phone: Optional[PhoneSource]

    @classmethod
    def validate_contry_state_city(cls, country: str, state: str, id_city: int) -> bool:
        sinacor_types_repository = SinacorTypesRepository()
        is_valid = sinacor_types_repository.validate_contry_state_and_id_city(
            country, state, id_city
        )
        return is_valid

    @root_validator()
    def validate(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        CountrySource(**values.get("country"))
        StateSource(**values.get("state"))
        CountySource(**values.get("city"))
        NeighborhoodSource(**values.get("neighborhood"))
        StreetNameSource(**values.get("street_name"))
        AddressNumberSource(**values.get("number"))
        ZipCodeSource(**values.get("zip_code"))

        country = values.get("country").get("value")
        state = values.get("state").get("value")
        city = values.get("city").get("value")
        is_valid = cls.validate_contry_state_city(
            country,
            state,
            city,
        )
        if not is_valid:
            raise ValueError(
                f"The combination of values country: '{country}', state: '{state}', city_id: '{city}' does not match"
            )
        return values


class ClientValidationData(BaseModel):
    personal: UserPersonalDataValidation
    marital: UserMaritalDataSource
    documents: UserDocumentsDataValidation
    address: UserAddressDataValidation


class UserPersonalDataUpdate(BaseModel):
    name: Optional[NameSource]
    nick_name: Optional[NameSource]
    birth_date: Optional[BirthDateSource]
    gender: Optional[GenderSource]
    father_name: Optional[NameSource]
    mother_name: Optional[NameSource]
    email: Optional[EmailSource]
    phone: Optional[CelPhoneSource]
    nationality: Optional[NationalitySource]
    occupation_activity: Optional[ActivitySource]
    company_name: Optional[CompanyNameSource]
    company_cnpj: Optional[CnpjSource]
    patrimony: Optional[PatrimonySource]
    income: Optional[IncomeSource]
    tax_residences: Optional[TaxResidenceSource]
    birth_place_country: Optional[CountrySource]
    birth_place_state: Optional[StateSource]
    birth_place_city: Optional[CountySource]


class UserDocumentsDataUpdate(BaseModel):
    cpf: Optional[CpfSource]
    identity_type: Optional[DocumentTypesSource]
    identity_number: Optional[DocumentNumberSource]
    expedition_date: Optional[DateSource]
    issuer: Optional[IssuerSource]
    state: Optional[StateSource]


class UserAddressDataUpdate(BaseModel):
    country: Optional[CountrySource]
    state: Optional[StateSource]
    city: Optional[CountySource]
    neighborhood: Optional[NeighborhoodSource]
    street_name: Optional[StreetNameSource]
    number: Optional[AddressNumberSource]
    zip_code: Optional[ZipCodeSource]
    phone: Optional[PhoneSource]


class UpdateCustomerRegistrationData(BaseModel):
    personal: Optional[UserPersonalDataUpdate]
    marital: Optional[UserMaritalDataSource]
    documents: Optional[UserDocumentsDataUpdate]
    address: Optional[UserAddressDataUpdate]
