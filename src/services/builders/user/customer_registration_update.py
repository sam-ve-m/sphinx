from typing import Tuple, Optional


class UpdateCustomerRegistrationBuilder:
    def __init__(self, old_personal_data: dict, new_personal_data: dict, email: str):
        self.__old_personal_data = old_personal_data
        self.__new_personal_data = new_personal_data
        self.__email = email
        self.__update_buffer = old_personal_data.copy()
        self.__diff_data = []

    def _update_diff_date(self, field: str, old_field: dict, new_filed: dict):
        self.__diff_data.append(
            {
                "old:": {field: old_field},
                "new":  {field: new_filed}
             }
        )

    def _get_new_value(self, field_name: str) -> Optional[any]:
        return self.__new_personal_data.get(field_name, {}).get("value")

    def personal_name(self):
        old_name = self.__old_personal_data.get("name")
        if new_name := self._get_new_value("name"):
            self._update_diff_date(
                field="name",
                old_field=old_name,
                new_filed=new_name
            )
            self.__update_buffer.update({"name": new_name})
        return self

    def personal_phone(self):
        old_phone = self.__old_personal_data.get("cel_phone")
        if new_phone := self._get_new_value("cel_phone"):
            self.__update_buffer["personal"].update({"cel_phone": new_phone})
            self._update_diff_date(
                field="cel_phone",
                old_field=old_phone,
                new_filed=new_phone
            )

        return self

    def personal_patrimony(self):
        old_patrimony = (self.__old_personal_data
                         .get("assets", {})
                         .get("patrimony"))

        if new_patrimony := self._get_new_value("patrimony"):
            if self.__update_buffer.get("assets") is None:
                self.__update_buffer["assets"] = {}

                self.__update_buffer["assets"]["patrimony"] = new_patrimony

            self._update_diff_date(
                field="patrimony",
                old_field=old_patrimony,
                new_filed=new_patrimony
            )
        return self

    def personal_occupation_activity(self):
        old_occupation_activity = (self.__old_personal_data
                                   .get("occupation", {})
                                   .get("activity"))

        if new_occupation_activity := self._get_new_value("occupation_activity"):
            if self.__update_buffer.get("occupation") is None:
                self.__update_buffer["occupation"] = {}

            self.__update_buffer["occupation"].update({"activity": new_occupation_activity})
            self._update_diff_date(
                field="occupation_activity",
                old_field=old_occupation_activity,
                new_filed=new_occupation_activity
            )
        return self

    def personal_work_company_name(self):
        old_work_company_name = (self.__old_personal_data
                                 .get("occupation", {})
                                 .get("company", {})
                                 .get("name"))

        if new_work_company_name := self._get_new_value("company_name"):
            if self.__update_buffer.get("occupation") is None:
                self.__update_buffer["occupation"] = {}

            if self.__update_buffer.get("occupation").get("company") is None:
                self.__update_buffer["occupation"]["company"] = {}

            self.__update_buffer["occupation"]["company"]["name"] = new_work_company_name
            self._update_diff_date(
                field="occupation_activity",
                old_field=old_work_company_name,
                new_filed=new_work_company_name
            )

        return self

    def marital_status(self):
        marital_status = (self.__old_personal_data
                          .get("marital", {})
                          .get("status"))
        self.__update_buffer["marital"].update({"marital_status": marital_status})
        return self

    def marital_spouse_name(self):
        spouse_name = (self.__old_personal_data
                       .get("marital", {})
                       .get("spouse", {})
                       .get("name"))
        self.__update_buffer["marital"].update({"spouse_name": spouse_name})
        return self

    def documents_cpf(self):
        cpf = self.__old_personal_data.get("cpf")
        self.__update_buffer["documents"].update({"cpf": cpf})
        return self

    def documents_identity_number(self):
        identity_number = (self.__old_personal_data
                           .get("identifier_document", {})
                           .get("document_data", {})
                           .get("number"))
        self.__update_buffer["documents"].update({"identity_number": identity_number})
        return self

    def documents_expedition_date(self):
        expedition_date = (self.__old_personal_data
                           .get("identifier_document", {})
                           .get("document_data", {})
                           .get("date"))
        self.__update_buffer["documents"].update({"expedition_date": expedition_date})
        return self

    def documents_issuer(self):
        issuer = (self.__old_personal_data
                  .get("identifier_document", {})
                  .get("document_data", {})
                  .get("issuer"))
        self.__update_buffer["documents"].update({"issuer": issuer})
        return self

    def documents_state(self):
        state = (self.__old_personal_data
                 .get("identifier_document", {})
                 .get("document_data", {})
                 .get("state"))
        self.__update_buffer["documents"].update({"state": state})
        return self

    def address_country(self):
        country = (self.__old_personal_data
                   .get("address", {})
                   .get("country"))
        self.__update_buffer["address"].update({"country": country})
        return self

    def address_street_name(self):
        street_name = (self.__old_personal_data
                       .get("address", {})
                       .get("street_name"))
        self.__update_buffer["address"].update({"street_name": street_name})
        return self

    def address_city(self):
        city = (self.__old_personal_data
                .get("address", {})
                .get("city"))
        self.__update_buffer["address"].update({"city": city})
        return self

    def address_zip_code(self):
        zip_code = (self.__old_personal_data
                    .get("address", {})
                    .get("zip_code"))
        self.__update_buffer["address"].update({"zip_code": zip_code})
        return self

    def address_state(self):
        state = (self.__old_personal_data
                 .get("address", {})
                 .get("state"))
        self.__update_buffer["address"].update({"state": state})
        return self

    def build(self) -> Tuple[dict, dict]:
        modified_register = {
            "email": self.__email,
            "modified_data": self.__diff_data
        }
        return self.__update_buffer, modified_register
