# OUTSIDE LIBRARIES
from fastapi import Request, Depends

# SPHINX
from src.controllers.base_controller import BaseController
from src.domain.validators.client_register_validators import CountryState, Country
from src.controllers.cliente_register_enums.controller import (
    ClientRegisterEnumsController,
)
from src.routers.routes_registers.user import UserRouter

router = UserRouter.instance()


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
    return BaseController.run(
        ClientRegisterEnumsController.get_county_update,
        payload=country_state.dict(),
        request=request,
    )


@router.get("/client_update_enums/state", tags=["client_update_enums"])
def get_state_update(request: Request, country: Country = Depends(Country)):
    return BaseController.run(
        ClientRegisterEnumsController.get_state_update,
        payload=country.dict(),
        request=request,
    )


@router.get("/client_update_enums/country", tags=["client_update_enums"])
def get_country_update(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_country_update, payload={}, request=request
    )


@router.get("/client_update_enums/economic_activity", tags=["client_update_enums"])
def get_economic_activity(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_economic_activity_update,
        payload={},
        request=request,
    )


@router.get("/client_update_enums/activity_type", tags=["client_update_enums"])
def get_economic_activity(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_activity_type_update,
        payload={},
        request=request,
    )


@router.get("/client_update_enums/issuing_body", tags=["client_update_enums"])
def get_economic_activity(request: Request):
    return BaseController.run(
        ClientRegisterEnumsController.get_issuing_body_update,
        payload={},
        request=request,
    )
