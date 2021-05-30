from fastapi import APIRouter
from src.routers.validators.base import Feature

router = APIRouter()


@router.put("/purchase", tags=["purchase"])
def add_features_to_user(feature: Feature):
    return feature, 200


@router.delete("/purchase", tags=["purchase"])
def remove_features_to_user(feature: Feature):
    return feature, 200
