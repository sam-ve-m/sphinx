# OUTSIDE LIBRARIES
from fastapi import Request

# SPHINX
from src.domain.validators.user_validators import UpdateCustomerRegistrationData
from src.services.jwts.service import JwtService
from src.controllers.base_controller import BaseController
from src.controllers.users.controller import UserController
from src.routers.routes_registers.client import ClientRouter

router = ClientRouter.instance()


@router.delete("/user", tags=["user"])
def delete_user(request: Request):
    jwt_data = JwtService.get_thebes_answer_from_request(request=request)

    return BaseController.run(UserController.delete, jwt_data, request)


@router.get("/user/customer_registration_data", tags=["user"])
def get_customer_registration_data(request: Request):
    jwt_data = JwtService.get_thebes_answer_from_request(request=request)

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
    jwt_data = JwtService.get_thebes_answer_from_request(request=request)

    payload = {
        "x-thebes-answer": jwt_data,
        "customer_registration_data": customer_registration_data.dict(),
    }

    return BaseController.run(
        UserController.update_customer_registration_data, payload, request
    )
