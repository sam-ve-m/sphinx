class CustomerRegistrationBuilder:
    def __init__(self, personal_data: dict):
        self.__personal_data = personal_data
        self.__buffer = {
            "personal": {},
            "marital": {},
            "documents": {},
            "address": {},

        }

    def personal_name(self):
        name = self.__personal_data.get("name")
        self.__buffer["personal"].update({"name": name})
        return self

    def personal_birth_date(self):
        birth_date = self.__personal_data.get("birth_date")
        self.__buffer["personal"].update({"birth_date": birth_date})
        return self

    def personal_parentage(self):
        father_name = self.__personal_data.get("father_name")
        self.__buffer["personal"].update({"father_name": father_name})
        mother_name = self.__personal_data.get("mother_name")
        self.__buffer["personal"].update({"father_name": mother_name})
        return self

    def personal_gender(self):
        gender = self.__personal_data.get("gender")
        self.__buffer["personal"].update({"gender": gender})
        return self

    def personal_email(self):
        email = self.__personal_data.get("email")
        self.__buffer["personal"].update({"email": email})
        return self

    def personal_phone(self):
        phone = self.__personal_data.get("cel_phone")
        self.__buffer["personal"].update({"phone": phone})
        return self

    def personal_patrimony(self):
        patrimony = (self.__personal_data
                     .get("assets", {})
                     .get("patrimony"))
        self.__buffer["personal"].update({"patrimony": patrimony})
        return self

    def personal_us_tin(self):
        us_tin = (self.__personal_data
                  .get("us_tin"))
        self.__buffer["personal"].update({"us_tin": us_tin})
        return self

    def personal_occupation_activity(self):
        occupation_activity = (self.__personal_data
                               .get("occupation", {})
                               .get("activity"))

        self.__buffer["personal"].update({"occupation_activity": occupation_activity})
        return self

    def personal_company_name(self):
        company_name = (self.__personal_data
                         .get("occupation", {})
                         .get("company", {})
                         .get("name"))
        self.__buffer["personal"].update({"company_name": company_name})
        return self

    def marital_status(self):
        marital_status = (self.__personal_data
                          .get("marital", {})
                          .get("status"))
        self.__buffer["marital"].update({"marital_status": marital_status})
        return self

    def marital_spouse_name(self):
        spouse_name = (self.__personal_data
                       .get("marital", {})
                       .get("spouse", {})
                       .get("name"))
        self.__buffer["marital"].update({"spouse_name": spouse_name})
        return self

    def marital_spouse_cpf(self):
        spouse_cpf = (self.__personal_data
                      .get("marital", {})
                      .get("spouse", {})
                      .get("cpf"))
        self.__buffer["marital"].update({"spouse_cpf": spouse_cpf})
        return self

    def marital_cpf(self):
        marital_cpf = (self.__personal_data
                           .get("marital", {})
                           .get("spouse", {})
                           .get("cpf"))
        self.__buffer["marital"].update({"marital_cpf": marital_cpf})
        return self

    def marital_nationality(self):
        nationality = (self.__personal_data
                           .get("marital", {})
                           .get("spouse", {})
                           .get("nationality"))
        self.__buffer["marital"].update({"nationality": nationality})
        return self

    def documents_cpf(self):
        cpf = self.__personal_data.get("cpf")
        self.__buffer["documents"].update({"cpf": cpf})
        return self

    def documents_identity_number(self):
        identity_number = (self.__personal_data
                           .get("identifier_document", {})
                           .get("document_data", {})
                           .get("number"))
        self.__buffer["documents"].update({"identity_number": identity_number})
        return self

    def documents_expedition_date(self):
        expedition_date = (self.__personal_data
                         .get("identifier_document", {})
                         .get("document_data", {})
                         .get("date"))
        self.__buffer["documents"].update({"expedition_date": expedition_date})
        return self

    def documents_issuer(self):
        issuer = (self.__personal_data
                  .get("identifier_document", {})
                  .get("document_data", {})
                  .get("issuer"))
        self.__buffer["documents"].update({"issuer": issuer})
        return self

    def documents_state(self):
        state = (self.__personal_data
                 .get("identifier_document", {})
                 .get("document_data", {})
                 .get("state"))
        self.__buffer["documents"].update({"state": state})
        return self

    def address_country(self):
        country = (self.__personal_data
                   .get("address", {})
                   .get("country"))
        self.__buffer["address"].update({"country": country})
        return self

    def address_number(self):
        number = (self.__personal_data
                   .get("address", {})
                   .get("number"))
        self.__buffer["address"].update({"number": number})
        return self

    def address_street_name(self):
        street_name = (self.__personal_data
                       .get("address", {})
                       .get("street_name"))
        self.__buffer["address"].update({"street_name": street_name})
        return self

    def address_city(self):
        city = (self.__personal_data
                .get("address", {})
                .get("city"))
        self.__buffer["address"].update({"city": city})
        return self

    def address_neighborhood(self):
        neighborhood = (self.__personal_data
                        .get("address", {})
                        .get("neighborhood"))
        self.__buffer["address"].update({"neighborhood": neighborhood})
        return self

    def address_zip_code(self):
        zip_code = (self.__personal_data
                    .get("address", {})
                    .get("zip_code"))
        self.__buffer["address"].update({"zip_code": zip_code})
        return self

    def address_state(self):
        state = (self.__personal_data
                 .get("address", {})
                 .get("state"))
        self.__buffer["address"].update({"state": state})
        return self

    def build(self) -> dict:
        return self.__buffer

