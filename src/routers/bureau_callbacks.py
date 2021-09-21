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
    DocumentNumber,
    MaritalStatusSource,
    validate_contry_state_city_and_id_city,
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
    def validate(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        country = values.get("country")
        state = values.get("state")
        city = values.get("city")
        id_city = values.get("id_city")

        if all([country, state, city, id_city]):
            is_valid = validate_contry_state_city_and_id_city(
                country.get("value"),
                state.get("value"),
                city.get("value"),
                id_city.get("value"),
            )
            if not is_valid:
                raise ValueError(
                    f"The combination of values {country}, {state}, {city}, {id_city} does not match"
                )

        return values


class Company(BaseModel):
    cnpj: Optional[CnpjSource]
    name: Optional[CompanyNameSource]


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


class Spouse(BaseModel):
    cpf: Optional[CpfSource]
    name: Optional[NameSource]
    nationality: Optional[NationalitySource]


class Marital(BaseModel):
    status: MaritalStatusSource
    spouse: Optional[Spouse]


class Birthplace(BaseModel):
    nationality: NationalitySource
    country: Optional[CountrySource]
    state: Optional[StateSource]
    city: Optional[CitySource]
    id_city: Optional[IdCitySource]

    @root_validator()
    def validate(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        country = values.get("country")
        state = values.get("state")
        city = values.get("city")
        id_city = values.get("id_city")

        if all([country, state, city, id_city]):
            is_valid = validate_contry_state_city_and_id_city(
                country.get("value"),
                state.get("value"),
                city.get("value"),
                id_city.get("value"),
            )
            if not is_valid:
                raise ValueError(
                    f"The combination of values {country}, {state}, {city}, {id_city} does not match"
                )

        return values


class Data(Decision, Status):
    email: EmailSource
    name: NameSource
    cpf: CpfSource
    self_link: SelfLinkSource
    person_type: PersonTypeSource
    client_type: ClientTypeSource
    investor_type: InvestorTypeSource
    cosif_tax_classification: CosifTaxClassificationSource
    gender: GenderSource
    is_us_person: IsUsPersonSource
    birth_date: BirthDateSource
    birthplace: Birthplace
    mother_name: MotherNameSource
    marital: Marital
    address: Address
    occupation: Occupation
    assets: Assets
    education: Education
    is_politically_exposed_person: IsPoliticallyExposedPerson
    connected_person: ConnectedPersonSource
    midia_person: MidiaPersonSource
    person_related_to_market_influencer: PersonRelatedToMarketInfluencerSource
    court_orders: CourtOrdersSource
    lawsuits: LawsuitsSource
    fund_admin_registration: FundAdminRegistrationSource
    investment_fund_administrators_registration: InvestmentFundAdministratorsRegistrationSource
    register_auditors_securities_commission: RegisterAuditorsSecuritiesCommissionSource
    registration_of_other_market_participants_securities_commission: RegistrationOfOtherMarketParticipantsSecuritiesCommissionSource
    foreign_investors_register_of_annex_iv_not_registered: ForeignInvestorsRegisterOfAnnexIvNotReregisteredSource
    registration_of_foreign_investors_securities_commission: RegistrationOfForeignInvestorsSecuritiesCommissionSource
    registration_representative_of_nonresident_investors_securities_commission: RegistrationRepresentativeOfNonresidentInvestorsSecuritiesCommissionSource
    date_of_acquisition: DateOfAcquisition
    us_tin: Optional[UsTinSource]
    irs_sharing: Optional[IrsSharingSource]
    father_name: Optional[FatherNameSource]
    identifier_document: Optional[IdentifierDocument]


class BureauCallback(Uuid):
    data: Data


@router.put("/bureau_callback", tags=["bureau_callback"])
def user_bureau_callback(bureau_callback: BureauCallback, request: Request):
    return BaseController.run(
        BureauCallbackController.process_callback, bureau_callback.dict(), request
    )
