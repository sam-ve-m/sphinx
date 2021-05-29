from fastapi import APIRouter, Request
from src.controllers.base_controller import BaseController
from src.controllers.view.controller import ViewController
from src.routers.validators.base import Name, DisplayName

router = APIRouter()


class View(Name, DisplayName):
    pass


@router.post("/view", tags=["view"])
async def create_view(view: View, request: Request):
    return BaseController.run(ViewController.create, dict(view), request)


@router.put("/view/{view_id}", tags=["view"])
async def update_view(view_id: str, view: DisplayName, request: Request):
    return BaseController.run(
        ViewController.update, {"view_id": view_id, "model": dict(view)}, request
    )


@router.delete("/view/{view_id}", tags=["view"])
async def delete_view(view_id: str, request: Request):
    return BaseController.run(ViewController.delete, {"view_id": view_id}, request)


@router.put("/view/{view_id}/{feature_id}", tags=["view"])
async def link_feature(view_id: str, feature_id: str, request: Request):
    return BaseController.run(
        ViewController.link_feature,
        {"view_id": view_id, "feature_id": feature_id},
        request,
    )


@router.get("/view/{view_id}", tags=["view"])
async def get_view(view_id: str, request: Request):
    return BaseController.run(ViewController.get_view, {"view_id": view_id}, request)
