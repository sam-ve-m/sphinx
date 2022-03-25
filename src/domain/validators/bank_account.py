from pydantic import BaseModel, UUID4
from typing import Optional
from src.domain.validators.onboarding_validators import Cpf


class CreateUserBankAccount(Cpf):
    bank: str
    account_type: str
    agency: str
    account_number: str
    account_name: Optional[str]


class UpdateUserBankAccounts(BaseModel):
    bank: Optional[str]
    account_type: Optional[str]
    agency: Optional[str]
    account_number: Optional[str]
    account_name: str
    id: UUID4


class DeleteUsersBankAccount(BaseModel):
    id: str


