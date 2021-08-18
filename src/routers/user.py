# STANDARD LIBS
from typing import Union, List, Optional

# OUTSIDE LIBRARIES
from fastapi import APIRouter, Request, Response, UploadFile, File, Depends
from pydantic import BaseModel

# SPHINX
from src.routers.validators.base import (
    Email,
    PIN,
    Name,
    View,
    OptionalPIN,
    Feature,
    TermFile,
    Cpf,
    CelPhone,
    MaritalStatus,
    Nationality,
    QuizQuestionOption,
    IsUsPerson,
    UsTin,
    NickName,
    IsCvmQualifiedInvestor,
    FileBase64,
    ElectronicSignature,
)
from src.utils.jwt_utils import JWTHandler
from src.controllers.base_controller import BaseController
from src.controllers.users.controller import UserController

router = APIRouter()


class UserSimple(Email, NickName, OptionalPIN):
    pass


class Spouse(Name, Cpf, Nationality):
    pass


class UserIdentifierData(Cpf, CelPhone):
    pass


class UserComplementaryData(MaritalStatus, IsUsPerson, UsTin, IsCvmQualifiedInvestor):
    spouse: Optional[Spouse]


class QuizResponses(BaseModel):
    responses: List[QuizQuestionOption]


@router.post("/user", tags=["user"])
def create_user(user: UserSimple, request: Request):
    return BaseController.run(UserController.create, dict(user), request)


@router.post("/user_admin", tags=["user"])
def create_admin(user: UserSimple, request: Request):
    return BaseController.run(UserController.create_admin, dict(user), request)


@router.get("/user/forgot_password", tags=["user"])
def forgot_password(request: Request, user: Email = Depends(Email)):
    return BaseController.run(UserController.forgot_password, user.dict(), request)


@router.put("/user/identifier_data", tags=["user"])
def update_user_identifier_data(user_identifier: UserIdentifierData, request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "x-thebes-answer": jwt_data_or_error_response,
        "user_identifier": user_identifier.dict(),
    }
    return BaseController.run(UserController.user_identifier_data, payload, request)


@router.put("/user/complementary_data", tags=["user"])
def update_user_complementary_data(
    user_identifier: UserComplementaryData, request: Request
):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "x-thebes-answer": jwt_data_or_error_response,
        "user_complementary": user_identifier.dict(),
    }
    return BaseController.run(UserController.user_complementary_data, payload, request)


@router.get("/user/quiz", tags=["user"])
def user_quiz(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response

    payload = {
        "x-thebes-answer": jwt_data_or_error_response,
    }
    return BaseController.run(UserController.user_quiz, payload, request)


@router.put("/user/send_quiz_responses", tags=["user"])
def send_quiz_responses(quiz_response: QuizResponses, request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "x-thebes-answer": jwt_data_or_error_response,
        "quiz": quiz_response.dict(),
    }
    return BaseController.run(UserController.send_quiz_responses, payload, request)


@router.delete("/user", tags=["user"])
def delete_user(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    return BaseController.run(
        UserController.delete, jwt_data_or_error_response, request
    )


@router.put("/user/change_password", tags=["user"])
def change_user_password(pin: PIN, request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "x-thebes-answer": jwt_data_or_error_response,
        "new_pin": pin.dict().get("pin"),
    }
    return BaseController.run(UserController.change_password, payload, request)


@router.put("/user/logout_all", tags=["user"])
def logout_all(request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    return BaseController.run(
        UserController.logout_all, jwt_data_or_error_response, request
    )


@router.put("/user/views", tags=["user"])
def change_user_view(view: View, request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "x-thebes-answer": jwt_data_or_error_response,
        "new_view": view.dict().get("views"),
    }
    return BaseController.run(UserController.change_view, payload, request)


@router.put("/user/purchase", tags=["user"])
def add_features_to_user(feature: Feature, request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "x-thebes-answer": jwt_data_or_error_response,
        "feature": feature.dict().get("feature"),
    }
    return BaseController.run(UserController.add_feature, dict(payload), request)


@router.delete("/user/purchase", tags=["user"])
def remove_features_to_user(feature: Feature, request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "x-thebes-answer": jwt_data_or_error_response,
        "feature": feature.dict().get("feature"),
    }
    return BaseController.run(UserController.delete_feature, dict(payload), request)


@router.post("/user/selfie", tags=["user"], include_in_schema=True)
async def save_user_selfie(request: Request, file_or_base64: FileBase64):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "x-thebes-answer": jwt_data_or_error_response,
        "file_or_base64": file_or_base64.file_or_base64,
    }
    return BaseController.run(UserController.save_user_selfie, payload, request)


@router.put("/user/sign_term", tags=["user"])
async def sign_term(
    request: Request,
    file_type: TermFile,
):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = file_type.dict()
    payload.update({"x-thebes-answer": jwt_data_or_error_response})
    return BaseController.run(UserController.sign_term, payload, request)


@router.get("/user/signed_term", tags=["user"])
async def get_assigned_term(
    request: Request,
    file_type: TermFile = Depends(TermFile),
):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = file_type.dict()
    payload.update({"x-thebes-answer": jwt_data_or_error_response})
    return BaseController.run(UserController.get_signed_term, payload, request)


@router.get("/user/onboarding_user_current_step", tags=["user"])
async def get_onboarding_user_current_step(
    request: Request,
):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response

    payload = {
        "x-thebes-answer": jwt_data_or_error_response,
    }
    return BaseController.run(
        UserController.get_onboarding_user_current_step, payload, request
    )


@router.put("/user/electronic_signature", tags=["user"])
def set_user_electronic_signature(
    electronic_signature: ElectronicSignature, request: Request
):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "x-thebes-answer": jwt_data_or_error_response,
        "electronic_signature": electronic_signature.dict().get("electronic_signature"),
    }
    return BaseController.run(
        UserController.set_user_electronic_signature, payload, request
    )
