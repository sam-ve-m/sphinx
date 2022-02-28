# OUTSIDE LIBRARIES
from fastapi import Request, Depends

# SPHINX
from src.domain.validators.base import (
    PIN,
    ElectronicSignature,
    ChangeElectronicSignature,
    View,
    Feature,
)
from src.domain.validators.onboarding_validators import (
    TermFile,
    FileBase64,
)
from src.services.jwts.service import JwtService
from src.controllers.base_controller import BaseController
from src.controllers.users.controller import UserController
from src.routers.routes_registers.user import UserRouter
from src.domain.validators.bureau_validators import (
    UpdateCustomerRegistrationData,
    ClientValidationData,
    UserMaritalData,
)
from src.domain.validators.user_validators import UserIdentifierData

router = UserRouter.instance()


@router.put("/user/identifier_data", tags=["user"])
async def update_user_identifier_data(
    user_identifier: UserIdentifierData, request: Request
):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)

    payload = {
        "x-thebes-answer": jwt_data,
        "user_identifier": user_identifier.dict(),
    }
    return await BaseController.run(
        UserController.user_identifier_data, payload, request
    )


@router.put("/user/complementary_data", tags=["user"])
async def update_user_complementary_data(
    user_identifier: UserMaritalData, request: Request
):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)

    payload = {
        "x-thebes-answer": jwt_data,
        "user_complementary": user_identifier.dict(),
    }
    return await BaseController.run(
        UserController.user_complementary_data, payload, request
    )


@router.delete("/user", tags=["user"])
async def delete_user(request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)

    return BaseController.run(UserController.delete, jwt_data, request)


@router.put("/user/change_password", tags=["user"])
async def change_user_password(pin: PIN, request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)

    payload = {
        "x-thebes-answer": jwt_data,
        "new_pin": pin.dict()["pin"],
    }
    return await BaseController.run(UserController.change_password, payload, request)


@router.put("/user/logout_all", tags=["user"])
async def logout_all(request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    return await BaseController.run(UserController.logout_all, jwt_data, request)


@router.put("/user/views", tags=["user"])
async def change_user_view(view: View, request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    payload = {
        "x-thebes-answer": jwt_data,
        "new_view": view.dict()["views"],
    }
    return await BaseController.run(UserController.change_view, payload, request)


@router.put("/user/purchase", tags=["user"])
async def add_features_to_user(feature: Feature, request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)

    payload = {
        "x-thebes-answer": jwt_data,
        "feature": feature.dict()["feature"],
    }
    return await BaseController.run(UserController.add_feature, dict(payload), request)


@router.delete("/user/purchase", tags=["user"])
async def remove_features_to_user(feature: Feature, request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)

    payload = {
        "x-thebes-answer": jwt_data,
        "feature": feature.dict()["feature"],
    }
    return await BaseController.run(
        UserController.delete_feature, dict(payload), request
    )


@router.post("/user/selfie", tags=["user"], include_in_schema=True)
async def save_user_selfie(request: Request, file_or_base64: FileBase64):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)

    payload = {
        "x-thebes-answer": jwt_data,
        "file_or_base64": file_or_base64.file_or_base64,
    }
    return await BaseController.run(UserController.save_user_selfie, payload, request)


@router.put("/user/sign_term", tags=["user"])
async def sign_term(
    request: Request,
    file_type: TermFile,
):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)

    payload = file_type.dict()
    payload.update({"x-thebes-answer": jwt_data})
    return await BaseController.run(UserController.sign_term, payload, request)


@router.get("/user/signed_term", tags=["user"])
async def get_assigned_term(
    request: Request,
    file_type: TermFile = Depends(TermFile),
):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    payload = file_type.dict()
    payload.update({"x-thebes-answer": jwt_data})
    return await BaseController.run(UserController.get_signed_term, payload, request)


@router.get("/user/onboarding_user_current_step", tags=["user"])
async def get_onboarding_user_current_step(
    request: Request,
):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)

    payload = {
        "x-thebes-answer": jwt_data,
    }
    return await BaseController.run(
        UserController.get_onboarding_user_current_step, payload, request
    )


@router.put("/user/electronic_signature", tags=["user"])
async def set_user_electronic_signature(
    electronic_signature: ElectronicSignature, request: Request
):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)

    payload = {
        "x-thebes-answer": jwt_data,
        "electronic_signature": electronic_signature.dict().get("electronic_signature"),
    }
    return await BaseController.run(
        UserController.set_user_electronic_signature, payload, request
    )


@router.get("/user/forgot_electronic_signature", tags=["user"])
async def forgot_electronic_signature(request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)

    payload = {
        "x-thebes-answer": jwt_data,
    }

    return await BaseController.run(
        UserController.forgot_electronic_signature, payload, request
    )


@router.put("/user/reset_electronic_signature", tags=["user"])
async def reset_electronic_signature(
    electronic_signature: ElectronicSignature, request: Request
):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)

    payload = {
        "x-thebes-answer": jwt_data,
        "new_electronic_signature": electronic_signature.dict()["electronic_signature"],
    }

    return await BaseController.run(
        UserController.reset_electronic_signature, payload, request
    )


@router.put("/user/change_electronic_signature", tags=["user"])
async def change_electronic_signature(
    electronic_signatures: ChangeElectronicSignature, request: Request
):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)

    electronic_signatures_dict = electronic_signatures.dict()
    payload = {
        "x-thebes-answer": jwt_data,
        "current_electronic_signature": electronic_signatures_dict.get(
            "electronic_signature"
        ),
        "new_electronic_signature": electronic_signatures_dict.get(
            "new_electronic_signature"
        ),
    }

    return await BaseController.run(
        UserController.change_electronic_signature, payload, request
    )


@router.get("/user/customer_registration_data", tags=["user"])
async def get_customer_registration_data(request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    payload = {
        "x-thebes-answer": jwt_data,
    }
    return await BaseController.run(
        UserController.get_customer_registration_data, payload, request
    )


@router.put("/user/customer_registration_data", tags=["user"])
async def update_customer_registration_data(
    customer_registration_data: UpdateCustomerRegistrationData, request: Request
):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    payload = {
        "x-thebes-answer": jwt_data,
        "customer_registration_data": customer_registration_data.dict(),
    }
    return await BaseController.run(
        UserController.update_customer_registration_data, payload, request
    )


@router.get("/user/customer_validation_data", tags=["user"])
async def get_customer_registration_data(request: Request):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    payload = {
        "x-thebes-answer": jwt_data,
    }
    return await BaseController.run(
        UserController.get_customer_registration_data, payload, request
    )


@router.put("/user/customer_validation_data", tags=["user"])
async def update_customer_registration_data(
    customer_validation_data: ClientValidationData, request: Request
):
    jwt_data = await JwtService.get_thebes_answer_from_request(request=request)
    payload = {
        "x-thebes-answer": jwt_data,
        "customer_registration_data": customer_validation_data.dict(),
    }
    return await BaseController.run(
        UserController.update_customer_registration_data, payload, request
    )
