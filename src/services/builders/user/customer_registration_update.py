from typing import Tuple, Optional


class UpdateCustomerRegistrationBuilder:
    def __init__(self, old_personal_data: dict, new_personal_data: dict, unique_id: str):
        self.__old_personal_data = old_personal_data
        self.__new_personal_data = new_personal_data
        self.__unique_id = unique_id
        self.__update_buffer = old_personal_data.copy()
        self.__modified_data = []

    def _update_modified_data(self, levels: tuple, old_field: dict, new_filed: dict):
        UpdateCustomerRegistrationBuilder._dictionary_insert_with_levels(
            *levels, _value=new_filed, _current_dict_level=self.__update_buffer
        )
        field_id = "/".join(levels)
        self.__modified_data.append(
            {"old:": {field_id: old_field}, "new": {field_id: new_filed}}
        )

    @staticmethod
    def _dictionary_insert_with_levels(
        *levels, _value: any, _current_dict_level: dict, _current_arg_id: int = 0
    ):
        level_size = len(levels)
        if level_size == 0:
            return

        if _current_arg_id == level_size - 1:
            _current_dict_level[levels[_current_arg_id]] = _value
            return

        level = levels[_current_arg_id]
        if _current_dict_level.get(level) is None:
            _current_dict_level.update({level: {}})

        UpdateCustomerRegistrationBuilder._dictionary_insert_with_levels(
            *levels,
            _value=_value,
            _current_arg_id=_current_arg_id + 1,
            _current_dict_level=_current_dict_level[level],
        )

    def _get_new_value(self, field_name: str) -> Optional[any]:
        if source := self.__new_personal_data.get(field_name, {}):
            return source.get("value")

    def personal_name(self):
        old_name = self.__old_personal_data.get("name")
        if new_name := self._get_new_value("name"):
            self._update_modified_data(
                levels=("name",), old_field=old_name, new_filed=new_name
            )
        return self

    def personal_nationality(self):
        old_name = self.__old_personal_data.get("personal_nationality")
        if new_name := self._get_new_value("personal_nationality"):
            self._update_modified_data(
                levels=("personal_nationality",), old_field=old_name, new_filed=new_name
            )
        return self

    def personal_nick_name(self):
        old_name = self.__old_personal_data.get("nick_name")
        if new_name := self._get_new_value("nick_name"):
            self._update_modified_data(
                levels=("nick_name",), old_field=old_name, new_filed=new_name
            )
        return self

    def personal_phone(self):
        old_phone = self.__old_personal_data.get("cel_phone")
        if new_phone := self._get_new_value("cel_phone"):
            self._update_modified_data(
                levels=("cel_phone",), old_field=old_phone, new_filed=new_phone
            )

        return self

    def personal_patrimony(self):
        old_patrimony = self.__old_personal_data.get("assets", {}).get("patrimony")

        if new_patrimony := self._get_new_value("patrimony"):
            self._update_modified_data(
                levels=("assets", "patrimony"),
                old_field=old_patrimony,
                new_filed=new_patrimony,
            )

        return self

    def personal_occupation_activity(self):
        old_occupation_activity = self.__old_personal_data.get("occupation", {}).get(
            "activity"
        )

        if new_occupation_activity := self._get_new_value("occupation_activity"):
            self._update_modified_data(
                levels=("occupation", "activity"),
                old_field=old_occupation_activity,
                new_filed=new_occupation_activity,
            )

        return self

    def personal_occupation_cnpj(self):
        old_occupation_cnpj = (
            self.__old_personal_data.get("occupation", {})
            .get("company", {})
            .get("cnpj")
        )

        if new_occupation_cnpj := self._get_new_value("occupation_cnpj"):
            self._update_modified_data(
                levels=("occupation", "company", "cnpj"),
                old_field=old_occupation_cnpj,
                new_filed=new_occupation_cnpj,
            )

        return self

    def personal_company_name(self):
        old_company_name = (
            self.__old_personal_data.get("occupation", {})
            .get("company", {})
            .get("name")
        )

        if new_company_name := self._get_new_value("company_name"):
            self._update_modified_data(
                levels=("occupation", "company", "name"),
                old_field=old_company_name,
                new_filed=new_company_name,
            )

        return self

    def personal_tax_residences(self):
        old_tax_residences = self.__old_personal_data.get("tax_residences")
        if new_tax_residences := self._get_new_value("tax_residences"):
            self._update_modified_data(
                levels=("tax_residences",), old_field=old_tax_residences, new_filed=new_tax_residences
            )
        return self

    def marital_status(self):
        old_marital_status = self.__old_personal_data.get("marital", {}).get("status")

        if new_marital_status := self._get_new_value("status"):
            self._update_modified_data(
                levels=("marital", "status"),
                old_field=old_marital_status,
                new_filed=new_marital_status,
            )

        return self

    def marital_cpf(self):
        spouse = self.__old_personal_data.get("marital", {}).get("spouse", {})
        if spouse:
            old_marital_cpf = spouse.get("cpf")

            if new_marital_cpf := self._get_new_value("marital_cpf"):
                self._update_modified_data(
                    levels=("marital", "spouse", "cpf"),
                    old_field=old_marital_cpf,
                    new_filed=new_marital_cpf,
                )

        return self

    def marital_nationality(self):
        spouse = self.__old_personal_data.get("marital", {}).get("spouse", {})
        if spouse:
            old_marital_nationality = spouse.get("nationality")

            if new_marital_nationality := self._get_new_value("marital_nationality"):
                self._update_modified_data(
                    levels=("marital", "spouse", "nationality"),
                    old_field=old_marital_nationality,
                    new_filed=new_marital_nationality,
                )
        return self

    def marital_spouse_name(self):
        spouse = self.__old_personal_data.get("marital", {}).get("spouse", {})
        if spouse:
            old_spouse_name = spouse.get("name")

            if new_marital_spouse_name := self._get_new_value("marital_spouse_name"):
                self._update_modified_data(
                    levels=("marital", "spouse", "name"),
                    old_field=old_spouse_name,
                    new_filed=new_marital_spouse_name,
                )

        return self

    def documents_cpf(self):
        old_cpf = self.__old_personal_data.get("cpf")
        if new_cpf := self._get_new_value("document_cpf"):
            self._update_modified_data(
                levels=("cpf",), old_field=old_cpf, new_filed=new_cpf
            )
        return self

    def documents_identity_type(self):
        old_document_identity_type = (
            self.__old_personal_data.get("identifier_document", {})
            .get("document_data", {})
            .get("type")
        )

        if new_document_identity_type := self._get_new_value(
            "document_identity_type"
        ):
            self._update_modified_data(
                levels=("identifier_document", "document_data", "type"),
                old_field=old_document_identity_type,
                new_filed=new_document_identity_type,
            )
        return self

    def documents_identity_number(self):
        old_document_identity_number = (
            self.__old_personal_data.get("identifier_document", {})
            .get("document_data", {})
            .get("number")
        )

        if new_document_identity_number := self._get_new_value(
            "document_identity_number"
        ):
            self._update_modified_data(
                levels=("identifier_document", "document_data", "number"),
                old_field=old_document_identity_number,
                new_filed=new_document_identity_number,
            )
        return self

    def documents_expedition_date(self):
        old_document_expedition_date = (
            self.__old_personal_data.get("identifier_document", {})
            .get("document_data", {})
            .get("date")
        )

        if new_document_expedition_date := self._get_new_value(
            "document_expedition_date"
        ):
            self._update_modified_data(
                levels=("identifier_document", "document_data", "date"),
                old_field=old_document_expedition_date,
                new_filed=new_document_expedition_date,
            )
        return self

    def documents_issuer(self):
        old_document_issuer = (
            self.__old_personal_data.get("identifier_document", {})
            .get("document_data", {})
            .get("issuer")
        )

        if new_document_issuer := self._get_new_value("document_issuer"):
            self._update_modified_data(
                levels=("identifier_document", "document_data", "issuer"),
                old_field=old_document_issuer,
                new_filed=new_document_issuer,
            )
        return self

    def documents_state(self):
        old_document_state = (
            self.__old_personal_data.get("identifier_document", {})
            .get("document_data", {})
            .get("state")
        )
        if new_document_state := self._get_new_value("document_issuer"):
            self._update_modified_data(
                levels=("identifier_document", "document_data", "state"),
                old_field=old_document_state,
                new_filed=new_document_state,
            )
        return self

    def address_country(self):
        old_address_country = self.__old_personal_data.get("address", {}).get("country")

        if new_address_country := self._get_new_value("address_country"):
            self._update_modified_data(
                levels=("address", "country"),
                old_field=old_address_country,
                new_filed=new_address_country,
            )

        return self

    def address_street_name(self):
        old_address_street_name = self.__old_personal_data.get("address", {}).get(
            "street_name"
        )

        if new_address_street_name := self._get_new_value("address_street_name"):
            self._update_modified_data(
                levels=("address", "street_name"),
                old_field=old_address_street_name,
                new_filed=new_address_street_name,
            )
        return self

    def address_city(self):
        old_address_city = self.__old_personal_data.get("address", {}).get("city")

        if new_address_city := self._get_new_value("address_city"):
            self._update_modified_data(
                levels=("address", "city"),
                old_field=old_address_city,
                new_filed=new_address_city,
            )
        return self

    def address_number(self):
        old_address_number = self.__old_personal_data.get("address", {}).get("number")

        if new_address_number := self._get_new_value("address_number"):
            self._update_modified_data(
                levels=("address", "number"),
                old_field=old_address_number,
                new_filed=new_address_number,
            )
        return self

    def address_id_city(self):
        old_address_id_city = self.__old_personal_data.get("address", {}).get("id_city")

        if new_address_id_city := self._get_new_value("address_id_city"):
            self._update_modified_data(
                levels=("address", "id_city"),
                old_field=old_address_id_city,
                new_filed=new_address_id_city,
            )
        return self

    def address_zip_code(self):
        old_address_zip_code = self.__old_personal_data.get("address", {}).get(
            "zip_code"
        )

        if new_address_zip_code := self._get_new_value("address_zip_code"):
            self._update_modified_data(
                levels=("address", "zip_code"),
                old_field=old_address_zip_code,
                new_filed=new_address_zip_code,
            )

        return self

    def address_neighborhood(self):
        old_address_neighborhood = self.__old_personal_data.get("address", {}).get(
            "neighborhood"
        )

        if new_address_neighborhood := self._get_new_value("address_neighborhood"):
            self._update_modified_data(
                levels=("address", "neighborhood"),
                old_field=old_address_neighborhood,
                new_filed=new_address_neighborhood,
            )
        return self

    def address_state(self):
        old_address_state = self.__old_personal_data.get("address", {}).get("state")

        if new_address_state := self._get_new_value("address_state"):
            self._update_modified_data(
                levels=("address", "state"),
                old_field=old_address_state,
                new_filed=new_address_state,
            )
        return self

    def build(self) -> Tuple[dict, dict]:
        modified_register = {
            "unique_id": self.__unique_id,
            "modified_data": self.__modified_data,
            "source": "user",
        }
        return self.__update_buffer, modified_register
