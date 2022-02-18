# STANDARD LIBS
from typing import Type, List, Optional
from hashlib import sha1

# SPHINX
from src.repositories.base_repository.oracle.base import OracleBaseRepository
from src.repositories.cache.redis import RepositoryRedis


class SinacorTypesRepository(OracleBaseRepository):
    def get_county_name_by_id(self, id: int) -> Optional[str]:
        sql = f"""
            SELECT NOME_MUNI
            FROM TSCDXMUNICIPIO
            WHERE NUM_SEQ_MUNI = {id}
        """
        tuple_result = self.query_with_cache(sql=sql)
        if tuple_result:
            return tuple_result[0][0]

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
        tuple_result = self.query_with_cache(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_activity_type(self):
        sql = """
            SELECT CD_ATIV as code, DS_ATIV as description
            FROM TSCATIV
        """
        tuple_result = self.query_with_cache(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result


    def get_nationality(self):
        sql = """
            SELECT CD_NACION as code, DS_NACION as description
            FROM TSCNACION
        """
        tuple_result = self.query_with_cache(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_document_issuing_body(self):
        sql = """
            SELECT CD_ORG_EMIT as code, DS_ORG_EMIT as description
            FROM TSCOREMI
        """
        tuple_result = self.query_with_cache(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_document_type(self):
        sql = """
            SELECT CD_TIPO_DOC as code, DS_TIPO_DOC as description
            FROM TSCTIPDOC
        """
        tuple_result = self.query_with_cache(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_county(self, country: str, state: str):
        sql = f"""
            SELECT NUM_SEQ_MUNI as code, NOME_MUNI as description
            FROM TSCDXMUNICIPIO
            WHERE SIGL_PAIS='{country}'
            AND SIGL_ESTADO='{state}'
        """
        tuple_result = self.query_with_cache(sql=sql)
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
        tuple_result = self.query_with_cache(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_country(self):
        sql = """
            SELECT SG_PAIS as initials, NM_PAIS as description
            FROM TSCPAIS
        """
        tuple_result = self.query_with_cache(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_economic_activity(self):
        sql = """
            SELECT COD_AECO as code, NOME_AECO as description
            FROM TSCDXAECO
        """
        tuple_result = self.query_with_cache(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    def get_issuing_body(self):
        sql = """
            SELECT CD_ORG_EMIT as code, DS_ORG_EMIT as description
            FROM TSCOREMI
        """
        tuple_result = self.query_with_cache(sql=sql)
        dict_result = self.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    async def query_with_cache(self, sql: str, cache=RepositoryRedis) -> list:
        _sha1 = sha1()
        _sha1.update(str(sql).encode())
        partial_key = _sha1.hexdigest()
        key = f"sinacor_types:{partial_key}"
        value = await cache.get(key=key)
        if not value:
            partial_value = self.query(sql=sql)
            value = {"value": partial_value}
            await cache.set(key=key, value=value, ttl=86400)

        value = value.get("value")
        return value

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

    def validate_state(
        self,
        value: str,
    ) -> bool:
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
            WHERE CD_ATIV = {value}
        """
        return self.base_validator(sql=sql)

    def is_unemployed(self, value: str, cnpj: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCATIV
            WHERE DS_ATIV = 'OUTROS'
            AND CD_ATIV = {value}
        """
        is_other = self.base_validator(sql=sql)
        has_cnpj = cnpj is not None

        return is_other and not has_cnpj

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

    def validate_marital_status(self, value: str) -> bool:
        sql = f""" SELECT 1 FROM TSCESTCIV where CD_EST_CIVIL = {value}"""
        return self.base_validator(sql=sql)

    def validate_contry_state_city_and_id_city(
        self, contry: str, state: str, city: str, id_city: int
    ) -> bool:
        sql = f"""SELECT 1 FROM TSCDXMUNICIPIO WHERE SIGL_PAIS = '{contry}' 
        AND SIGL_ESTADO = '{state}' AND NOME_MUNI = '{city}' AND NUM_SEQ_MUNI = {id_city}"""
        return self.base_validator(sql=sql)

    def validate_contry_state_and_id_city(
        self, contry: str, state: str, id_city: int
    ) -> bool:
        sql = f"""SELECT 1 FROM TSCDXMUNICIPIO WHERE SIGL_PAIS = '{contry}' 
        AND SIGL_ESTADO = '{state}' AND NUM_SEQ_MUNI = {id_city}"""
        return self.base_validator(sql=sql)
