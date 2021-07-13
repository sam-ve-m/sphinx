# STANDARD LIBS
from typing import Type

# SPHINX
from src.infrastructures.oracle.infrastructure import OracleInfrastructure
from src.repositories.client_register.builder import ClientRegisterBuilder
from src.repositories.sinacor_types.repository import SinaCorTypesRepository


class ClientRegisterRepository(OracleInfrastructure):

    def cleanup_temp_tables(self):
        client_temp = """TRUNCATE TABLE TSCIMPCLIH;"""
        error_temp = """TRUNCATE TABLE TSCERROH;"""
        self.query(sql=client_temp + error_temp)

    def run_data_validator_in_register_user_tmp_table(self, user_cpf: int):
        result = self.execute(name="PROC_CLIECOH_V2_LIONX", values=[user_cpf])

    def validate_errors_on_temp_tables(self):
        sql = """
            SELECT count(*) 
            FROM TSCERROH E
            JOIN TSCIMCPLI I on E.CD_CPFCGC = I.CD_CPFCGC
            WHERE I.TP_REGISTRO = 'P';
        """
        result = self.query(sql=sql)
        return len(result) == 0

    def register_validated_users(self):
        # TODO: Validate this values
        values = ["CD_EMPRESA", "CD_USUARIO", "TP_OCORRENCIA", "CD_CLIENTE_PADRAO"]
        self.execute(name="PROC_IMPCLIH_V2", values=values)

    def get_builder(self, data: dict, sinacor_types_repository=SinaCorTypesRepository()):
        activity = data['occupation']['activity']
        is_married = data['marital']['status'] == 'married'
        is_business_person = sinacor_types_repository.is_business_person(value=activity)
        is_not_employed_or_business_person = sinacor_types_repository.is_others(value=activity)

        if is_married:
            if is_not_employed_or_business_person:
                self.is_not_employed_or_business_and_married_person(data=data)
            elif is_business_person:
                self.is_business_and_married_person(data=data)
            else:
                self.is_employed_and_married_person(data=data)
        elif is_not_employed_or_business_person:
            self.is_not_employed_or_business_and_not_married_person(data=data)
        elif is_business_person:
            self.is_business_and_not_married_person(data=data)
        else:
            self.is_employed_and_not_married_person(data=data)


    def is_not_employed_or_business_and_not_married_person(
        self, data: dict
    ) -> ClientRegisterBuilder:
        builder = ClientRegisterBuilder()
        builder.add_tp_registro(value="").add_dt_criacao(value="").add_dt_atualiz(
            value=""
        ).add_cd_cpfcgc(value="").add_dt_nasc_fund(value="").add_cd_con_dep(
            value=""
        ).add_in_irsdiv(
            value=""
        ).add_in_pess_vinc(
            value=""
        ).add_nm_cliente(
            value=""
        ).add_tp_cliente(
            value=""
        ).add_tp_pessoa(
            value=""
        ).add_tp_investidor(
            value=""
        ).add_in_situac_cliger(
            value=""
        ).add_cd_ativ(
            value=""
        ).add_cd_cosif(
            value=""
        ).add_cd_cosif_ci(
            value=""
        ).add_cd_est_civil(
            value=""
        ).add_cd_nacion(
            value=""
        ).add_cd_tipo_doc(
            value=""
        ).add_id_sexo(
            value=""
        ).add_nm_e_mail(
            value=""
        ).add_nm_loc_nasc(
            value=""
        ).add_nm_mae(
            value=""
        ).add_sg_estado_nasc(
            value=""
        ).add_sg_pais(
            value=""
        ).add_cd_cep(
            value=""
        ).add_cd_ddd_tel(
            value=""
        ).add_in_ende(
            value=""
        ).add_nm_bairro(
            value=""
        ).add_nm_cidade(
            value=""
        ).add_nm_logradouro(
            value=""
        ).add_nr_predio(
            value=""
        ).add_nr_telefone(
            value=""
        ).add_sg_estado(
            value=""
        ).add_sg_pais_ende1(
            value=""
        ).add_cd_origem(
            value=""
        ).add_dv_cliente(
            value=""
        ).add_in_cart_prop(
            value=""
        ).add_in_situac(
            value=""
        ).add_tp_cliente_bol(
            value=""
        ).add_tp_investidor_bol(
            value=""
        ).add_ind_pcta(
            value=""
        ).add_ind_end_vinc_con(
            value=""
        ).add_ind_end_crsp(
            value=""
        ).add_ind_env_email_bvmf(
            value=""
        ).add_tp_cliente_bmf(
            value=""
        ).add_ind_oprc_td(
            value=""
        ).add_ind_oprc_agnt_td(
            value=""
        ).add_cod_cidade_nasc(
            value=""
        ).add_sigl_pais_resid(
            value=""
        ).add_num_seq_muni_end1(
            value=""
        ).add_cod_tipo_colt(
            value=""
        ).add_cod_cep_estr1(
            value=""
        ).add_uf_estr1(
            value=""
        ).add_num_class_risc_cmtt(
            value=""
        ).add_desc_risc_cmtt(
            value=""
        ).add_data_ult_atlz(
            value=""
        ).add_num_us_person(
            value=""
        ).add_val_cfin(
            value=""
        ).add_data_cfin(
            value=""
        )
        return builder

    @staticmethod
    def is_employed_and_not_married_person(data: dict) -> ClientRegisterBuilder:
        builder = ClientRegisterBuilder()
        builder.add_tp_registro(value="").add_dt_criacao(value="").add_dt_atualiz(
            value=""
        ).add_cd_cpfcgc(value="").add_dt_nasc_fund(value="").add_cd_con_dep(
            value=""
        ).add_in_irsdiv(
            value=""
        ).add_in_pess_vinc(
            value=""
        ).add_nm_cliente(
            value=""
        ).add_tp_cliente(
            value=""
        ).add_tp_pessoa(
            value=""
        ).add_tp_investidor(
            value=""
        ).add_in_situac_cliger(
            value=""
        ).add_cd_ativ(
            value=""
        ).add_cd_cosif(
            value=""
        ).add_cd_cosif_ci(
            value=""
        ).add_cd_est_civil(
            value=""
        ).add_cd_nacion(
            value=""
        ).add_cd_tipo_doc(
            value=""
        ).add_id_sexo(
            value=""
        ).add_nm_e_mail(
            value=""
        ).add_nm_loc_nasc(
            value=""
        ).add_nm_mae(
            value=""
        ).add_sg_estado_nasc(
            value=""
        ).add_sg_pais(
            value=""
        ).add_cd_cep(
            value=""
        ).add_cd_ddd_tel(
            value=""
        ).add_in_ende(
            value=""
        ).add_nm_bairro(
            value=""
        ).add_nm_cidade(
            value=""
        ).add_nm_logradouro(
            value=""
        ).add_nr_predio(
            value=""
        ).add_nr_telefone(
            value=""
        ).add_sg_estado(
            value=""
        ).add_sg_pais_ende1(
            value=""
        ).add_cd_origem(
            value=""
        ).add_dv_cliente(
            value=""
        ).add_in_cart_prop(
            value=""
        ).add_in_situac(
            value=""
        ).add_tp_cliente_bol(
            value=""
        ).add_tp_investidor_bol(
            value=""
        ).add_ind_pcta(
            value=""
        ).add_ind_end_vinc_con(
            value=""
        ).add_ind_end_crsp(
            value=""
        ).add_ind_env_email_bvmf(
            value=""
        ).add_tp_cliente_bmf(
            value=""
        ).add_ind_oprc_td(
            value=""
        ).add_ind_oprc_agnt_td(
            value=""
        ).add_cod_cidade_nasc(
            value=""
        ).add_sigl_pais_resid(
            value=""
        ).add_num_seq_muni_end1(
            value=""
        ).add_cod_tipo_colt(
            value=""
        ).add_cod_cep_estr1(
            value=""
        ).add_uf_estr1(
            value=""
        ).add_num_class_risc_cmtt(
            value=""
        ).add_desc_risc_cmtt(
            value=""
        ).add_data_ult_atlz(
            value=""
        ).add_num_trab_empr(
            value=""
        ).add_num_us_person(
            value=""
        ).add_val_cfin(
            value=""
        ).add_data_cfin(
            value=""
        ).add_cd_cnpj_empresa(
            value=""
        )
        return builder

    @staticmethod
    def is_business_and_not_married_person(data: dict) -> ClientRegisterBuilder:
        builder = ClientRegisterBuilder()
        builder.add_tp_registro(value="").add_dt_criacao(value="").add_dt_atualiz(
            value=""
        ).add_cd_cpfcgc(value="").add_dt_nasc_fund(value="").add_cd_con_dep(
            value=""
        ).add_in_irsdiv(
            value=""
        ).add_in_pess_vinc(
            value=""
        ).add_nm_cliente(
            value=""
        ).add_tp_cliente(
            value=""
        ).add_tp_pessoa(
            value=""
        ).add_tp_investidor(
            value=""
        ).add_in_situac_cliger(
            value=""
        ).add_cd_ativ(
            value=""
        ).add_cd_cosif(
            value=""
        ).add_cd_cosif_ci(
            value=""
        ).add_cd_est_civil(
            value=""
        ).add_cd_nacion(
            value=""
        ).add_cd_tipo_doc(
            value=""
        ).add_id_sexo(
            value=""
        ).add_nm_e_mail(
            value=""
        ).add_nm_loc_nasc(
            value=""
        ).add_nm_mae(
            value=""
        ).add_sg_estado_nasc(
            value=""
        ).add_sg_pais(
            value=""
        ).add_cd_cep(
            value=""
        ).add_cd_ddd_tel(
            value=""
        ).add_in_ende(
            value=""
        ).add_nm_bairro(
            value=""
        ).add_nm_cidade(
            value=""
        ).add_nm_logradouro(
            value=""
        ).add_nr_predio(
            value=""
        ).add_nr_telefone(
            value=""
        ).add_sg_estado(
            value=""
        ).add_sg_pais_ende1(
            value=""
        ).add_cd_origem(
            value=""
        ).add_dv_cliente(
            value=""
        ).add_in_cart_prop(
            value=""
        ).add_in_situac(
            value=""
        ).add_tp_cliente_bol(
            value=""
        ).add_tp_investidor_bol(
            value=""
        ).add_ind_pcta(
            value=""
        ).add_ind_end_vinc_con(
            value=""
        ).add_ind_end_crsp(
            value=""
        ).add_ind_env_email_bvmf(
            value=""
        ).add_tp_cliente_bmf(
            value=""
        ).add_ind_oprc_td(
            value=""
        ).add_ind_oprc_agnt_td(
            value=""
        ).add_cod_cidade_nasc(
            value=""
        ).add_sigl_pais_resid(
            value=""
        ).add_num_seq_muni_end1(
            value=""
        ).add_cod_tipo_colt(
            value=""
        ).add_cod_cep_estr1(
            value=""
        ).add_uf_estr1(
            value=""
        ).add_num_class_risc_cmtt(
            value=""
        ).add_desc_risc_cmtt(
            value=""
        ).add_data_ult_atlz(
            value=""
        ).add_num_us_person(
            value=""
        ).add_val_cfin(
            value=""
        ).add_data_cfin(
            value=""
        ).add_cd_cnpj_empresa(
            value=""
        )
        return builder

    @staticmethod
    def is_not_employed_or_business_and_married_person(
        data: dict,
    ) -> ClientRegisterBuilder:
        builder = ClientRegisterBuilder()
        builder.add_tp_registro(values="").add_dt_criacao(values="").add_dt_atualiz(
            values=""
        ).add_cd_cpfcgc(values="").add_dt_nasc_fund(values="").add_cd_con_dep(
            values=""
        ).add_in_irsdiv(
            values=""
        ).add_in_pess_vinc(
            values=""
        ).add_nm_cliente(
            values=""
        ).add_tp_cliente(
            values=""
        ).add_tp_pessoa(
            values=""
        ).add_tp_investidor(
            values=""
        ).add_in_situac_cliger(
            values=""
        ).add_cd_ativ(
            values=""
        ).add_cd_cosif(
            values=""
        ).add_cd_cosif_ci(
            values=""
        ).add_cd_est_civil(
            values=""
        ).add_cd_nacion(
            values=""
        ).add_cd_tipo_doc(
            values=""
        ).add_id_sexo(
            values=""
        ).add_nm_conjuge(
            values=""
        ).add_nm_e_mail(
            values=""
        ).add_nm_loc_nasc(
            values=""
        ).add_nm_mae(
            values=""
        ).add_sg_estado_nasc(
            values=""
        ).add_sg_pais(
            values=""
        ).add_tp_regcas(
            values=""
        ).add_cd_cep(
            values=""
        ).add_cd_ddd_tel(
            values=""
        ).add_in_ende(
            values=""
        ).add_nm_bairro(
            values=""
        ).add_nm_cidade(
            values=""
        ).add_nm_logradouro(
            values=""
        ).add_nr_predio(
            values=""
        ).add_nr_telefone(
            values=""
        ).add_sg_estado(
            values=""
        ).add_sg_pais_ende1(
            values=""
        ).add_cd_origem(
            values=""
        ).add_dv_cliente(
            values=""
        ).add_in_cart_prop(
            values=""
        ).add_in_situac(
            values=""
        ).add_tp_cliente_bol(
            values=""
        ).add_tp_investidor_bol(
            values=""
        ).add_ind_pcta(
            values=""
        ).add_ind_end_vinc_con(
            values=""
        ).add_ind_end_crsp(
            values=""
        ).add_ind_env_email_bvmf(
            values=""
        ).add_tp_cliente_bmf(
            values=""
        ).add_ind_oprc_td(
            values=""
        ).add_ind_oprc_agnt_td(
            values=""
        ).add_cod_cidade_nasc(
            values=""
        ).add_sigl_pais_resid(
            values=""
        ).add_num_seq_muni_end1(
            values=""
        ).add_cod_tipo_colt(
            values=""
        ).add_cod_cep_estr1(
            values=""
        ).add_uf_estr1(
            values=""
        ).add_num_class_risc_cmtt(
            values=""
        ).add_desc_risc_cmtt(
            values=""
        ).add_data_ult_atlz(
            values=""
        ).add_num_us_person(
            values=""
        ).add_val_cfin(
            values=""
        ).add_data_cfin(
            values=""
        ).add_cd_cpf_conjuge(
            values=""
        ).add_dt_nasc_conjuge(
            values=""
        )
        return builder

    @staticmethod
    def is_employed_and_married_person(data: dict) -> ClientRegisterBuilder:
        builder = ClientRegisterBuilder()
        builder.add_tp_registro(values="").add_dt_criacao(values="").add_dt_atualiz(
            values=""
        ).add_cd_cpfcgc(values="").add_dt_nasc_fund(values="").add_cd_con_dep(
            values=""
        ).add_in_irsdiv(
            values=""
        ).add_in_pess_vinc(
            values=""
        ).add_nm_cliente(
            values=""
        ).add_tp_cliente(
            values=""
        ).add_tp_pessoa(
            values=""
        ).add_tp_investidor(
            values=""
        ).add_in_situac_cliger(
            values=""
        ).add_cd_ativ(
            values=""
        ).add_cd_cosif(
            values=""
        ).add_cd_cosif_ci(
            values=""
        ).add_cd_est_civil(
            values=""
        ).add_cd_nacion(
            values=""
        ).add_cd_tipo_doc(
            values=""
        ).add_id_sexo(
            values=""
        ).add_nm_conjuge(
            values=""
        ).add_nm_e_mail(
            values=""
        ).add_nm_loc_nasc(
            values=""
        ).add_nm_mae(
            values=""
        ).add_sg_estado_nasc(
            values=""
        ).add_sg_pais(
            values=""
        ).add_tp_regcas(
            values=""
        ).add_cd_cep(
            values=""
        ).add_cd_ddd_tel(
            values=""
        ).add_in_ende(
            values=""
        ).add_nm_bairro(
            values=""
        ).add_nm_cidade(
            values=""
        ).add_nm_logradouro(
            values=""
        ).add_nr_predio(
            values=""
        ).add_nr_telefone(
            values=""
        ).add_sg_estado(
            values=""
        ).add_sg_pais_ende1(
            values=""
        ).add_cd_origem(
            values=""
        ).add_dv_cliente(
            values=""
        ).add_in_cart_prop(
            values=""
        ).add_in_situac(
            values=""
        ).add_tp_cliente_bol(
            values=""
        ).add_tp_investidor_bol(
            values=""
        ).add_ind_pcta(
            values=""
        ).add_ind_end_vinc_con(
            values=""
        ).add_ind_end_crsp(
            values=""
        ).add_ind_env_email_bvmf(
            values=""
        ).add_tp_cliente_bmf(
            values=""
        ).add_ind_oprc_td(
            values=""
        ).add_ind_oprc_agnt_td(
            values=""
        ).add_cod_cidade_nasc(
            values=""
        ).add_sigl_pais_resid(
            values=""
        ).add_num_seq_muni_end1(
            values=""
        ).add_cod_tipo_colt(
            values=""
        ).add_cod_cep_estr1(
            values=""
        ).add_uf_estr1(
            values=""
        ).add_num_class_risc_cmtt(
            values=""
        ).add_desc_risc_cmtt(
            values=""
        ).add_data_ult_atlz(
            values=""
        ).add_num_trab_empr(
            values=""
        ).add_num_us_person(
            values=""
        ).add_val_cfin(
            values=""
        ).add_data_cfin(
            values=""
        ).add_cd_cpf_conjuge(
            values=""
        ).add_dt_nasc_conjuge(
            values=""
        ).add_cd_cnpj_empresa(
            values=""
        )
        return builder

    @staticmethod
    def is_business_and_married_person(data: dict) -> ClientRegisterBuilder:
        builder = ClientRegisterBuilder()
        builder.add_tp_registro().add_dt_criacao(
            data=data
        ).add_dt_atualiz().add_cd_cpfcgc(
            data=data
        ).add_dt_nasc_fund(
            data=data
        ).add_cd_con_dep().add_in_irsdiv(
            data=data
        ).add_in_pess_vinc(
            data=data
        ).add_nm_cliente(
            values=""
        ).add_tp_cliente(
            values=""
        ).add_tp_pessoa(
            values=""
        ).add_tp_investidor(
            values=""
        ).add_in_situac_cliger(
            values=""
        ).add_cd_ativ(
            values=""
        ).add_cd_cosif(
            values=""
        ).add_cd_cosif_ci(
            values=""
        ).add_cd_est_civil(
            values=""
        ).add_cd_nacion(
            values=""
        ).add_cd_tipo_doc(
            values=""
        ).add_id_sexo(
            values=""
        ).add_nm_conjuge(
            values=""
        ).add_nm_e_mail(
            values=""
        ).add_nm_loc_nasc(
            values=""
        ).add_nm_mae(
            values=""
        ).add_sg_estado_nasc(
            values=""
        ).add_sg_pais(
            values=""
        ).add_tp_regcas(
            values=""
        ).add_cd_cep(
            values=""
        ).add_cd_ddd_tel(
            values=""
        ).add_in_ende(
            values=""
        ).add_nm_bairro(
            values=""
        ).add_nm_cidade(
            values=""
        ).add_nm_logradouro(
            values=""
        ).add_nr_predio(
            values=""
        ).add_nr_telefone(
            values=""
        ).add_sg_estado(
            values=""
        ).add_sg_pais_ende1(
            values=""
        ).add_cd_origem(
            values=""
        ).add_dv_cliente(
            values=""
        ).add_in_cart_prop(
            values=""
        ).add_in_situac(
            values=""
        ).add_tp_cliente_bol(
            values=""
        ).add_tp_investidor_bol(
            values=""
        ).add_ind_pcta(
            values=""
        ).add_ind_end_vinc_con(
            values=""
        ).add_ind_end_crsp(
            values=""
        ).add_ind_env_email_bvmf(
            values=""
        ).add_tp_cliente_bmf(
            values=""
        ).add_ind_oprc_td(
            values=""
        ).add_ind_oprc_agnt_td(
            values=""
        ).add_cod_cidade_nasc(
            values=""
        ).add_sigl_pais_resid(
            values=""
        ).add_num_seq_muni_end1(
            values=""
        ).add_cod_tipo_colt(
            values=""
        ).add_cod_cep_estr1(
            values=""
        ).add_uf_estr1(
            values=""
        ).add_num_class_risc_cmtt(
            values=""
        ).add_desc_risc_cmtt(
            values=""
        ).add_data_ult_atlz(
            values=""
        ).add_num_us_person(
            values=""
        ).add_val_cfin(
            values=""
        ).add_data_cfin(
            values=""
        ).add_cd_cpf_conjuge(
            values=""
        ).add_dt_nasc_conjuge(
            values=""
        )
        return builder

    def register_user_data_in_register_users_temp_table(
        self, builder: Type[ClientRegisterBuilder]
    ):
        client_register = builder.build()
        fields = client_register.keys()
        sql = f"""
            INSERT INTO TSCIMPCLIH({','.join(fields)}) 
            VALUES(:{',:'.join(fields)});
        """
        self.insert(sql=sql, values=client_register.get_values())
