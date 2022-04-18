from typing import List
from src.infrastructures.env_config import config


class ClientUpdateRegisterBuilderUs:
    def __init__(self):
        self._basic_information = {"type": "BASIC_INFO", "data": {}}
        self._tax_id_information = {"type": "IDENTIFICATION_INFO", "data": {}}
        self._tax_residence_information = {"type": "", "data": {}}
        self._personal_information = {"type": "PERSONAL_INFO", "data": {}}
        self._address = {"type": "ADDRESS_INFO", "data": {}}
        self._employment = {"type": "EMPLOYMENT_INFO", "data": {}}
        self._investing_profile = {"type": "INVESTOR_PROFILE_INFO", "data": {}}
        self._disclosures = {"type": "DISCLOSURES", "data": {}}
        self._margin_disclosure = {"type": "MARGIN_DISCLOSURE", "data": {}}
        self._parent_ibid = None
        self._user_type = None
        self._wlp_id = None

    def __get_filed_documents(self) -> List[dict]:
        possible_documents = [
            self._basic_information,
            self._tax_id_information,
            self._tax_residence_information,
            self._personal_information,
            self._address,
            self._employment,
            self._investing_profile,
            self._disclosures,
            self._margin_disclosure,
        ]
        documents = []
        for document in possible_documents:
            if document["data"]:
                documents.append(document)
        return documents

    def build(self):
        data = {"documents": self.__get_filed_documents()}
        if self._parent_ibid:
            data.update({"parentIBID": self._parent_ibid})
        if self._user_type:
            data.update({"userType": self._user_type})
        if self._wlp_id:
            data.update({"wlpID": self._wlp_id})

        return data

    def add_parent_ibid(self):
        self._parent_ibid = config("DW_PARENT_IBID")
        return self

    def add_parent_wlp_id(self):
        self._wlp_id = config("DW_WLP_ID")
        return self

    def add_user_type(self):
        self._user_type = "INDIVIDUAL_TRADER"
        return self

    def add_basic_information_first_name(self, user_data: dict):
        first_name = user_data["name"].split(" ")[0]
        self._basic_information["data"].update({"firstName": first_name})
        return self

    def add_basic_information_last_name(self, user_data: dict):
        last_name = user_data["name"].split(" ")[-1]
        self._basic_information["data"].update({"lastName": last_name})
        return self

    def add_basic_information_country(self, user_data: dict):
        country = user_data["address"]["country"]
        self._basic_information["data"].update({"country": country})
        return self

    def add_basic_information_phone(self, user_data: dict):
        country = user_data["phone"]
        self._basic_information["data"].update({"phone": country})
        return self

    def add_basic_information_email(self, user_data: dict):
        email = user_data["email"]
        self._basic_information["data"].update({"emailAddress": email})
        return self

    def add_basic_information_language(self):
        self._basic_information["data"].update({"language": "pt_BR"})
        return self

    def add_tax_id_information_number(self, user_data: dict):
        us_tax_id_information_filtered = list(
            filter(lambda x: x["country"] == "USA", user_data.get("tax_residences", []))
        )
        if us_tax_id_information_filtered:
            tax_id_information = us_tax_id_information_filtered[0]
            number = tax_id_information["tax_number"]
            self._tax_id_information["data"].update({"value": number.replace("-", "")})
        else:
            self._tax_id_information["data"].update(
                {"value": user_data["identifier_document"]["cpf"]}
            )
        return self

    def add_tax_id_information_type(self, user_data: dict):
        us_tax_id_information_filtered = list(
            filter(lambda x: x["country"] == "USA", user_data.get("tax_residences", []))
        )
        tax_ype = "other"
        if us_tax_id_information_filtered:
            tax_id_information = us_tax_id_information_filtered[0]
            self._tax_id_information["data"].update({"type": tax_ype})
        else:
            self._tax_id_information["data"].update({"type": tax_ype})
        return self

    def add_tax_id_information_citizenship(self, user_data: dict):
        us_tax_id_information_filtered = list(
            filter(lambda x: x["country"] == "USA", user_data.get("tax_residences", []))
        )
        if us_tax_id_information_filtered:
            tax_id_information = us_tax_id_information_filtered[0]
            country = tax_id_information["country"]
            self._tax_id_information["data"].update({"citizenship": country})
        else:
            self._tax_id_information["data"].update({"citizenship": "BRA"})
        return self

    def add_tax_id_information_us_tax_payer(self, user_data: dict):
        us_tax_id_information_filtered = list(
            filter(lambda x: x["country"] == "USA", user_data.get("tax_residences", []))
        )
        if us_tax_id_information_filtered:
            self._tax_id_information["data"].update({"usTaxPayer": True})
        else:
            self._tax_id_information["data"].update({"usTaxPayer": False})
        return self

    def add_tax_residence_information_tax_treaty_with_us(self, user_data: dict):
        us_tax_id_information_filtered = list(
            filter(lambda x: x["country"] == "USA", user_data.get("tax_residences", []))
        )
        if us_tax_id_information_filtered:
            self._tax_residence_information["data"].update({"taxTreatyWithUS": True})
        return self

    def add_personal_information_birth_date(self, user_data: dict):
        birth_date = user_data["birth_date"]
        self._personal_information["data"].update(
            {
                "birthDay": birth_date.day,
                "birthMonth": birth_date.month,
                "birthYear": birth_date.year,
            }
        )
        return self

    def add_personal_information_gender(self, user_data: dict):
        gender = user_data["gender"]
        # TODO: When integrated with CAF use gender that recived by them
        gender_map = {
            "M": "Male",
            "F": "Female",
        }
        self._personal_information["data"].update(
            {"gender": gender_map.get(gender, "Female")}
        )
        return self

    def add_personal_information_marital(self, user_data: dict):
        marital_status = user_data["marital"]["status"]
        marital_status_map = {
            1: "SINGLE",
            2: "MARRIED",
            3: "DIVORCED",
            4: "DIVORCED",
            5: "WIDOWED",
            6: "PARTNER",
        }
        self._personal_information["data"].update(
            {"marital": marital_status_map[marital_status]}
        )
        return self

    def add_personal_information_politically_exposed_names(self, user_data: dict):
        value = None
        if user_data["external_exchange_requirements"]["us"]["is_politically_exposed"]:
            value = user_data["name"].split(" ")[-1]
        self._personal_information["data"].update({"politicallyExposedNames": value})
        return self

    def add_personal_information_irs_backup_withholdings(self):
        self._personal_information["data"].update({"irsBackupWithholdings": False})
        return self

    def add_address_street1(self, user_data: dict):
        address = user_data["address"]
        street = (
            f"{address['number']}, {address['street_name']} {address['neighborhood']}"
        )
        self._address["data"].update({"street1": street})
        return self

    def add_address_city(self, user_data: dict):
        # TODO PEGAR DO SINACOR
        address = user_data["address"]
        city = address["city"]
        self._address["data"].update({"city": city})
        return self

    def add_address_province(self, user_data: dict):
        address = user_data["address"]
        state = address["state"]
        self._address["data"].update({"province": state})
        return self

    def add_address_zip_code(self, user_data: dict):
        address = user_data["address"]
        zip_code = address["zip_code"]
        self._address["data"].update({"postalCode": zip_code})
        return self

    def add_address_country(self, user_data: dict):
        address = user_data["address"]
        country = address["country"]
        self._address["data"].update({"country": country})
        return self

    def add_employment_status(self, user_data: dict):
        occupation = user_data["occupation"]
        activity = occupation["activity"]
        # TODO MAPA MISSING
        value = None
        self._employment["data"].update({"status": value})
        return self

    def add_employment_company(self, user_data: dict):
        if self._employment["data"]["status"] in ["EMPLOYED", "SELF_EMPLOYED"]:
            occupation = user_data["occupation"]
            company_name = occupation["company"]["name"]
            # TODO CONDIFITNAL IF EMPLOYED ad SELF_EMPLOYED
            self._employment["data"].update({"company": company_name})
        return self

    def add_employment_type(self, user_data: dict):
        if self._employment["data"]["status"] in ["EMPLOYED", "SELF_EMPLOYED"]:
            occupation = user_data["occupation"]
            # TODO MAPA MISSING
            # TODO CONDIFITNAL IF EMPLOYED ad SELF_EMPLOYED
            value = None
            self._employment["data"].update({"type": value})
        return self

    def add_employment_position(self, user_data: dict):
        if self._employment["data"]["status"] in ["EMPLOYED", "SELF_EMPLOYED"]:
            occupation = user_data["occupation"]
            # TODO MAPA MISSING
            # TODO CONDIFITNAL IF EMPLOYED ad SELF_EMPLOYED
            value = None
            self._employment["data"].update({"position": value})
        return self

    def add_employment_broker(self, user_data: dict):
        broker = user_data["external_exchange_requirements"]["us"]["is_exchange_member"]
        self._employment["data"].update({"broker": broker})
        return self

    def add_employment_director_of(self, user_data: dict):
        value = None
        if user_data["external_exchange_requirements"]["us"]["is_company_director"]:
            value = user_data["external_exchange_requirements"]["us"][
                "is_company_director_of"
            ]
        self._employment["data"].update({"directorOf": value})
        return self

    def add_investing_profile_investment_experience(self, user_data: dict):
        time_experience = user_data["external_exchange_requirements"]["us"][
            "time_experience"
        ]
        self._investing_profile["data"].update(
            {"investmentExperience": time_experience}
        )
        return self

    def add_investing_profile_investment_objectives(self):
        self._investing_profile["data"].update({"investmentObjectives": "ACTIVE_DAILY"})
        return self

    def add_investing_profile_annual_income(self, user_data: dict):
        income = user_data["assets"]["income"]
        self._investing_profile["data"].update({"annualIncome": (income * 12)})
        return self

    def add_investing_profile_networth(self, user_data: dict):
        networth = user_data["assets"]["patrimony"]
        self._investing_profile["data"].update(
            {
                "networthTotal": networth,
                "networthLiquid": networth,
            }
        )
        return self

    def add_investing_profile_risk_tolerance(self):
        self._investing_profile["data"].update({"riskTolerance": "HIGH"})
        return self

    def add_disclosures_customer_agreement(self, user_data: dict):
        value = False
        if user_data["terms"]["term_open_account_dw"]:
            value = True
        self._disclosures["data"].update({"customerAgreement": value})
        return self

    def add_disclosures_terms_of_use(self, user_data: dict):
        value = False
        if user_data["terms"]["term_application_dw"]:
            value = True
        self._disclosures["data"].update({"termsOfUse": value})
        return self

    def add_disclosures_data_sharing(self, user_data: dict):
        value = False
        if user_data["terms"]["term_data_sharing_policy_dw"]:
            value = True
        self._disclosures["data"].update({"dataSharing": value})
        return self

    def add_disclosures_privacy_policy(self, user_data: dict):
        value = False
        if user_data["terms"]["term_privacy_policy_dw"]:
            value = True
        self._disclosures["data"].update({"privacyPolicy": value})
        return self

    def add_disclosures_name(self, user_data: dict):
        name = user_data["name"]
        self._disclosures["data"].update({"signedBy": name})
        return self

    def add_disclosures_rule14b(self, user_data: dict):
        value = False
        # TODO PRECISA IMPLEMENTAR ISSO AKI
        # if user_data["terms"]['term_rule14b_dw']:
        #     value = True
        self._disclosures["data"].update({"rule14b": value})
        return self

    def add_disclosures_defaults(self):
        self._disclosures["data"].update(
            {
                "marketDataAgreement": False,
                "findersFee": False,
                "extendedHoursAgreement": False,
            }
        )
        return self

    def add_margin_disclosure_agreement(self):
        self._margin_disclosure["data"].update({"marginAgreement": True})
        return self
