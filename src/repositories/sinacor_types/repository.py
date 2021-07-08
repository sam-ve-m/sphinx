# STANDARD LIBS
from typing import Type

# SPHINX
from src.infrastructures.oracle.infrastructure import OracleInfrastructure
from src.repositories.client_register.builder import ClientRegisterBuilder


class SinaCorTypesRepository(OracleInfrastructure):

    def get_type_of_income_tax(self):
        sql = """
            SELECT codigo as code, descricao as description
            FROM TSCTIPIR;
        """
        return self.query(sql=sql)

    def get_client_type(self):
        sql = """
            SELECT codigo as code, descricao as description
            FROM TSCTIPCLI;
        """
        return self.query(sql=sql)

    def get_investor_type(self):
        sql = """
            SELECT codigo as code, descricao as description
            FROM TSCTPINVESTIDOR;
        """
        return self.query(sql=sql)

    def get_activity_type(self):
        sql = """
            SELECT codigo as code, descricao as description
            FROM TSCATIV;
        """
        return self.query(sql=sql)

    def get_type_ability_person(self):
        sql = """
            SELECT codigo as code, descricao as description
            FROM TSCCAPAC;
        """
        return self.query(sql=sql)

    def get_customer_qualification_type(self):
        sql = """
            SELECT codigo as code, descricao as description
            FROM TSCTIPFIL;
        """
        return self.query(sql=sql)

    def get_cosif_tax_classification(self):
        sql = """
            SELECT codigo as code, descricao as description
            FROM TSCCOSIF;
        """
        return self.query(sql=sql)

    def get_marital_status(self):
        sql = """
            SELECT codigo as code, descricao as description
            FROM TSCESTCIV;
        """
        return self.query(sql=sql)

    def get_nationality(self):
        sql = """
            SELECT codigo as code, descricao as description
            FROM TSCNACION;
        """
        return self.query(sql=sql)

    def get_document_issuing_body(self):
        sql = """
            SELECT codigo as code, descricao as description
            FROM TSCOREMI;
        """
        return self.query(sql=sql)

    def get_document_type(self):
        sql = """
            SELECT codigo as code, descricao as description
            FROM TSCTIPDOC;
        """
        return self.query(sql=sql)

    def get_county(self, country: str, state: str):
        sql = f"""
            SELECT codigo as code, descricao as description
            FROM TSCDXMUNICIPIO
            WHERE pais='{country}'
            AND estado='{state}';
        """
        return self.query(sql=sql)

    def get_state(self, country: str):
        sql = """
            SELECT sigla as initials, descricao as description
            FROM TSCESTADO
            WHERE pais='{country}';
        """
        return self.query(sql=sql)

    def get_country(self):
        sql = """
            SELECT sigla as initials, descricao as description
            FROM TSCPAIS;
        """
        return self.query(sql=sql)

    def get_marriage_regime(self):
        sql = """
            SELECT codigo as code, descricao as description
            FROM TSCREGCAS;
        """
        return self.query(sql=sql)

    def get_customer_origin(self):
        sql = """
            SELECT codigo as code, descricao as description
            FROM TSCCADORIGEM;
        """
        return self.query(sql=sql)

    def get_customer_status(self):
        sql = """
            SELECT codigo as code, descricao as description
            FROM TSCTPSITUACAO;
        """
        return self.query(sql=sql)

    def get_bmf_customer_type(self, client_type: str):
        sql = f"""
            SELECT codigo as code, descricao as description
            FROM TSCTIPCLIBMF
            WHERE TIPO_CLIENT='{client_type}';
        """
        return self.query(sql=sql)

    def get_economic_activity(self):
        sql = """
            SELECT codigo as code, descricao as description
            FROM TSCDXAECO;
        """
        return self.query(sql=sql)

    def get_account_type(self):
        sql = """
            SELECT codigo as code, descricao as description
            FROM TSCDXTIPO_CON;
        """
        return self.query(sql=sql)
