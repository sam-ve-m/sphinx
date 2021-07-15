# STANDARD LIBS
from datetime import datetime

# SPHINX
from src.repositories.sinacor_types.enum.register_type import RegisterType
from src.repositories.sinacor_types.enum.dependency_condition import DependencyCondition
from src.repositories.sinacor_types.enum.client_status_basic_registration import (
    ClientStatusBasicRegistration,
)
from src.repositories.sinacor_types.enum.receipt_dividends_by_stock_exchange import (
    ReceiptDividendsByStockExchange,
)
from src.repositories.sinacor_types.enum.address_type import AddressType
from src.repositories.sinacor_types.enum.address_purpose import AddressPurpose
from src.repositories.sinacor_types.enum.client_origin import ClientOrigin
from src.repositories.sinacor_types.enum.client_registration_status import (
    ClientRegistrationStatus,
)
from src.repositories.sinacor_types.enum.is_own_trader import IsOwnTrader
from src.repositories.sinacor_types.enum.client_type_of_exchange_activity import (
    ClientTypeOfExchangeActivity,
)
from src.repositories.sinacor_types.enum.investor_type_of_exchange_activity import (
    InvestorTypeOfExchangeActivity,
)
from src.repositories.sinacor_types.enum.indicator_by_account import IndicatorByAccount
from src.repositories.sinacor_types.enum.mailing_address import MailingAddress
from src.repositories.sinacor_types.enum.account_linked_address import (
    AccountLinkedAddress,
)
from src.repositories.sinacor_types.enum.must_send_email_to_bvmf import (
    MustSendEmailToBvmf,
)
from src.repositories.sinacor_types.enum.operates_by_treasury_direct_agent import (
    OperatesByTreasuryDirectAgent,
)
from src.repositories.sinacor_types.enum.register_in_the_direct_treasure_activity import (
    RegisterInTheDirectTreasureActivity,
)
from src.repositories.sinacor_types.enum.collateralization_type_code import (
    CollateralizationTypeCode,
)
from src.repositories.sinacor_types.enum.customer_risk_rating import CustomerRiskRating
from src.repositories.sinacor_types.enum.risk import Risk
from src.repositories.sinacor_types.enum.work_in_some_company import WorkInSomeCompany
from src.repositories.sinacor_types.enum.is_us_person import IsUsPerson
from src.repositories.sinacor_types.enum.client_digit import ClientDigit
from src.repositories.sinacor_types.enum.brokerage_note_issuance_indicator import (
    BrokerageNoteIssuanceIndicator,
)
from src.repositories.sinacor_types.enum.foreign_zip_code import ForeignZipCode
from src.repositories.sinacor_types.enum.foreign_state import ForeignState
from src.repositories.sinacor_types.enum.bmf_client import BmfClient


class ClientRegisterBuilder:
    def __init__(self):
        self._fields_added = dict()

    def build(self):
        return self._fields_added

    def add_tp_registro(self):
        self._fields_added.update({"TP_REGISTRO": RegisterType.UPDATE_INCLUSION.value})
        return self

    def add_dt_criacao(self, user_data: dict):
        self._fields_added.update({"DT_CRIACAO": user_data["created_at"]})
        return self

    def add_dt_atualiz(self):
        self._fields_added.update({"DT_ATUALIZ": datetime.now()})
        return self

    def add_cd_cpfcgc(self, user_data: dict):
        self._fields_added.update({"CD_CPFCGC": user_data["cpf"]})
        return self

    def add_dt_nasc_fund(self, user_data: dict):
        self._fields_added.update({"DT_NASC_FUND": user_data["birth_date"]})
        return self

    def add_cd_con_dep(self):
        self._fields_added.update({"CD_CON_DEP": DependencyCondition.HOLDER.value})
        return self

    def add_in_irsdiv(self, user_data: dict):
        self._fields_added.update({"IN_IRSDIV": user_data["assets"]["income_tax_type"]})
        return self

    def add_in_pess_vinc(self, user_data: dict):
        self._fields_added.update({"IN_PESS_VINC": user_data["connected_person"]})
        return self

    def add_nm_cliente(self, user_data: dict):
        self._fields_added.update({"NM_CLIENTE": user_data["name"]})
        return self

    def add_tp_cliente(self, user_data: dict):
        self._fields_added.update({"TP_CLIENTE": user_data["client_type"]})
        return self

    def add_tp_pessoa(self, user_data: dict):
        self._fields_added.update({"TP_PESSOA": user_data["person_type"]})
        return self

    def add_tp_investidor(self, user_data: dict):
        self._fields_added.update({"TP_INVESTIDOR": user_data["investor_type"]})
        return self

    def add_in_situac_cliger(self):
        self._fields_added.update(
            {"IN_SITUAC_CLIGER": ClientStatusBasicRegistration.ACTIVATE.value}
        )
        return self

    def add_cd_ativ(self, user_data: dict):
        self._fields_added.update({"CD_ATIV": user_data["occupation"]["activity"]})
        return self

    def add_cd_cosif(self, user_data: dict):
        self._fields_added.update({"CD_COSIF": user_data["cosif_tax_classification"]})
        return self

    def add_cd_cosif_ci(self, user_data: dict):
        self._fields_added.update(
            {"CD_COSIF_CI": user_data["cosif_tax_classification"]}
        )
        return self

    def add_cd_est_civil(self, user_data: dict):
        key_values = {
            "not_married": 1,
            "married": 5,
            "divorced": 4,
            "widower": 3,
        }
        value = key_values.get(user_data["marital"]["status"])
        self._fields_added.update({"CD_EST_CIVIL": value})
        return self

    def add_cd_nacion(self, user_data: dict):
        self._fields_added.update({"CD_NACION": user_data["birthplace"]["nationality"]})
        return self

    def add_cd_tipo_doc(self, user_data: dict):
        key_values = {
            "CPF": 523,
        }
        value = key_values.get(user_data["identifier_document"]["type"])
        self._fields_added.update({"CD_TIPO_DOC": value})
        return self

    def add_cd_doc_ident(self, user_data: dict):
        self._fields_added.update({"CD_DOC_IDENT": user_data["cpf"]})
        return self

    def add_id_sexo(self, user_data: dict):
        self._fields_added.update({"ID_SEXO": user_data["gender"]})
        return self

    def add_in_rec_divi(self):
        self._fields_added.update(
            {"IN_REC_DIVI": ReceiptDividendsByStockExchange.YES.value}
        )
        return self

    def add_nm_conjuge(self, user_data: dict):
        self._fields_added.update(
            {"NM_CONJUGE": user_data["marital"]["spouse"]["name"]}
        )
        return self

    def add_nm_e_mail(self, user_data: dict):
        self._fields_added.update({"NM_E_MAIL": user_data["email"]})
        return self

    def add_nm_loc_nasc(self, user_data: dict):
        self._fields_added.update({"NM_LOC_NASC": user_data["birthplace"]["city"]})
        return self

    def add_nm_mae(self, user_data: dict):
        self._fields_added.update({"NM_MAE": user_data["mother_name"]})
        return self

    def add_sg_estado_nasc(self, user_data: dict):
        self._fields_added.update({"SG_ESTADO_NASC": user_data["birthplace"]["state"]})
        return self

    def add_sg_pais(self, user_data: dict):
        self._fields_added.update({"SG_PAIS": user_data["birthplace"]["country"]})
        return self

    def add_tp_regcas(self, user_data: dict):
        self._fields_added.update(
            {"TP_REGCAS": user_data["marital_update"]["marital_regime"]}
        )
        return self

    def add_cd_cep(self, user_data: dict):
        self._fields_added.update({"CD_CEP": int(user_data["address"]["zip_code"])})
        return self

    def add_cd_ddd_celular1(self, user_data: dict):
        # TODO: celphone format validate
        self._fields_added.update({"CD_DDD_CELULAR1": int(user_data["cel_phone"][:2])})
        return self

    def add_cd_ddd_tel(self, user_data: dict):
        self._fields_added.update(
            {"CD_DDD_TEL": int(user_data["address"]["phone_number"][:2])}
        )
        return self

    def add_in_ende(self):
        self._fields_added.update({"IN_ENDE": AddressType.RESIDENTIAL.value})
        return self

    def add_nm_bairro(self, user_data: dict):
        self._fields_added.update({"NM_BAIRRO": user_data["address"]["neighborhood"]})
        return self

    def add_nr_celular1(self, user_data: dict):
        self._fields_added.update({"NR_CELULAR1": user_data["cel_phone"][2:]})
        return self

    def add_nm_cidade(self, user_data: dict):
        self._fields_added.update({"NM_CIDADE": user_data["address"]["city"]})
        return self

    def add_nm_logradouro(self, user_data: dict):
        self._fields_added.update(
            {"NM_LOGRADOURO": user_data["address"]["street_name"]}
        )
        return self

    def add_nr_predio(self, user_data: dict):
        self._fields_added.update({"NR_PREDIO": user_data["address"]["number"]})
        return self

    def add_nr_telefone(self, user_data: dict):
        self._fields_added.update(
            {"NR_TELEFONE": int(user_data["address"]["phone_number"][2:])}
        )
        return self

    def add_sg_estado(self, user_data: dict):
        self._fields_added.update({"SG_ESTADO": user_data["address"]["state"]})
        return self

    def add_sg_pais_ende1(self, user_data: dict):
        self._fields_added.update({"SG_PAIS_ENDE1": user_data["address"]["country"]})
        return self

    def add_cod_finl_end1(self):
        self._fields_added.update({"COD_FINL_END1": AddressPurpose.MAIN.value})
        return self

    def add_cd_agente(self, value=None):
        self._fields_added.update({"CD_AGENTE": value})
        return self

    def add_cd_assessor(self, value=None):
        self._fields_added.update({"CD_ASSESSOR": value})
        return self

    def add_cd_cliente(self, value=None):
        self._fields_added.update({"CD_CLIENTE": value})
        return self

    def add_cd_origem(self):
        self._fields_added.update({"CD_ORIGEM": ClientOrigin.BROKER.value})
        return self

    def add_cd_vinculo(self, value=None):
        self._fields_added.update({"CD_VINCULO": value})
        return self

    def add_dv_cliente(self):
        self._fields_added.update({"DV_CLIENTE": ClientDigit.DEFAULT.value})
        return self

    def add_in_cart_prop(self):
        self._fields_added.update({"IN_CART_PROP": IsOwnTrader.YES.value})
        return self

    def add_in_emite_nota(self):
        self._fields_added.update(
            {"IN_EMITE_NOTA": BrokerageNoteIssuanceIndicator.DEFAULT.value}
        )
        return self

    def add_in_situac(self):
        self._fields_added.update(
            {"IN_SITUAC": ClientRegistrationStatus.ACTIVATE.value}
        )
        return self

    def add_pc_corcor_prin(self, value=None):
        self._fields_added.update({"PC_CORCOR_PRIN": value})
        return self

    def add_tp_cliente_bol(self):
        self._fields_added.update(
            {"TP_CLIENTE_BOL": ClientTypeOfExchangeActivity.NORMAL.value}
        )
        return self

    def add_tp_conta(self, value=None):
        self._fields_added.update({"TP_CONTA": value})
        return self

    def add_tp_investidor_bol(self):
        self._fields_added.update(
            {"TP_INVESTIDOR_BOL": InvestorTypeOfExchangeActivity.PHYSICAL_PERSON.value}
        )
        return self

    def add_in_lifo_fifo(self, value=None):
        self._fields_added.update({"IN_LIFO_FIFO": value})
        return self

    def add_ind_pcta(self):
        self._fields_added.update({"IND_PCTA": IndicatorByAccount.YES.value})
        return self

    def add_cod_tipo_colt(self, value=None):
        self._fields_added.update({"COD_TIPO_COLT": value})
        return self

    def add_in_emite_nota_cs(self, value=None):
        self._fields_added.update({"IN_EMITE_NOTA_CS": value})
        return self

    def add_ind_end_vinc_con(self):
        self._fields_added.update({"IND_END_VINC_CON": MailingAddress.FIRST.value})
        return self

    def add_ind_end_crsp(self):
        self._fields_added.update({"IND_END_CRSP": AccountLinkedAddress.FIRST.value})
        return self

    def add_ind_env_email_bvmf(self):
        self._fields_added.update({"IND_ENV_EMAIL_BVMF": MustSendEmailToBvmf.YES.value})
        return self

    def add_tp_cliente_bmf(self):
        self._fields_added.update({"TP_CLIENTE_BMF": BmfClient.DEFAULT.value})
        return self

    def add_ind_oprc_td(self):
        self._fields_added.update(
            {"IND_OPRC_TD": RegisterInTheDirectTreasureActivity.YES.value}
        )
        return self

    def add_ind_oprc_agnt_td(self):
        self._fields_added.update(
            {"IND_OPRC_AGNT_TD": OperatesByTreasuryDirectAgent.YES.value}
        )
        return self

    def add_cod_cidade_nasc(self, user_data: dict):
        self._fields_added.update(
            {"COD_CIDADE_NASC": user_data["birthplace"]["id_city"]}
        )
        return self

    def add_sigl_pais_resid(self, user_data: dict):
        self._fields_added.update({"SIGL_PAIS_RESID": user_data["address"]["country"]})
        return self

    def add_num_seq_muni_end1(self, user_data: dict):
        self._fields_added.update(
            {"NUM_SEQ_MUNI_END1": user_data["address"]["id_city"]}
        )
        return self

    def add_num_tipo_con(self, value=None):
        self._fields_added.update({"NUM_TIPO_CON": value})
        return self

    def add_cod_tipo_colt(self):
        self._fields_added.update(
            {"COD_TIPO_COLT": CollateralizationTypeCode.INVESTOR.value}
        )
        return self

    def add_cod_cep_estr1(self):
        self._fields_added.update({"COD_CEP_ESTR1": ForeignZipCode.DEFAULT.value})
        return self

    def add_uf_estr1(self):
        self._fields_added.update({"UF_ESTR1": ForeignState.DEFAULT.value})
        return self

    def add_num_class_risc_cmtt(self):
        self._fields_added.update({"NUM_CLASS_RISC_CMTT": CustomerRiskRating.NO.value})
        return self

    def add_desc_risc_cmtt(self):
        # TODO: FROM STONEAGE
        self._fields_added.update({"DESC_RISC_CMTT": Risk.HIGH.value})
        return self

    def add_data_ult_atlz(self):
        self._fields_added.update({"DATA_ULT_ATLZ": datetime.now()})
        return self

    def add_num_trab_empr(self, user_data: dict):
        value = WorkInSomeCompany.NO.value
        if user_data["occupation"].get("company"):
            value = WorkInSomeCompany.YES.value
        self._fields_added.update({"NUM_TRAB_EMPR": value})
        return self

    def add_num_us_person(self, user_data: dict):
        value = IsUsPerson.NO.value
        if user_data["is_us_person"]:
            value = IsUsPerson.YES.value
        self._fields_added.update({"NUM_US_PERSON": value})
        return self

    def add_val_cfin(self, user_data: dict):
        self._fields_added.update({"VAL_CFIN": user_data["assets"]["income"]})
        return self

    def add_data_cfin(self, user_data: dict):
        self._fields_added.update({"DATA_CFIN": user_data["assets"]["date"]})
        return self

    def add_cd_cpf_conjuge(self, user_data: dict):
        self._fields_added.update(
            {"CD_CPF_CONJUGE": user_data["marital"]["spouse"]["cpf"]}
        )
        return self

    def add_dt_nasc_conjuge(self, user_data: dict):
        self._fields_added.update(
            {"DT_NASC_CONJUGE": user_data["marital_update"]["spouse_birth_date"]}
        )
        return self

    def add_cd_cnpj_empresa(self, user_data: dict):
        self._fields_added.update(
            {"CD_CNPJ_EMPRESA": user_data["occupation"]["company"]["cpnj"]}
        )
        return self

    def add_cd_capac(self, value=None):
        self._fields_added.update({"CD_CAPAC": value})
        return self

    def add_cd_codqua(self, value=None):
        self._fields_added.update({"CD_CODQUA": value})
        return self

    def add_ds_cargo(self, value=None):
        self._fields_added.update({"DS_CARGO": value})
        return self

    def add_cd_doc_ident(self, value=None):
        self._fields_added.update({"CD_DOC_IDENT": value})
        return self

    def add_cd_org_emit(self, value=None):
        self._fields_added.update({"CD_ORG_EMIT": value})
        return self

    def add_dt_doc_ident(self, value=None):
        self._fields_added.update({"DT_DOC_IDENT": value})
        return self

    def add_nm_empresa(self, value=None):
        self._fields_added.update({"NM_EMPRESA": value})
        return self

    def add_nm_pai(self, value=None):
        self._fields_added.update({"NM_PAI": value})
        return self

    def add_sg_estado_emis(self, value=None):
        self._fields_added.update({"SG_ESTADO_EMIS": value})
        return self

    def add_sg_estado_emiss_rg(self, value=None):
        self._fields_added.update({"SG_ESTADO_EMISS_RG": value})
        return self

    def add_dt_emiss_rg(self, value=None):
        self._fields_added.update({"DT_EMISS_RG": value})
        return self

    def add_cd_org_emit_rg(self, value=None):
        self._fields_added.update({"CD_ORG_EMIT_RG": value})
        return self

    def add_nr_rg(self, value=None):
        self._fields_added.update({"NR_RG": value})
        return self

    def add_cd_ddd_celular2(self, value=None):
        self._fields_added.update({"CD_DDD_CELULAR2": value})
        return self

    def add_cd_ddd_fax(self, value=None):
        self._fields_added.update({"CD_DDD_FAX": value})
        return self

    def add_nr_celular2(self, value=None):
        self._fields_added.update({"NR_CELULAR2": value})
        return self

    def add_nm_comp_ende(self, value=None):
        self._fields_added.update({"NM_COMP_ENDE": value})
        return self

    def add_nr_fax(self, value=None):
        self._fields_added.update({"NR_FAX": value})
        return self

    def add_nm_contato1(self, value=None):
        self._fields_added.update({"NM_CONTATO1": value})
        return self

    def add_nm_contato2(self, value=None):
        self._fields_added.update({"NM_CONTATO2": value})
        return self

    def add_nr_ramal(self, value=None):
        self._fields_added.update({"NR_RAMAL": value})
        return self

    def add_cd_cep2(self, value=None):
        self._fields_added.update({"CD_CEP2": value})
        return self

    def add_cd_ddd_celular12(self, value=None):
        self._fields_added.update({"CD_DDD_CELULAR12": value})
        return self

    def add_cd_ddd_celular22(self, value=None):
        self._fields_added.update({"CD_DDD_CELULAR22": value})
        return self

    def add_cd_ddd_fax12(self, value=None):
        self._fields_added.update({"CD_DDD_FAX12": value})
        return self

    def add_cd_ddd_fax22(self, value=None):
        self._fields_added.update({"CD_DDD_FAX22": value})
        return self

    def add_cd_ddd_tel2(self, value=None):
        self._fields_added.update({"CD_DDD_TEL2": value})
        return self

    def add_in_tipo_ende2(self, value=None):
        self._fields_added.update({"IN_TIPO_ENDE2": value})
        return self

    def add_nm_bairro2(self, value=None):
        self._fields_added.update({"NM_BAIRRO2": value})
        return self

    def add_nm_cidade2(self, value=None):
        self._fields_added.update({"NM_CIDADE2": value})
        return self

    def add_nm_comp_ende2(self, value=None):
        self._fields_added.update({"NM_COMP_ENDE2": value})
        return self

    def add_nm_logradouro2(self, value=None):
        self._fields_added.update({"NM_LOGRADOURO2": value})
        return self

    def add_nr_celular12(self, value=None):
        self._fields_added.update({"NR_CELULAR12": value})
        return self

    def add_nr_celular22(self, value=None):
        self._fields_added.update({"NR_CELULAR22": value})
        return self

    def add_nr_fax12(self, value=None):
        self._fields_added.update({"NR_FAX12": value})
        return self

    def add_nr_fax22(self, value=None):
        self._fields_added.update({"NR_FAX22": value})
        return self

    def add_nm_contato12(self, value=None):
        self._fields_added.update({"NM_CONTATO12": value})
        return self

    def add_nm_contato22(self, value=None):
        self._fields_added.update({"NM_CONTATO22": value})
        return self

    def add_nr_predio2(self, value=None):
        self._fields_added.update({"NR_PREDIO2": value})
        return self

    def add_nr_ramal2(self, value=None):
        self._fields_added.update({"NR_RAMAL2": value})
        return self

    def add_nr_telefone2(self, value=None):
        self._fields_added.update({"NR_TELEFONE2": value})
        return self

    def add_sg_estado2(self, value=None):
        self._fields_added.update({"SG_ESTADO2": value})
        return self

    def add_sg_pais_ende2(self, value=None):
        self._fields_added.update({"SG_PAIS_ENDE2": value})
        return self

    def add_cod_finl_end2(self, value=None):
        self._fields_added.update({"COD_FINL_END2": value})
        return self

    def add_cd_admin_cvm(self, value=None):
        self._fields_added.update({"CD_ADMIN_CVM": value})
        return self

    def add_cd_agencia(self, value=None):
        self._fields_added.update({"CD_AGENCIA": value})
        return self

    def add_cd_agente_comp(self, value=None):
        self._fields_added.update({"CD_AGENTE_COMP": value})
        return self

    def add_cd_banco(self, value=None):
        self._fields_added.update({"CD_BANCO": value})
        return self

    def add_cd_bolsa(self, value=None):
        self._fields_added.update({"CD_BOLSA": value})
        return self

    def add_cd_cliente_comp(self, value=None):
        self._fields_added.update({"CD_CLIENTE_COMP": value})
        return self

    def add_cd_clie_inst(self, value=None):
        self._fields_added.update({"CD_CLIE_INST": value})
        return self

    def add_cd_clie_outr_bolsa(self, value=None):
        self._fields_added.update({"CD_CLIE_OUTR_BOLSA": value})
        return self

    def add_cd_cnpj_cvm(self, value=None):
        self._fields_added.update({"CD_CNPJ_CVM": value})
        return self

    def add_cd_corr_outr_bolsa(self, value=None):
        self._fields_added.update({"CD_CORR_OUTR_BOLSA": value})
        return self

    def add_cd_cvm(self, value=None):
        self._fields_added.update({"CD_CVM": value})
        return self

    def add_cd_relatorio(self, value=None):
        self._fields_added.update({"CD_RELATORIO": value})
        return self

    def add_cd_situac(self, value=None):
        self._fields_added.update({"CD_SITUAC": value})
        return self

    def add_cd_usua_inst(self, value=None):
        self._fields_added.update({"CD_USUA_INST": value})
        return self

    def add_dv_agente_comp(self, value=None):
        self._fields_added.update({"DV_AGENTE_COMP": value})
        return self

    def add_dv_clie_inst(self, value=None):
        self._fields_added.update({"DV_CLIE_INST": value})
        return self

    def add_dv_cliente_comp(self, value=None):
        self._fields_added.update({"DV_CLIENTE_COMP": value})
        return self

    def add_dv_usua_inst(self, value=None):
        self._fields_added.update({"DV_USUA_INST": value})
        return self

    def add_ds_comnom(self, value=None):
        self._fields_added.update({"DS_COMNOM": value})
        return self

    def add_nm_apelido(self, value=None):
        self._fields_added.update({"NM_APELIDO": value})
        return self

    def add_nm_conta(self, value=None):
        self._fields_added.update({"NM_CONTA": value})
        return self

    def add_pc_corcor_prin_cs(self, value=None):
        self._fields_added.update({"PC_CORCOR_PRIN_CS": value})
        return self

    def add_in_tipo_corret_exec_cs(self, value=None):
        self._fields_added.update({"IN_TIPO_CORRET_EXEC_CS": value})
        return self

    def add_pc_total_cs(self, value=None):
        self._fields_added.update({"PC_TOTAL_CS": value})
        return self

    def add_vl_corret_max_cs(self, value=None):
        self._fields_added.update({"VL_CORRET_MAX_CS": value})
        return self

    def add_vl_corret_min_princ_cs(self, value=None):
        self._fields_added.update({"VL_CORRET_MIN_PRINC_CS": value})
        return self

    def add_cd_banco_clicta_principal(self, value=None):
        self._fields_added.update({"CD_BANCO_CLICTA_PRINCIPAL": value})
        return self

    def add_cd_agencia_clicta_principal(self, value=None):
        self._fields_added.update({"CD_AGENCIA_CLICTA_PRINCIPAL": value})
        return self

    def add_nr_conta_clicta_principal(self, value=None):
        self._fields_added.update({"NR_CONTA_CLICTA_PRINCIPAL": value})
        return self

    def add_dv_conta_clicta_principal(self, value=None):
        self._fields_added.update({"DV_CONTA_CLICTA_PRINCIPAL": value})
        return self

    def add_cd_banco_clicta_a(self, value=None):
        self._fields_added.update({"CD_BANCO_CLICTA_A": value})
        return self

    def add_cd_agencia_clicta_a(self, value=None):
        self._fields_added.update({"CD_AGENCIA_CLICTA_A": value})
        return self

    def add_nr_conta_clicta_a1(self, value=None):
        self._fields_added.update({"NR_CONTA_CLICTA_A1": value})
        return self

    def add_dv_conta_clicta_a1(self, value=None):
        self._fields_added.update({"DV_CONTA_CLICTA_A1": value})
        return self

    def add_nr_conta_clicta_a2(self, value=None):
        self._fields_added.update({"NR_CONTA_CLICTA_A2": value})
        return self

    def add_dv_conta_clicta_a2(self, value=None):
        self._fields_added.update({"DV_CONTA_CLICTA_A2": value})
        return self

    def add_cd_banco_clicta_b(self, value=None):
        self._fields_added.update({"CD_BANCO_CLICTA_B": value})
        return self

    def add_cd_agencia_clicta_b(self, value=None):
        self._fields_added.update({"CD_AGENCIA_CLICTA_B": value})
        return self

    def add_nr_conta_clicta_b1(self, value=None):
        self._fields_added.update({"NR_CONTA_CLICTA_B1": value})
        return self

    def add_dv_conta_clicta_b1(self, value=None):
        self._fields_added.update({"DV_CONTA_CLICTA_B1": value})
        return self

    def add_nr_conta_clicta_b2(self, value=None):
        self._fields_added.update({"NR_CONTA_CLICTA_B2": value})
        return self

    def add_dv_conta_clicta_b2(self, value=None):
        self._fields_added.update({"DV_CONTA_CLICTA_B2": value})
        return self

    def add_in_liminar_ir_oper(self, value=None):
        self._fields_added.update({"IN_LIMINAR_IR_OPER": value})
        return self

    def add_cd_cliente_bmf(self, value=None):
        self._fields_added.update({"CD_CLIENTE_BMF": value})
        return self

    def add_cd_operac_cvm(self, value=None):
        self._fields_added.update({"CD_OPERAC_CVM": value})
        return self

    def add_clinst(self, value=None):
        self._fields_added.update({"CLINST": value})
        return self

    def add_cormax(self, value=None):
        self._fields_added.update({"CORMAX": value})
        return self

    def add_pertax(self, value=None):
        self._fields_added.update({"PERTAX": value})
        return self

    def add_socefe(self, value=None):
        self._fields_added.update({"SOCEFE": value})
        return self

    def add_in_cobra_mc(self, value=None):
        self._fields_added.update({"IN_COBRA_MC": value})
        return self

    def add_indbro(self, value=None):
        self._fields_added.update({"INDBRO": value})
        return self

    def add_indpld(self, value=None):
        self._fields_added.update({"INDPLD": value})
        return self

    def add_in_integra_cc(self, value=None):
        self._fields_added.update({"IN_INTEGRA_CC": value})
        return self

    def add_in_integra_corr(self, value=None):
        self._fields_added.update({"IN_INTEGRA_CORR": value})
        return self

    def add_in_nao_reside(self, value=None):
        self._fields_added.update({"IN_NAO_RESIDE": value})
        return self

    def add_intliq(self, value=None):
        self._fields_added.update({"INTLIQ": value})
        return self

    def add_in_tribut_especial(self, value=None):
        self._fields_added.update({"IN_TRIBUT_ESPECIAL": value})
        return self

    def add_txt_email_td(self, value=None):
        self._fields_added.update({"TXT_EMAIL_TD": value})
        return self

    def add_val_lim_neg_td(self, value=None):
        self._fields_added.update({"VAL_LIM_NEG_TD": value})
        return self

    def add_val_taxa_agnt_td(self, value=None):
        self._fields_added.update({"VAL_TAXA_AGNT_TD": value})
        return self

    def add_cod_aeco_princ(self, value=None):
        self._fields_added.update({"COD_AECO_PRINC": value})
        return self

    def add_num_seq_muni_end2(self, value=None):
        self._fields_added.update({"NUM_SEQ_MUNI_END2": value})
        return self

    def add_cod_tipo_titd_con(self, value=None):
        self._fields_added.update({"COD_TIPO_TITD_CON": value})
        return self

    def add_cod_poss_nif(self, value=None):
        self._fields_added.update({"COD_POSS_NIF": value})
        return self

    def add_ind_soc_titu_potd(self, value=None):
        self._fields_added.update({"IND_SOC_TITU_POTD": value})
        return self

    def add_ind_cvm286(self, value=None):
        self._fields_added.update({"IND_CVM286": value})
        return self

    def add_ind_fun_inve_excs(self, value=None):
        self._fields_added.update({"IND_FUN_INVE_EXCS": value})
        return self

    def add_cod_tipo_pess_cott(self, value=None):
        self._fields_added.update({"COD_TIPO_PESS_COTT": value})
        return self

    def add_nome_cott_pj(self, value=None):
        self._fields_added.update({"NOME_COTT_PJ": value})
        return self

    def add_nome_cott_pf(self, value=None):
        self._fields_added.update({"NOME_COTT_PF": value})
        return self

    def add_ind_pol_expc(self, value=None):
        self._fields_added.update({"IND_POL_EXPC": value})
        return self

    def add_ind_con_orig_priv(self, value=None):
        self._fields_added.update({"IND_CON_ORIG_PRIV": value})
        return self

    def add_cod_nat_jurd(self, value=None):
        self._fields_added.update({"COD_NAT_JURD": value})
        return self

    def add_nif(self, value=None):
        self._fields_added.update({"NIF": value})
        return self

    def add_ind_pcta(self, value=None):
        self._fields_added.update({"IND_PCTA": value})
        return self

    def add_cod_cep_estr2(self, value=None):
        self._fields_added.update({"COD_CEP_ESTR2": value})
        return self

    def add_uf_estr2(self, value=None):
        self._fields_added.update({"UF_ESTR2": value})
        return self

    def add_num_aut_tra_orde_prcd(self, value=None):
        self._fields_added.update({"NUM_AUT_TRA_ORDE_PRCD": value})
        return self

    def add_val_fatu_med_mes_ult_ano(self, value=None):
        self._fields_added.update({"VAL_FATU_MED_MES_ULT_ANO": value})
        return self

    def add_data_ref_fatu_med_mes(self, value=None):
        self._fields_added.update({"DATA_REF_FATU_MED_MES": value})
        return self

    def add_num_fun_cott_infl_sign(self, value=None):
        self._fields_added.update({"NUM_FUN_COTT_INFL_SIGN": value})
        return self

    def add_num_empr_sem_fins_lucr(self, value=None):
        self._fields_added.update({"NUM_EMPR_SEM_FINS_LUCR": value})
        return self

    def add_nome_tit_cta_cole(self, value=None):
        self._fields_added.update({"NOME_TIT_CTA_COLE": value})
        return self

    def add_num_gstr_fund_inv(self, value=None):
        self._fields_added.update({"NUM_GSTR_FUND_INV": value})
        return self

    def add_num_gstr_cart_ad(self, value=None):
        self._fields_added.update({"NUM_GSTR_CART_AD": value})
        return self
