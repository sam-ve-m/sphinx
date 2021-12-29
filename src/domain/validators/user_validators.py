from typing import List

from src.domain.validators.base import *
from src.repositories.sinacor_types.repository import SinaCorTypesRepository


class UserSimple(Email, NickName, OptionalPIN):
    pass


class Spouse(Name, Cpf, Nationality):
    pass


class Country(BaseModel):
    country: constr(min_length=3, max_length=3)

    @validator("country", always=True, allow_reuse=True)
    def validate_country(cls, e):
        sinacor_types_repository = SinaCorTypesRepository()
        if sinacor_types_repository.validate_country(value=e):
            return e
        raise ValueError("nationality not exists")


class TaxResidence(Country):
    tax_number: str


class UserIdentifierData(Cpf, CelPhone):
    tax_residences: Optional[List[TaxResidence]]
