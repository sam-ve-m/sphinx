# OUTSIDE LIBRARIES
from typing import List

from fastapi import status

# PERSEPHONE
from src.domain.drive_wealth.employed_position import EmployedPosition
from src.domain.drive_wealth.employed_status import EmployedStatus
from src.domain.drive_wealth.employed_type import EmployedType
from src.repositories.sinacor_types.repository import SinacorTypesRepository
from src.repositories.user.enum.time_experience import TimeExperienceEnum


class SinaCorTypes:
    @staticmethod
    async def get_activity_type(sinacor_types_repository=SinacorTypesRepository):
        activities = await sinacor_types_repository.get_activity_type()
        activities_enum = SinaCorTypes.convert_description_to_title(activities)
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": activities_enum},
        }

    @staticmethod
    async def get_nationality(sinacor_types_repository=SinacorTypesRepository):
        nationalities = await sinacor_types_repository.get_nationality()
        nationalities_enum = SinaCorTypes.convert_description_to_title(nationalities)
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": nationalities_enum},
        }

    @staticmethod
    async def get_document_issuing_body(
        sinacor_types_repository=SinacorTypesRepository,
    ):
        issuing_body = await sinacor_types_repository.get_issuing_body()
        issuing_body_enum = SinaCorTypes.convert_description_to_title(issuing_body)
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": issuing_body_enum},
        }

    @staticmethod
    async def get_time_experience():
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "enums": [
                    {"code": TimeExperienceEnum.NONE.value, "value": "N/D"},
                    {
                        "code": TimeExperienceEnum.ONE_TO_TWO_YEARS.value,
                        "value": "1 a 2 anos",
                    },
                    {
                        "code": TimeExperienceEnum.THREE_TO_FIVE_YEARS.value,
                        "value": "3 a 5 anos",
                    },
                    {
                        "code": TimeExperienceEnum.FIVE_TO_TEN_YEARS.value,
                        "value": "5 a 10 anos",
                    },
                    {
                        "code": TimeExperienceEnum.OVER_TEN_YEARS.value,
                        "value": "Mais de 10 anos",
                    },
                ]
            },
        }

    @staticmethod
    async def get_employ_status():
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "enums": [
                    {"code": EmployedStatus.EMPLOYED.value, "value": "EMPREGADO(A)"},
                    {"code": EmployedStatus.RETIRED.value, "value": "APOSENTADO(A)"},
                    {"code": EmployedStatus.STUDENT.value, "value": "ALUNO(A)"},
                    {
                        "code": EmployedStatus.UNEMPLOYED.value,
                        "value": "DESEMPREGADO(A)",
                    },
                    {
                        "code": EmployedStatus.SELF_EMPLOYED.value,
                        "value": "TRABALHADOR(A) POR CONTA PRÓPRIA",
                    },
                ]
            },
        }

    @staticmethod
    async def get_employ_type():
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "enums": [
                    {"code": EmployedType.AGRICULTURE.value, "value": "AGRICULTURA"},
                    {"code": EmployedType.MINING.value, "value": "MINERAÇÃO"},
                    {
                        "code": EmployedType.UTILITIES.value,
                        "value": "SERVIÇOS DE UTILIDADE PÚBLICA",
                    },
                    {"code": EmployedType.CONSTRUCTION.value, "value": "CONSTRUÇÃO"},
                    {"code": EmployedType.MANUFACTURING.value, "value": "FABRICAÇÃO"},
                    {"code": EmployedType.WHOLESALE.value, "value": "ATACADO"},
                    {"code": EmployedType.RETAIL.value, "value": "RETALHO"},
                    {"code": EmployedType.TRANSPORT.value, "value": "TRANSPORTE"},
                    {"code": EmployedType.INFORMATION.value, "value": "EM FORMAÇÃO"},
                    {"code": EmployedType.FINANCE.value, "value": "FINANÇA"},
                    {"code": EmployedType.REAL_ESTATE.value, "value": "IMOBILIÁRIA"},
                    {"code": EmployedType.PROFESSIONAL.value, "value": "PROFISSIONAL"},
                    {"code": EmployedType.MANAGEMENT.value, "value": "GERENCIAMENTO"},
                    {"code": EmployedType.EDUCATION.value, "value": "EDUCAÇÃO"},
                    {"code": EmployedType.HEALTH.value, "value": "SAÚDE"},
                    {"code": EmployedType.ART.value, "value": "ARTE"},
                    {"code": EmployedType.FOOD.value, "value": "COMIDA"},
                    {"code": EmployedType.PUBLIC.value, "value": "PÚBLICO"},
                    {"code": EmployedType.WASTE.value, "value": "DESPERDÍCIO"},
                ]
            },
        }

    @staticmethod
    async def get_employ_position():
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "enums": [
                    {"code": EmployedPosition.ACCOUNTANT.value, "value": "CONTADOR"},
                    {"code": EmployedPosition.ACTUARY.value, "value": "ATUÁRIO"},
                    {"code": EmployedPosition.ADJUSTER.value, "value": "AJUSTADOR"},
                    {
                        "code": EmployedPosition.ADMINISTRATOR.value,
                        "value": "ADMINISTRADOR",
                    },
                    {"code": EmployedPosition.ADVERTISER.value, "value": "ANUNCIANTE"},
                    {"code": EmployedPosition.AGENT.value, "value": "AGENTE"},
                    {"code": EmployedPosition.ATC.value, "value": "ATC"},
                    {"code": EmployedPosition.AMBASSADOR.value, "value": "EMBAIXADOR"},
                    {"code": EmployedPosition.ANALYST.value, "value": "ANALISTA"},
                    {"code": EmployedPosition.APPRAISER.value, "value": "AVALIADOR"},
                    {"code": EmployedPosition.ARCHITECT.value, "value": "ARQUITETO"},
                    {"code": EmployedPosition.ARTIST.value, "value": "ARTISTA"},
                    {"code": EmployedPosition.ASSISTANT.value, "value": "ASSISTENTE"},
                    {"code": EmployedPosition.ATHLETE.value, "value": "ATLETA"},
                    {"code": EmployedPosition.ATTENDANT.value, "value": "ASSISTENTE"},
                    {"code": EmployedPosition.ATTORNEY.value, "value": "ADVOGADO"},
                    {"code": EmployedPosition.AUCTIONEER.value, "value": "LEILOEIRO"},
                    {"code": EmployedPosition.AUDITOR.value, "value": "AUDITOR"},
                    {"code": EmployedPosition.BARBER.value, "value": "BARBEIRO"},
                    {"code": EmployedPosition.BROKER.value, "value": "CORRETOR"},
                    {
                        "code": EmployedPosition.BUSINESS_EXEC.value,
                        "value": "BUSINESS_EXEC",
                    },
                    {
                        "code": EmployedPosition.BUSINESS_OWNER.value,
                        "value": "DONO DO NEGÓCIO",
                    },
                    {"code": EmployedPosition.CAREGIVER.value, "value": "CUIDADOR"},
                    {"code": EmployedPosition.CARPENTER.value, "value": "CARPINTEIRO"},
                    {"code": EmployedPosition.CASHIER.value, "value": "CAIXA"},
                    {"code": EmployedPosition.CHEF.value, "value": "CHEFE DE COZINHA"},
                    {
                        "code": EmployedPosition.CHIROPRACTOR.value,
                        "value": "QUIROPRÁTICO",
                    },
                    {"code": EmployedPosition.CIVIL.value, "value": "CIVIL"},
                    {"code": EmployedPosition.CLERGY.value, "value": "CLERO"},
                    {"code": EmployedPosition.CLERK.value, "value": "ATENDENTE"},
                    {
                        "code": EmployedPosition.COMPLIANCE.value,
                        "value": "CONFORMIDADE",
                    },
                    {"code": EmployedPosition.CONSULTANT.value, "value": "CONSULTOR"},
                    {"code": EmployedPosition.CONTRACTOR.value, "value": "CONTRATANTE"},
                    {"code": EmployedPosition.COUNSELOR.value, "value": "CONSELHEIRO"},
                    {
                        "code": EmployedPosition.CUSTOMER_SERVICE.value,
                        "value": "ATENDIMENTO AO CLIENTE",
                    },
                    {"code": EmployedPosition.DEALER.value, "value": "DISTRIBUIDOR"},
                    {
                        "code": EmployedPosition.DEVELOPER.value,
                        "value": "DESENVOLVEDOR",
                    },
                    {
                        "code": EmployedPosition.DISTRIBUTOR.value,
                        "value": "DISTRIBUIDOR",
                    },
                    {"code": EmployedPosition.DOCTOR.value, "value": "DOUTOR"},
                    {"code": EmployedPosition.DRIVER.value, "value": "MOTORISTA"},
                    {"code": EmployedPosition.ENGINEER.value, "value": "ENGENHEIRO"},
                    {"code": EmployedPosition.EXAMINER.value, "value": "EXAMINADOR"},
                    {
                        "code": EmployedPosition.EXTERMINATOR.value,
                        "value": "EXTERMINADOR",
                    },
                    {"code": EmployedPosition.FACTORY.value, "value": "FÁBRICA"},
                    {"code": EmployedPosition.FARMER.value, "value": "AGRICULTOR"},
                    {"code": EmployedPosition.FINANCIAL.value, "value": "FINANCEIRO"},
                    {"code": EmployedPosition.FISHERMAN.value, "value": "PESCADOR"},
                    {"code": EmployedPosition.FLIGHT.value, "value": "VOAR"},
                    {"code": EmployedPosition.HR.value, "value": "RH"},
                    {"code": EmployedPosition.IMPEX.value, "value": "IMPEX"},
                    {"code": EmployedPosition.INSPECTOR.value, "value": "INSPETOR"},
                    {"code": EmployedPosition.INTERN.value, "value": "ESTÁGIO"},
                    {
                        "code": EmployedPosition.INVESTMENT.value,
                        "value": "INVESTIMENTO",
                    },
                    {"code": EmployedPosition.INVESTOR.value, "value": "INVESTIDOR"},
                    {"code": EmployedPosition.IT.value, "value": "ISTO"},
                    {"code": EmployedPosition.JANITOR.value, "value": "ZELADOR"},
                    {"code": EmployedPosition.JEWELER.value, "value": "JOALHEIRO"},
                    {"code": EmployedPosition.LABORER.value, "value": "TRABALHADOR"},
                    {"code": EmployedPosition.LANDSCAPER.value, "value": "PAISAGISTA"},
                    {"code": EmployedPosition.LENDING.value, "value": "EMPRÉSTIMO"},
                    {"code": EmployedPosition.MANAGER.value, "value": "GERENTE"},
                    {"code": EmployedPosition.MECHANIC.value, "value": "MECÂNICO"},
                    {"code": EmployedPosition.MILITARY.value, "value": "MILITARES"},
                    {"code": EmployedPosition.MORTICIAN.value, "value": "FUNCIONÁRIO"},
                    {"code": EmployedPosition.NURSE.value, "value": "ENFERMEIRA"},
                    {
                        "code": EmployedPosition.NUTRITIONIST.value,
                        "value": "NUTRICIONISTA",
                    },
                    {"code": EmployedPosition.OFFICE.value, "value": "ESCRITÓRIO"},
                    {
                        "code": EmployedPosition.PHARMACIST.value,
                        "value": "FARMACÊUTICO",
                    },
                    {"code": EmployedPosition.PHYSICAL.value, "value": "FÍSICO"},
                    {"code": EmployedPosition.PILOT.value, "value": "PILOTO"},
                    {"code": EmployedPosition.POLICE.value, "value": "POLÍCIA"},
                    {"code": EmployedPosition.POLITICIAN.value, "value": "POLÍTICO"},
                    {"code": EmployedPosition.PM.value, "value": "PM"},
                    {"code": EmployedPosition.REP.value, "value": "REP"},
                    {
                        "code": EmployedPosition.RESEARCHER.value,
                        "value": "INVESTIGADOR",
                    },
                    {"code": EmployedPosition.SAILOR.value, "value": "MARINHEIRO"},
                    {"code": EmployedPosition.SALES.value, "value": "VENDAS"},
                    {"code": EmployedPosition.SCIENTIST.value, "value": "CIENTISTA"},
                    {"code": EmployedPosition.SEAMSTRESS.value, "value": "COSTUREIRA"},
                    {"code": EmployedPosition.SECURITY.value, "value": "SEGURANÇA"},
                    {"code": EmployedPosition.SOCIAL.value, "value": "SOCIAL"},
                    {"code": EmployedPosition.TEACHER.value, "value": "PROFESSORA"},
                    {"code": EmployedPosition.TECHNICIAN.value, "value": "TÉCNICO"},
                    {"code": EmployedPosition.TELLER.value, "value": "CAIXA"},
                    {
                        "code": EmployedPosition.TRADESPERSON.value,
                        "value": "COMERCIANTE",
                    },
                    {"code": EmployedPosition.TRAINER.value, "value": "TREINADOR"},
                    {
                        "code": EmployedPosition.TRANSPORTER.value,
                        "value": "TRANSPORTADOR",
                    },
                    {"code": EmployedPosition.UNDERWRITER.value, "value": "SEGURADOR"},
                    {"code": EmployedPosition.WRITER.value, "value": "ESCRITOR"},
                ]
            },
        }

    @staticmethod
    async def all_in_one(sinacor_types_repository=SinacorTypesRepository):
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {
                "activity_type": await sinacor_types_repository.get_activity_type(),
                "nationality": await sinacor_types_repository.get_nationality(),
                "document_issuing_body": await sinacor_types_repository.get_issuing_body(),
                "document_type": await sinacor_types_repository.get_document_type(),
                "country": await sinacor_types_repository.get_country(),
            },
        }

    @staticmethod
    async def get_document_type(sinacor_types_repository=SinacorTypesRepository):
        document_types = await sinacor_types_repository.get_document_type()
        document_types_enum = SinaCorTypes.convert_description_to_title(document_types)
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": document_types_enum},
        }

    @staticmethod
    async def get_city(payload: dict, sinacor_types_repository=SinacorTypesRepository):
        cities = await sinacor_types_repository.get_county(
            country=payload.get("country"), state=payload.get("state")
        )
        cities_enum = SinaCorTypes.convert_description_to_title(cities)
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": cities_enum},
        }

    @staticmethod
    async def get_state(payload: dict, sinacor_types_repository=SinacorTypesRepository):
        states = await sinacor_types_repository.get_state(
            country=payload.get("country")
        )
        states_enum = SinaCorTypes.convert_description_to_title(states)
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": states_enum},
        }

    @staticmethod
    async def get_country(sinacor_types_repository=SinacorTypesRepository):
        countries = await sinacor_types_repository.get_country()
        countries_enum = SinaCorTypes.convert_description_to_title(countries)
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": countries_enum},
        }

    @staticmethod
    async def get_gender(sinacor_types_repository=SinacorTypesRepository):
        genders = await sinacor_types_repository.get_gender()
        gender_enum = SinaCorTypes.convert_description_to_title(genders)
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": gender_enum},
        }

    @staticmethod
    async def get_marital_status(sinacor_types_repository=SinacorTypesRepository):
        marital_status = await sinacor_types_repository.get_marital_status()
        marital_status_enum = SinaCorTypes.convert_description_to_title(marital_status)
        return {
            "status_code": status.HTTP_200_OK,
            "payload": {"enums": marital_status_enum},
        }

    @staticmethod
    def convert_description_to_title(enum: List[dict]) -> List[dict]:
        titled_enum = [
            {"code": item["code"], "value": item["description"].title()}
            for item in enum
        ]
        return titled_enum
