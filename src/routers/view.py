from fastapi import APIRouter, Request
from src.controllers.base_controller import BaseController
from src.controllers.views.controller import ViewController
from src.routers.validators.base import Name, DisplayName

router = APIRouter()


class View(Name, DisplayName):
    pass


@router.post("/views", tags=["views"])
def create_view(view: View, request: Request):
    return BaseController.run(ViewController.create, dict(view), request)


@router.put("/views/{view_id}", tags=["views"])
def update_view(view_id: str, view: DisplayName, request: Request):
    return BaseController.run(
        ViewController.update, {"view_id": view_id, "model": dict(view)}, request
    )


@router.delete("/views/{view_id}", tags=["views"])
def delete_view(view_id: str, request: Request):
    return BaseController.run(ViewController.delete, {"view_id": view_id}, request)


@router.put("/views/{view_id}/{feature_id}", tags=["views"])
def link_feature(view_id: str, feature_id: str, request: Request):
    return BaseController.run(
        ViewController.link_feature,
        {"view_id": view_id, "feature_id": feature_id},
        request,
    )


@router.get("/views/{view_id}", tags=["views"])
def get_view(view_id: str, request: Request):
    return BaseController.run(ViewController.get_view, {"view_id": view_id}, request)
