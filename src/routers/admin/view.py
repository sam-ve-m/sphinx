from fastapi import Request

from src.controllers.base_controller import BaseController
from src.controllers.views.controller import ViewController
from src.domain.validators.base import View, LinkViewFeature
from src.routers.routes_registers.admin import AdminRouter

router = AdminRouter.instance()


@router.post("/view", tags=["views"])
async def create_view(view: View, request: Request):
    return await BaseController.run(ViewController.create, view.dict(), request)


@router.put("/view/id/{view_id}", tags=["views"])
async def update_view(view_id: str, view: View, request: Request):
    return await BaseController.run(
        ViewController.update, {"view_id": view_id, "model": view.dict()}, request
    )


@router.delete("/view/id/{view_id}", tags=["views"])
async def delete_view(view_id: str, request: Request):
    return await BaseController.run(
        ViewController.delete, {"view_id": view_id}, request
    )


@router.get("/view/id/{view_id}", tags=["views"])
async def get_view(view_id: str, request: Request):
    return await BaseController.run(
        ViewController.get_view, {"view_id": view_id}, request
    )


@router.get("/views", tags=["views"])
async def get_all(request: Request):
    return await BaseController.run(
        ViewController.get, {}, request
    )


@router.put("/view/link_feature", tags=["views_link"])
async def link_feature(link: LinkViewFeature, request: Request):
    return await BaseController.run(
        ViewController.link_feature,
        link.dict(),
        request,
    )


@router.delete("/view/link_feature", tags=["views_link"])
async def link_feature(link: LinkViewFeature, request: Request):
    return await BaseController.run(
        ViewController.delete_link_feature,
        link.dict(),
        request,
    )


@router.get("/views/link", tags=["views_link"])
async def link_feature(request: Request):
    return await BaseController.run(
        ViewController.get,
        {},
        request,
    )

#
# @router.delete("/view/link_feature", tags=["views_link"])
# # @router.requested_permissions(views=["async default"], features=["async default"])
# async def link_feature(link: LinkViewFeature, request: Request):
#     return await BaseController.run(
#         ViewController.delink_feature,
#         link.dict(),
#         request,
#     )
