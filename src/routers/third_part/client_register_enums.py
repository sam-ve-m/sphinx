# OUTSIDE LIBRARIES
from fastapi import Request, Depends

# SPHINX
from src.controllers.base_controller import BaseController
from src.domain.validators.client_register_validators import CountryState
from src.domain.validators.bureau_validators import Country
from src.controllers.cliente_register_enums.controller import (
    ClientRegisterEnumsController,
)
from src.routers.routes_registers.third_part import ThirdPartRouter

router = ThirdPartRouter.instance()


@router.get("/client_register_enums/city", tags=["client_register_enums"])
async def get_county(
    request: Request, country_state: CountryState = Depends(CountryState)
):
    return await BaseController.run(
        ClientRegisterEnumsController.get_county,
        payload=country_state.dict(),
        request=request,
    )


@router.get("/client_register_enums/state", tags=["client_register_enums"])
async def get_state(request: Request, country: Country = Depends(Country)):
    return await BaseController.run(
        ClientRegisterEnumsController.get_state, payload=country.dict(), request=request
    )


@router.get("/client_register_enums/nationality", tags=["client_register_enums"])
async def get_nationality(request: Request):
    return await BaseController.run(
        ClientRegisterEnumsController.get_nationality, payload={}, request=request
    )


@router.get("/client_register_enums/document_type", tags=["client_register_enums"])
async def get_document_type(request: Request):
    return await BaseController.run(
        ClientRegisterEnumsController.get_document_type, payload={}, request=request
    )


@router.get("/client_register_enums/country", tags=["client_register_enums"])
async def get_country(request: Request):
    return await BaseController.run(
        ClientRegisterEnumsController.get_country, payload={}, request=request
    )


@router.get("/client_register_enums/activity_type", tags=["client_register_enums"])
async def get_activity_type(request: Request):
    return await BaseController.run(
        ClientRegisterEnumsController.get_activity_type, payload={}, request=request
    )


@router.get(
    "/client_register_enums/document_issuing_body", tags=["client_register_enums"]
)
async def get_activity_type(request: Request):
    return await BaseController.run(
        ClientRegisterEnumsController.get_document_issuing_body,
        payload={},
        request=request,
    )


@router.get("/client_register_enums/all_in_one", tags=["client_register_enums"])
async def get_activity_type(request: Request):
    return await BaseController.run(
        ClientRegisterEnumsController.all_in_one, payload={}, request=request
    )
