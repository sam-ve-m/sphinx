from typing import List

from src.domain.validators.base import *
from src.domain.validators.bureau_validators import *
from src.repositories.sinacor_types.repository import SinaCorTypesRepository


class UserSimple(Email, NickName, OptionalPIN):
    pass


class Spouse(Name, Cpf, Nationality):
    pass


class Country(BaseModel):
    country: constr(min_length=3, max_length=3)

    @validator("country", always=True, allow_reuse=True)
    def validate_country(cls, e):
        sinacor_types_repository = SinaCorTypesRepository()
        if sinacor_types_repository.validate_country(value=e):
            return e
        raise ValueError("nationality not exists")


class TaxResidence(Country):
    tax_number: str


class UserIdentifierData(Cpf, CelPhone):
    tax_residences: Optional[List[TaxResidence]]


# TODO: IsCvmQualifiedInvestor must relly remove this?
class UserComplementaryData(MaritalStatus):
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

    marital_status: Optional[MaritalStatus]
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
