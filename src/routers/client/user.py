# STANDARD LIBS
from enum import Enum
from typing import Union, List, Optional

# OUTSIDE LIBRARIES
from fastapi import APIRouter, Request, Response, UploadFile, File, Depends
from pydantic import BaseModel, constr, ValidationError

# SPHINX
from src.routers.validators.base import (
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
)

from src.utils.jwt_utils import JWTHandler
from src.controllers.base_controller import BaseController
from src.controllers.users.controller import UserController
from src.routers.routes_registers.client import ClientRouter

router = ClientRouter.instance()


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


@router.delete("/user", tags=["user"])
def delete_user(request: Request):
    jwt_data = JWTHandler.get_thebes_answer_from_request(request=request)

    return BaseController.run(UserController.delete, jwt_data, request)


@router.get("/user/customer_registration_data", tags=["user"])
def get_customer_registration_data(request: Request):
    jwt_data = JWTHandler.get_thebes_answer_from_request(request=request)

    payload = {
        "x-thebes-answer": jwt_data,
    }

    return BaseController.run(
        UserController.get_customer_registration_data, payload, request
    )


@router.put("/user/customer_registration_data", tags=["user"])
def update_customer_registration_data(
    customer_registration_data: UpdateCustomerRegistrationData, request: Request
):
    jwt_data = JWTHandler.get_thebes_answer_from_request(request=request)

    payload = {
        "x-thebes-answer": jwt_data,
        "customer_registration_data": customer_registration_data.dict(),
    }

    return BaseController.run(
        UserController.update_customer_registration_data, payload, request
    )
