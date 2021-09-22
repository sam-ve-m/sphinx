from typing import Optional, List

from pydantic import BaseModel

from src.routers.validators.base import (
    Email,
    PIN,
    Name,
    View,
    OptionalPIN,
    Feature,
    TermFile,
    Cpf,
    CelPhone,
    MaritalStatus,
    Nationality,
    QuizQuestionOption,
    IsUsPerson,
    UsTin,
    NickName,
    IsCvmQualifiedInvestor,
    FileBase64,
    ElectronicSignature,
    ChangeElectronicSignature,
    GenderSource,
    PatrimonySource,
    CompanyNameSource,
    CelPhoneSource,
    NationalitySource,
    CpfSource,
    CitySource,
    StreetNameSource,
    ZipCodeSource,
    UsTinSource,
    NameSource,
    CountrySource,
    StateSource,
    IssuerSource,
    IdentityDocumentNumber,
    DateSource,
    AddressNumberSource,
    IdCitySource,
    NeighborhoodSource,
    CnpjSource,
    ActivitySource,
    MaritalStatusSource,
    DeviceInformation,
    DeviceInformationOptional,
)


class UserSimple(Email, NickName, OptionalPIN):
    pass


class Spouse(Name, Cpf, Nationality):
    pass


class UserIdentifierData(Cpf, CelPhone):
    pass


class UserComplementaryData(MaritalStatus, IsUsPerson, UsTin, IsCvmQualifiedInvestor):
    spouse: Optional[Spouse]


class QuizResponses(BaseModel):
    device_information: Optional[DeviceInformationOptional]
    responses: List[QuizQuestionOption]


class UpdateCustomerRegistrationData(BaseModel):
    name: Optional[NameSource]
    gender: Optional[GenderSource]
    cel_phone: Optional[CelPhoneSource]
    patrimony: Optional[PatrimonySource]

    document_issuer: Optional[IssuerSource]
    document_state: Optional[StateSource]
    document_expedition_date: Optional[DateSource]
    document_identity_number: Optional[IdentityDocumentNumber]

    marital_status: Optional[MaritalStatusSource]
    marital_spouse_name: Optional[NameSource]
    marital_nationality: Optional[NationalitySource]
    marital_cpf: Optional[CpfSource]

    company_name: Optional[CompanyNameSource]
    occupation_activity: Optional[ActivitySource]
    occupation_cnpj: Optional[CnpjSource]

    address_country: Optional[CountrySource]
    address_state: Optional[StateSource]
    address_id_city: Optional[IdCitySource]
    address_city: Optional[CitySource]
    address_number: Optional[AddressNumberSource]
    address_street_name: Optional[StreetNameSource]
    address_zip_code: Optional[ZipCodeSource]
    address_neighborhood: Optional[NeighborhoodSource]

    us_tin: Optional[UsTinSource]

