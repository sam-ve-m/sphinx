# STANDARD LIBS
from typing import Type

# SPHINX
from src.infrastructures.oracle.infrastructure import OracleInfrastructure
from src.repositories.client_register.builder import ClientRegisterBuilder


class SinaCorTypesRepository(OracleInfrastructure):

    def get_type_of_income_tax(self):
        sql = """
            SELECT TP_IMP_RENDA as code, DS_IMP_RENDA as description
            FROM TSCTIPIR;
        """
        return self.query(sql=sql)

    def get_client_type(self):
        sql = """
            SELECT TP_CLIENTE as code, DS_TIPO_CLIENTE as description
            FROM TSCTIPCLI;
        """
        return self.query(sql=sql)

    def get_investor_type(self):
        sql = """
            SELECT TP_INVESTIDOR as code, DS_INVESTIDOR as description
            FROM TSCTPINVESTIDOR;
        """
        return self.query(sql=sql)

    def get_activity_type(self):
        sql = """
            SELECT CD_ATIV as code, DS_ATIV as description
            FROM TSCATIV;
        """
        return self.query(sql=sql)

    def get_type_ability_person(self):
        sql = """
            SELECT CD_CAPAC as code, DS_CAPAC as description
            FROM TSCCAPAC;
        """
        return self.query(sql=sql)

    def get_customer_qualification_type(self):
        sql = """
            SELECT CD_TIPO_FILI as code, DS_TIPO_FILI as description
            FROM TSCTIPFIL;
        """
        return self.query(sql=sql)

    def get_cosif_tax_classification(self):
        sql = """
            SELECT CD_COSIF as code, DS_COSIF as description
            FROM TSCCOSIF;
        """
        return self.query(sql=sql)

    def get_marital_status(self):
        sql = """
            SELECT CD_EST_CIVIL as code, DS_EST_CIVIL as description
            FROM TSCESTCIV;
        """
        return self.query(sql=sql)

    def get_nationality(self):
        sql = """
            SELECT CD_NACION as code, DS_NACION as description
            FROM TSCNACION;
        """
        return self.query(sql=sql)

    def get_document_issuing_body(self):
        sql = """
            SELECT CD_ORG_EMIT as code, DS_ORG_EMIT as description
            FROM TSCOREMI;
        """
        return self.query(sql=sql)

    def get_document_type(self):
        sql = """
            SELECT CD_TIPO_DOC as code, DS_TIPO_DOC as description
            FROM TSCTIPDOC;
        """
        return self.query(sql=sql)

    def get_county(self, country: str, state: str):
        sql = f"""
            SELECT COD_MUNI as code, NOME_MUNI as description
            FROM TSCDXMUNICIPIO
            WHERE pais='{country}'
            AND estado='{state}';
        """
        return self.query(sql=sql)

    def get_state(self, country: str):
        sql = """
            SELECT SG_ESTADO as initials, NM_ESTADO as description
            FROM TSCESTADO
            WHERE pais='{country}';
        """
        return self.query(sql=sql)

    def get_country(self):
        sql = """
            SELECT SG_PAIS as initials, NM_PAIS as description
            FROM TSCPAIS;
        """
        return self.query(sql=sql)

    def get_marriage_regime(self):
        sql = """
            SELECT TP_REGCAS as code, DS_REGCAS as description
            FROM TSCREGCAS;
        """
        return self.query(sql=sql)

    def get_customer_origin(self):
        sql = """
            SELECT CD_ORIGEM as code, DS_ORIGEM as description
            FROM TSCCADORIGEM;
        """
        return self.query(sql=sql)

    def get_customer_status(self):
        sql = """
            SELECT TP_SITUAC as code, DS_SITUAC as description
            FROM TSCTPSITUACAO;
        """
        return self.query(sql=sql)

    def get_bmf_customer_type(self, client_type: str):
        sql = f"""
            SELECT TP_CLIENTE_BMF as code, DS_TIPO_CLIENTE as description
            FROM TSCTIPCLIBMF
            WHERE TIPO_CLIENT='{client_type}';
        """
        return self.query(sql=sql)

    def get_economic_activity(self):
        sql = """
            SELECT COD_AECO as code, NOME_AECO as description
            FROM TSCDXAECO;
        """
        return self.query(sql=sql)

    def get_account_type(self):
        sql = """
            SELECT NUM_TIPO_CON as code, NOME_TIPO_CON as description
            FROM TSCDXTIPO_CON;
        """
        return self.query(sql=sql)
