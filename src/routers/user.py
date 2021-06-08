# STANDARD LIBS
from typing import Union, List

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
    MaritalStatus,
    Nationality,
    QuizQuestionOption
)
from src.utils.jwt_utils import JWTHandler
from src.controllers.base_controller import BaseController
from src.controllers.users.controller import UserController

router = APIRouter()


class UserSimple(Email, Name, OptionalPIN):
    pass


class Spouse(Name, Cpf, Nationality):
    pass


class UserIdentifierData(Cpf, MaritalStatus):
    spouse: Spouse


class QuizResponses(BaseModel):
    responses: List[QuizQuestionOption]


@router.post("/user", tags=["user"])
def create_user(user: UserSimple, request: Request):
    return BaseController.run(UserController.create, dict(user), request)


@router.post("/user_admin", tags=["user"])
def create_admin(user: UserSimple, request: Request):
    return BaseController.run(UserController.create_admin, dict(user), request)


@router.get("/user/forgot_password", tags=["user"])
def forgot_password(user: Email, request: Request):
    return BaseController.run(UserController.forgot_password, user.dict(), request)


@router.put("/user/identifier_data", tags=["user"])
def update_user_data(user_identifier: UserIdentifierData, request: Request):
    # TODO: salvar dados minimos para envio para STONEAGE e retornar quiz
    return BaseController.run(UserController.create_admin, user_identifier.dict(), request)


@router.put("/user/fill_user_data", tags=["user"])
def update_user_data(quiz_response: QuizResponses, request: Request):
    # TODO: recebe respostas do quiz e manda apra STONEAGE espera o retorno com dados ou um retorno async
    return BaseController.run(UserController.create_admin, quiz_response.dict(), request)


@router.put("/user/table_callback", tags=["user"])
def update_user_data(user: UserSimple, request: Request):
    # TODO: Callback da STONEAGE
    pass
    # return BaseController.run(UserController.create_admin, dict(user), request)


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
        "thebes_answer": jwt_data_or_error_response,
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
        "thebes_answer": jwt_data_or_error_response,
        "new_view": view.dict().get("views"),
    }
    return BaseController.run(UserController.change_view, payload, request)


@router.put("/user/purchase", tags=["user"])
def add_features_to_user(feature: Feature, request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response,
        "feature": feature.dict().get("feature"),
    }
    return BaseController.run(UserController.add_feature, dict(payload), request)


@router.delete("/user/purchase", tags=["user"])
def remove_features_to_user(feature: Feature, request: Request):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = {
        "thebes_answer": jwt_data_or_error_response,
        "feature": feature.dict().get("feature"),
    }
    return BaseController.run(UserController.delete_feature, dict(payload), request)


@router.post("/user/self", tags=["user"])
async def save_user_self(
    request: Request, file_or_base64: Union[UploadFile, str] = File(...)
):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    if isinstance(file_or_base64, str) is False:
        file_or_base64 = await file_or_base64.read()
    payload = {
        "thebes_answer": jwt_data_or_error_response,
        "file_or_base64": file_or_base64,
    }
    return BaseController.run(UserController.save_user_self, payload, request)


@router.put("/user/sign_term", tags=["user"])
async def sign_term(
    request: Request, file_type: TermFile,
):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = file_type.dict()
    payload.update({"thebes_answer": jwt_data_or_error_response})
    return BaseController.run(UserController.sign_term, payload, request)


@router.get("/user/signed_term", tags=["user"])
async def get_assigned_term(
    request: Request, file_type: TermFile = Depends(TermFile),
):
    jwt_data_or_error_response = JWTHandler.get_payload_from_request(request=request)
    if isinstance(jwt_data_or_error_response, Response):
        return jwt_data_or_error_response
    payload = file_type.dict()
    payload.update({"thebes_answer": jwt_data_or_error_response})
    return BaseController.run(UserController.get_signed_term, payload, request)
