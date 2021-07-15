# STANDARD LIBS
from typing import Union, List, Optional

# OUTSIDE LIBRARIES
from fastapi import APIRouter, Request, Response
from pydantic import BaseModel

# SPHINX
from src.routers.validators.base import (
    Uuid,
    AppName,
    Successful,
    Error,
    Decision,
    Status,
    GenderSource,
    BirthDateSource,
    CountrySource,
    StateSource,
    MotherNameSource,
    DocumentTypeSource,
    CpfOrCnpjSource,
    DateSource,
    StateSource,
    IssuerSource,
    StreetNameSource,
    AddressNumberSource,
    CountrySource,
    CitySource,
    IdCitySource,
    ZipCodeSource,
    PhoneNumberSource,
    ActivitySource,
    CnpjSource,
    CompanyNameSource,
    PatrimonySource,
    IncomeSource,
    EducationLevelSource,
    EducationCourseSource,
    IsPoliticallyExposedPerson,
    DateOfAcquisition,
    Email,
    IncomeTaxTypeSource,
    ConnectedPersonSource,
    ClientTypeSource,
    PersonTypeSource,
    InvestorTypeTypeSource,
    CosifTaxClassificationSource,
    MaritalRegimeSource,
    NeighborhoodSource,
    AssetsDateSource,
    NationalitySource,
)
from src.controllers.base_controller import BaseController
from src.controllers.bureau_callbacks.bureau_callback import BureauCallbackController

router = APIRouter()


class DocumentData(BaseModel):
    number: CpfOrCnpjSource
    date: DateSource
    state: StateSource
    issuer: IssuerSource


class IdentifierDocument(BaseModel):
    type: DocumentTypeSource
    document_data: DocumentData


class Address(BaseModel):
    country: CountrySource
    street_name: StreetNameSource
    number: AddressNumberSource
    neighborhood: NeighborhoodSource
    country: CountrySource
    state: StateSource
    city: CitySource
    id_city: IdCitySource
    zip_code: ZipCodeSource
    phone_number: PhoneNumberSource


class Company(BaseModel):
    cpnj: CnpjSource
    name: CompanyNameSource


class Occupation(BaseModel):
    activity: ActivitySource
    company: Optional[Company]


class Assets(BaseModel):
    patrimony: PatrimonySource
    income: IncomeSource
    income_tax_type: IncomeTaxTypeSource
    date: AssetsDateSource


class Education(BaseModel):
    level: EducationLevelSource
    course: Optional[EducationCourseSource]


class PoliticallyExposedPerson(BaseModel):
    is_politically_exposed_person: IsPoliticallyExposedPerson


class Marital(BaseModel):
    marital_regime: MaritalRegimeSource
    spouse_birth_date: BirthDateSource


class Birthplace(BaseModel):
    nationality: NationalitySource
    country: CountrySource
    state: StateSource
    city: CitySource
    id_city: IdCitySource


class Output(Decision, Status, Email):
    gender: GenderSource
    birth_date: BirthDateSource
    birthplace: Birthplace
    mother_name: MotherNameSource
    identifier_document: IdentifierDocument
    address: Address
    occupation: Occupation
    assets: Assets
    education: Education
    politically_exposed_person: PoliticallyExposedPerson
    date_of_acquisition: DateOfAcquisition
    connected_person: ConnectedPersonSource
    person_type: PersonTypeSource
    client_type: ClientTypeSource
    investor_type: InvestorTypeTypeSource
    cosif_tax_classification: CosifTaxClassificationSource
    marital_update: Optional[Marital]


class BureauCallback(Uuid, AppName, Successful, Error):
    output: Output


@router.put("/bureau_callback", tags=["bureau_callback"])
def user_bureau_callback(bureau_callback: BureauCallback, request: Request):
    return BaseController.run(
        BureauCallbackController.process_callback, bureau_callback.dict(), request
    )
