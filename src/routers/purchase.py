from fastapi import APIRouter

router = APIRouter()


@router.put("/purchase/{feature_id}", tags=["purchase"])
async def add_features_to_user(feature_id: str):
    return feature_id, 200


@router.delete("/purchase/{feature_id}", tags=["purchase"])
async def remove_features_to_user(feature_id: str):
    return feature_id, 200
