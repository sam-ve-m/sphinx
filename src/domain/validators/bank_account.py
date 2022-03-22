from pydantic import BaseModel, UUID4
from typing import Optional
from src.domain.validators.onboarding_validators import Cpf


class CreateBankAccount(Cpf):
    bank: str
    account_type: str
    agency: str
    account_number: str
    account_name: Optional[str]


class UpdateBankAccounts(BaseModel):
    bank: Optional[str]
    account_type: Optional[str]
    agency: Optional[str]
    account_number: Optional[str]
    account_name: str
    id: UUID4


class DeleteBankAccount(BaseModel):
    id: str


