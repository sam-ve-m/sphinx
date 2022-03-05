# STANDARD LIBS
import asyncio
from hashlib import sha1
from typing import List, Optional

import nest_asyncio

nest_asyncio.apply()

# SPHINX
from src.repositories.base_repository.oracle.base import OracleBaseRepository
from src.repositories.cache.redis import RepositoryRedis


class SinacorTypesRepository(OracleBaseRepository):
    cache = RepositoryRedis

    @classmethod
    def get_county_name_by_id(cls, id: int) -> Optional[str]:
        sql = f"""
            SELECT NOME_MUNI
            FROM TSCDXMUNICIPIO
            WHERE NUM_SEQ_MUNI = {id}
        """
        current_event_loop = asyncio.get_running_loop()
        task = current_event_loop.create_task(cls.query_with_cache(sql=sql))
        tuple_result = current_event_loop.run_until_complete(task)
        if tuple_result:
            return tuple_result[0][0]

    @staticmethod
    def tuples_to_dict_list(fields: List[str], values: List[tuple]) -> List:
        dicts_result = list()
        for value in values:
            dicts_result.append(dict(zip(fields, value)))
        return dicts_result

    @classmethod
    async def get_type_of_income_tax(cls) -> list:
        sql = """
            SELECT TP_IMP_RENDA as code, DS_IMP_RENDA as description
            FROM TSCTIPIR
        """
        tuple_result = await cls.query_with_cache(sql=sql)
        dict_result = cls.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    @classmethod
    async def get_activity_type(cls) -> list:
        sql = """
            SELECT CD_ATIV as code, DS_ATIV as description
            FROM TSCATIV
        """
        tuple_result = await cls.query_with_cache(sql=sql)
        dict_result = cls.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    @classmethod
    async def get_nationality(cls) -> list:
        sql = """
            SELECT CD_NACION as code, DS_NACION as description
            FROM TSCNACION
        """
        tuple_result = await cls.query_with_cache(sql=sql)
        dict_result = cls.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    @classmethod
    async def get_document_issuing_body(cls) -> list:
        sql = """
            SELECT CD_ORG_EMIT as code, DS_ORG_EMIT as description
            FROM TSCOREMI
        """
        tuple_result = await cls.query_with_cache(sql=sql)
        dict_result = cls.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    @classmethod
    async def get_document_type(cls) -> list:
        sql = """
            SELECT CD_TIPO_DOC as code, DS_TIPO_DOC as description
            FROM TSCTIPDOC
        """
        tuple_result = await cls.query_with_cache(sql=sql)
        dict_result = cls.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    @classmethod
    async def get_county(cls, country: str, state: str) -> list:
        sql = f"""
            SELECT NUM_SEQ_MUNI as code, NOME_MUNI as description
            FROM TSCDXMUNICIPIO
            WHERE SIGL_PAIS='{country}'
            AND SIGL_ESTADO='{state}'
        """
        tuple_result = await cls.query_with_cache(sql=sql)
        dict_result = cls.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    @classmethod
    async def get_state(cls, country: str) -> list:
        sql = f"""
            SELECT SG_ESTADO as initials, NM_ESTADO as description
            FROM TSCESTADO
            WHERE SG_PAIS='{country}'
        """
        tuple_result = await cls.query_with_cache(sql=sql)
        dict_result = cls.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    @classmethod
    async def get_country(cls) -> list:
        sql = """
            SELECT SG_PAIS as initials, NM_PAIS as description
            FROM TSCPAIS
        """
        tuple_result = await cls.query_with_cache(sql=sql)
        dict_result = cls.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    @classmethod
    async def get_economic_activity(cls) -> list:
        sql = """
            SELECT COD_AECO as code, NOME_AECO as description
            FROM TSCDXAECO
        """
        tuple_result = await cls.query_with_cache(sql=sql)
        dict_result = cls.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    @classmethod
    async def get_issuing_body(cls) -> list:
        sql = """
            SELECT CD_ORG_EMIT as code, DS_ORG_EMIT as description
            FROM TSCOREMI
        """
        tuple_result = await cls.query_with_cache(sql=sql)
        dict_result = cls.tuples_to_dict_list(
            fields=["code", "description"], values=tuple_result
        )
        return dict_result

    @classmethod
    async def query_with_cache(cls, sql: str) -> list:
        _sha1 = sha1()
        _sha1.update(str(sql).encode())
        partial_key = _sha1.hexdigest()
        key = f"sinacor_types:{partial_key}"
        value = await cls.cache.get(key=key)
        if not value:
            partial_value = await cls.query(sql=sql)
            value = {"value": partial_value}
            await cls.cache.set(key=key, value=value, ttl=86400)

        value = value.get("value")
        return value

    @classmethod
    def base_validator(cls, sql: str) -> bool:
        current_event_loop = asyncio.get_running_loop()
        task = current_event_loop.create_task(cls.query_with_cache(sql=sql))
        value = current_event_loop.run_until_complete(task)
        return len(value) == 1 and value[0][0] == 1

    @classmethod
    def validate_country(cls, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCPAIS
            WHERE SG_PAIS = '{value}'
        """
        return cls.base_validator(sql=sql)

    @classmethod
    def validate_nationality(cls, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCNACION
            WHERE CD_NACION = {value}
        """
        return cls.base_validator(sql=sql)

    @classmethod
    def validate_state(
        cls,
        value: str,
    ) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCESTADO
            WHERE SG_ESTADO = '{value}'
        """
        return cls.base_validator(sql=sql)

    @classmethod
    def validate_city_id(cls, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCDXMUNICIPIO
            WHERE COD_MUNI = '{value}'
        """
        return cls.base_validator(sql=sql)

    @classmethod
    def validate_city(cls, value: str) -> bool:
        sql = f"""
              SELECT 1
              FROM TSCDXMUNICIPIO
              WHERE NOME_MUNI = '{value}'
          """
        return cls.base_validator(sql=sql)

    @classmethod
    def validate_activity(cls, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCATIV
            WHERE CD_ATIV = {value}
        """
        return cls.base_validator(sql=sql)

    @classmethod
    def is_unemployed(cls, value: str, cnpj: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCATIV
            WHERE DS_ATIV = 'OUTROS'
            AND CD_ATIV = {value}
        """
        is_other = cls.base_validator(sql=sql)
        has_cnpj = cnpj is not None

        return is_other and not has_cnpj

    @classmethod
    def is_business_person(cls, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCATIV
            WHERE DS_ATIV = 'EMPRESARIO'
            AND CD_ATIV = {value}
        """
        return cls.base_validator(sql=sql)

    @classmethod
    def validate_client_type(cls, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCTIPCLI
            WHERE TP_CLIENTE = {value}
        """
        return cls.base_validator(sql=sql)

    @classmethod
    def validate_document_type(cls, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCTIPDOC
            WHERE CD_TIPO_DOC = {value}
        """
        return cls.base_validator(sql=sql)

    @classmethod
    def validate_county(cls, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCDXMUNICIPIO
            WHERE NUM_SEQ_MUNI = {value}
        """
        return cls.base_validator(sql=sql)

    @classmethod
    def validate_marital_regime(cls, value: str) -> bool:
        sql = f"""
            SELECT 1
            FROM TSCREGCAS
            WHERE TP_REGCAS = {value}
        """
        return cls.base_validator(sql=sql)

    @classmethod
    def validate_marital_status(cls, value: str) -> bool:
        sql = f""" SELECT 1 FROM TSCESTCIV where CD_EST_CIVIL = {value}"""
        return cls.base_validator(sql=sql)

    @classmethod
    def validate_contry_state_city_and_id_city(
        cls, contry: str, state: str, city: str, id_city: int
    ) -> bool:
        sql = f"""SELECT 1 FROM TSCDXMUNICIPIO WHERE SIGL_PAIS = '{contry}' 
        AND SIGL_ESTADO = '{state}' AND NOME_MUNI = '{city}' AND NUM_SEQ_MUNI = {id_city}"""
        return cls.base_validator(sql=sql)

    @classmethod
    def validate_contry_state_and_id_city(
        cls, contry: str, state: str, id_city: int
    ) -> bool:
        sql = f"""SELECT 1 FROM TSCDXMUNICIPIO WHERE SIGL_PAIS = '{contry}' 
        AND SIGL_ESTADO = '{state}' AND NUM_SEQ_MUNI = {id_city}"""
        return cls.base_validator(sql=sql)
