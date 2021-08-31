# STANDARD LIBS
from typing import Union, List, Optional

# OUTSIDE LIBRARIES
from fastapi import APIRouter, Request, Response
from pydantic import BaseModel

# SPHINX
from src.routers.validators.base import (
    Uuid,
    AppName,
    Successful,
    Error,
    Decision,
    Status,
    GenderSource,
    BirthDateSource,
    MotherNameSource,
    DocumentTypeSource,
    CpfOrCnpjSource,
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
    MaritalRegimeSource,
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
)
from src.controllers.base_controller import BaseController
from src.controllers.bureau_callbacks.bureau_callback import BureauCallbackController

router = APIRouter()


class DocumentData(BaseModel):
    number: CpfOrCnpjSource
    date: DateSource
    state: StateSource
    issuer: IssuerSource


class IdentifierDocument(BaseModel):
    type: DocumentTypeSource
    document_data: DocumentData


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


class Company(BaseModel):
    cnpj: CnpjSource
    name: CompanyNameSource


class Occupation(BaseModel):
    activity: ActivitySource
    company: Optional[Company]


class Assets(BaseModel):
    patrimony: PatrimonySource
    income: IncomeSource
    income_tax_type: IncomeTaxTypeSource
    date: AssetsDateSource


class Education(BaseModel):
    level: EducationLevelSource
    course: Optional[EducationCourseSource]


class PoliticallyExposedPerson(BaseModel):
    is_politically_exposed_person: IsPoliticallyExposedPerson


class Marital(BaseModel):
    marital_regime: MaritalRegimeSource
    spouse_birth_date: BirthDateSource


class Birthplace(BaseModel):
    nationality: NationalitySource
    country: CountrySource
    state: StateSource
    city: CitySource
    id_city: IdCitySource


class Output(Decision, Status):
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
    marital_update: Optional[Marital]
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


class BureauCallback(Uuid, AppName, Successful, Error):
    output: Output


@router.put("/bureau_callback", tags=["bureau_callback"])
def user_bureau_callback(bureau_callback: BureauCallback, request: Request):
    return BaseController.run(
        BureauCallbackController.process_callback, bureau_callback.dict(), request
    )
