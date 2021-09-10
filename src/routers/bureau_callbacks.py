# STANDARD LIBS
from typing import Optional, Dict, Any

# OUTSIDE LIBRARIES
from fastapi import APIRouter, Request
from pydantic import BaseModel, root_validator

# SPHINX
from src.routers.validators.base import (
    Uuid,
    Decision,
    Status,
    GenderSource,
    BirthDateSource,
    MotherNameSource,
    DocumentTypeSource,
    DateSource,
    StateSource,
    IssuerSource,
    StreetNameSource,
    AddressNumberSource,
    CountrySource,
    CitySource,
    IdCitySource,
    ZipCodeSource,
    PhoneNumberSource,
    ActivitySource,
    CnpjSource,
    CompanyNameSource,
    PatrimonySource,
    IncomeSource,
    EducationLevelSource,
    EducationCourseSource,
    IsPoliticallyExposedPerson,
    DateOfAcquisition,
    IncomeTaxTypeSource,
    ConnectedPersonSource,
    ClientTypeSource,
    PersonTypeSource,
    InvestorTypeSource,
    CosifTaxClassificationSource,
    NeighborhoodSource,
    AssetsDateSource,
    NationalitySource,
    EmailSource,
    NameSource,
    CpfSource,
    MidiaPersonSource,
    PersonRelatedToMarketInfluencerSource,
    CourtOrdersSource,
    LawsuitsSource,
    FundAdminRegistrationSource,
    InvestmentFundAdministratorsRegistrationSource,
    RegisterAuditorsSecuritiesCommissionSource,
    RegistrationOfOtherMarketParticipantsSecuritiesCommissionSource,
    ForeignInvestorsRegisterOfAnnexIvNotReregisteredSource,
    RegistrationOfForeignInvestorsSecuritiesCommissionSource,
    RegistrationRepresentativeOfNonresidentInvestorsSecuritiesCommissionSource,
    SelfLinkSource,
    IsUsPersonSource,
    UsTinSource,
    IrsSharingSource,
    FatherNameSource,
    DocumentNumber, MaritalStatusSource, validate_contry_state_city_and_id_city
)
from src.controllers.base_controller import BaseController
from src.controllers.bureau_callbacks.bureau_callback import BureauCallbackController

router = APIRouter()


class DocumentData(BaseModel):
    number: Optional[DocumentNumber]
    date: Optional[DateSource]
    state: Optional[StateSource]
    issuer: Optional[IssuerSource]


class IdentifierDocument(BaseModel):
    type: Optional[DocumentTypeSource]
    document_data: Optional[DocumentData]


class Address(BaseModel):
    street_name: StreetNameSource
    number: AddressNumberSource
    neighborhood: NeighborhoodSource
    country: CountrySource
    state: StateSource
    city: CitySource
    id_city: IdCitySource
    zip_code: ZipCodeSource
    phone_number: PhoneNumberSource

    @root_validator()
    def validate(cls, values):
        country = values.get('country').get('value')
        state = values.get('state').get('value')
        city = values.get('city').get('value')
        id_city = values.get('id_city').get('value')
        is_valid = validate_contry_state_city_and_id_city(country, state, city, id_city)

        if not is_valid:
            raise ValueError(f"The combination of values {country}, {state}, {city}, {id_city} does not match")

        return values


class Company(BaseModel):
    cnpj: Optional[CnpjSource]
    name: Optional[CompanyNameSource]


class Occupation(BaseModel):
    activity: Optional[ActivitySource]
    company: Optional[Company]


class Assets(BaseModel):
    patrimony: Optional[PatrimonySource]
    income: Optional[IncomeSource]
    income_tax_type: Optional[IncomeTaxTypeSource]
    date: Optional[AssetsDateSource]


class Education(BaseModel):
    level: EducationLevelSource
    course: Optional[EducationCourseSource]


class PoliticallyExposedPerson(BaseModel):
    is_politically_exposed_person: Optional[IsPoliticallyExposedPerson]


class Spouse(BaseModel):
    cpf: Optional[CpfSource]
    name: Optional[NameSource]
    nationality: Optional[NationalitySource]


class Marital(BaseModel):
    status: Optional[MaritalStatusSource]
    spouse: Optional[Spouse]


class Birthplace(BaseModel):
    nationality: Optional[NationalitySource]
    country: Optional[CountrySource]
    state: Optional[StateSource]
    city: Optional[CitySource]
    id_city: Optional[IdCitySource]

    @root_validator()
    def validate(cls, values):
        country = values.get('country').get('value')
        state = values.get('state').get('value')
        city = values.get('city').get('value')
        id_city = values.get('id_city').get('value')
        is_valid = validate_contry_state_city_and_id_city(country, state, city, id_city)

        if not is_valid:
            raise ValueError(f"The combination of values {country}, {state}, {city}, {id_city} does not match")

        return values


class Data(Decision, Status):
    email: Optional[EmailSource]
    name: Optional[NameSource]
    cpf: Optional[CpfSource]
    self_link: Optional[SelfLinkSource]
    connected_person: Optional[ConnectedPersonSource]
    person_type: Optional[PersonTypeSource]
    client_type: Optional[ClientTypeSource]
    investor_type: Optional[InvestorTypeSource]
    cosif_tax_classification: Optional[CosifTaxClassificationSource]
    gender: Optional[GenderSource]
    is_us_person: Optional[IsUsPersonSource]
    us_tin: Optional[UsTinSource]
    irs_sharing: Optional[IrsSharingSource]
    birth_date: Optional[BirthDateSource]
    birthplace: Optional[Birthplace]
    mother_name: Optional[MotherNameSource]
    father_name: Optional[FatherNameSource]
    identifier_document: Optional[IdentifierDocument]
    marital: Optional[Marital]
    address: Optional[Address]
    occupation: Optional[Occupation]
    assets: Optional[Assets]
    education: Optional[Education]
    politically_exposed_person: Optional[PoliticallyExposedPerson]
    midia_person: Optional[MidiaPersonSource]
    person_related_to_market_influencer: Optional[PersonRelatedToMarketInfluencerSource]
    court_orders: Optional[CourtOrdersSource]
    lawsuits: Optional[LawsuitsSource]
    fund_admin_registration: Optional[FundAdminRegistrationSource]
    investment_fund_administrators_registration: Optional[InvestmentFundAdministratorsRegistrationSource]
    register_auditors_securities_commission: Optional[RegisterAuditorsSecuritiesCommissionSource]
    registration_of_other_market_participants_securities_commission: Optional[RegistrationOfOtherMarketParticipantsSecuritiesCommissionSource]
    foreign_investors_register_of_annex_iv_not_registered: Optional[ForeignInvestorsRegisterOfAnnexIvNotReregisteredSource]
    registration_of_foreign_investors_securities_commission: Optional[RegistrationOfForeignInvestorsSecuritiesCommissionSource]
    registration_representative_of_nonresident_investors_securities_commission: Optional[RegistrationRepresentativeOfNonresidentInvestorsSecuritiesCommissionSource]
    date_of_acquisition: Optional[DateOfAcquisition]


class BureauCallback(Uuid):
    data: Data


@router.put("/bureau_callback", tags=["bureau_callback"])
def user_bureau_callback(bureau_callback: BureauCallback, request: Request):
    return BaseController.run(
        BureauCallbackController.process_callback, bureau_callback.dict(), request
    )
