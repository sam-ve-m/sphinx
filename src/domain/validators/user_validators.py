from typing import List, Optional

from src.domain.validators.base import *
from src.repositories.sinacor_types.repository import SinacorTypesRepository


class UserSimple(Email, NickName):
    pass


class Spouse(Name, Cpf, Nationality):
    pass


class Country(BaseModel):
    country: constr(min_length=3, max_length=3)

    @validator("country", always=True, allow_reuse=True)
    def validate_country(cls, e):
        sinacor_types_repository = SinacorTypesRepository()
        if sinacor_types_repository.validate_country(value=e):
            return e
        raise ValueError("country not exists")


class TaxResidence(Country):
    tax_number: str


class TaxResidences(BaseModel):
    tax_residences: List[TaxResidence]


class UserIdentifierData(Cpf, CelPhone):
    tax_residences: Optional[List[TaxResidence]]
