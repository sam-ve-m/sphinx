# OUTSIDE LIBRARIES
from fastapi import APIRouter, Request, Depends

# SPHINX
from src.controllers.base_controller import BaseController
from src.routers.validators.base import ClientType, Country, State
from src.controllers.cliente_register_enums.controller import (
    ClientRegisterEnumsController,
)

router = APIRouter()


class CountryState(Country, State):
    pass


@router.get("/client_register_enums/type_of_income_tax", tags=["client_register_enums"])
def get_type_of_income_tax(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_type_of_income_tax,
        payload={},
        request=request,
    )


@router.get("/client_register_enums/client_type", tags=["client_register_enums"])
def get_client_type(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_client_type, payload={}, request=request
    )


@router.get("/client_register_enums/investor_type", tags=["client_register_enums"])
def get_investor_type(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_investor_type, payload={}, request=request
    )


@router.get("/client_register_enums/activity_type", tags=["client_register_enums"])
def get_activity_type(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_activity_type, payload={}, request=request
    )


@router.get(
    "/client_register_enums/type_ability_person", tags=["client_register_enums"]
)
def get_type_ability_person(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_type_ability_person,
        payload={},
        request=request,
    )


@router.get(
    "/client_register_enums/customer_qualification_type", tags=["client_register_enums"]
)
def get_customer_qualification_type(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_customer_qualification_type,
        payload={},
        request=request,
    )


@router.get(
    "/client_register_enums/cosif_tax_classification", tags=["client_register_enums"]
)
def get_cosif_tax_classification(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_cosif_tax_classification,
        payload={},
        request=request,
    )


@router.get("/client_register_enums/marital_status", tags=["client_register_enums"])
def get_marital_status(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_marital_status, payload={}, request=request
    )


@router.get("/client_register_enums/nationality", tags=["client_register_enums"])
def get_nationality(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_nationality, payload={}, request=request
    )


@router.get(
    "/client_register_enums/document_issuing_body", tags=["client_register_enums"]
)
def get_document_issuing_body(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_document_issuing_body,
        payload={},
        request=request,
    )


@router.get("/client_register_enums/document_type", tags=["client_register_enums"])
def get_document_type(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_document_type, payload={}, request=request
    )


@router.get("/client_register_enums/county", tags=["client_register_enums"])
def get_county(request: Request, country_state: CountryState = Depends(CountryState)):
    payload = dict()
    payload.update(country_state.dict())
    return BaseController.run(
        ClientRegisterEnumsController.get_county, payload=payload, request=request
    )


@router.get("/client_register_enums/state", tags=["client_register_enums"])
def get_state(request: Request, country: Country = Depends(Country)):
    payload = dict()
    payload.update(country.dict())
    return BaseController.run(
        ClientRegisterEnumsController.get_state, payload=payload, request=request
    )


@router.get("/client_register_enums/country", tags=["client_register_enums"])
def get_country(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_country, payload={}, request=request
    )


@router.get("/client_register_enums/marriage_regime", tags=["client_register_enums"])
def get_marriage_regime(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_marriage_regime, payload={}, request=request
    )


@router.get("/client_register_enums/customer_origin", tags=["client_register_enums"])
def get_customer_origin(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_customer_origin, payload={}, request=request
    )


@router.get("/client_register_enums/customer_status", tags=["client_register_enums"])
def get_customer_status(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_customer_status, payload={}, request=request
    )


@router.get("/client_register_enums/customer_status", tags=["client_register_enums"])
def get_bmf_customer_type(client_type: ClientType, request: Request):
    payload = dict()
    payload.update(client_type.dict(), request=request)
    return BaseController.run(
        ClientRegisterEnumsController.get_bmf_customer_type(payload=payload),
        request=request,
    )


@router.get("/client_register_enums/economic_activity", tags=["client_register_enums"])
def get_economic_activity(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_economic_activity, payload={}, request=request
    )


@router.get("/client_register_enums/account_type", tags=["client_register_enums"])
def get_account_type(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_account_type, payload={}, request=request
    )


@router.get("/client_update_enums/gender", tags=["client_update_enums"])
def get_gender_update(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_gender_update, payload={}, request=request
    )


@router.get("/client_update_enums/marital_status", tags=["client_update_enums"])
def get_marital_status_update(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_marital_status_update,
        payload={},
        request=request,
    )


@router.get("/client_update_enums/nationality", tags=["client_update_enums"])
def get_nationality_update(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_nationality_update,
        payload={},
        request=request,
    )


@router.get("/client_update_enums/county", tags=["client_update_enums"])
def get_county_update(
    request: Request, country_state: CountryState = Depends(CountryState)
):
    payload = dict()
    payload.update(country_state.dict())
    return BaseController.run(
        ClientRegisterEnumsController.get_county_update,
        payload=payload,
        request=request,
    )


@router.get("/client_update_enums/state", tags=["client_update_enums"])
def get_state_update(request: Request, country: Country = Depends(Country)):
    payload = dict()
    payload.update(country.dict())
    return BaseController.run(
        ClientRegisterEnumsController.get_state_update, payload=payload, request=request
    )


@router.get("/client_update_enums/country", tags=["client_update_enums"])
def get_country_update(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_country_update, payload={}, request=request
    )


@router.get("/client_update_enums/economic_activity", tags=["client_register_enums"])
def get_economic_activity(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_economic_activity_update,
        payload={},
        request=request,
    )


@router.get("/client_update_enums/activity_type", tags=["client_register_enums"])
def get_economic_activity(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_activity_type_update,
        payload={},
        request=request,
    )
