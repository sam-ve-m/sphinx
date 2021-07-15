# STANDARD LIBS
from typing import Type

# SPHINX
from src.infrastructures.oracle.infrastructure import OracleInfrastructure
from src.repositories.client_register.builder import ClientRegisterBuilder
from src.repositories.sinacor_types.repository import SinaCorTypesRepository


class ClientRegisterRepository(OracleInfrastructure):
    def register_validated_users(self, user_cpf: str):
        # TODO: Validate this values
        values = [1, "CD_USUARIO", "I", 0, user_cpf]
        self.execute(name="PROC_IMPCLIH_V2", values=values)

    def cleanup_temp_tables(self, user_cpf: str):
        client_temp = "DELETE FROM TSCIMPCLIH WHERE CD_CPFCGC = :cpf"
        self.delete(sql=client_temp, values={"cpf": user_cpf})
        error_temp = "DELETE FROM TSCERROH WHERE CD_CPFCGC = :cpf"
        self.delete(sql=error_temp, values={"cpf": user_cpf})

    def validate_user_data_erros(self, user_cpf: int) -> bool:
        self._run_data_validator_in_register_user_tmp_table(user_cpf=user_cpf)
        return self._validate_errors_on_temp_tables(user_cpf=user_cpf)

    def _validate_errors_on_temp_tables(self, user_cpf: int) -> bool:
        sql = f"""
            SELECT 1 
            FROM TSCERROH
            WHERE CD_CPFCGC = {user_cpf}
        """
        result = self.query(sql=sql)
        return len(result) >= 0

    def _run_data_validator_in_register_user_tmp_table(self, user_cpf: int) -> int:
        self.execute(sql="call PROC_CLIECOH_V2_LIONX.EXECCONH(:s, :cpf)", values={'s': "S", 'cpf': str(user_cpf)})

    def register_user_data_in_register_users_temp_table(
        self, builder: Type[ClientRegisterBuilder]
    ):
        client_register = builder.build()
        fields = client_register.keys()
        sql = f"""INSERT INTO TSCIMPCLIH({','.join(fields)}) VALUES(:{',:'.join(fields)})"""
        self.insert(sql=sql, values=client_register)

    def get_builder(
        self, user_data: dict, sinacor_types_repository=SinaCorTypesRepository()
    ) -> Type[ClientRegisterBuilder]:
        activity = user_data["occupation"]["activity"]
        is_married = user_data["marital"]["status"] == "married"
        is_business_person = sinacor_types_repository.is_business_person(value=activity)
        is_not_employed_or_business_person = sinacor_types_repository.is_others(
            value=activity
        )

        callback_key = (
            is_married,
            is_not_employed_or_business_person,
            is_business_person,
        )

        callbacks = {
            (
                True,
                True,
                False,
            ): ClientRegisterRepository._is_not_employed_or_business_and_married_person,
            (
                True,
                False,
                True,
            ): ClientRegisterRepository._is_business_and_married_person,
            (
                True,
                False,
                False,
            ): ClientRegisterRepository._is_employed_and_married_person,
            (
                False,
                True,
                False,
            ): ClientRegisterRepository._is_not_employed_or_business_and_not_married_person,
            (
                False,
                False,
                True,
            ): ClientRegisterRepository._is_business_and_not_married_person,
            (
                False,
                False,
                False,
            ): ClientRegisterRepository._is_employed_and_not_married_person,
        }
        if callback := callbacks.get(callback_key):
            return callback(user_data=user_data)

    @staticmethod
    def _is_not_employed_or_business_and_not_married_person(
        user_data: dict,
    ) -> ClientRegisterBuilder:
        builder = ClientRegisterBuilder()
        (
            builder.add_tp_registro()
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
            .add_dv_cliente()
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
            .add_data_ult_atlz()
            .add_num_us_person()
            .add_val_cfin()
            .add_data_cfin()
        )
        return builder

    @staticmethod
    def _is_employed_and_not_married_person(user_data: dict) -> ClientRegisterBuilder:
        builder = ClientRegisterBuilder()
        (
            builder.add_tp_registro()
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
            .add_dv_cliente()
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
            .add_data_ult_atlz()
            .add_num_trab_empr(user_data=user_data)
            .add_num_us_person(user_data=user_data)
            .add_val_cfin(user_data=user_data)
            .add_data_cfin(user_data=user_data)
            .add_cd_cnpj_empresa(user_data=user_data)
        )
        return builder

    @staticmethod
    def _is_business_and_not_married_person(user_data: dict) -> ClientRegisterBuilder:
        builder = ClientRegisterBuilder()
        (
            builder.add_tp_registro()
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
            .add_dv_cliente()
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
            .add_data_ult_atlz()
            .add_num_us_person(user_data=user_data)
            .add_val_cfin(user_data=user_data)
            .add_data_cfin(user_data=user_data)
            .add_cd_cnpj_empresa(user_data=user_data)
        )
        return builder

    @staticmethod
    def _is_not_employed_or_business_and_married_person(
        user_data: dict,
    ) -> ClientRegisterBuilder:
        builder = ClientRegisterBuilder()
        (
            builder.add_tp_registro()
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
            .add_tp_regcas(user_data=user_data)
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
            .add_dv_cliente()
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
            .add_data_ult_atlz()
            .add_num_us_person(user_data=user_data)
            .add_val_cfin(user_data=user_data)
            .add_data_cfin(user_data=user_data)
            .add_cd_cpf_conjuge(user_data=user_data)
            .add_dt_nasc_conjuge(user_data=user_data)
        )
        return builder

    @staticmethod
    def _is_employed_and_married_person(user_data: dict) -> ClientRegisterBuilder:
        builder = ClientRegisterBuilder()
        (
            builder.add_tp_registro()
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
            .add_tp_regcas(user_data=user_data)
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
            .add_dv_cliente()
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
            .add_data_ult_atlz()
            .add_num_trab_empr(user_data=user_data)
            .add_num_us_person(user_data=user_data)
            .add_val_cfin(user_data=user_data)
            .add_data_cfin(user_data=user_data)
            .add_cd_cpf_conjuge(user_data=user_data)
            .add_dt_nasc_conjuge(user_data=user_data)
            .add_cd_cnpj_empresa(user_data=user_data)
        )
        return builder

    @staticmethod
    def _is_business_and_married_person(user_data: dict) -> ClientRegisterBuilder:
        builder = ClientRegisterBuilder()
        (
            builder.add_tp_registro()
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
            .add_tp_regcas(user_data=user_data)
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
            .add_dv_cliente()
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
            .add_data_ult_atlz()
            .add_num_us_person(user_data=user_data)
            .add_val_cfin(user_data=user_data)
            .add_data_cfin(user_data=user_data)
            .add_cd_cpf_conjuge(user_data=user_data)
            .add_dt_nasc_conjuge(user_data=user_data)
        )
        return builder
