from datetime import datetime

from pydantic import BaseModel, validator
from typing import List, Optional


class TpRegistro(BaseModel):
    TP_REGISTRO: str


class CdCliente(BaseModel):
    CD_CLIENTE: int


class CdOrgEmit(BaseModel):
    CD_ORG_EMIT: Optional[int]


class DtDocIdent(BaseModel):
    DT_DOC_IDENT: Optional[datetime]


class NrRg(BaseModel):
    NR_RG: int


class SgEstadoEmissRg(BaseModel):
    SG_ESTADO_EMISS_RG: str


class DtEmissRg(BaseModel):
    DT_EMISS_RG: datetime


class CdOrgEmitRg(BaseModel):
    CD_ORG_EMIT_RG: Optional[str]


class CdDocIdent(BaseModel):
    CD_DOC_IDENT: Optional[int]


class InRecDivi(BaseModel):
    IN_REC_DIVI: str


class InEmiteNota(BaseModel):
    IN_EMITE_NOTA: int


class PcCorcorPrin(BaseModel):
    PC_CORCOR_PRIN: int


class InEmiteNotaCs(BaseModel):
    IN_EMITE_NOTA_CS: str


class PcCorcorPrinCs(BaseModel):
    PC_CORCOR_PRIN_CS: int


class ValLimNegTd(BaseModel):
    VAL_LIM_NEG_TD: int


class ValTaxaAgntTd(BaseModel):
    VAL_TAXA_AGNT_TD: int


class TxtEmailTd(BaseModel):
    TXT_EMAIL_TD: str


class DtCriacao(BaseModel):
    DT_CRIACAO: datetime


class DtAtualiz(BaseModel):
    DT_ATUALIZ: datetime


class CdCpfcgc(BaseModel):
    CD_CPFCGC: int


class DtNascFund(BaseModel):
    DT_NASC_FUND: datetime


class CdConDep(BaseModel):
    CD_CON_DEP: int


class InIrsdiv(BaseModel):
    IN_IRSDIV: int


class InPessVinc(BaseModel):
    IN_PESS_VINC: str


class NmCliente(BaseModel):
    NM_CLIENTE: str


class TpCliente(BaseModel):
    TP_CLIENTE: int


class TpPessoa(BaseModel):
    TP_PESSOA: str


class TpInvestidor(BaseModel):
    TP_INVESTIDOR: int


class InSituacCliger(BaseModel):
    IN_SITUAC_CLIGER: str


class CdAtiv(BaseModel):
    CD_ATIV: int


class CdCosif(BaseModel):
    CD_COSIF: int


class CdCosifCi(BaseModel):
    CD_COSIF_CI: int


class CdEstCivil(BaseModel):
    CD_EST_CIVIL: int


class CdNacion(BaseModel):
    CD_NACION: int


class CdTipoDoc(BaseModel):
    CD_TIPO_DOC: str


class IdSexo(BaseModel):
    ID_SEXO: str


class NmEMail(BaseModel):
    NM_E_MAIL: str


class NmLocNasc(BaseModel):
    NM_LOC_NASC: str


class NmMae(BaseModel):
    NM_MAE: str


class SgEstadoNasc(BaseModel):
    SG_ESTADO_NASC: str


class SgPais(BaseModel):
    SG_PAIS: str


class CdCep(BaseModel):
    CD_CEP: int


class CdDddTel(BaseModel):
    CD_DDD_TEL: int


class InEnde(BaseModel):
    IN_ENDE: str


class NmBairro(BaseModel):
    NM_BAIRRO: str


class NmCidade(BaseModel):
    NM_CIDADE: str


class NmLogradouro(BaseModel):
    NM_LOGRADOURO: str


class NrPredio(BaseModel):
    NR_PREDIO: str


class NrTelefone(BaseModel):
    NR_TELEFONE: int


class SgEstado(BaseModel):
    SG_ESTADO: str


class SgPaisEnde1(BaseModel):
    SG_PAIS_ENDE1: str


class CdDddCelular1(BaseModel):
    CD_DDD_CELULAR1: int


class NrCelular1(BaseModel):
    NR_CELULAR1: str


class CdOrigem(BaseModel):
    CD_ORIGEM: int


class DvCliente(BaseModel):
    DV_CLIENTE: int


class InCartProp(BaseModel):
    IN_CART_PROP: str


class InSituac(BaseModel):
    IN_SITUAC: str


class TpClienteBol(BaseModel):
    TP_CLIENTE_BOL: int


class TpInvestidorBol(BaseModel):
    TP_INVESTIDOR_BOL: int


class IndPcta(BaseModel):
    IND_PCTA: Optional[str]


class IndEndVincCon(BaseModel):
    IND_END_VINC_CON: str


class IndEndCrsp(BaseModel):
    IND_END_CRSP: str


class IndEnvEmailBvmf(BaseModel):
    IND_ENV_EMAIL_BVMF: str


class TpClienteBmf(BaseModel):
    TP_CLIENTE_BMF: int


class IndOprcTd(BaseModel):
    IND_OPRC_TD: str


class IndOprcAgntTd(BaseModel):
    IND_OPRC_AGNT_TD: str


class CodCidadeNasc(BaseModel):
    COD_CIDADE_NASC: int


class SiglPaisResid(BaseModel):
    SIGL_PAIS_RESID: str


class NumSeqMuniEnd1(BaseModel):
    NUM_SEQ_MUNI_END1: int


class CodTipoColt(BaseModel):
    COD_TIPO_COLT: str


class CodCepEstr1(BaseModel):
    COD_CEP_ESTR1: str


class UfEstr1(BaseModel):
    UF_ESTR1: str


class NumClassRiscCmtt(BaseModel):
    NUM_CLASS_RISC_CMTT: int


class DescRiscCmtt(BaseModel):
    DESC_RISC_CMTT: str


class NumUsPerson(BaseModel):
    NUM_US_PERSON: int


class ValCfin(BaseModel):
    VAL_CFIN: float


class DataCfin(BaseModel):
    DATA_CFIN: datetime


class CdCnpjEmpresa(BaseModel):
    CD_CNPJ_EMPRESA: str


class CdCpfConjuge(BaseModel):
    CD_CPF_CONJUGE: str


class NmConjuge(BaseModel):
    NM_CONJUGE: str


class ValidNotMarriedBusinessPerson(
    TpRegistro,
    CdCliente,
    CdOrgEmit,
    DtDocIdent,
    NrRg,
    SgEstadoEmissRg,
    DtEmissRg,
    CdOrgEmitRg,
    CdDocIdent,
    InRecDivi,
    InEmiteNota,
    PcCorcorPrin,
    InEmiteNotaCs,
    PcCorcorPrinCs,
    ValLimNegTd,
    ValTaxaAgntTd,
    TxtEmailTd,
    DtCriacao,
    DtAtualiz,
    CdCpfcgc,
    DtNascFund,
    CdConDep,
    InIrsdiv,
    InPessVinc,
    NmCliente,
    TpCliente,
    TpPessoa,
    TpInvestidor,
    InSituacCliger,
    CdAtiv,
    CdCosif,
    CdCosifCi,
    CdEstCivil,
    CdNacion,
    CdTipoDoc,
    IdSexo,
    NmEMail,
    NmLocNasc,
    NmMae,
    SgEstadoNasc,
    SgPais,
    CdCep,
    CdDddTel,
    InEnde,
    NmBairro,
    NmCidade,
    NmLogradouro,
    NrPredio,
    NrTelefone,
    SgEstado,
    SgPaisEnde1,
    CdDddCelular1,
    NrCelular1,
    CdOrigem,
    DvCliente,
    InCartProp,
    InSituac,
    TpClienteBol,
    TpInvestidorBol,
    IndPcta,
    IndEndVincCon,
    IndEndCrsp,
    IndEnvEmailBvmf,
    TpClienteBmf,
    IndOprcTd,
    IndOprcAgntTd,
    CodCidadeNasc,
    SiglPaisResid,
    NumSeqMuniEnd1,
    CodTipoColt,
    CodCepEstr1,
    UfEstr1,
    NumClassRiscCmtt,
    DescRiscCmtt,
    NumUsPerson,
    ValCfin,
    DataCfin,
    CdCnpjEmpresa,
):
    class Config:
        extra = "forbid"


class ValidMarriedBusinessPerson(
    TpRegistro,
    CdCliente,
    CdOrgEmit,
    DtDocIdent,
    NrRg,
    SgEstadoEmissRg,
    DtEmissRg,
    CdOrgEmitRg,
    CdDocIdent,
    InRecDivi,
    InEmiteNota,
    PcCorcorPrin,
    InEmiteNotaCs,
    PcCorcorPrinCs,
    ValLimNegTd,
    ValTaxaAgntTd,
    TxtEmailTd,
    DtCriacao,
    DtAtualiz,
    CdCpfcgc,
    DtNascFund,
    CdConDep,
    InIrsdiv,
    InPessVinc,
    NmCliente,
    TpCliente,
    TpPessoa,
    TpInvestidor,
    InSituacCliger,
    CdAtiv,
    CdCosif,
    CdCosifCi,
    CdEstCivil,
    CdNacion,
    CdTipoDoc,
    IdSexo,
    NmEMail,
    NmLocNasc,
    NmMae,
    SgEstadoNasc,
    SgPais,
    CdCep,
    CdDddTel,
    InEnde,
    NmBairro,
    NmCidade,
    NmLogradouro,
    NrPredio,
    NrTelefone,
    SgEstado,
    SgPaisEnde1,
    CdDddCelular1,
    NrCelular1,
    CdOrigem,
    DvCliente,
    InCartProp,
    InSituac,
    TpClienteBol,
    TpInvestidorBol,
    IndPcta,
    IndEndVincCon,
    IndEndCrsp,
    IndEnvEmailBvmf,
    TpClienteBmf,
    IndOprcTd,
    IndOprcAgntTd,
    CodCidadeNasc,
    SiglPaisResid,
    NumSeqMuniEnd1,
    CodTipoColt,
    CodCepEstr1,
    UfEstr1,
    NumClassRiscCmtt,
    DescRiscCmtt,
    NumUsPerson,
    ValCfin,
    DataCfin,
    CdCnpjEmpresa,
    CdCpfConjuge,
    NmConjuge,
):
    class Config:
        extra = "forbid"


class ValidMarriedUnemployed(
    TpRegistro,
    CdCliente,
    CdOrgEmit,
    DtDocIdent,
    NrRg,
    SgEstadoEmissRg,
    DtEmissRg,
    CdOrgEmitRg,
    CdDocIdent,
    InRecDivi,
    InEmiteNota,
    PcCorcorPrin,
    InEmiteNotaCs,
    PcCorcorPrinCs,
    ValLimNegTd,
    ValTaxaAgntTd,
    TxtEmailTd,
    DtCriacao,
    DtAtualiz,
    CdCpfcgc,
    DtNascFund,
    CdConDep,
    InIrsdiv,
    InPessVinc,
    NmCliente,
    TpCliente,
    TpPessoa,
    TpInvestidor,
    InSituacCliger,
    CdAtiv,
    CdCosif,
    CdCosifCi,
    CdEstCivil,
    CdNacion,
    CdTipoDoc,
    IdSexo,
    NmEMail,
    NmLocNasc,
    NmMae,
    SgEstadoNasc,
    SgPais,
    CdCep,
    CdDddTel,
    InEnde,
    NmBairro,
    NmCidade,
    NmLogradouro,
    NrPredio,
    NrTelefone,
    SgEstado,
    SgPaisEnde1,
    CdDddCelular1,
    NrCelular1,
    CdOrigem,
    DvCliente,
    InCartProp,
    InSituac,
    TpClienteBol,
    TpInvestidorBol,
    IndPcta,
    IndEndVincCon,
    IndEndCrsp,
    IndEnvEmailBvmf,
    TpClienteBmf,
    IndOprcTd,
    IndOprcAgntTd,
    CodCidadeNasc,
    SiglPaisResid,
    NumSeqMuniEnd1,
    CodTipoColt,
    CodCepEstr1,
    UfEstr1,
    NumClassRiscCmtt,
    DescRiscCmtt,
    NumUsPerson,
    ValCfin,
    DataCfin,
    CdCpfConjuge,
    NmConjuge,
):
    class Config:
        extra = "forbid"


class ValidNotMarriedUnemployed(
    TpRegistro,
    CdCliente,
    CdOrgEmit,
    DtDocIdent,
    NrRg,
    SgEstadoEmissRg,
    DtEmissRg,
    CdOrgEmitRg,
    CdDocIdent,
    InRecDivi,
    InEmiteNota,
    PcCorcorPrin,
    InEmiteNotaCs,
    PcCorcorPrinCs,
    ValLimNegTd,
    ValTaxaAgntTd,
    TxtEmailTd,
    DtCriacao,
    DtAtualiz,
    CdCpfcgc,
    DtNascFund,
    CdConDep,
    InIrsdiv,
    InPessVinc,
    NmCliente,
    TpCliente,
    TpPessoa,
    TpInvestidor,
    InSituacCliger,
    CdAtiv,
    CdCosif,
    CdCosifCi,
    CdEstCivil,
    CdNacion,
    CdTipoDoc,
    IdSexo,
    NmEMail,
    NmLocNasc,
    NmMae,
    SgEstadoNasc,
    SgPais,
    CdCep,
    CdDddTel,
    InEnde,
    NmBairro,
    NmCidade,
    NmLogradouro,
    NrPredio,
    NrTelefone,
    SgEstado,
    SgPaisEnde1,
    CdDddCelular1,
    NrCelular1,
    CdOrigem,
    DvCliente,
    InCartProp,
    InSituac,
    TpClienteBol,
    TpInvestidorBol,
    IndPcta,
    IndEndVincCon,
    IndEndCrsp,
    IndEnvEmailBvmf,
    TpClienteBmf,
    IndOprcTd,
    IndOprcAgntTd,
    CodCidadeNasc,
    SiglPaisResid,
    NumSeqMuniEnd1,
    CodTipoColt,
    CodCepEstr1,
    UfEstr1,
    NumClassRiscCmtt,
    DescRiscCmtt,
    NumUsPerson,
    ValCfin,
    DataCfin,
):
    class Config:
        extra = "forbid"


class ValidMarriedEmployed(
    TpRegistro,
    CdCliente,
    CdOrgEmit,
    DtDocIdent,
    NrRg,
    SgEstadoEmissRg,
    DtEmissRg,
    CdOrgEmitRg,
    CdDocIdent,
    InRecDivi,
    InEmiteNota,
    PcCorcorPrin,
    InEmiteNotaCs,
    PcCorcorPrinCs,
    ValLimNegTd,
    ValTaxaAgntTd,
    TxtEmailTd,
    DtCriacao,
    DtAtualiz,
    CdCpfcgc,
    DtNascFund,
    CdConDep,
    InIrsdiv,
    InPessVinc,
    NmCliente,
    TpCliente,
    TpPessoa,
    TpInvestidor,
    InSituacCliger,
    CdAtiv,
    CdCosif,
    CdCosifCi,
    CdEstCivil,
    CdNacion,
    CdTipoDoc,
    IdSexo,
    NmEMail,
    NmLocNasc,
    NmMae,
    SgEstadoNasc,
    SgPais,
    CdCep,
    CdDddTel,
    InEnde,
    NmBairro,
    NmCidade,
    NmLogradouro,
    NrPredio,
    NrTelefone,
    SgEstado,
    SgPaisEnde1,
    CdDddCelular1,
    NrCelular1,
    CdOrigem,
    DvCliente,
    InCartProp,
    InSituac,
    TpClienteBol,
    TpInvestidorBol,
    IndPcta,
    IndEndVincCon,
    IndEndCrsp,
    IndEnvEmailBvmf,
    TpClienteBmf,
    IndOprcTd,
    IndOprcAgntTd,
    CodCidadeNasc,
    SiglPaisResid,
    NumSeqMuniEnd1,
    CodTipoColt,
    CodCepEstr1,
    UfEstr1,
    NumClassRiscCmtt,
    DescRiscCmtt,
    NumUsPerson,
    ValCfin,
    DataCfin,
    CdCnpjEmpresa,
    CdCpfConjuge,
    NmConjuge,
):
    class Config:
        extra = "forbid"


class ValidNotMarriedEmployed(
    TpRegistro,
    CdCliente,
    CdOrgEmit,
    DtDocIdent,
    NrRg,
    SgEstadoEmissRg,
    DtEmissRg,
    CdOrgEmitRg,
    CdDocIdent,
    InRecDivi,
    InEmiteNota,
    PcCorcorPrin,
    InEmiteNotaCs,
    PcCorcorPrinCs,
    ValLimNegTd,
    ValTaxaAgntTd,
    TxtEmailTd,
    DtCriacao,
    DtAtualiz,
    CdCpfcgc,
    DtNascFund,
    CdConDep,
    InIrsdiv,
    InPessVinc,
    NmCliente,
    TpCliente,
    TpPessoa,
    TpInvestidor,
    InSituacCliger,
    CdAtiv,
    CdCosif,
    CdCosifCi,
    CdEstCivil,
    CdNacion,
    CdTipoDoc,
    IdSexo,
    NmEMail,
    NmLocNasc,
    NmMae,
    SgEstadoNasc,
    SgPais,
    CdCep,
    CdDddTel,
    InEnde,
    NmBairro,
    NmCidade,
    NmLogradouro,
    NrPredio,
    NrTelefone,
    SgEstado,
    SgPaisEnde1,
    CdDddCelular1,
    NrCelular1,
    CdOrigem,
    DvCliente,
    InCartProp,
    InSituac,
    TpClienteBol,
    TpInvestidorBol,
    IndPcta,
    IndEndVincCon,
    IndEndCrsp,
    IndEnvEmailBvmf,
    TpClienteBmf,
    IndOprcTd,
    IndOprcAgntTd,
    CodCidadeNasc,
    SiglPaisResid,
    NumSeqMuniEnd1,
    CodTipoColt,
    CodCepEstr1,
    UfEstr1,
    NumClassRiscCmtt,
    DescRiscCmtt,
    NumUsPerson,
    ValCfin,
    DataCfin,
):
    class Config:
        extra = "forbid"
