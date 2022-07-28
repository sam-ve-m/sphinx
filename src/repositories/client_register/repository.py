# STANDARD LIBS
from etria_logger import Gladsheim
from typing import Optional
from datetime import datetime

# SPHINX
from src.exceptions.exceptions import InternalServerError
from src.repositories.base_repository.oracle.base import OracleBaseRepository
from src.services.builders.client_register.br.builder import ClientRegisterBuilderBr
from src.repositories.sinacor_types.repository import SinacorTypesRepository
from src.domain.validators.marital_status_sinacor import (
    MaritalStatusSinacor,
)
from src.infrastructures.env_config import config


class ClientRegisterRepository(OracleBaseRepository):
    @classmethod
    async def register_validated_users(cls, user_cpf: str):
        values = {
            "cd_empresa": config("COMPANY_OPERATION_CODE"),
            "cd_usuario": "1",
            "tp_ocorrencia": "I",
            "cd_cliente_padrao": "1",
            "cpf": str(user_cpf),
        }
        await cls.execute(
            sql="call CORRWIN.PROC_IMPCLIH_V2_LIONX.EXECIMPH(:cd_empresa, :cd_usuario, :tp_ocorrencia, :cd_cliente_padrao, :cpf)",
            values=values,
        )

    @classmethod
    async def register_users_register_update(cls, user_cpf: str, birth_date: datetime):
        values = {
            "birth_date": birth_date,
            "cpf": str(user_cpf),
        }
        await cls.execute(
            sql="""
                MERGE INTO CORRWIN.tscdocs USING dual ON (cd_cpfcgc=:cpf)
                WHEN NOT MATCHED THEN INSERT (
                    cd_cpfcgc, dt_nasc_fund, cd_con_dep, dt_validade, in_fich_cad, in_cpfcgc, in_doc_ident, in_comp_res, in_procur, in_contr_bolsa, in_contr_bmf, in_contr_social, in_contr_opc, in_contr_ter, dt_val_cgc, in_ata_contrat, dt_val_procur, dt_val_mandir, in_ficha_bmf, in_cgc, in_rg, in_proposta, in_aut_oper, in_doc_adm, in_autentic, in_contr_internet, in_situac_financ, in_bal_patrimonial, in_regulamento, dt_val_rg, in_contr_tst, in_contr_btc, dt_contr_bolsa, dt_contr_bmf, dt_fich_cad, dt_fich_bmf, in_web_trading, dt_bal_patrimonial, in_conta_margem, dt_conta_margem, tm_stamp, tp_situac
                ) VALUES (
                    :cpf, :birth_date, (SELECT CD_CON_DEP from CORRWIN.tsccliger where CD_CPFCGC = :cpf fetch first 1 row only), add_months(SYSDATE, 24), 'S', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', NULL, 'N', NULL, NULL, 'S', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', NULL, 'N', 'N', NULL, NULL, SYSDATE, SYSDATE, 'N', NULL, 'N', NULL, SYSDATE, NULL
                )
            """,
            values=values,
        )

    @classmethod
    async def cleanup_temp_tables(cls, user_cpf: str):
        client_temp = "DELETE FROM CORRWIN.TSCIMPCLIH WHERE CD_CPFCGC = :cpf"
        await cls.execute(sql=client_temp, values={"cpf": str(user_cpf)})
        error_temp = "DELETE FROM CORRWIN.TSCERROH WHERE CD_CPFCGC = :cpf"
        await cls.execute(sql=error_temp, values={"cpf": str(user_cpf)})

    @classmethod
    async def allow_cash_transfer(cls, client_code: int):
        insert_query = f"""
            INSERT INTO CORRWIN.TSCCLISIS(
                CD_CLIENTE,
                CD_SISTEMA,
                CD_CLISIS,
                IND_EXPT_BANC_BMF
            ) VALUES(:client_code, 'OUT', :client_code,'N')
        """
        await cls.execute(sql=insert_query, values={"client_code": client_code})

    @classmethod
    async def link_client_with_graphic_account(cls, cpf: int):
        insert_query = """
            INSERT INTO CORRWIN.TTSRELCTACLI (CD_CPFCGC, CD_CLIENTE_CC, CD_CLIENTE_CI, CD_CLIENTE_CP)
            (
                SELECT
                    CD_CPFCGC,
                    MAX(NVL((SELECT MIN(CD_CLIENTE) FROM CORRWIN.TSCCLICC WHERE CD_CPFCGC = CC.CD_CPFCGC AND IN_CONTA_INV = 'N' AND IN_SITUAC='A'), 0)) CLIENTE_CC,
                    MAX( NVL(( SELECT MIN(CD_CLIENTE) FROM CORRWIN.TSCCLICC WHERE  CD_CPFCGC = CC.CD_CPFCGC AND IN_CONTA_INV = 'S'), 0)) CLIENTE_CI,
                    MAX(NVL((SELECT MIN(CD_CLIENTE) FROM CORRWIN.TSCCLICC WHERE CD_CPFCGC = CC.CD_CPFCGC AND IN_CONTA_INV = 'N'AND IN_SITUAC = 'A'), 0)) CLIENTE_CP
                FROM CORRWIN.TSCCLICC CC
                WHERE
                NOT EXISTS (SELECT 0 FROM CORRWIN.TTSRELCTACLI C WHERE C.CD_CPFCGC = CC.CD_CPFCGC)
                AND IN_CONTA_INV = 'N'
                AND IN_SITUAC = 'A'
                AND CC.CD_CPFCGC = :cpf
                GROUP BY CD_CPFCGC
            )
        """
        await cls.execute(sql=insert_query, values={"cpf": cpf})

    @classmethod
    async def client_has_already_link_with_graphic_account(cls, cpf: int):
        select_query = f"""
            SELECT 1 FROM CORRWIN.TTSRELCTACLI
            WHERE CD_CPFCGC = {cpf}
        """
        result = await cls.query(sql=select_query)
        return bool(result)

    @classmethod
    async def client_has_already_allowed_cash_transfer(cls, client_code: int):
        select_query = f"""
            SELECT 1 FROM CORRWIN.TSCCLISIS
            WHERE CD_CLIENTE = {client_code}
            AND CD_SISTEMA = 'OUT'
        """
        result = await cls.query(sql=select_query)
        return bool(result)

    @classmethod
    async def validate_user_data_errors(cls, user_cpf: int) -> bool:
        await cls._run_data_validator_in_register_user_tmp_table(user_cpf=user_cpf)
        return await cls._validate_errors_on_temp_tables(user_cpf=user_cpf)

    @classmethod
    async def _validate_errors_on_temp_tables(cls, user_cpf: int) -> bool:
        sql = f"""
            SELECT 1 
            FROM CORRWIN.TSCERROH
            WHERE CD_CPFCGC = {user_cpf}
        """
        result = await cls.query(sql=sql)
        return len(result) > 0

    @classmethod
    async def _run_data_validator_in_register_user_tmp_table(cls, user_cpf: int):
        await cls.execute(
            sql="call CORRWIN.PROC_CLIECOH_V2_LIONX.EXECCONH(:s, :cpf)",
            values={"s": "S", "cpf": str(user_cpf)},
        )

    @classmethod
    async def register_user_data_in_register_users_temp_table(
        cls, builder: ClientRegisterBuilderBr
    ):
        client_register = builder.build()
        fields = client_register.keys()
        sql = f"INSERT INTO CORRWIN.TSCIMPCLIH({','.join(fields)}) VALUES(:{',:'.join(fields)})"
        await cls.execute(sql=sql, values=client_register)

    @classmethod
    async def get_user_control_data_if_user_already_exists(cls, user_cpf: int):
        verify_user_data_sql = (
            f"SELECT 1 FROM CORRWIN.TSCCLIGER WHERE CD_CPFCGC = {user_cpf}"
        )
        verify_user_bovespa_account = (
            f"SELECT 1 FROM CORRWIN.TSCCLIBOL WHERE CD_CPFCGC = {user_cpf}"
        )
        verify_user_bmf_account = (
            f"SELECT 1 FROM CORRWIN.TSCCLIBMF WHERE CD_CPFCGC = {user_cpf}"
        )
        verify_user_account = (
            f"SELECT 1 FROM CORRWIN.TSCCLICOMP WHERE CD_CPFCGC = {user_cpf}"
        )
        verify_user_treasury = (
            f"SELECT 1 FROM CORRWIN.TSCCLITSD WHERE CD_CPFCGC = {user_cpf}"
        )
        all_validation_query = [
            verify_user_data_sql,
            verify_user_bovespa_account,
            verify_user_bmf_account,
            verify_user_account,
            verify_user_treasury,
        ]
        result = await cls.query(sql=" union ".join(all_validation_query))
        if result and len(result) > 0:
            result = await cls.query(
                sql=f"SELECT CD_CLIENTE, DV_CLIENTE FROM CORRWIN.TSCCLIBOL WHERE CD_CPFCGC = {user_cpf}"
            )
            return result[0]
        return None

    @classmethod
    async def get_sincad_status(cls, user_cpf: int):
        sql = (
            f"SELECT COD_SITU_ENVIO FROM CORRWIN.TSCCLIBOL WHERE CD_CPFCGC = {user_cpf}"
        )
        result = await cls.query(sql=sql)
        if result and len(result) > 0:
            return result[0]
        return None

    @classmethod
    async def get_sinacor_status(cls, user_cpf: str, user_bmf_account: str):
        sql = f"SELECT IN_SITUAC FROM CORRWIN.TSCCLIBOL WHERE CD_CPFCGC = {user_cpf} AND CD_CLIENTE = '{user_bmf_account}'"
        result = await cls.query(sql=sql)
        if result and len(result) > 0:
            return result[0]
        return None

    @staticmethod
    def is_married(user_data: dict):
        is_married = user_data["marital"]["status"] in [
            MaritalStatusSinacor.MARRIED_TO_BRAZILIAN.value,
            MaritalStatusSinacor.MARRIED_TO_A_NATURALIZED_BRAZILIAN.value,
            MaritalStatusSinacor.MARRIED_TO_A_FOREIGN.value,
            MaritalStatusSinacor.STABLE_UNION.value,
        ]
        return is_married

    @classmethod
    async def get_builder(
        cls,
        user_data: dict,
        sinacor_user_control_data: Optional[tuple],
        sinacor_types_repository=SinacorTypesRepository(),
    ) -> ClientRegisterBuilderBr:
        occupation = user_data["occupation"]
        activity = occupation["activity"]
        company = occupation.get("company", {})
        cnpj = company.get("cnpj")

        is_married = cls.is_married(user_data=user_data)
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
            Gladsheim.error(message=message)
            raise InternalServerError("internal_error")

        return callback(
            user_data=user_data, sinacor_user_control_data=sinacor_user_control_data
        )

    @classmethod
    async def client_is_allowed_to_cancel_registration(
        cls, user_cpf: int, bmf_account: int
    ):
        is_client_blocked = await cls._is_client_blocked(user_cpf)
        client_has_value_blocked = await cls._client_has_value_blocked(bmf_account)
        client_has_receivables = await cls._client_has_receivables(bmf_account)
        client_has_options_blocked = await cls._client_has_options_blocked(bmf_account)
        client_has_options_receivables = await cls._client_has_options_receivables(
            bmf_account
        )
        client_has_values_in_bank_account = (
            await cls._client_has_values_in_bank_account(bmf_account)
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

    @classmethod
    async def _is_client_blocked(cls, user_cpf: int):
        result = await cls.query(
            sql=f"SELECT 1 from CORRWIN.TSCCLIGER WHERE CD_CPFCGC = {user_cpf} and IN_SITUAC = 'BL'"
        )
        return len(result) > 0

    @classmethod
    async def _client_has_value_blocked(cls, bmf_account: int):
        result = await cls.query(
            sql=f"SELECT 1 from CORRWIN.TCCSALDO_BLOQ WHERE COD_CLI = {bmf_account} and VAL_BLOQ > 0"
        )
        return len(result) > 0

    @classmethod
    async def _client_has_receivables(cls, bmf_account: int):
        result = await cls.query(
            sql=f"SELECT 1 from CORRWIN.TCCMOVTO WHERE CD_CLIENTE = {bmf_account} and DT_LIQUIDACAO >= SYSDATE"
        )
        return len(result) > 0

    @classmethod
    async def _client_has_options_blocked(cls, bmf_account: int):
        result = await cls.query(
            sql=f"SELECT 1 from CORRWIN.VCFPOSICAO WHERE COD_CLI = {bmf_account} and QTDE_BLQD is not null and QTDE_BLQD > 0"
        )
        return len(result) > 0

    @classmethod
    async def _client_has_options_receivables(cls, bmf_account: int):
        result = await cls.query(
            sql=f"SELECT 1 from CORRWIN.VCFPOSICAO where COD_CLI = {bmf_account} and tipo_merc in ('OPC','OPV') and data_venc >= SYSDATE"
        )
        return len(result) > 0

    @classmethod
    async def _client_has_values_in_bank_account(cls, bmf_account: int):
        result = await cls.query(
            sql=f"select 1 from CORRWIN.tccsaldo WHERE CD_CLIENTE = {bmf_account} and VL_TOTAL > 0"
        )
        return len(result) > 0

    @staticmethod
    def _is_unemployed_and_not_married_person(
        user_data: dict, sinacor_user_control_data: Optional[tuple]
    ) -> ClientRegisterBuilderBr:
        builder = ClientRegisterBuilderBr()
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
            .add_dt_criacao()
            .add_dt_atualiz()
            .add_cd_cpfcgc(user_data=user_data)
            .add_dt_nasc_fund(user_data=user_data)
            .add_cd_con_dep()
            .add_in_irsdiv()
            .add_in_pess_vinc()
            .add_nm_cliente(user_data=user_data)
            .add_tp_cliente()
            .add_tp_pessoa()
            .add_tp_investidor()
            .add_in_situac_cliger()
            .add_cd_ativ(user_data=user_data)
            .add_cd_cosif()
            .add_cd_cosif_ci()
            .add_cd_est_civil(user_data=user_data)
            .add_cd_nacion(user_data=user_data)
            .add_cd_tipo_doc(user_data=user_data)
            .add_id_sexo(user_data=user_data)
            .add_nm_e_mail(user_data=user_data)
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
    ) -> ClientRegisterBuilderBr:
        builder = ClientRegisterBuilderBr()
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
            .add_dt_criacao()
            .add_dt_atualiz()
            .add_cd_cpfcgc(user_data=user_data)
            .add_dt_nasc_fund(user_data=user_data)
            .add_cd_con_dep()
            .add_in_irsdiv()
            .add_in_pess_vinc()
            .add_nm_cliente(user_data=user_data)
            .add_tp_cliente()
            .add_tp_pessoa()
            .add_tp_investidor()
            .add_in_situac_cliger()
            .add_cd_ativ(user_data=user_data)
            .add_cd_cosif()
            .add_cd_cosif_ci()
            .add_cd_est_civil(user_data=user_data)
            .add_cd_nacion(user_data=user_data)
            .add_cd_tipo_doc(user_data=user_data)
            .add_id_sexo(user_data=user_data)
            .add_nm_e_mail(user_data=user_data)
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
            .add_nm_empresa(user_data=user_data)
        )
        return builder

    @staticmethod
    def _is_business_and_not_married_person(
        user_data: dict, sinacor_user_control_data: Optional[tuple]
    ) -> ClientRegisterBuilderBr:
        builder = ClientRegisterBuilderBr()
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
            .add_dt_criacao()
            .add_dt_atualiz()
            .add_cd_cpfcgc(user_data=user_data)
            .add_dt_nasc_fund(user_data=user_data)
            .add_cd_con_dep()
            .add_in_irsdiv()
            .add_in_pess_vinc()
            .add_nm_cliente(user_data=user_data)
            .add_tp_cliente()
            .add_tp_pessoa()
            .add_tp_investidor()
            .add_in_situac_cliger()
            .add_cd_ativ(user_data=user_data)
            .add_cd_cosif()
            .add_cd_cosif_ci()
            .add_cd_est_civil(user_data=user_data)
            .add_cd_nacion(user_data=user_data)
            .add_cd_tipo_doc(user_data=user_data)
            .add_id_sexo(user_data=user_data)
            .add_nm_e_mail(user_data=user_data)
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
            .add_nm_empresa(user_data=user_data)
        )
        return builder

    @staticmethod
    def _is_unemployed_and_married_person(
        user_data: dict, sinacor_user_control_data: Optional[tuple]
    ) -> ClientRegisterBuilderBr:
        builder = ClientRegisterBuilderBr()
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
            .add_dt_criacao()
            .add_dt_atualiz()
            .add_cd_cpfcgc(user_data=user_data)
            .add_dt_nasc_fund(user_data=user_data)
            .add_cd_con_dep()
            .add_in_irsdiv()
            .add_in_pess_vinc()
            .add_nm_cliente(user_data=user_data)
            .add_tp_cliente()
            .add_tp_pessoa()
            .add_tp_investidor()
            .add_in_situac_cliger()
            .add_cd_ativ(user_data=user_data)
            .add_cd_cosif()
            .add_cd_cosif_ci()
            .add_cd_est_civil(user_data=user_data)
            .add_cd_nacion(user_data=user_data)
            .add_cd_tipo_doc(user_data=user_data)
            .add_id_sexo(user_data=user_data)
            .add_nm_conjuge(user_data=user_data)
            .add_nm_e_mail(user_data=user_data)
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
    ) -> ClientRegisterBuilderBr:
        builder = ClientRegisterBuilderBr()
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
            .add_dt_criacao()
            .add_dt_atualiz()
            .add_cd_cpfcgc(user_data=user_data)
            .add_dt_nasc_fund(user_data=user_data)
            .add_cd_con_dep()
            .add_in_irsdiv()
            .add_in_pess_vinc()
            .add_nm_cliente(user_data=user_data)
            .add_tp_cliente()
            .add_tp_pessoa()
            .add_tp_investidor()
            .add_in_situac_cliger()
            .add_cd_ativ(user_data=user_data)
            .add_cd_cosif()
            .add_cd_cosif_ci()
            .add_cd_est_civil(user_data=user_data)
            .add_cd_nacion(user_data=user_data)
            .add_cd_tipo_doc(user_data=user_data)
            .add_id_sexo(user_data=user_data)
            .add_nm_conjuge(user_data=user_data)
            .add_nm_e_mail(user_data=user_data)
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
            .add_nm_empresa(user_data=user_data)
        )
        return builder

    @staticmethod
    def _is_business_and_married_person(
        user_data: dict, sinacor_user_control_data: Optional[tuple]
    ) -> ClientRegisterBuilderBr:
        builder = ClientRegisterBuilderBr()
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
            .add_dt_criacao()
            .add_dt_atualiz()
            .add_cd_cpfcgc(user_data=user_data)
            .add_dt_nasc_fund(user_data=user_data)
            .add_cd_con_dep()
            .add_in_irsdiv()
            .add_in_pess_vinc()
            .add_nm_cliente(user_data=user_data)
            .add_tp_cliente()
            .add_tp_pessoa()
            .add_tp_investidor()
            .add_in_situac_cliger()
            .add_cd_ativ(user_data=user_data)
            .add_cd_cosif()
            .add_cd_cosif_ci()
            .add_cd_est_civil(user_data=user_data)
            .add_cd_nacion(user_data=user_data)
            .add_cd_tipo_doc(user_data=user_data)
            .add_id_sexo(user_data=user_data)
            .add_nm_conjuge(user_data=user_data)
            .add_nm_e_mail(user_data=user_data)
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
            .add_nm_empresa(user_data=user_data)
            # .add_dt_nasc_conjuge(valid_user_data=valid_user_data)
        )
        return builder
