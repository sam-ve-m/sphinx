from pydantic import BaseModel
from typing import Optional


class CreateAccount(BaseModel):
    bank_name: Optional[str] = None
    account_type: Optional[str] = None
    bak_agency: str = Field(min_length=5)
    phoneList: List[Dict]
    address: Optional[str] = None