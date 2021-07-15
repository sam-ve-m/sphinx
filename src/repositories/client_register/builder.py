class ClientRegisterBuilder:
    def __init__(self):
        self._fields_added = dict()

    def build(self):
        return self._fields_added

    def add_tp_registro(self, value):
        self._fields_added.update({"TP_REGISTRO", value})
        return self

    def add_dt_criacao(self, value):
        self._fields_added.update({"DT_CRIACAO", value})
        return self

    def add_dt_atualiz(self, value):
        self._fields_added.update({"DT_ATUALIZ", value})
        return self

    def add_cd_cpfcgc(self, value):
        self._fields_added.update({"CD_CPFCGC", value})
        return self

    def add_dt_nasc_fund(self, value):
        self._fields_added.update({"DT_NASC_FUND", value})
        return self

    def add_cd_con_dep(self, value):
        self._fields_added.update({"CD_CON_DEP", value})
        return self

    def add_in_irsdiv(self, value):
        self._fields_added.update({"IN_IRSDIV", value})
        return self

    def add_in_pess_vinc(self, value):
        self._fields_added.update({"IN_PESS_VINC", value})
        return self

    def add_nm_cliente(self, value):
        self._fields_added.update({"NM_CLIENTE", value})
        return self

    def add_tp_cliente(self, value):
        self._fields_added.update({"TP_CLIENTE", value})
        return self

    def add_tp_pessoa(self, value):
        self._fields_added.update({"TP_PESSOA", value})
        return self

    def add_tp_investidor(self, value):
        self._fields_added.update({"TP_INVESTIDOR", value})
        return self

    def add_in_situac_cliger(self, value):
        self._fields_added.update({"IN_SITUAC_CLIGER", value})
        return self

    def add_cd_ativ(self, value):
        self._fields_added.update({"CD_ATIV", value})
        return self

    def add_cd_cosif(self, value):
        self._fields_added.update({"CD_COSIF", value})
        return self

    def add_cd_cosif_ci(self, value):
        self._fields_added.update({"CD_COSIF_CI", value})
        return self

    def add_cd_est_civil(self, value):
        self._fields_added.update({"CD_EST_CIVIL", value})
        return self

    def add_cd_nacion(self, value):
        self._fields_added.update({"CD_NACION", value})
        return self

    def add_cd_tipo_doc(self, value):
        self._fields_added.update({"CD_TIPO_DOC", value})
        return self

    def add_id_sexo(self, value):
        self._fields_added.update({"ID_SEXO", value})
        return self

    def add_in_rec_divi(self, value):
        self._fields_added.update({"IN_REC_DIVI", value})
        return self

    def add_nm_conjuge(self, value):
        self._fields_added.update({"NM_CONJUGE", value})
        return self

    def add_nm_e_mail(self, value):
        self._fields_added.update({"NM_E_MAIL", value})
        return self

    def add_nm_loc_nasc(self, value):
        self._fields_added.update({"NM_LOC_NASC", value})
        return self

    def add_nm_mae(self, value):
        self._fields_added.update({"NM_MAE", value})
        return self

    def add_sg_estado_nasc(self, value):
        self._fields_added.update({"SG_ESTADO_NASC", value})
        return self

    def add_sg_pais(self, value):
        self._fields_added.update({"SG_PAIS", value})
        return self

    def add_tp_regcas(self, value):
        self._fields_added.update({"TP_REGCAS", value})
        return self

    def add_cd_cep(self, value):
        self._fields_added.update({"CD_CEP", value})
        return self

    def add_cd_ddd_celular1(self, value):
        self._fields_added.update({"CD_DDD_CELULAR1", value})
        return self

    def add_cd_ddd_tel(self, value):
        self._fields_added.update({"CD_DDD_TEL", value})
        return self

    def add_in_ende(self, value):
        self._fields_added.update({"IN_ENDE", value})
        return self

    def add_nm_bairro(self, value):
        self._fields_added.update({"NM_BAIRRO", value})
        return self

    def add_nr_celular1(self, value):
        self._fields_added.update({"NR_CELULAR1", value})
        return self

    def add_nm_cidade(self, value):
        self._fields_added.update({"NM_CIDADE", value})
        return self

    def add_nm_logradouro(self, value):
        self._fields_added.update({"NM_LOGRADOURO", value})
        return self

    def add_nr_predio(self, value):
        self._fields_added.update({"NR_PREDIO", value})
        return self

    def add_nr_telefone(self, value):
        self._fields_added.update({"NR_TELEFONE", value})
        return self

    def add_sg_estado(self, value):
        self._fields_added.update({"SG_ESTADO", value})
        return self

    def add_sg_pais_ende1(self, value):
        self._fields_added.update({"SG_PAIS_ENDE1", value})
        return self

    def add_cod_finl_end1(self, value):
        self._fields_added.update({"COD_FINL_END1", value})
        return self

    def add_cd_agente(self, value):
        self._fields_added.update({"CD_AGENTE", value})
        return self

    def add_cd_assessor(self, value):
        self._fields_added.update({"CD_ASSESSOR", value})
        return self

    def add_cd_cliente(self, value):
        self._fields_added.update({"CD_CLIENTE", value})
        return self

    def add_cd_origem(self, value):
        self._fields_added.update({"CD_ORIGEM", value})
        return self

    def add_cd_vinculo(self, value):
        self._fields_added.update({"CD_VINCULO", value})
        return self

    def add_dv_cliente(self, value):
        self._fields_added.update({"DV_CLIENTE", value})
        return self

    def add_in_cart_prop(self, value):
        self._fields_added.update({"IN_CART_PROP", value})
        return self

    def add_in_emite_nota(self, value):
        self._fields_added.update({"IN_EMITE_NOTA", value})
        return self

    def add_in_situac(self, value):
        self._fields_added.update({"IN_SITUAC", value})
        return self

    def add_pc_corcor_prin(self, value):
        self._fields_added.update({"PC_CORCOR_PRIN", value})
        return self

    def add_tp_cliente_bol(self, value):
        self._fields_added.update({"TP_CLIENTE_BOL", value})
        return self

    def add_tp_conta(self, value):
        self._fields_added.update({"TP_CONTA", value})
        return self

    def add_tp_investidor_bol(self, value):
        self._fields_added.update({"TP_INVESTIDOR_BOL", value})
        return self

    def add_in_lifo_fifo(self, value):
        self._fields_added.update({"IN_LIFO_FIFO", value})
        return self

    def add_ind_pcta(self, value):
        self._fields_added.update({"IND_PCTA", value})
        return self

    def add_cod_tipo_colt(self, value):
        self._fields_added.update({"COD_TIPO_COLT", value})
        return self

    def add_in_emite_nota_cs(self, value):
        self._fields_added.update({"IN_EMITE_NOTA_CS", value})
        return self

    def add_ind_end_vinc_con(self, value):
        self._fields_added.update({"IND_END_VINC_CON", value})
        return self

    def add_ind_end_crsp(self, value):
        self._fields_added.update({"IND_END_CRSP", value})
        return self

    def add_ind_env_email_bvmf(self, value):
        self._fields_added.update({"IND_ENV_EMAIL_BVMF", value})
        return self

    def add_tp_cliente_bmf(self, value):
        self._fields_added.update({"TP_CLIENTE_BMF", value})
        return self

    def add_ind_oprc_td(self, value):
        self._fields_added.update({"IND_OPRC_TD", value})
        return self

    def add_ind_oprc_agnt_td(self, value):
        self._fields_added.update({"IND_OPRC_AGNT_TD", value})
        return self

    def add_cod_cidade_nasc(self, value):
        self._fields_added.update({"COD_CIDADE_NASC", value})
        return self

    def add_sigl_pais_resid(self, value):
        self._fields_added.update({"SIGL_PAIS_RESID", value})
        return self

    def add_num_seq_muni_end1(self, value):
        self._fields_added.update({"NUM_SEQ_MUNI_END1", value})
        return self

    def add_num_tipo_con(self, value):
        self._fields_added.update({"NUM_TIPO_CON", value})
        return self

    def add_cod_tipo_colt(self, value):
        self._fields_added.update({"COD_TIPO_COLT", value})
        return self

    def add_cod_cep_estr1(self, value):
        self._fields_added.update({"COD_CEP_ESTR1", value})
        return self

    def add_uf_estr1(self, value):
        self._fields_added.update({"UF_ESTR1", value})
        return self

    def add_num_class_risc_cmtt(self, value):
        self._fields_added.update({"NUM_CLASS_RISC_CMTT", value})
        return self

    def add_desc_risc_cmtt(self, value):
        self._fields_added.update({"DESC_RISC_CMTT", value})
        return self

    def add_data_ult_atlz(self, value):
        self._fields_added.update({"DATA_ULT_ATLZ", value})
        return self

    def add_num_trab_empr(self, value):
        self._fields_added.update({"NUM_TRAB_EMPR", value})
        return self

    def add_num_us_person(self, value):
        self._fields_added.update({"NUM_US_PERSON", value})
        return self

    def add_val_cfin(self, value):
        self._fields_added.update({"VAL_CFIN", value})
        return self

    def add_data_cfin(self, value):
        self._fields_added.update({"DATA_CFIN", value})
        return self

    def add_cd_cpf_conjuge(self, value):
        self._fields_added.update({"CD_CPF_CONJUGE", value})
        return self

    def add_dt_nasc_conjuge(self, value):
        self._fields_added.update({"DT_NASC_CONJUGE", value})
        return self

    def add_cd_cnpj_empresa(self, value):
        self._fields_added.update({"CD_CNPJ_EMPRESA", value})
        return self

    def add_cd_capac(self, value):
        self._fields_added.update({"CD_CAPAC", value})
        return self

    def add_cd_codqua(self, value):
        self._fields_added.update({"CD_CODQUA", value})
        return self

    def add_ds_cargo(self, value):
        self._fields_added.update({"DS_CARGO", value})
        return self

    def add_cd_doc_ident(self, value):
        self._fields_added.update({"CD_DOC_IDENT", value})
        return self

    def add_cd_org_emit(self, value):
        self._fields_added.update({"CD_ORG_EMIT", value})
        return self

    def add_dt_doc_ident(self, value):
        self._fields_added.update({"DT_DOC_IDENT", value})
        return self

    def add_nm_empresa(self, value):
        self._fields_added.update({"NM_EMPRESA", value})
        return self

    def add_nm_pai(self, value):
        self._fields_added.update({"NM_PAI", value})
        return self

    def add_sg_estado_emis(self, value):
        self._fields_added.update({"SG_ESTADO_EMIS", value})
        return self

    def add_sg_estado_emiss_rg(self, value):
        self._fields_added.update({"SG_ESTADO_EMISS_RG", value})
        return self

    def add_dt_emiss_rg(self, value):
        self._fields_added.update({"DT_EMISS_RG", value})
        return self

    def add_cd_org_emit_rg(self, value):
        self._fields_added.update({"CD_ORG_EMIT_RG", value})
        return self

    def add_nr_rg(self, value):
        self._fields_added.update({"NR_RG", value})
        return self

    def add_cd_ddd_celular2(self, value):
        self._fields_added.update({"CD_DDD_CELULAR2", value})
        return self

    def add_cd_ddd_fax(self, value):
        self._fields_added.update({"CD_DDD_FAX", value})
        return self

    def add_nr_celular2(self, value):
        self._fields_added.update({"NR_CELULAR2", value})
        return self

    def add_nm_comp_ende(self, value):
        self._fields_added.update({"NM_COMP_ENDE", value})
        return self

    def add_nr_fax(self, value):
        self._fields_added.update({"NR_FAX", value})
        return self

    def add_nm_contato1(self, value):
        self._fields_added.update({"NM_CONTATO1", value})
        return self

    def add_nm_contato2(self, value):
        self._fields_added.update({"NM_CONTATO2", value})
        return self

    def add_nr_ramal(self, value):
        self._fields_added.update({"NR_RAMAL", value})
        return self

    def add_cd_cep2(self, value):
        self._fields_added.update({"CD_CEP2", value})
        return self

    def add_cd_ddd_celular12(self, value):
        self._fields_added.update({"CD_DDD_CELULAR12", value})
        return self

    def add_cd_ddd_celular22(self, value):
        self._fields_added.update({"CD_DDD_CELULAR22", value})
        return self

    def add_cd_ddd_fax12(self, value):
        self._fields_added.update({"CD_DDD_FAX12", value})
        return self

    def add_cd_ddd_fax22(self, value):
        self._fields_added.update({"CD_DDD_FAX22", value})
        return self

    def add_cd_ddd_tel2(self, value):
        self._fields_added.update({"CD_DDD_TEL2", value})
        return self

    def add_in_tipo_ende2(self, value):
        self._fields_added.update({"IN_TIPO_ENDE2", value})
        return self

    def add_nm_bairro2(self, value):
        self._fields_added.update({"NM_BAIRRO2", value})
        return self

    def add_nm_cidade2(self, value):
        self._fields_added.update({"NM_CIDADE2", value})
        return self

    def add_nm_comp_ende2(self, value):
        self._fields_added.update({"NM_COMP_ENDE2", value})
        return self

    def add_nm_logradouro2(self, value):
        self._fields_added.update({"NM_LOGRADOURO2", value})
        return self

    def add_nr_celular12(self, value):
        self._fields_added.update({"NR_CELULAR12", value})
        return self

    def add_nr_celular22(self, value):
        self._fields_added.update({"NR_CELULAR22", value})
        return self

    def add_nr_fax12(self, value):
        self._fields_added.update({"NR_FAX12", value})
        return self

    def add_nr_fax22(self, value):
        self._fields_added.update({"NR_FAX22", value})
        return self

    def add_nm_contato12(self, value):
        self._fields_added.update({"NM_CONTATO12", value})
        return self

    def add_nm_contato22(self, value):
        self._fields_added.update({"NM_CONTATO22", value})
        return self

    def add_nr_predio2(self, value):
        self._fields_added.update({"NR_PREDIO2", value})
        return self

    def add_nr_ramal2(self, value):
        self._fields_added.update({"NR_RAMAL2", value})
        return self

    def add_nr_telefone2(self, value):
        self._fields_added.update({"NR_TELEFONE2", value})
        return self

    def add_sg_estado2(self, value):
        self._fields_added.update({"SG_ESTADO2", value})
        return self

    def add_sg_pais_ende2(self, value):
        self._fields_added.update({"SG_PAIS_ENDE2", value})
        return self

    def add_cod_finl_end2(self, value):
        self._fields_added.update({"COD_FINL_END2", value})
        return self

    def add_cd_admin_cvm(self, value):
        self._fields_added.update({"CD_ADMIN_CVM", value})
        return self

    def add_cd_agencia(self, value):
        self._fields_added.update({"CD_AGENCIA", value})
        return self

    def add_cd_agente_comp(self, value):
        self._fields_added.update({"CD_AGENTE_COMP", value})
        return self

    def add_cd_banco(self, value):
        self._fields_added.update({"CD_BANCO", value})
        return self

    def add_cd_bolsa(self, value):
        self._fields_added.update({"CD_BOLSA", value})
        return self

    def add_cd_cliente_comp(self, value):
        self._fields_added.update({"CD_CLIENTE_COMP", value})
        return self

    def add_cd_clie_inst(self, value):
        self._fields_added.update({"CD_CLIE_INST", value})
        return self

    def add_cd_clie_outr_bolsa(self, value):
        self._fields_added.update({"CD_CLIE_OUTR_BOLSA", value})
        return self

    def add_cd_cnpj_cvm(self, value):
        self._fields_added.update({"CD_CNPJ_CVM", value})
        return self

    def add_cd_corr_outr_bolsa(self, value):
        self._fields_added.update({"CD_CORR_OUTR_BOLSA", value})
        return self

    def add_cd_cvm(self, value):
        self._fields_added.update({"CD_CVM", value})
        return self

    def add_cd_relatorio(self, value):
        self._fields_added.update({"CD_RELATORIO", value})
        return self

    def add_cd_situac(self, value):
        self._fields_added.update({"CD_SITUAC", value})
        return self

    def add_cd_usua_inst(self, value):
        self._fields_added.update({"CD_USUA_INST", value})
        return self

    def add_dv_agente_comp(self, value):
        self._fields_added.update({"DV_AGENTE_COMP", value})
        return self

    def add_dv_clie_inst(self, value):
        self._fields_added.update({"DV_CLIE_INST", value})
        return self

    def add_dv_cliente_comp(self, value):
        self._fields_added.update({"DV_CLIENTE_COMP", value})
        return self

    def add_dv_usua_inst(self, value):
        self._fields_added.update({"DV_USUA_INST", value})
        return self

    def add_ds_comnom(self, value):
        self._fields_added.update({"DS_COMNOM", value})
        return self

    def add_nm_apelido(self, value):
        self._fields_added.update({"NM_APELIDO", value})
        return self

    def add_nm_conta(self, value):
        self._fields_added.update({"NM_CONTA", value})
        return self

    def add_pc_corcor_prin_cs(self, value):
        self._fields_added.update({"PC_CORCOR_PRIN_CS", value})
        return self

    def add_in_tipo_corret_exec_cs(self, value):
        self._fields_added.update({"IN_TIPO_CORRET_EXEC_CS", value})
        return self

    def add_pc_total_cs(self, value):
        self._fields_added.update({"PC_TOTAL_CS", value})
        return self

    def add_vl_corret_max_cs(self, value):
        self._fields_added.update({"VL_CORRET_MAX_CS", value})
        return self

    def add_vl_corret_min_princ_cs(self, value):
        self._fields_added.update({"VL_CORRET_MIN_PRINC_CS", value})
        return self

    def add_cd_banco_clicta_principal(self, value):
        self._fields_added.update({"CD_BANCO_CLICTA_PRINCIPAL", value})
        return self

    def add_cd_agencia_clicta_principal(self, value):
        self._fields_added.update({"CD_AGENCIA_CLICTA_PRINCIPAL", value})
        return self

    def add_nr_conta_clicta_principal(self, value):
        self._fields_added.update({"NR_CONTA_CLICTA_PRINCIPAL", value})
        return self

    def add_dv_conta_clicta_principal(self, value):
        self._fields_added.update({"DV_CONTA_CLICTA_PRINCIPAL", value})
        return self

    def add_cd_banco_clicta_a(self, value):
        self._fields_added.update({"CD_BANCO_CLICTA_A", value})
        return self

    def add_cd_agencia_clicta_a(self, value):
        self._fields_added.update({"CD_AGENCIA_CLICTA_A", value})
        return self

    def add_nr_conta_clicta_a1(self, value):
        self._fields_added.update({"NR_CONTA_CLICTA_A1", value})
        return self

    def add_dv_conta_clicta_a1(self, value):
        self._fields_added.update({"DV_CONTA_CLICTA_A1", value})
        return self

    def add_nr_conta_clicta_a2(self, value):
        self._fields_added.update({"NR_CONTA_CLICTA_A2", value})
        return self

    def add_dv_conta_clicta_a2(self, value):
        self._fields_added.update({"DV_CONTA_CLICTA_A2", value})
        return self

    def add_cd_banco_clicta_b(self, value):
        self._fields_added.update({"CD_BANCO_CLICTA_B", value})
        return self

    def add_cd_agencia_clicta_b(self, value):
        self._fields_added.update({"CD_AGENCIA_CLICTA_B", value})
        return self

    def add_nr_conta_clicta_b1(self, value):
        self._fields_added.update({"NR_CONTA_CLICTA_B1", value})
        return self

    def add_dv_conta_clicta_b1(self, value):
        self._fields_added.update({"DV_CONTA_CLICTA_B1", value})
        return self

    def add_nr_conta_clicta_b2(self, value):
        self._fields_added.update({"NR_CONTA_CLICTA_B2", value})
        return self

    def add_dv_conta_clicta_b2(self, value):
        self._fields_added.update({"DV_CONTA_CLICTA_B2", value})
        return self

    def add_in_liminar_ir_oper(self, value):
        self._fields_added.update({"IN_LIMINAR_IR_OPER", value})
        return self

    def add_cd_cliente_bmf(self, value):
        self._fields_added.update({"CD_CLIENTE_BMF", value})
        return self

    def add_cd_operac_cvm(self, value):
        self._fields_added.update({"CD_OPERAC_CVM", value})
        return self

    def add_clinst(self, value):
        self._fields_added.update({"CLINST", value})
        return self

    def add_cormax(self, value):
        self._fields_added.update({"CORMAX", value})
        return self

    def add_pertax(self, value):
        self._fields_added.update({"PERTAX", value})
        return self

    def add_socefe(self, value):
        self._fields_added.update({"SOCEFE", value})
        return self

    def add_in_cobra_mc(self, value):
        self._fields_added.update({"IN_COBRA_MC", value})
        return self

    def add_indbro(self, value):
        self._fields_added.update({"INDBRO", value})
        return self

    def add_indpld(self, value):
        self._fields_added.update({"INDPLD", value})
        return self

    def add_in_integra_cc(self, value):
        self._fields_added.update({"IN_INTEGRA_CC", value})
        return self

    def add_in_integra_corr(self, value):
        self._fields_added.update({"IN_INTEGRA_CORR", value})
        return self

    def add_in_nao_reside(self, value):
        self._fields_added.update({"IN_NAO_RESIDE", value})
        return self

    def add_intliq(self, value):
        self._fields_added.update({"INTLIQ", value})
        return self

    def add_in_tribut_especial(self, value):
        self._fields_added.update({"IN_TRIBUT_ESPECIAL", value})
        return self

    def add_txt_email_td(self, value):
        self._fields_added.update({"TXT_EMAIL_TD", value})
        return self

    def add_val_lim_neg_td(self, value):
        self._fields_added.update({"VAL_LIM_NEG_TD", value})
        return self

    def add_val_taxa_agnt_td(self, value):
        self._fields_added.update({"VAL_TAXA_AGNT_TD", value})
        return self

    def add_cod_aeco_princ(self, value):
        self._fields_added.update({"COD_AECO_PRINC", value})
        return self

    def add_num_seq_muni_end2(self, value):
        self._fields_added.update({"NUM_SEQ_MUNI_END2", value})
        return self

    def add_cod_tipo_titd_con(self, value):
        self._fields_added.update({"COD_TIPO_TITD_CON", value})
        return self

    def add_cod_poss_nif(self, value):
        self._fields_added.update({"COD_POSS_NIF", value})
        return self

    def add_ind_soc_titu_potd(self, value):
        self._fields_added.update({"IND_SOC_TITU_POTD", value})
        return self

    def add_ind_cvm286(self, value):
        self._fields_added.update({"IND_CVM286", value})
        return self

    def add_ind_fun_inve_excs(self, value):
        self._fields_added.update({"IND_FUN_INVE_EXCS", value})
        return self

    def add_cod_tipo_pess_cott(self, value):
        self._fields_added.update({"COD_TIPO_PESS_COTT", value})
        return self

    def add_nome_cott_pj(self, value):
        self._fields_added.update({"NOME_COTT_PJ", value})
        return self

    def add_nome_cott_pf(self, value):
        self._fields_added.update({"NOME_COTT_PF", value})
        return self

    def add_ind_pol_expc(self, value):
        self._fields_added.update({"IND_POL_EXPC", value})
        return self

    def add_ind_con_orig_priv(self, value):
        self._fields_added.update({"IND_CON_ORIG_PRIV", value})
        return self

    def add_cod_nat_jurd(self, value):
        self._fields_added.update({"COD_NAT_JURD", value})
        return self

    def add_nif(self, value):
        self._fields_added.update({"NIF", value})
        return self

    def add_ind_pcta(self, value):
        self._fields_added.update({"IND_PCTA", value})
        return self

    def add_cod_cep_estr2(self, value):
        self._fields_added.update({"COD_CEP_ESTR2", value})
        return self

    def add_uf_estr2(self, value):
        self._fields_added.update({"UF_ESTR2", value})
        return self

    def add_num_aut_tra_orde_prcd(self, value):
        self._fields_added.update({"NUM_AUT_TRA_ORDE_PRCD", value})
        return self

    def add_val_fatu_med_mes_ult_ano(self, value):
        self._fields_added.update({"VAL_FATU_MED_MES_ULT_ANO", value})
        return self

    def add_data_ref_fatu_med_mes(self, value):
        self._fields_added.update({"DATA_REF_FATU_MED_MES", value})
        return self

    def add_num_fun_cott_infl_sign(self, value):
        self._fields_added.update({"NUM_FUN_COTT_INFL_SIGN", value})
        return self

    def add_num_empr_sem_fins_lucr(self, value):
        self._fields_added.update({"NUM_EMPR_SEM_FINS_LUCR", value})
        return self

    def add_nome_tit_cta_cole(self, value):
        self._fields_added.update({"NOME_TIT_CTA_COLE", value})
        return self

    def add_num_gstr_fund_inv(self, value):
        self._fields_added.update({"NUM_GSTR_FUND_INV", value})
        return self

    def add_num_gstr_cart_ad(self, value):
        self._fields_added.update({"NUM_GSTR_CART_AD", value})
        return self
