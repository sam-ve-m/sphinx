# STANDARD LIBS
from typing import Type, List
from hashlib import sha1

# SPHINX
from src.infrastructures.oracle.infrastructure import OracleInfrastructure
from src.repositories.cache.redis import RepositoryRedis


class SinaCorTypesRepository(OracleInfrastructure):
    @staticmethod
    def tuples_to_dict_list(fields: List[str], values: List[tuple]):
        dicts_result = list()
        for value in values:
            dicts_result.append(dict(zip(fields, value)))
        return dicts_result

    def get_type_of_income_tax(self):
        sql = """
            SELECT TP_IMP_RENDA as code, DS_IMP_RENDA as description
            FROM TSCTIPIR
        """
        tuple_result = self.query(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_client_type(self):
        sql = """
            SELECT TP_CLIENTE as code, DS_TIPO_CLIENTE as description
            FROM TSCTIPCLI
        """
        tuple_result = self.query(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_investor_type(self):
        sql = """
            SELECT TP_INVESTIDOR as code, DS_INVESTIDOR as description
            FROM TSCTPINVESTIDOR
        """
        tuple_result = self.query(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_activity_type(self):
        sql = """
            SELECT CD_ATIV as code, DS_ATIV as description
            FROM TSCATIV
        """
        tuple_result = self.query(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_type_ability_person(self):
        sql = """
            SELECT CD_CAPAC as code, DS_CAPAC as description
            FROM TSCCAPAC
        """
        tuple_result = self.query(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_customer_qualification_type(self):
        sql = """
            SELECT CD_TIPO_FILI as code, DS_TIPO_FILI as description
            FROM TSCTIPFIL
        """
        tuple_result = self.query(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_cosif_tax_classification(self):
        sql = """
            SELECT CD_COSIF as code, DS_COSIF as description
            FROM TSCCOSIF
        """
        tuple_result = self.query(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_marital_status(self):
        sql = """
            SELECT CD_EST_CIVIL as code, DS_EST_CIVIL as description
            FROM TSCESTCIV
        """
        tuple_result = self.query(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_nationality(self):
        sql = """
            SELECT CD_NACION as code, DS_NACION as description
            FROM TSCNACION
        """
        tuple_result = self.query(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_document_issuing_body(self):
        sql = """
            SELECT CD_ORG_EMIT as code, DS_ORG_EMIT as description
            FROM TSCOREMI
        """
        tuple_result = self.query(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_document_type(self):
        sql = """
            SELECT CD_TIPO_DOC as code, DS_TIPO_DOC as description
            FROM TSCTIPDOC
        """
        tuple_result = self.query(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_county(self, country: str, state: str):
        sql = f"""
            SELECT COD_MUNI as code, NOME_MUNI as description
            FROM TSCDXMUNICIPIO
            WHERE SIGL_PAIS='{country}'
            AND SIGL_ESTADO='{state}'
        """
        tuple_result = self.query(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_state(self, country: str):
        sql = f"""
            SELECT SG_ESTADO as initials, NM_ESTADO as description
            FROM TSCESTADO
            WHERE SG_PAIS='{country}'
        """
        tuple_result = self.query(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["initials", "description"], values=tuple_result
        )
        return dict_result

    def get_country(self):
        sql = """
            SELECT SG_PAIS as initials, NM_PAIS as description
            FROM TSCPAIS
        """
        tuple_result = self.query(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["initials", "description"], values=tuple_result
        )
        return dict_result

    def get_marriage_regime(self):
        sql = """
            SELECT TP_REGCAS as code, DS_REGCAS as description
            FROM TSCREGCAS
        """
        tuple_result = self.query(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_customer_origin(self):
        sql = """
            SELECT CD_ORIGEM as code, DS_ORIGEM as description
            FROM TSCCADORIGEM
        """
        tuple_result = self.query(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_customer_status(self):
        sql = """
            SELECT TP_SITUAC as code, DS_SITUAC as description
            FROM TSCTPSITUACAO
        """
        tuple_result = self.query(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_nationality(self):
        sql = """
            SELECT TP_SITUAC as code, DS_SITUAC as description
            FROM TSCTPSITUACAO
        """
        tuple_result = self.query(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_bmf_customer_type(self, client_type: str):
        sql = f"""
            SELECT TP_CLIENTE_BMF as code, DS_TIPO_CLIENTE as description
            FROM TSCTIPCLIBMF
            WHERE TIPO_CLIENT='{client_type}'
        """
        tuple_result = self.query(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_economic_activity(self):
        sql = """
            SELECT COD_AECO as code, NOME_AECO as description
            FROM TSCDXAECO
        """
        tuple_result = self.query(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_account_type(self):
        sql = """
            SELECT NUM_TIPO_CON as code, NOME_TIPO_CON as description
            FROM TSCDXTIPO_CON
        """
        tuple_result = self.query(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def query_with_cache(self, sql: str, cache=RepositoryRedis) -> list:
        _sha1 = sha1()
        _sha1.update(str(sql).encode())
        partial_key = _sha1.hexdigest()
        key = f"sinacor_types:{partial_key}"
        value = cache.get(key=key)
        if not value:
            partial_value = self.query(sql=sql)
            value = {"value": partial_value}
            cache.set(key=key, value=value, ttl=86400)
        return value.get("value")

    def base_validator(self, sql: str) -> bool:
        value = self.query_with_cache(sql=sql)
        return len(value) == 1 and value[0][0] == 1

    def validate_country(self, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCPAIS
            WHERE SG_PAIS = '{value}'
        """
        return self.base_validator(sql=sql)

    def validate_nationality(self, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCNACION
            WHERE CD_NACION = {value}
        """
        return self.base_validator(sql=sql)

    def validate_state(self, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCESTADO
            WHERE SG_ESTADO = '{value}'
        """
        return self.base_validator(sql=sql)

    def validate_city_id(self, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCDXMUNICIPIO
            WHERE COD_MUNI = '{value}'
        """
        return self.base_validator(sql=sql)

    def validate_city(self, value: str) -> bool:
        sql = f"""
              SELECT 1
              FROM TSCDXMUNICIPIO
              WHERE NOME_MUNI = '{value}'
          """
        return self.base_validator(sql=sql)

    def validate_activity(self, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCATIV
            WHERE CD_ATIV = '{value}'
        """
        return self.base_validator(sql=sql)

    def validate_income_tax_type(self, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCTIPIR
            WHERE TP_IMP_RENDA = '{value}'
        """
        return self.base_validator(sql=sql)

    def is_others(self, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCATIV
            WHERE DS_ATIV = 'OUTROS'
            AND CD_ATIV = {value}
        """
        return self.base_validator(sql=sql)

    def is_business_person(self, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCATIV
            WHERE DS_ATIV = 'EMPRESARIO'
            AND CD_ATIV = {value}
        """
        return self.base_validator(sql=sql)

    def validate_client_type(self, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCTIPCLI
            WHERE TP_CLIENTE = {value}
        """
        return self.base_validator(sql=sql)

    def validate_investor_type(self, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCTPINVESTIDOR
            WHERE TP_INVESTIDOR = {value}
        """
        return self.base_validator(sql=sql)

    def validate_cosif_tax_classification(self, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCCOSIF
            WHERE CD_COSIF = {value}
        """
        return self.base_validator(sql=sql)

    def validate_document_type(self, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCTIPDOC
            WHERE CD_TIPO_DOC = {value}
        """
        return self.base_validator(sql=sql)

    def validate_county(self, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCDXMUNICIPIO
            WHERE NUM_SEQ_MUNI = {value}
        """
        return self.base_validator(sql=sql)

    def validate_marital_regime(self, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCREGCAS
            WHERE TP_REGCAS = {value}
        """
        return self.base_validator(sql=sql)
