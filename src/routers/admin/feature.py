from fastapi import Request

from src.controllers.base_controller import BaseController
from src.controllers.features.controller import FeatureController
from src.domain.validators.base import Feature
from src.routers.routes_registers.admin import AdminRouter

router = AdminRouter.instance()


@router.post("/feature", tags=["feature"])
async def create_feature(feature: Feature, request: Request):
    return await BaseController.run(FeatureController.create, feature.dict(), request)


@router.put("/feature/{feature_id}", tags=["feature"])
async def update_feature(feature_id: str, feature: Feature, request: Request):
    return await BaseController.run(
        FeatureController.update,
        {"feature_id": feature_id, "model": feature.dict()},
        request,
    )


@router.delete("/feature/{feature_id}", tags=["feature"])
async def delete_feature(feature_id: str, request: Request):
    return await BaseController.run(
        FeatureController.delete, {"feature_id": feature_id}, request
    )


@router.get("/features", tags=["feature"])
async def get_feature(request: Request):
    return await BaseController.run(FeatureController.get, {}, request)
