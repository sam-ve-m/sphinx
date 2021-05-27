from fastapi import APIRouter, Request
from pydantic import BaseModel
from src.controllers.base_controller import BaseController
from src.controllers.features.controller import FeatureController

router = APIRouter()


class Feature(BaseModel):
    name: str
    display_name: str


@router.post("/feature", tags=["feature"])
async def create_feature(feature: Feature, request: Request):
    return BaseController.run(FeatureController.create, dict(feature), request)


@router.put("/feature/{feature_id}", tags=["feature"])
async def update_feature_data(feature_id: str, feature: Feature, request: Request):
    return BaseController.run(
        FeatureController.update,
        {"feature_id": feature_id, "model": dict(feature)},
        request,
    )


@router.delete("/feature/{feature_id}", tags=["feature"])
async def delete_feature(feature_id: str, request: Request):
    return BaseController.run(
        FeatureController.update, {"feature_id": feature_id}, request
    )
