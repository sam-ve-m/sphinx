from src.services.builders.client_register.us.builder import ClientRegisterBuilderUs


class DriveWealthService:

    @classmethod
    async def registry_client(cls, user_data: dict):
        body = cls.__get_registry_body(user_data=user_data)
        pass

    @staticmethod
    def __get_registry_body(user_data: dict) -> ClientRegisterBuilderUs:
        client_register_builder_us = ClientRegisterBuilderUs()
        (
            client_register_builder_us.add_basic_information_first_name(user_data=user_data)
            .add_basic_information_last_name(user_data=user_data)
            .add_basic_information_country(user_data=user_data)
            .add_basic_information_phone(user_data=user_data)
            .add_basic_information_email(user_data=user_data)
            .add_basic_information_language()
            .add_tax_id_information_number(user_data=user_data)
            .add_tax_id_information_type(user_data=user_data)
            .add_tax_id_information_citizenship(user_data=user_data)
            .add_tax_id_information_us_tax_payer(user_data=user_data)
            .add_tax_residence_information_tax_treaty_with_us(user_data=user_data)
            .add_personal_information_birth_date(user_data=user_data)
            .add_personal_information_gender(user_data=user_data)
            .add_personal_information_marital(user_data=user_data)
            .add_personal_information_politically_exposed_names(user_data=user_data)
            .add_personal_information_irs_backup_withholdings()
            .add_address_street1(user_data=user_data)
            .add_address_city(user_data=user_data)
            .add_address_province(user_data=user_data)
            .add_address_zip_code(user_data=user_data)
            .add_address_country(user_data=user_data)
            .add_employment_status(user_data=user_data)
            .add_employment_company(user_data=user_data)
            .add_employment_type(user_data=user_data)
            .add_employment_position(user_data=user_data)
            .add_employment_broker(user_data=user_data)
            .add_employment_director_of(user_data=user_data)
            .add_investing_profile_investment_experience(user_data=user_data)
            .add_investing_profile_investment_objectives()
            .add_investing_profile_annual_income(user_data=user_data)
            .add_investing_profile_networth(user_data=user_data)
            .add_investing_profile_risk_tolerance()
            .add_disclosures_customer_agreement(user_data=user_data)
            .add_disclosures_terms_of_use(user_data=user_data)
            .add_disclosures_data_sharing(user_data=user_data)
            .add_disclosures_privacy_policy(user_data=user_data)
            .add_disclosures_name(user_data=user_data)
            .add_disclosures_rule14b(user_data=user_data)
            .add_disclosures_defaults()
        )
        return client_register_builder_us