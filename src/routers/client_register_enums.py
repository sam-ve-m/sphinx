# OUTSIDE LIBRARIES
from fastapi import APIRouter, Request, Response

# SPHINX
from src.controllers.base_controller import BaseController
from src.routers.validators.base import (
    ClientType,
    Country,
    State
)
from src.utils.jwt_utils import JWTHandler
from src.controllers.cliente_register_enums.controller import ClientRegisterEnumsController

router = APIRouter()


class CountryState(Country, State):
    pass


@router.get('/client_register_enums/type_of_income_tax', tags=['client_register_enums'])
def get_type_of_income_tax(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response
    }
    return BaseController.run(ClientRegisterEnumsController.get_type_of_income_tax(payload=payload))


@router.get('/client_register_enums/client_type', tags=['client_register_enums'])
def get_client_type(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response
    }
    return BaseController.run(ClientRegisterEnumsController.get_client_type(payload=payload))


@router.get('/client_register_enums/investor_type', tags=['client_register_enums'])
def get_investor_type(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response
    }
    return BaseController.run(ClientRegisterEnumsController.get_investor_type(payload=payload))


@router.get('/client_register_enums/activity_type', tags=['client_register_enums'])
def get_activity_type(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response
    }
    return BaseController.run(ClientRegisterEnumsController.get_activity_type(payload=payload))


@router.get('/client_register_enums/type_ability_person', tags=['client_register_enums'])
def get_type_ability_person(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response
    }
    return BaseController.run(ClientRegisterEnumsController.get_type_ability_person(payload=payload))


@router.get('/client_register_enums/customer_qualification_type', tags=['client_register_enums'])
def get_customer_qualification_type(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response
    }
    return BaseController.run(ClientRegisterEnumsController.get_customer_qualification_type(payload=payload))


@router.get('/client_register_enums/cosif_tax_classification', tags=['client_register_enums'])
def get_cosif_tax_classification(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response
    }
    return BaseController.run(ClientRegisterEnumsController.get_cosif_tax_classification(payload=payload))


@router.get('/client_register_enums/marital_status', tags=['client_register_enums'])
def get_marital_status(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response
    }
    return BaseController.run(ClientRegisterEnumsController.get_marital_status(payload=payload))


@router.get('/client_register_enums/nationality', tags=['client_register_enums'])
def get_nationality(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response
    }
    return BaseController.run(ClientRegisterEnumsController.get_nationality(payload=payload))


@router.get('/client_register_enums/document_issuing_body', tags=['client_register_enums'])
def get_document_issuing_body(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response
    }
    return BaseController.run(ClientRegisterEnumsController.get_document_issuing_body(payload=payload))


@router.get('/client_register_enums/document_type', tags=['client_register_enums'])
def get_document_type(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response
    }
    return BaseController.run(ClientRegisterEnumsController.get_document_type(payload=payload))


@router.get('/client_register_enums/county', tags=['client_register_enums'])
def get_county(country_state: CountryState, request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response
    }
    payload.update(country_state.dict())
    return BaseController.run(ClientRegisterEnumsController.get_county(payload=payload))


@router.get('/client_register_enums/state', tags=['client_register_enums'])
def get_state(country: Country, request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response
    }
    payload.update(country.dict())
    return BaseController.run(ClientRegisterEnumsController.get_state(payload=payload))


@router.get('/client_register_enums/country', tags=['client_register_enums'])
def get_country(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response
    }
    return BaseController.run(ClientRegisterEnumsController.get_country(payload=payload))


@router.get('/client_register_enums/marriage_regime', tags=['client_register_enums'])
def get_marriage_regime(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response
    }
    return BaseController.run(ClientRegisterEnumsController.get_marriage_regime(payload=payload))


@router.get('/client_register_enums/customer_origin', tags=['client_register_enums'])
def get_customer_origin(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response
    }
    return BaseController.run(ClientRegisterEnumsController.get_customer_origin(payload=payload))


@router.get('/client_register_enums/customer_status', tags=['client_register_enums'])
def get_customer_status(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response
    }
    return BaseController.run(ClientRegisterEnumsController.get_customer_status(payload=payload))


@router.get('/client_register_enums/bmf_customer_type', tags=['client_register_enums'])
def get_bmf_customer_type(client_type: ClientType, request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response
    }
    payload.update(client_type.dict())
    return BaseController.run(ClientRegisterEnumsController.get_bmf_customer_type(payload=payload))


@router.get('/client_register_enums/economic_activity', tags=['client_register_enums'])
def get_economic_activity(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response
    }
    return BaseController.run(ClientRegisterEnumsController.get_economic_activity(payload=payload))


@router.get('/client_register_enums/account_type', tags=['client_register_enums'])
def get_account_type(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response
    }
    return BaseController.run(ClientRegisterEnumsController.get_account_type(payload=payload))
