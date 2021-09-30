from fastapi import Request
from src.controllers.base_controller import BaseController
from src.controllers.views.controller import ViewController
from src.services.validators.onboarding_validators import DisplayName
from src.services.validators.base import View
from src.routers.routes_registers.admin import AdminRouter


router = AdminRouter.instance()


@router.post("/views", tags=["views"])
def create_view(view: View, request: Request):
    return BaseController.run(ViewController.create, view.dict(), request)


@router.put("/views/{view_id}", tags=["views"])
def update_view(view_id: str, view: DisplayName, request: Request):
    return BaseController.run(
        ViewController.update, {"view_id": view_id, "model": view.dict()}, request
    )


@router.delete("/views/{view_id}", tags=["views"])
def delete_view(view_id: str, request: Request):
    return BaseController.run(ViewController.delete, {"view_id": view_id}, request)


@router.put("/views/{view_id}/{feature_id}", tags=["views"])
def link_feature(view_id: str, feature_id: str, request: Request):
    # TODO: Create validator to ensure the view_id and feature_id
    return BaseController.run(
        ViewController.link_feature,
        {"view_id": view_id, "feature_id": feature_id},
        request,
    )


@router.get("/views/{view_id}", tags=["views"])
def get_view(view_id: str, request: Request):
    return BaseController.run(ViewController.get_view, {"view_id": view_id}, request)
