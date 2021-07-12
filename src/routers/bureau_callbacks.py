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
    NationalitySource,
    NaturalnessSource,
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
    ZipCodeSource,
    PhoneNumberSource,
    ActivitySource,
    CnpjSource,
    CompanyNameSource
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
    street_name: StreetNameSource
    number: AddressNumberSource
    country: CountrySource
    state: StateSource
    city: CitySource
    zip_code: ZipCodeSource
    phone_number: PhoneNumberSource


class Company(BaseModel):
    cpnj: CnpjSource
    name: CompanyNameSource


class Occupation(BaseModel):
    activity: ActivitySource
    company: Optional[Company]


class Output(Decision, Status):
    gender: GenderSource
    birth_date: BirthDateSource
    nationality: NationalitySource
    naturalness: NaturalnessSource
    mother_name: MotherNameSource
    identifier_document: IdentifierDocument
    address: Address
    occupation: Occupation


class BureauCallback(Uuid, AppName, Successful, Error):
    output: Output


@router.put("/bureau_callback", tags=["bureau_callback"])
def user_bureau_callback(bureau_callback: BureauCallback, request: Request):
    return BaseController.run(
        BureauCallbackController.process_callback, bureau_callback.dict(), request
    )
