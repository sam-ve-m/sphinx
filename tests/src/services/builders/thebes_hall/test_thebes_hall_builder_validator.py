from datetime import datetime

from pydantic import BaseModel, validator
from typing import List, Optional


class NickName(BaseModel):
    nick_name: str


class Email(BaseModel):
    email: str


class ScopeDict(BaseModel):
    view_type: str
    features: List[str]


class Scope(BaseModel):
    scope: ScopeDict


class IsActiveUser(BaseModel):
    is_active_user: bool


class IsBlockedElectronicSignature(BaseModel):
    is_blocked_electronic_signature: bool


class TermsDict(BaseModel):
    TermApplication: Optional[str]
    TermOpenAccount: Optional[str]
    TermRetailLiquidProvider: Optional[str]
    TermRefusal: Optional[str]
    TermNonCompliance: Optional[str]


class Terms(BaseModel):
    terms: TermsDict


class SuitabilityMonthsPast(BaseModel):
    suitability_months_past: int


class LastModifiedDateMonthsPast(BaseModel):
    last_modified_date_months_past: int


class ClientHasTradeAllowed(BaseModel):
    client_has_trade_allowed: bool


class CreatedAt(BaseModel):
    created_at: datetime


class Exp(BaseModel):
    exp: int


class UsingSuitabilityOrRefuseTerm(BaseModel):
    using_suitability_or_refuse_term: str

    @validator("using_suitability_or_refuse_term")
    def validate_using_suitability_or_refuse_term(
        cls, using_suitability_or_refuse_term
    ):
        using_suitability_or_refuse_term_enum_list = ["suitability", "term_refusal"]
        if (
            using_suitability_or_refuse_term
            not in using_suitability_or_refuse_term_enum_list
        ):
            raise ValueError(
                f"This value not existis in our enum: {using_suitability_or_refuse_term}"
            )
        return using_suitability_or_refuse_term


class BovespaAccount(BaseModel):
    bovespa_account: str


class BmfAccount(BaseModel):
    bmf_account: str


class RegisterAnalyses(BaseModel):
    register_analyses: str


class IsAdmin(BaseModel):
    is_admin: bool


class ForgotElectronicSignature(BaseModel):
    forgot_electronic_signature: bool

    @validator("forgot_electronic_signature")
    def validate_forgot_electronic_signature(cls, forgot_electronic_signature):
        forgot_electronic_signature_enum_list = [True, False]
        if (
            forgot_electronic_signature not in forgot_electronic_signature_enum_list
            and type(forgot_electronic_signature) == bool
        ):
            raise ValueError(
                f"This value not existis in our enum: {forgot_electronic_signature}"
            )
        return forgot_electronic_signature


class ForgotPassword(BaseModel):
    forgot_password: bool

    @validator("forgot_password")
    def validate_forgot_password_signature(cls, forgot_password):
        forgot_password_enum_list = [True, False]
        if (
            forgot_password not in forgot_password_enum_list
            and type(forgot_password) == bool
        ):
            raise ValueError(f"This value not existis in our enum: {forgot_password}")
        return forgot_password


class ValidJwtPayloadToCompleteDtvmClient(
    NickName,
    Email,
    Scope,
    IsActiveUser,
    IsBlockedElectronicSignature,
    Terms,
    SuitabilityMonthsPast,
    LastModifiedDateMonthsPast,
    ClientHasTradeAllowed,
    CreatedAt,
    Exp,
    UsingSuitabilityOrRefuseTerm,
    BovespaAccount,
    BmfAccount,
    RegisterAnalyses,
    IsAdmin,
):
    class Config:
        extra = "forbid"


class ForgotElectronicSignatureJwtPayload(
    NickName,
    Email,
    Scope,
    IsActiveUser,
    IsBlockedElectronicSignature,
    Terms,
    SuitabilityMonthsPast,
    LastModifiedDateMonthsPast,
    ClientHasTradeAllowed,
    CreatedAt,
    Exp,
    UsingSuitabilityOrRefuseTerm,
    BovespaAccount,
    BmfAccount,
    RegisterAnalyses,
    IsAdmin,
    ForgotElectronicSignature,
):
    class Config:
        extra = "forbid"


class ForgotPasswordJwtPayload(
    NickName,
    Email,
    Scope,
    IsActiveUser,
    IsBlockedElectronicSignature,
    Terms,
    SuitabilityMonthsPast,
    LastModifiedDateMonthsPast,
    ClientHasTradeAllowed,
    CreatedAt,
    Exp,
    UsingSuitabilityOrRefuseTerm,
    BovespaAccount,
    BmfAccount,
    RegisterAnalyses,
    IsAdmin,
    ForgotPassword,
):
    class Config:
        extra = "forbid"


class ValidJwtPayloadToCompleteAppUser(
    NickName,
    Email,
    Scope,
    IsActiveUser,
    Terms,
    LastModifiedDateMonthsPast,
    CreatedAt,
    Exp,
):
    class Config:
        extra = "forbid"
