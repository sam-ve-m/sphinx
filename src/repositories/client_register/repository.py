# STANDARD LIBS
import logging
from typing import Type, Optional

# SPHINX
from src.exceptions.exceptions import InternalServerError
from src.repositories.base_repository.oracle.base import OracleBaseRepository
from src.services.builders.client_register.builder import ClientRegisterBuilder
from src.repositories.sinacor_types.repository import SinacorTypesRepository
from src.domain.validators.marital_status_stone_age_to_sphinx import (
    MaritalStatusStoneAgeToSphinxEnum,
)
from src.infrastructures.env_config import config


class ClientRegisterRepository(OracleBaseRepository):
    def register_validated_users(self, user_cpf: str):
        values = {
            "cd_empresa": config("COMPANY_OPERATION_CODE"),
            "cd_usuario": "1",
            "tp_ocorrencia": "I",
            "cd_cliente_padrao": "1",
            "cpf": str(user_cpf),
        }
        self.execute(
            sql="call PROC_IMPCLIH_V2_LIONX.EXECIMPH(:cd_empresa, :cd_usuario, :tp_ocorrencia, :cd_cliente_padrao, :cpf)",
            values=values,
        )

    async def cleanup_temp_tables(self, user_cpf: str):
        client_temp = "DELETE FROM TSCIMPCLIH WHERE CD_CPFCGC = :cpf"
        self.execute(sql=client_temp, values={"cpf": str(user_cpf)})
        error_temp = "DELETE FROM TSCERROH WHERE CD_CPFCGC = :cpf"
        self.execute(sql=error_temp, values={"cpf": str(user_cpf)})

    async def validate_user_data_errors(self, user_cpf: int) -> bool:
        self._run_data_validator_in_register_user_tmp_table(user_cpf=user_cpf)
        return await self._validate_errors_on_temp_tables(user_cpf=user_cpf)

    async def _validate_errors_on_temp_tables(self, user_cpf: int) -> bool:
        sql = f"""
            SELECT 1 
            FROM TSCERROH
            WHERE CD_CPFCGC = {user_cpf}
        """
        result = await self.query(sql=sql)
        return len(result) > 0

    def _run_data_validator_in_register_user_tmp_table(self, user_cpf: int) -> int:
        self.execute(
            sql="call PROC_CLIECOH_V2_LIONX.EXECCONH(:s, :cpf)",
            values={"s": "S", "cpf": str(user_cpf)},
        )

    def register_user_data_in_register_users_temp_table(
        self, builder: Type[ClientRegisterBuilder]
    ):
        client_register = builder.build()
        fields = client_register.keys()
        sql = f"INSERT INTO TSCIMPCLIH({','.join(fields)}) VALUES(:{',:'.join(fields)})"
        self.execute(sql=sql, values=client_register)

    async def get_user_control_data_if_user_already_exists(self, user_cpf: int):
        verify_user_data_sql = f"SELECT 1 FROM TSCCLIGER WHERE CD_CPFCGC = {user_cpf}"
        verify_user_bovespa_account = (
            f"SELECT 1 FROM TSCCLIBOL WHERE CD_CPFCGC = {user_cpf}"
        )
        verify_user_bmf_account = (
            f"SELECT 1 FROM TSCCLIBMF WHERE CD_CPFCGC = {user_cpf}"
        )
        verify_user_account = f"SELECT 1 FROM TSCCLICOMP WHERE CD_CPFCGC = {user_cpf}"
        verify_user_treasury = f"SELECT 1 FROM TSCCLITSD WHERE CD_CPFCGC = {user_cpf}"
        all_validation_query = [
            verify_user_data_sql,
            verify_user_bovespa_account,
            verify_user_bmf_account,
            verify_user_account,
            verify_user_treasury,
        ]
        result = await self.query(sql=" union ".join(all_validation_query))
        if result and len(result) > 0:
            result = await self.query(
                sql=f"SELECT CD_CLIENTE, DV_CLIENTE FROM TSCCLIBOL WHERE CD_CPFCGC = {user_cpf}"
            )
            return result[0]
        return None

    async def get_sincad_status(self, user_cpf: int):
        sql = f"SELECT COD_SITU_ENVIO FROM TSCCLIBOL WHERE CD_CPFCGC = {user_cpf}"
        result = await self.query(sql=sql)
        if result and len(result) > 0:
            return result[0]
        return None

    async def get_sinacor_status(self, user_cpf: int):
        sql = f"SELECT IN_SITUAC FROM TSCCLIBOL WHERE CD_CPFCGC = {user_cpf}"
        result = await self.query(sql=sql)
        if result and len(result) > 0:
            return result[0]
        return None

    def is_married(self, user_data: dict):
        is_married = user_data["marital"]["status"] in [
            MaritalStatusStoneAgeToSphinxEnum.MARRIED_TO_BRAZILIAN.value,
            MaritalStatusStoneAgeToSphinxEnum.MARRIED_TO_A_NATURALIZED_BRAZILIAN.value,
            MaritalStatusStoneAgeToSphinxEnum.MARRIED_TO_A_FOREIGN.value,
            MaritalStatusStoneAgeToSphinxEnum.STABLE_UNION.value,
        ]

        return is_married

    async def get_builder(
        self,
        user_data: dict,
        sinacor_user_control_data: Optional[tuple],
        sinacor_types_repository=SinacorTypesRepository(),
    ) -> Type[ClientRegisterBuilder]:
        occupation = user_data["occupation"]
        activity = occupation["activity"]
        company = occupation.get("company", {})
        cnpj = company.get("cnpj")

        is_married = self.is_married(user_data=user_data)
        is_unemployed = sinacor_types_repository.is_unemployed(
            value=activity, cnpj=cnpj
        )
        is_business_person = sinacor_types_repository.is_business_person(value=activity)

        callback_key = (
            is_married,
            is_unemployed,
            is_business_person,
        )

        callbacks = {
            (
                True,
                True,
                False,
            ): ClientRegisterRepository._is_unemployed_and_married_person,
            (
                False,
                True,
                False,
            ): ClientRegisterRepository._is_unemployed_and_not_married_person,
            (
                True,
                False,
                False,
            ): ClientRegisterRepository._is_employed_and_married_person,
            (
                False,
                False,
                False,
            ): ClientRegisterRepository._is_employed_and_not_married_person,
            (
                True,
                False,
                True,
            ): ClientRegisterRepository._is_business_and_married_person,
            (
                False,
                False,
                True,
            ): ClientRegisterRepository._is_business_and_not_married_person,
        }

        callback = callbacks.get(callback_key)

        if callback is None:
            message = f"Sinacor builder callback not implemented. Parameters: (is_married: {is_married}, is_unemployed: {is_unemployed}, is_business_person: {is_business_person})"
            logging.error(msg=message)
            raise InternalServerError("internal_error")

        return await callback(
            user_data=user_data, sinacor_user_control_data=sinacor_user_control_data
        )

    async def client_is_allowed_to_cancel_registration(self, user_cpf: int, bmf_account: int):
        is_client_blocked = await self._is_client_blocked(user_cpf)
        client_has_value_blocked = await self._client_has_value_blocked(bmf_account)
        client_has_receivables = await self._client_has_receivables(bmf_account)
        client_has_options_blocked = await self._client_has_options_blocked(bmf_account)
        client_has_options_receivables = await self._client_has_options_receivables(
            bmf_account
        )
        client_has_values_in_bank_account = await self._client_has_values_in_bank_account(
            bmf_account
        )
        return (
            any(
                [
                    is_client_blocked,
                    client_has_value_blocked,
                    client_has_receivables,
                    client_has_options_blocked,
                    client_has_options_receivables,
                    client_has_values_in_bank_account,
                ]
            )
            is False
        )

    async def _is_client_blocked(self, user_cpf: int):
        result = await self.query(
            sql=f"SELECT 1 from TSCCLIGER WHERE CD_CPFCGC = {user_cpf} and IN_SITUAC = 'BL'"
        )
        return len(result) > 0

    async def _client_has_value_blocked(self, bmf_account: int):
        result = await self.query(
            sql=f"SELECT 1 from TCCSALDO_BLOQ WHERE COD_CLI = {bmf_account} and VAL_BLOQ > 0"
        )
        return len(result) > 0

    async def _client_has_receivables(self, bmf_account: int):
        result = await self.query(
            sql=f"SELECT 1 from TCCMOVTO WHERE CD_CLIENTE = {bmf_account} and DT_LIQUIDACAO >= SYSDATE"
        )
        return len(result) > 0

    async def _client_has_options_blocked(self, bmf_account: int):
        result = await self.query(
            sql=f"SELECT 1 from VCFPOSICAO WHERE COD_CLI = {bmf_account} and QTDE_BLQD is not null and QTDE_BLQD > 0"
        )
        return len(result) > 0

    async def _client_has_options_receivables(self, bmf_account: int):
        result = await self.query(
            sql=f"SELECT 1 from VCFPOSICAO where COD_CLI = {bmf_account} and tipo_merc in ('OPC','OPV') and data_venc >= SYSDATE"
        )
        return len(result) > 0

    async def _client_has_values_in_bank_account(self, bmf_account: int):
        result = await self.query(
            sql=f"select 1 from tccsaldo WHERE CD_CLIENTE = {bmf_account} and VL_TOTAL > 0"
        )
        return len(result) > 0

    @staticmethod
    def _is_unemployed_and_not_married_person(
        user_data: dict, sinacor_user_control_data: Optional[tuple]
    ) -> ClientRegisterBuilder:
        builder = ClientRegisterBuilder()
        (
            builder.add_tp_registro(sinacor_user_id=sinacor_user_control_data)
            .add_cd_cliente(sinacor_user_control_data=sinacor_user_control_data)
            .add_cd_org_emit(user_data=user_data)
            .add_dt_doc_ident(user_data=user_data)
            .add_nr_rg(user_data=user_data)
            .add_sg_estado_emiss_rg(user_data=user_data)
            .add_dt_emiss_rg(user_data=user_data)
            .add_cd_org_emit_rg(user_data=user_data)
            .add_cd_doc_ident(user_data=user_data)
            .add_in_rec_divi()
            .add_in_emite_nota()
            .add_pc_corcor_prin()
            .add_in_emite_nota_cs()
            .add_pc_corcor_prin_cs()
            .add_val_lim_neg_td()
            .add_val_taxa_agnt_td()
            .add_txt_email_td(user_data=user_data)
            .add_dt_criacao(user_data=user_data)
            .add_dt_atualiz()
            .add_cd_cpfcgc(user_data=user_data)
            .add_dt_nasc_fund(user_data=user_data)
            .add_cd_con_dep()
            .add_in_irsdiv(user_data=user_data)
            .add_in_pess_vinc(user_data=user_data)
            .add_nm_cliente(user_data=user_data)
            .add_tp_cliente(user_data=user_data)
            .add_tp_pessoa(user_data=user_data)
            .add_tp_investidor(user_data=user_data)
            .add_in_situac_cliger()
            .add_cd_ativ(user_data=user_data)
            .add_cd_cosif(user_data=user_data)
            .add_cd_cosif_ci(user_data=user_data)
            .add_cd_est_civil(user_data=user_data)
            .add_cd_nacion(user_data=user_data)
            .add_cd_tipo_doc(user_data=user_data)
            .add_id_sexo(user_data=user_data)
            .add_nm_e_mail(user_data=user_data)
            .add_nm_loc_nasc(user_data=user_data)
            .add_nm_mae(user_data=user_data)
            .add_sg_estado_nasc(user_data=user_data)
            .add_sg_pais(user_data=user_data)
            .add_cd_cep(user_data=user_data)
            .add_cd_ddd_tel(user_data=user_data)
            .add_in_ende()
            .add_nm_bairro(user_data=user_data)
            .add_nm_cidade(user_data=user_data)
            .add_nm_logradouro(user_data=user_data)
            .add_nr_predio(user_data=user_data)
            .add_nr_telefone(user_data=user_data)
            .add_sg_estado(user_data=user_data)
            .add_sg_pais_ende1(user_data=user_data)
            .add_cd_ddd_celular1(user_data=user_data)
            .add_nr_celular1(user_data=user_data)
            .add_cd_origem()
            .add_dv_cliente(sinacor_user_control_data=sinacor_user_control_data)
            .add_in_cart_prop()
            .add_in_situac()
            .add_tp_cliente_bol()
            .add_tp_investidor_bol()
            .add_ind_pcta()
            .add_ind_end_vinc_con()
            .add_ind_end_crsp()
            .add_ind_env_email_bvmf()
            .add_tp_cliente_bmf()
            .add_ind_oprc_td()
            .add_ind_oprc_agnt_td()
            .add_cod_cidade_nasc(user_data=user_data)
            .add_sigl_pais_resid(user_data=user_data)
            .add_num_seq_muni_end1(user_data=user_data)
            .add_cod_tipo_colt()
            .add_cod_cep_estr1()
            .add_uf_estr1()
            .add_num_class_risc_cmtt()
            .add_desc_risc_cmtt()
            .add_num_us_person(user_data=user_data)
            .add_val_cfin(user_data=user_data)
            .add_data_cfin(user_data=user_data)
        )
        return builder

    @staticmethod
    def _is_employed_and_not_married_person(
        user_data: dict, sinacor_user_control_data: Optional[tuple]
    ) -> ClientRegisterBuilder:
        builder = ClientRegisterBuilder()
        (
            builder.add_tp_registro(sinacor_user_id=sinacor_user_control_data)
            .add_cd_cliente(sinacor_user_control_data=sinacor_user_control_data)
            .add_cd_org_emit(user_data=user_data)
            .add_dt_doc_ident(user_data=user_data)
            .add_nr_rg(user_data=user_data)
            .add_sg_estado_emiss_rg(user_data=user_data)
            .add_dt_emiss_rg(user_data=user_data)
            .add_cd_org_emit_rg(user_data=user_data)
            .add_cd_doc_ident(user_data=user_data)
            .add_in_rec_divi()
            .add_in_emite_nota()
            .add_pc_corcor_prin()
            .add_in_emite_nota_cs()
            .add_pc_corcor_prin_cs()
            .add_val_lim_neg_td()
            .add_val_taxa_agnt_td()
            .add_txt_email_td(user_data=user_data)
            .add_dt_criacao(user_data=user_data)
            .add_dt_atualiz()
            .add_cd_cpfcgc(user_data=user_data)
            .add_dt_nasc_fund(user_data=user_data)
            .add_cd_con_dep()
            .add_in_irsdiv(user_data=user_data)
            .add_in_pess_vinc(user_data=user_data)
            .add_nm_cliente(user_data=user_data)
            .add_tp_cliente(user_data=user_data)
            .add_tp_pessoa(user_data=user_data)
            .add_tp_investidor(user_data=user_data)
            .add_in_situac_cliger()
            .add_cd_ativ(user_data=user_data)
            .add_cd_cosif(user_data=user_data)
            .add_cd_cosif_ci(user_data=user_data)
            .add_cd_est_civil(user_data=user_data)
            .add_cd_nacion(user_data=user_data)
            .add_cd_tipo_doc(user_data=user_data)
            .add_id_sexo(user_data=user_data)
            .add_nm_e_mail(user_data=user_data)
            .add_nm_loc_nasc(user_data=user_data)
            .add_nm_mae(user_data=user_data)
            .add_sg_estado_nasc(user_data=user_data)
            .add_sg_pais(user_data=user_data)
            .add_cd_cep(user_data=user_data)
            .add_cd_ddd_tel(user_data=user_data)
            .add_in_ende()
            .add_nm_bairro(user_data=user_data)
            .add_nm_cidade(user_data=user_data)
            .add_nm_logradouro(user_data=user_data)
            .add_nr_predio(user_data=user_data)
            .add_nr_telefone(user_data=user_data)
            .add_sg_estado(user_data=user_data)
            .add_sg_pais_ende1(user_data=user_data)
            .add_cd_ddd_celular1(user_data=user_data)
            .add_nr_celular1(user_data=user_data)
            .add_cd_origem()
            .add_dv_cliente(sinacor_user_control_data=sinacor_user_control_data)
            .add_in_cart_prop()
            .add_in_situac()
            .add_tp_cliente_bol()
            .add_tp_investidor_bol()
            .add_ind_pcta()
            .add_ind_end_vinc_con()
            .add_ind_end_crsp()
            .add_ind_env_email_bvmf()
            .add_tp_cliente_bmf()
            .add_ind_oprc_td()
            .add_ind_oprc_agnt_td()
            .add_cod_cidade_nasc(user_data=user_data)
            .add_sigl_pais_resid(user_data=user_data)
            .add_num_seq_muni_end1(user_data=user_data)
            .add_cod_tipo_colt()
            .add_cod_cep_estr1()
            .add_uf_estr1()
            .add_num_class_risc_cmtt()
            .add_desc_risc_cmtt()
            .add_num_trab_empr(user_data=user_data)
            .add_num_us_person(user_data=user_data)
            .add_val_cfin(user_data=user_data)
            .add_data_cfin(user_data=user_data)
            .add_cd_cnpj_empresa(user_data=user_data)
        )
        return builder

    @staticmethod
    def _is_business_and_not_married_person(
        user_data: dict, sinacor_user_control_data: Optional[tuple]
    ) -> ClientRegisterBuilder:
        builder = ClientRegisterBuilder()
        (
            builder.add_tp_registro(sinacor_user_id=sinacor_user_control_data)
            .add_cd_cliente(sinacor_user_control_data=sinacor_user_control_data)
            .add_cd_org_emit(user_data=user_data)
            .add_dt_doc_ident(user_data=user_data)
            .add_nr_rg(user_data=user_data)
            .add_sg_estado_emiss_rg(user_data=user_data)
            .add_dt_emiss_rg(user_data=user_data)
            .add_cd_org_emit_rg(user_data=user_data)
            .add_cd_doc_ident(user_data=user_data)
            .add_in_rec_divi()
            .add_in_emite_nota()
            .add_pc_corcor_prin()
            .add_in_emite_nota_cs()
            .add_pc_corcor_prin_cs()
            .add_val_lim_neg_td()
            .add_val_taxa_agnt_td()
            .add_txt_email_td(user_data=user_data)
            .add_dt_criacao(user_data=user_data)
            .add_dt_atualiz()
            .add_cd_cpfcgc(user_data=user_data)
            .add_dt_nasc_fund(user_data=user_data)
            .add_cd_con_dep()
            .add_in_irsdiv(user_data=user_data)
            .add_in_pess_vinc(user_data=user_data)
            .add_nm_cliente(user_data=user_data)
            .add_tp_cliente(user_data=user_data)
            .add_tp_pessoa(user_data=user_data)
            .add_tp_investidor(user_data=user_data)
            .add_in_situac_cliger()
            .add_cd_ativ(user_data=user_data)
            .add_cd_cosif(user_data=user_data)
            .add_cd_cosif_ci(user_data=user_data)
            .add_cd_est_civil(user_data=user_data)
            .add_cd_nacion(user_data=user_data)
            .add_cd_tipo_doc(user_data=user_data)
            .add_id_sexo(user_data=user_data)
            .add_nm_e_mail(user_data=user_data)
            .add_nm_loc_nasc(user_data=user_data)
            .add_nm_mae(user_data=user_data)
            .add_sg_estado_nasc(user_data=user_data)
            .add_sg_pais(user_data=user_data)
            .add_cd_cep(user_data=user_data)
            .add_cd_ddd_tel(user_data=user_data)
            .add_in_ende()
            .add_nm_bairro(user_data=user_data)
            .add_nm_cidade(user_data=user_data)
            .add_nm_logradouro(user_data=user_data)
            .add_nr_predio(user_data=user_data)
            .add_nr_telefone(user_data=user_data)
            .add_sg_estado(user_data=user_data)
            .add_sg_pais_ende1(user_data=user_data)
            .add_cd_ddd_celular1(user_data=user_data)
            .add_nr_celular1(user_data=user_data)
            .add_cd_origem()
            .add_dv_cliente(sinacor_user_control_data=sinacor_user_control_data)
            .add_in_cart_prop()
            .add_in_situac()
            .add_tp_cliente_bol()
            .add_tp_investidor_bol()
            .add_ind_pcta()
            .add_ind_end_vinc_con()
            .add_ind_end_crsp()
            .add_ind_env_email_bvmf()
            .add_tp_cliente_bmf()
            .add_ind_oprc_td()
            .add_ind_oprc_agnt_td()
            .add_cod_cidade_nasc(user_data=user_data)
            .add_sigl_pais_resid(user_data=user_data)
            .add_num_seq_muni_end1(user_data=user_data)
            .add_cod_tipo_colt()
            .add_cod_cep_estr1()
            .add_uf_estr1()
            .add_num_class_risc_cmtt()
            .add_desc_risc_cmtt()
            .add_num_us_person(user_data=user_data)
            .add_val_cfin(user_data=user_data)
            .add_data_cfin(user_data=user_data)
            .add_cd_cnpj_empresa(user_data=user_data)
        )
        return builder

    @staticmethod
    def _is_unemployed_and_married_person(
        user_data: dict, sinacor_user_control_data: Optional[tuple]
    ) -> ClientRegisterBuilder:
        builder = ClientRegisterBuilder()
        (
            builder.add_tp_registro(sinacor_user_id=sinacor_user_control_data)
            .add_cd_cliente(sinacor_user_control_data=sinacor_user_control_data)
            .add_cd_org_emit(user_data=user_data)
            .add_dt_doc_ident(user_data=user_data)
            .add_nr_rg(user_data=user_data)
            .add_sg_estado_emiss_rg(user_data=user_data)
            .add_dt_emiss_rg(user_data=user_data)
            .add_cd_org_emit_rg(user_data=user_data)
            .add_cd_doc_ident(user_data=user_data)
            .add_in_rec_divi()
            .add_in_emite_nota()
            .add_pc_corcor_prin()
            .add_in_emite_nota_cs()
            .add_pc_corcor_prin_cs()
            .add_val_lim_neg_td()
            .add_val_taxa_agnt_td()
            .add_txt_email_td(user_data=user_data)
            .add_dt_criacao(user_data=user_data)
            .add_dt_atualiz()
            .add_cd_cpfcgc(user_data=user_data)
            .add_dt_nasc_fund(user_data=user_data)
            .add_cd_con_dep()
            .add_in_irsdiv(user_data=user_data)
            .add_in_pess_vinc(user_data=user_data)
            .add_nm_cliente(user_data=user_data)
            .add_tp_cliente(user_data=user_data)
            .add_tp_pessoa(user_data=user_data)
            .add_tp_investidor(user_data=user_data)
            .add_in_situac_cliger()
            .add_cd_ativ(user_data=user_data)
            .add_cd_cosif(user_data=user_data)
            .add_cd_cosif_ci(user_data=user_data)
            .add_cd_est_civil(user_data=user_data)
            .add_cd_nacion(user_data=user_data)
            .add_cd_tipo_doc(user_data=user_data)
            .add_id_sexo(user_data=user_data)
            .add_nm_conjuge(user_data=user_data)
            .add_nm_e_mail(user_data=user_data)
            .add_nm_loc_nasc(user_data=user_data)
            .add_nm_mae(user_data=user_data)
            .add_sg_estado_nasc(user_data=user_data)
            .add_sg_pais(user_data=user_data)
            # .add_tp_regcas(valid_user_data=valid_user_data)
            .add_cd_cep(user_data=user_data)
            .add_cd_ddd_tel(user_data=user_data)
            .add_in_ende()
            .add_nm_bairro(user_data=user_data)
            .add_nm_cidade(user_data=user_data)
            .add_nm_logradouro(user_data=user_data)
            .add_nr_predio(user_data=user_data)
            .add_nr_telefone(user_data=user_data)
            .add_sg_estado(user_data=user_data)
            .add_sg_pais_ende1(user_data=user_data)
            .add_cd_ddd_celular1(user_data=user_data)
            .add_nr_celular1(user_data=user_data)
            .add_cd_origem()
            .add_dv_cliente(sinacor_user_control_data=sinacor_user_control_data)
            .add_in_cart_prop()
            .add_in_situac()
            .add_tp_cliente_bol()
            .add_tp_investidor_bol()
            .add_ind_pcta()
            .add_ind_end_vinc_con()
            .add_ind_end_crsp()
            .add_ind_env_email_bvmf()
            .add_tp_cliente_bmf()
            .add_ind_oprc_td()
            .add_ind_oprc_agnt_td()
            .add_cod_cidade_nasc(user_data=user_data)
            .add_sigl_pais_resid(user_data=user_data)
            .add_num_seq_muni_end1(user_data=user_data)
            .add_cod_tipo_colt()
            .add_cod_cep_estr1()
            .add_uf_estr1()
            .add_num_class_risc_cmtt()
            .add_desc_risc_cmtt()
            .add_num_us_person(user_data=user_data)
            .add_val_cfin(user_data=user_data)
            .add_data_cfin(user_data=user_data)
            .add_cd_cpf_conjuge(user_data=user_data)
            # .add_dt_nasc_conjuge(valid_user_data=valid_user_data)
        )
        return builder

    @staticmethod
    def _is_employed_and_married_person(
        user_data: dict, sinacor_user_control_data: Optional[tuple]
    ) -> ClientRegisterBuilder:
        builder = ClientRegisterBuilder()
        (
            builder.add_tp_registro(sinacor_user_id=sinacor_user_control_data)
            .add_cd_cliente(sinacor_user_control_data=sinacor_user_control_data)
            .add_cd_org_emit(user_data=user_data)
            .add_dt_doc_ident(user_data=user_data)
            .add_nr_rg(user_data=user_data)
            .add_sg_estado_emiss_rg(user_data=user_data)
            .add_dt_emiss_rg(user_data=user_data)
            .add_cd_org_emit_rg(user_data=user_data)
            .add_cd_doc_ident(user_data=user_data)
            .add_in_rec_divi()
            .add_in_emite_nota()
            .add_pc_corcor_prin()
            .add_in_emite_nota_cs()
            .add_pc_corcor_prin_cs()
            .add_val_lim_neg_td()
            .add_val_taxa_agnt_td()
            .add_txt_email_td(user_data=user_data)
            .add_dt_criacao(user_data=user_data)
            .add_dt_atualiz()
            .add_cd_cpfcgc(user_data=user_data)
            .add_dt_nasc_fund(user_data=user_data)
            .add_cd_con_dep()
            .add_in_irsdiv(user_data=user_data)
            .add_in_pess_vinc(user_data=user_data)
            .add_nm_cliente(user_data=user_data)
            .add_tp_cliente(user_data=user_data)
            .add_tp_pessoa(user_data=user_data)
            .add_tp_investidor(user_data=user_data)
            .add_in_situac_cliger()
            .add_cd_ativ(user_data=user_data)
            .add_cd_cosif(user_data=user_data)
            .add_cd_cosif_ci(user_data=user_data)
            .add_cd_est_civil(user_data=user_data)
            .add_cd_nacion(user_data=user_data)
            .add_cd_tipo_doc(user_data=user_data)
            .add_id_sexo(user_data=user_data)
            .add_nm_conjuge(user_data=user_data)
            .add_nm_e_mail(user_data=user_data)
            .add_nm_loc_nasc(user_data=user_data)
            .add_nm_mae(user_data=user_data)
            .add_sg_estado_nasc(user_data=user_data)
            .add_sg_pais(user_data=user_data)
            # .add_tp_regcas(valid_user_data=valid_user_data)
            .add_cd_cep(user_data=user_data)
            .add_cd_ddd_tel(user_data=user_data)
            .add_in_ende()
            .add_nm_bairro(user_data=user_data)
            .add_nm_cidade(user_data=user_data)
            .add_nm_logradouro(user_data=user_data)
            .add_nr_predio(user_data=user_data)
            .add_nr_telefone(user_data=user_data)
            .add_sg_estado(user_data=user_data)
            .add_sg_pais_ende1(user_data=user_data)
            .add_cd_ddd_celular1(user_data=user_data)
            .add_nr_celular1(user_data=user_data)
            .add_cd_origem()
            .add_dv_cliente(sinacor_user_control_data=sinacor_user_control_data)
            .add_in_cart_prop()
            .add_in_situac()
            .add_tp_cliente_bol()
            .add_tp_investidor_bol()
            .add_ind_pcta()
            .add_ind_end_vinc_con()
            .add_ind_end_crsp()
            .add_ind_env_email_bvmf()
            .add_tp_cliente_bmf()
            .add_ind_oprc_td()
            .add_ind_oprc_agnt_td()
            .add_cod_cidade_nasc(user_data=user_data)
            .add_sigl_pais_resid(user_data=user_data)
            .add_num_seq_muni_end1(user_data=user_data)
            .add_cod_tipo_colt()
            .add_cod_cep_estr1()
            .add_uf_estr1()
            .add_num_class_risc_cmtt()
            .add_desc_risc_cmtt()
            .add_num_trab_empr(user_data=user_data)
            .add_num_us_person(user_data=user_data)
            .add_val_cfin(user_data=user_data)
            .add_data_cfin(user_data=user_data)
            .add_cd_cpf_conjuge(user_data=user_data)
            # .add_dt_nasc_conjuge(valid_user_data=valid_user_data)
            .add_cd_cnpj_empresa(user_data=user_data)
        )
        return builder

    @staticmethod
    def _is_business_and_married_person(
        user_data: dict, sinacor_user_control_data: Optional[tuple]
    ) -> ClientRegisterBuilder:
        builder = ClientRegisterBuilder()
        (
            builder.add_tp_registro(sinacor_user_id=sinacor_user_control_data)
            .add_cd_cliente(sinacor_user_control_data=sinacor_user_control_data)
            .add_cd_org_emit(user_data=user_data)
            .add_dt_doc_ident(user_data=user_data)
            .add_nr_rg(user_data=user_data)
            .add_sg_estado_emiss_rg(user_data=user_data)
            .add_dt_emiss_rg(user_data=user_data)
            .add_cd_org_emit_rg(user_data=user_data)
            .add_cd_doc_ident(user_data=user_data)
            .add_in_rec_divi()
            .add_in_emite_nota()
            .add_pc_corcor_prin()
            .add_in_emite_nota_cs()
            .add_pc_corcor_prin_cs()
            .add_val_lim_neg_td()
            .add_val_taxa_agnt_td()
            .add_txt_email_td(user_data=user_data)
            .add_dt_criacao(user_data=user_data)
            .add_dt_atualiz()
            .add_cd_cpfcgc(user_data=user_data)
            .add_dt_nasc_fund(user_data=user_data)
            .add_cd_con_dep()
            .add_in_irsdiv(user_data=user_data)
            .add_in_pess_vinc(user_data=user_data)
            .add_nm_cliente(user_data=user_data)
            .add_tp_cliente(user_data=user_data)
            .add_tp_pessoa(user_data=user_data)
            .add_tp_investidor(user_data=user_data)
            .add_in_situac_cliger()
            .add_cd_ativ(user_data=user_data)
            .add_cd_cosif(user_data=user_data)
            .add_cd_cosif_ci(user_data=user_data)
            .add_cd_est_civil(user_data=user_data)
            .add_cd_nacion(user_data=user_data)
            .add_cd_tipo_doc(user_data=user_data)
            .add_id_sexo(user_data=user_data)
            .add_nm_conjuge(user_data=user_data)
            .add_nm_e_mail(user_data=user_data)
            .add_nm_loc_nasc(user_data=user_data)
            .add_nm_mae(user_data=user_data)
            .add_sg_estado_nasc(user_data=user_data)
            .add_sg_pais(user_data=user_data)
            # .add_tp_regcas(valid_user_data=valid_user_data)
            .add_cd_cep(user_data=user_data)
            .add_cd_ddd_tel(user_data=user_data)
            .add_in_ende()
            .add_nm_bairro(user_data=user_data)
            .add_nm_cidade(user_data=user_data)
            .add_nm_logradouro(user_data=user_data)
            .add_nr_predio(user_data=user_data)
            .add_nr_telefone(user_data=user_data)
            .add_sg_estado(user_data=user_data)
            .add_sg_pais_ende1(user_data=user_data)
            .add_cd_ddd_celular1(user_data=user_data)
            .add_nr_celular1(user_data=user_data)
            .add_cd_origem()
            .add_dv_cliente(sinacor_user_control_data=sinacor_user_control_data)
            .add_in_cart_prop()
            .add_in_situac()
            .add_tp_cliente_bol()
            .add_tp_investidor_bol()
            .add_ind_pcta()
            .add_ind_end_vinc_con()
            .add_ind_end_crsp()
            .add_ind_env_email_bvmf()
            .add_tp_cliente_bmf()
            .add_ind_oprc_td()
            .add_ind_oprc_agnt_td()
            .add_cod_cidade_nasc(user_data=user_data)
            .add_sigl_pais_resid(user_data=user_data)
            .add_num_seq_muni_end1(user_data=user_data)
            .add_cod_tipo_colt()
            .add_cod_cep_estr1()
            .add_uf_estr1()
            .add_num_class_risc_cmtt()
            .add_desc_risc_cmtt()
            .add_num_us_person(user_data=user_data)
            .add_val_cfin(user_data=user_data)
            .add_data_cfin(user_data=user_data)
            .add_cd_cpf_conjuge(user_data=user_data)
            .add_cd_cnpj_empresa(user_data=user_data)
            # .add_dt_nasc_conjuge(valid_user_data=valid_user_data)
        )
        return builder
