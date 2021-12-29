# STANDARD LIBS
from __future__ import annotations
import logging

# OUTSIDE LIBRARIES
from email_validator import validate_email


# SPHIX
from src.domain.validators.onboarding_validators import *
from src.infrastructures.env_config import config
from src.repositories.view.repository import ViewRepository
from src.repositories.feature.repository import FeatureRepository

signature_regex = r"^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])[a-zA-Z0-9]{8,}$"


class Email(BaseModel):
    email: constr(min_length=4, max_length=255)

    @validator("email", always=True, allow_reuse=True)
    def validate_email(cls, value):
        # return value
        try:
            is_valid = validate_email(value)
            if is_valid:
                return value
            raise ValueError("The given email is invalid")
        except Exception as e:
            logger = logging.getLogger(config("LOG_NAME"))
            logger.error(e, exc_info=True)
        raise ValueError("The given email is invalid")


class ViewId(BaseModel):
    view_id: constr(min_length=1)

    @validator("view_id", always=True, allow_reuse=True)
    def validate_view_id(cls, e):
        view_repository = ViewRepository()
        if view_repository.find_one({"_id": e}, ttl=60):
            return e
        raise ValueError("view not exists")


class FeatureId(BaseModel):
    feature_id: constr(min_length=1)

    @validator("feature_id", always=True, allow_reuse=True)
    def validate_feature_id(cls, e):
        feature_repository = FeatureRepository()
        if feature_repository.find_one({"_id": e}, ttl=60):
            return e
        raise ValueError("feature not exists")


class LinkViewFeature(ViewId, FeatureId):
    pass


class Feature(BaseModel):
    name: constr(min_length=1)
    display_name: constr(min_length=1)


class View(BaseModel):
    name: constr(min_length=1)
    display_name: constr(min_length=1)


class OptionalPIN(BaseModel):
    pin: Optional[constr(min_length=6, max_length=6)]


class PIN(BaseModel):
    pin: constr(min_length=6, max_length=6)


class ElectronicSignature(BaseModel):
    electronic_signature: constr(regex=signature_regex)


class NewElectronicSignature(BaseModel):
    new_electronic_signature: constr(regex=signature_regex)


class ChangeElectronicSignature(ElectronicSignature, NewElectronicSignature):
    pass