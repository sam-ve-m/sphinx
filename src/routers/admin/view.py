from typing import Callable
from fastapi import Request, Depends
from src.controllers.base_controller import BaseController
from src.controllers.views.controller import ViewController
from src.domain.validators.base import View, LinkViewFeature
from src.routers.routes_registers.admin import AdminRouter


router = AdminRouter.instance()


@router.post("/views", tags=["views"])
def create_view(view: View, request: Request):
    return BaseController.run(ViewController.create, view.dict(), request)


@router.put("/views/id/{view_id}", tags=["views"])
def update_view(view_id: str, view: View, request: Request):
    return BaseController.run(
        ViewController.update, {"view_id": view_id, "model": view.dict()}, request
    )


@router.delete("/views/id/{view_id}", tags=["views"])
def delete_view(view_id: str, request: Request):
    return BaseController.run(ViewController.delete, {"view_id": view_id}, request)


@router.get("/views/id/{view_id}", tags=["views"])
def get_view(view_id: str, request: Request):
    return BaseController.run(ViewController.get_view, {"view_id": view_id}, request)


@router.put("/views/link_feature", tags=["views_link"])
def link_feature(link: LinkViewFeature, request: Request):
    return BaseController.run(
        ViewController.link_feature,
        link.dict(),
        request,
    )


@router.delete("/views/link_feature", tags=["views_link"])
@router.requested_permissions(views=["default"], features=["default"])
def link_feature(link: LinkViewFeature, request: Request):
    return BaseController.run(
        ViewController.delink_feature,
        link.dict(),
        request,
    )
