# Índice

___

- [Sphinx](#sphinx)
    - [Iniciando o projeto](#iniciando-o-projeto)
        - [Passo 1](#passo-1)
        - [Passo 2](#passo-2)
        - [Passo 3](#passo-3)
        - [Passo 4](#passo-4)
    - [Endpoints](#endpoints)
        - [1. Authentication](#1-authentication)
        - [1.1. `thebes_hall`](#11-thebes_hall)
        - [1.2. `logout`](#12-logout)
        - [1.3. `validate_electronic_signature`](#13-validate_electronic_signature)
        - [1.4. `login`](#14-login)
        - [1.5. `thebes_gate`](#15-thebes_gate)
        - [2. Suitability](#2-suitability)
        - [2.1. `profile`](#21-profile)
        - [2.2. `profile`](#22-profile)
        - [2.2. `quiz`](#22-quiz)
        - [3. User](#3-user)
        - [3.1. `identifier_data`](#31-identifier_data)
        - [3.2. `complementary_data`](#32-complementary_data)
        - [3.3. `user`](#33-user)
        - [3.4. `user`](#34-user)
        - [3.5. `logout_all`](#35-logout_all)
        - [3.6. `views`](#36-views)
        - [3.7. `purchase`](#37-purchase)
        - [3.8. `purchase`](#38-purchase)
        - [3.9. `selfie`](#39-selfie)
        - [3.10. `document`](#310-document)
        - [3.11. `sign_terms`](#311-sign_terms)
        - [3.12. `signed_term`](#312-signed_term)
        - [3.13. `onboarding_user_current_step_br`](#313-onboarding_user_current_step_br)
        - [3.14. `onboarding_user_current_step_us`](#314-onboarding_user_current_step_us)
        - [3.15. `politically_exposed_us`](#315-politically_exposed_us)
        - [3.16. `exchange_member_us`](#316-exchange_member_us)
        - [3.17. `company_director_us`](#317-company_director_us)
        - [3.18. `time_experience_us`](#318-time_experience_us)
        - [3.19. `electronic_signature`](#319-electronic_signature)
        - [3.20. `forgot_electronic_signature`](#320-forgot_electronic_signature)
        - [3.21. `reset_electronic_signature`](#321-reset_electronic_signature)
        - [3.22. `change_electronic_signature`](#322-change_electronic_signature)
        - [3.23. `customer_registration_data`](#323-customer_registration_data)
        - [3.24. `customer_registration_data`](#324-customer_registration_data)
        - [3.25. `customer_validation_data`](#325-customer_validation_data)
        - [3.26. `customer_validation_data`](#326-customer_validation_data)
        - [3.27. `user_admin`](#327-user_admin)
        - [3.28. `bank_accounts`](#328-bank_accounts)
        - [3.29. `bank_accounts`](#329-bank_accounts)
        - [3.30. `bank_accounts`](#330-bank_accounts)
        - [3.31. `bank_account`](#331-bank_account)
        - [3.32. `external_fiscal_tax`](#332-external_fiscal_tax)
        - [3.33. `external_fiscal_tax_confirmation`](#333-external_fiscal_tax_confirmation)
        - [3.34. `employ_for_us`](#334-employ_for_us)
        - [3.35. `w8_form`](#335-w8_form)
        - [3.36. `w8_form_confirmation`](#336-w8_form_confirmation)
        - [4. Client update enums](#4-client-update-enums)
        - [4.1. `gender`](#41-gender)
        - [4.2. `document_type`](#42-document_type)
        - [4.3. `marital_status`](#43-marital_status)
        - [4.4. `nationality`](#44-nationality)
        - [4.5. `city`](#45-city)
        - [4.6. `state`](#46-state)
        - [4.7. `country`](#47-country)
        - [4.8. `activity_type`](#48-activity_type)
        - [4.9. `issuing_body`](#49-issuing_body)
        - [4.10. `time_experience_us`](#410-time_experience_us)
        - [5. Client register enums](#5-client-register-enums)
        - [5.1. `city`](#51-city)
        - [5.2. `state`](#52-state)
        - [5.3. `nationality`](#53-nationality)
        - [5.4. `document_type`](#54-document_type)
        - [5.5. `country`](#55-country)
        - [5.6. `activity_type`](#56-activity_type)
        - [5.7. `document_issuing_body`](#57-document_issuing_body)
        - [5.8. `all_in_one`](#58-all_in_one)
        - [6. Features](#6-features)
        - [6.1. `feature`](#61-feature)
        - [6.2. `feature/[feature_id]`](#62-feature/[feature_id])
        - [6.3. `feature/[feature_id]`](#63-feature/[feature_id])
        - [6.4. `features`](#64-features)
        - [7. Views](#7-views)
        - [7.1. `view`](#71-view)
        - [7.2. `id/[view_id]`](#72-id/[view_id])
        - [7.3. `id/[view_id]`](#73-id/[view_id])
        - [7.4. `id/[view_id]`](#74-id/[view_id])
        - [7.5. `views`](#75-views)
        - [8. Views link](#8-views-link)
        - [8.1. `link_feature`](#81-link_feature)
        - [8.2. `link_feature`](#82-link_feature)
        - [8.3. `link`](#83-link)
        - [9. Term](#9-term)
        - [9.1. `term`](#91-term)
        - [10. Terms](#10-terms)
        - [10.1. `terms`](#101-terms)
    - [Criação de usuário](#criação-de-usuário)
    - [Erros e exceções](#erros-e-exceções)
        - [BadRequestError](#badrequesterror)
        - [UnauthorizedError](#unauthorizederror)
        - [ForbiddenError](#forbiddenerror)
        - [InternalServerError](#internalservererror)
        - [ExceptionError](#exceptionerror)
    - [Swagger](#swagger)
    
---

# Sphinx
#### _Projeto destinado a manter as informações dos usuários (usuário, cliente) e autenticar/autorizar o acesso aos demais serviços._

___

## Iniciando o projeto

### Passo 1
#### Criação do ambiente
Crie e inicie um virtual env para o projeto. 

- Para criar o ambiente virtual execute:
```bash
python3 -m venv env
```
- Para realizar a ativação execute:

    No Linux:
    ```bash
    source env/bin/activate
    ```
    No Windows:
    ```shell
    env\Scripts\activate.bat
    ```

### Passo 2
#### Instalação de dependências
1. __Instalar os pacotes no virtual env a partir do seguinte comando:__
    
    ```bash
    pip install -r requirements.txt --extra-index-url "https://nexus.sigame.com.br/repository/pypi/simple/"
    ```  
    O comando pedirá um usuário e senha, preencha-os e os pacotes serão instalados.


2. __Instalar as bibliotecas do Cliente Oracle no computador, para poder acessar o banco de dados.__
    
    Os arquivos de download estão disponíveis a partir desse link:
    ```
    https://www.oracle.com/database/technologies/instant-client.html
    ```
| __Observação:__ no caso de sistemas Ubuntu é recomendado fazer o download do arquivo `.rpm` e fazer a conversão para `.deb`. |
|------------------------------------------------------------------------------------------------------------------------------|

3. __Certificar-se que o pacote `libaio1` está instalado (em algumas distribuições Linux o pacote pode se chamar apenas `libaio`).__

    Para instalar o pacote no Ubuntu use o seguinte comando:
    ```bash
    sudo apt-get install libaio1
    ```

### Passo 3
#### Criação das variáveis de ambiente

1. Crie um arquivo `.env` no caminho `/opt/envs/sphinx.lionx.com.br/`, seguindo esse modelo:

~~~bash
COMPANY_OPERATION_CODE=FILL_THIS_WITH_VALUE

MONGO_CONNECTION_URL=FILL_THIS_WITH_VALUE
MONGODB_DATABASE_NAME=FILL_THIS_WITH_VALUE
MONGODB_FEATURE_COLLECTION=FILL_THIS_WITH_VALUE
MONGODB_USER_COLLECTION=FILL_THIS_WITH_VALUE
MONGODB_VIEW_COLLECTION=FILL_THIS_WITH_VALUE
MONGODB_JWT_COLLECTION=FILL_THIS_WITH_VALUE
MONGODB_SUITABILITY_COLLECTION=FILL_THIS_WITH_VALUE
MONGODB_SUITABILITY_USER_PROFILE_COLLECTION=FILL_THIS_WITH_VALUE
MONGODB_SUITABILITY_ANSWERS_COLLECTION=FILL_THIS_WITH_VALUE

MAIL_KEY=FILL_THIS_WITH_VALUE
MAIL_SENDER=FILL_THIS_WITH_VALUE
TARGET_LINK=FILL_THIS_WITH_VALUE

REDIS_HOST_URL=FILL_THIS_WITH_VALUE
REDIS_CACHE_DB=FILL_THIS_WITH_VALUE
REDIS_PORTFOLIO_DB=FILL_THIS_WITH_VALUE

AWS_ACCESS_KEY_ID=FILL_THIS_WITH_VALUE
AWS_SECRET_ACCESS_KEY=FILL_THIS_WITH_VALUE
REGION_NAME=FILL_THIS_WITH_VALUE
AWS_BUCKET_USERS_FILES=FILL_THIS_WITH_VALUE
AWS_BUCKET_USERS_SELF=FILL_THIS_WITH_VALUE
AWS_BUCKET_TERMS=FILL_THIS_WITH_VALUE

ORACLE_BASE_DSN=FILL_THIS_WITH_VALUE
ORACLE_USER=FILL_THIS_WITH_VALUE
ORACLE_PASSWORD=FILL_THIS_WITH_VALUE
ORACLE_SERVICE=FILL_THIS_WITH_VALUE
ORACLE_ENCODING=FILL_THIS_WITH_VALUE
ORACLE_PORT=FILL_THIS_WITH_VALUE
LD_LIBRARY_PATH=FILL_THIS_WITH_VALUE

PERSEPHONE_QUEUE_HOST=FILL_THIS_WITH_VALUE
PERSEPHONE_QUEUE_PORT=FILL_THIS_WITH_VALUE
PERSEPHONE_TOPIC=FILL_THIS_WITH_VALUE
PERSEPHONE_TOPIC_USER=FILL_THIS_WITH_VALUE
PERSEPHONE_TOPIC_AUTHENTICATION=FILL_THIS_WITH_VALUE

SOLUTIONTECH_BASE_URL=FILL_THIS_WITH_VALUE
SOLUTIONTECH_VERIFY_DTVM_CLIENT=FILL_THIS_WITH_VALUE
SOLUTIONTECH_SYNC_DTVM_CLIENT=FILL_THIS_WITH_VALUE

SPHINX_PORT=FILL_THIS_WITH_VALUE
ROOT_PATH=FILL_THIS_WITH_VALUE

JWT_FILE_BUCKET_NAME=FILL_THIS_WITH_VALUE
BUCKET_NAME_KEY=FILL_THIS_WITH_VALUE

DW_APP_KEY=FILL_THIS_WITH_VALUE
DW_USER=FILL_THIS_WITH_VALUE
DW_PASSWORD=FILL_THIS_WITH_VALUE
DW_IGNORE_MARKET_HOURS_FOR_TEST=FILL_THIS_WITH_VALUE
DW_AUTHENTICATION_URL=FILL_THIS_WITH_VALUE
DW_CREATE_USER_URL=FILL_THIS_WITH_VALUE
DW_USER_FILE_UPLOAD_URL=FILL_THIS_WITH_VALUE
DW_CREATE_ACCOUNT_URL=FILL_THIS_WITH_VALUE
DW_UPDATE_USER_URL=FILL_THIS_WITH_VALUE
DW_KYC_USER_URL=FILL_THIS_WITH_VALUE
DW_PARENT_IBID=FILL_THIS_WITH_VALUE
DW_WLP_ID=FILL_THIS_WITH_VALUE

VALHALLA_HOST=FILL_THIS_WITH_VALUE
VALHALLA_PORT=FILL_THIS_WITH_VALUE

DW_USER_PHYSICAL_DOCUMENTS_URL=FILL_THIS_WITH_VALUE
DW_USER_PHYSICAL_DOCUMENT_URL=FILL_THIS_WITH_VALUE
~~~

2. Crie outro arquivo `.env` no caminho `/opt/envs/mepho.lionx.com.br/`, seguindo esse modelo:

~~~bash
MEPHO_DW_APP_KEY=FILL_THIS_WITH_VALUE
MEPHO_DW_USER=FILL_THIS_WITH_VALUE
MEPHO_DW_PASSWORD=FILL_THIS_WITH_VALUE
MEPHO_DW_AUTHENTICATION_URL=FILL_THIS_WITH_VALUE
MEPHO_REDIS_HOST=FILL_THIS_WITH_VALUE
MEPHO_REDIS_DB=FILL_THIS_WITH_VALUE
~~~

3. Crie outro arquivo `.env` no caminho `/opt/envs/heimdall.lionx.com.br/`, seguindo esse modelo:

    ~~~bash
    HEIMDALL_FILE_BUCKET_NAME=FILL_THIS_WITH_VALUE
    HEIMDALL_AWS_ACCESS_KEY_ID=FILL_THIS_WITH_VALUE
    HEIMDALL_AWS_SECRET_ACCESS_KEY=FILL_THIS_WITH_VALUE
    HEIMDALL_REGION_NAME=FILL_THIS_WITH_VALUE
    HEIMDALL_BUCKET_NAME_KEY=FILL_THIS_WITH_VALUE
    HEIMDALL_AWS_BUCKET_USERS_FILES=FILL_THIS_WITH_VALUE
    HEIMDALL_AWS_BUCKET_TERMS=FILL_THIS_WITH_VALUE
    HEIMDALL_JWT_REQUIRED_FIELDS=FILL_THIS_WITH_VALUE
    HEIMDALL_REDIS_HOST=FILL_THIS_WITH_VALUE
    HEIMDALL_REDIS_PORT=FILL_THIS_WITH_VALUE
    HEIMDALL_REDIS_DB=FILL_THIS_WITH_VALUE
    HEIMDALL_REDIS_USER=FILL_THIS_WITH_VALUE
    HEIMDALL_REDIS_PASSWORD=FILL_THIS_WITH_VALUE
    ~~~
   
4. Crie outro arquivo `.env` no caminho `/opt/envs/mist.lionx.com.br/`, seguindo esse modelo:

    ~~~bash
    MIST_REDIS_HOST=FILL_THIS_WITH_VALUE
    MIST_REDIS_PORT=FILL_THIS_WITH_VALUE
    MIST_REDIS_DB=FILL_THIS_WITH_VALUE
    MIST_REDIS_USER=FILL_THIS_WITH_VALUE
    MIST_REDIS_PASSWORD=FILL_THIS_WITH_VALUE
    MIST_AWS_ACCESS_KEY_ID=FILL_THIS_WITH_VALUE
    MIST_AWS_SECRET_ACCESS_KEY=FILL_THIS_WITH_VALUE
    MIST_REGION_NAME=FILL_THIS_WITH_VALUE
    MIST_BUCKET_NAME_KEY=FILL_THIS_WITH_VALUE
    MIST_JWT_FILE_BUCKET_NAME=FILL_THIS_WITH_VALUE
    MIST_ELECTRONIC_SIGNATURE_FILE_BUCKET_NAME=FILL_THIS_WITH_VALUE
    MIST_JWT_REQUIRED_FIELDS=FILL_THIS_WITH_VALUE
    MIST_MONGODB_CONNECTION=FILL_THIS_WITH_VALUE
    MIST_AUTH_DATABASE_NAME=FILL_THIS_WITH_VALUE
    MIST_AUTH_DATABASE_USER_COLLECTION=FILL_THIS_WITH_VALUE
    MIST_ELECTRONIC_SIGNATURE_MAX_ATTEMPTS=FILL_THIS_WITH_VALUE
    MIST_ENCRYPT_KEY=FILL_THIS_WITH_VALUE
    LOG_NAME=FILL_THIS_WITH_VALUE
    ~~~

5. Crie um arquivo `.env` no caminho `/opt/envs/persephone.client.python.lionx.com.br/`, seguindo esse modelo:

    ~~~bash
    PERSEPHONE_KAFKA_BROKERS=FILL_THIS_WITH_VALUE
    ~~~
   
6. Crie um arquivo `.env` no caminho `/opt/envs/etria.python.lionx.com.br/`, seguindo esse modelo:

    ~~~bash
    ROOT_LOG_LEVEL=INFO
    ETRIA_LOG_LEVEL=INFO
    ~~~

### Passo 4
Rodar o arquivo `main.py` para iniciar o projeto.

___

## Endpoints
O projeto possui os seguintes endpoints, listados abaixo por tópicos:


### 1. Authentication
> Endpoints para a validação de assinatura eletrônica do usuário, e inciar e finalizar a sessão.

### 1.1. `thebes_hall`
- Rota HTTP: `| PUT | http://localhost:8000/thebes_hall`
> _Faz a validação de uma sessão do usuário._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/thebes_hall
```

#### Modelo de corpo da requisição:
```json
{
  "device_name": "Android SDK built for x86",
  "device_model": "Android SDK built for x86",
  "is_emulator": true,
  "device_operating_system_name": "Android",
  "os_sdk_version": 30,
  "device_is_in_root_mode": true,
  "device_network_interfaces": "wifi",
  "public_ip": "10.0.2.16",
  "phone_wifi_ip": "10.0.2.2",
  "geolocation": "Rua Porto União, 295, Itaim Bibi, São Paulo - SP, 04568-020, Brasil"
}
```

#### Modelo de resposta:

~~~json
{
    "jwt": "TOKEN JWT",
    "control_data": {
        "is_blocked_electronic_signature": false,
        "using_suitability_or_refuse_term": "suitability",
        "last_modified_date_months_past": 1,
        "suitability_months_past": 1,
        "terms": [
            {
                "name": "term_application"
            },
            {
                "name": "term_open_account"
            },
            {
                "name": "term_refusal"
            },
            {
                "name": "term_non_compliance"
            },
            {
                "name": "term_retail_liquid_provider"
            },
            {
                "name": "term_open_account_dw"
            },
            {
                "name": "term_application_dw"
            },
            {
                "name": "term_privacy_policy_dw"
            },
            {
                "name": "term_data_sharing_policy_dw"
            }
        ]
    }
}
~~~

&nbsp;

### 1.2. `logout`
- Rota HTTP: `| PUT | http://localhost:8000/logout`
> _Faz logout da conta no dispositivo._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/logout
```

#### Modelo de corpo da requisição:
```json
{
  "device_name": "Android SDK built for x86",
  "device_model": "Android SDK built for x86",
  "is_emulator": true,
  "device_operating_system_name": "Android",
  "os_sdk_version": 30,
  "device_is_in_root_mode": true,
  "device_network_interfaces": "wifi",
  "public_ip": "10.0.2.16",
  "phone_wifi_ip": "10.0.2.2",
  "geolocation": "Rua Porto União, 295, Itaim Bibi, São Paulo - SP, 04568-020, Brasil"
}
```

#### Modelo de resposta:
~~~json
{
    "message": "Logout saved."
}
~~~

&nbsp; 

### 1.3. `validate_electronic_signature`
- Rota HTTP: `| POST | http://localhost:8000/validate_electronic_signature`
> _Valida a assinatura eletrônica do usuário e cria um token de assinatura eletrônica (token de sessão de trade)._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição       |
|------------------|-----------------|
| `SEM PARAMETROS` | SEM PARAMETROS  |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/validate_electronic_signature
```

#### Corpo da requisição:
```json
{
    "signature": "senha123",
    "signature_expire_time": 999999999999
}
```
#### Modelo de resposta:

~~~json
{
    "created": true,
    "jwt_token_session": "TOKEN DA SESSÃo",
    "message": "Session created with success"
}
~~~

&nbsp; 

### 1.4. `login`
- Rota HTTP: `| POST | http://localhost:8000/login`
> _Envia um email para confirmar o email de cadastro do usuário._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição       |
|------------------|-----------------|
| `SEM PARAMETROS` | SEM PARAMETROS  |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/login
```

#### Corpo da requisição

```json
{
    "email": "email@lionx.com.br"
}
```

#### Modelo de resposta:

~~~json
{
    "message": "We sent an email to the registered account, to conclude login"
}
~~~

&nbsp; 

### 1.5. `thebes_gate`
- Rota HTTP: `| GET | http://localhost:8000/thebes_gate`
> _Cria uma sessão para o usuário e retorna um token de sessão._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/thebes_gate
```

#### Modelo de resposta:
~~~json
{
    "jwt": "TOKEN JWT",
    "control_data": {
        "is_blocked_electronic_signature": false,
        "using_suitability_or_refuse_term": "suitability",
        "last_modified_date_months_past": 1,
        "suitability_months_past": 1,
        "terms": [
            {
                "name": "term_application"
            },
            {
                "name": "term_open_account"
            },
            {
                "name": "term_refusal"
            },
            {
                "name": "term_non_compliance"
            },
            {
                "name": "term_retail_liquid_provider"
            },
            {
                "name": "term_open_account_dw"
            },
            {
                "name": "term_application_dw"
            },
            {
                "name": "term_privacy_policy_dw"
            },
            {
                "name": "term_data_sharing_policy_dw"
            }
        ]
    }
}
~~~

&nbsp;

### 2. Suitability
> _Endpoints para definir o "Perfil de Investidor" do cliente._

### 2.1. `profile`
- Rota HTTP: `| GET | http://localhost:8000/suitability/profile`
> _Retorna o perfil de investidor do usuário._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição      |
|------------------|----------------|
| `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/suitability/profile
```

#### Modelo de resposta:

~~~json
{
    "detail": [
        {
            "msg": "Proccesses error."
        }
    ]
}
~~~

&nbsp;

### 2.2. `profile`
- Rota HTTP: `| POST | http://localhost:8000/suitability/profile`
> _Cria o perfil de investidor do usuário._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição      |
|------------------|----------------|
| `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/suitability/profile
```

#### Modelo de resposta:

~~~json
{
    "jwt": "TOKEN-JWT",
    "control_data": {
        "is_blocked_electronic_signature": false,
        "using_suitability_or_refuse_term": "suitability",
        "last_modified_date_months_past": 1,
        "suitability_months_past": 0,
        "terms": [
            {
                "name": "term_application"
            },
            {
                "name": "term_open_account"
            },
            {
                "name": "term_refusal"
            },
            {
                "name": "term_non_compliance"
            },
            {
                "name": "term_retail_liquid_provider"
            },
            {
                "name": "term_open_account_dw"
            },
            {
                "name": "term_application_dw"
            },
            {
                "name": "term_privacy_policy_dw"
            },
            {
                "name": "term_data_sharing_policy_dw"
            }
        ]
    }
}
~~~

&nbsp;

### 2.2. `quiz`
- Rota HTTP: `| POST | http://localhost:8000/suitability/quiz`
> _Envia os resultados do quiz para a identificação do perfil de investidor._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição      |
|------------------|----------------|
| `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/suitability/quiz
```

#### Modelo de corpo da requisição:
```json
{
    "version": 3,
    "questions": [
        {
            "value_text": "Quando você pretende utilizar os recursos investidos?",
            "score": 98,
            "order": 1,
            "answers": [
                {"value_text": "Em até 1 ano", "weight": 380},
                {"value_text": "De 1 a 2 anos", "weight": 381},
                {"value_text": "De 2 a 5 anos", "weight": 383},
                {"value_text": "Após 5 anos", "weight": 384}
            ]
        },
        {
            "value_text": "Em caso de uma eventual necessidade, suas reservas financeiras equivalem a quantos meses de suas despesas?",
            "score": 99,
            "order": 2,
            "answers": [
                {"value_text": "Não sei ou não possuo reservas", "weight": 385},
                {"value_text": "Até 6 meses", "weight": 386},
                {"value_text": "Entre 6 e 12 meses", "weight": 387},
                {"value_text": "Mais de 12 meses", "weight": 388}
            ]
        },
        {
            "value_text": "Quanto de seu patrimônio total (reservas financeiras, imóveis e outros bens) é destinado a investimentos financeiros?",
            "score": 100,
            "order": 3,
            "answers": [
                {"value_text": "Menos de 30%", "weight": 389},
                {"value_text": "Entre 30% e 60%", "weight": 390},
                {"value_text": "Mais de 60%", "weight": 391}
            ]
        },
        {
            "value_text": "Qual é o seu objetivo de investimento?",
            "score": 101,
            "order": 4,
            "answers": [
                {"value_text": "Preservar o capital, sem risco de perdas.", "weight": 392},
                {"value_text": "Obter rentabilidade equivalente a aplicações indexadas ao CDI, aceitando oscilações nos rendimentos.", "weight": 393},
                {"value_text": "Obter rentabilidade acima das aplicações indexadas ao CDI, aceitando oscilações do valor principal investido.", "weight": 394},
                {"value_text": "Obter rentabilidade elevada, aceitando o risco de expressivas oscilações do valor principal investido.", "weight": 395}
            ]
        },
        {
            "value_text": "Suponha que em um mês, seus investimentos se desvalorizem significativamente, por exemplo de R$ 50 mil para R$ 30 mil, o que você faria?",
            "score": 102,
            "order": 5,
            "answers": [
                {"value_text": "Resgataria o total investido imediatamente", "weight": 396},
                {"value_text": "Manteria os recursos aplicados aguardando uma recuperação", "weight": 397},
                {"value_text": "Aproveitaria para aplicar mais", "weight": 398}
            ]
        },
        {
            "value_text": "Indique os produtos que mais representam seu conhecimento e experiência com investimentos nos últimos 3 anos:",
            "score": 103,
            "order": 6,
            "answers": [
                {"value_text": "Poupança, CDB, LCI, LCA e/ou fundos DI;", "weight": 399},
                {"value_text": "Investimentos indicados na alternativa anterior + fundos Imobiliários, fundos Multimercados e/ou investimentos atrelados à inflação", "weight": 400},
                {"value_text": "Investimentos indicados nas alternativas anteriores + Ações, fundos de Ações e/ou fundos Cambiais", "weight": 401},
                {"value_text": "Investimentos indicados nas alternativas anteriores +  derivativos e/ou COE", "weight": 402}
            ]
        },
        {
            "value_text": "Considerando sua experiência com investimentos, formação acadêmica e experiência profissional, como você define seu conhecimento sobre mercado o financeiro?",
            "score": 104,
            "order": 7,
            "answers": [
                {"value_text": "Pouco ou nenhum", "weight": 403},
                {"value_text": "Possuo conhecimento sobre aplicações indexadas ao CDI", "weight": 404},
                {"value_text": "Conheço os principais produtos, de renda fixa a ações, e já investi em alguns ou vários deles", "weight": 405}
            ]
        }
    ]
}
```
#### Modelo de resposta:

~~~json
{
    "message": "Suitability was been saved successfully"
}
~~~

&nbsp;

### 3. User
> _Endpoints para a realização do cadastro de clientes, e atualizações dos dados cadastrais._  

### 3.1. `identifier_data`
- Rota HTTP: `| PUT | http://localhost:8000/user/identifier_data`
> _Atualiza os dados de identificação do usuário._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro         | Descrição      |
|-------------------|----------------|
|  `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/identifier_data`
```

#### Modelo de corpo da requisição:
```json
{
    "cpf": "1234567890",
    "phone": "+551140028922",
    "tax_residences": [
        {
            "country": "USA",
            "tax_number": "1212-012"
        },
        {
            "country": "CHE",
            "tax_number": "1212-012"
        }
    ]
}
```

#### Modelo de resposta:

~~~json
{
    "detail": [
        {
            "msg": "Invalid on boarding step, check your current step on /user/onboarding_user_current_step"
        }
    ]
}
~~~

&nbsp;

### 3.2. `complementary_data`
- Rota HTTP: `| PUT | http://localhost:8000/user/complementary_data`
> _Atualiza os dados complementares do usuário._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro          | Descrição        |
|--------------------|------------------|
| `SEM PARÂMETROS`   | SEM PARÂMETROS   |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/complementary_data
```

#### Modelo de corpo da requisição:
```json
{
    "marital_status": 1,
    "spouse": {
        "name": "Antonia Gererate",
        "cpf": "37141144676",
        "nationality": 1
    }
}
```

#### Modelo de resposta:
~~~json
{
    "detail": [
        {
            "msg": "Invalid on boarding step, check your current step on /user/onboarding_user_current_step"
        }
    ]
}
~~~

&nbsp;

### 3.3. `user`
- Rota HTTP: `| POST | http://localhost:8000/user`
> _Cria um novo usuário com um email._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição      |
|-----------------|----------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO  |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user
```

#### Modelo de corpo da requisição:
```json
{
    "nick_name": "User",
    "email": "email@lionx.com.br"
}
```

#### Modelo de resposta:
```json
{
    "detail": [
        {
            "msg": "Register alredy exists."
        }
    ]
}
```

&nbsp;

### 3.4. `user`
- Rota HTTP: `| DELETE | http://localhost:8000/user`
> _Deleta um usuário pelo JWT no cabeçalho da requisição._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição      |
|------------------|----------------|
| `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user
```

#### Modelo de resposta:

~~~json
{"detail": [{"msg": "User don't have permition to access this route or feature."}]}
~~~

&nbsp;

### 3.5. `logout_all`
- Rota HTTP: `| PUT | http://localhost:8000/user/logout_all`
> _Faz logout da conta em todos os dispositivos._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição      |
|------------------|----------------|
| `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/logout_all
```

#### Modelo de resposta:
~~~json
{
    "message": "You disconnect all your allowed devices."
}
~~~

&nbsp;

### 3.6. `views`
- Rota HTTP: `| PUT | http://localhost:8000/user/views`
> _Altera a view da conta do usuário._
> 
> _**Observação:** ver o tópico `6. Views` para mais detalhes._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição      |
|------------------|----------------|
| `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/views
```

#### Modelo de corpo da requisição:
```json
{
    "view": "lite"
}
```

#### Modelo de resposta:

~~~json
{"detail": [{"msg": "User don't have permition to access this route or feature."}]}
~~~

&nbsp;

### 3.7. `purchase`
- Rota HTTP: `| PUT | http://localhost:8000/user/purchase`
> _Adiciona views ao usuário._
> 
> _**Observação:** para mais detalhes ver tópico `7. Views`._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição      |
|------------------|----------------|
| `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/purchase
```

#### Modelo de corpo da requisição:
```json
{
  "name": "Purchase",
  "display_name": "Purchase"
}
```
#### Modelo de resposta:

~~~json
{"detail": [{"msg": "User don't have permition to access this route or feature."}]}
~~~

&nbsp;

### 3.8. `purchase`
- Rota HTTP: `| DELETE | http://localhost:8000/user/purchase`
> _Remove views do usuário._
> 
> _**Observação:** para mais detalhes ver tópico `7. Views`._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição      |
|------------------|----------------|
| `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/purchase
```

#### Modelo de corpo da requisição:
```json
{
  "name": "Purchase",
  "display_name": "Purchase"
}
```
#### Modelo de resposta:

~~~json
{"detail": [{"msg": "User don't have permition to access this route or feature."}]}
~~~

&nbsp;

### 3.9. `selfie`
- Rota HTTP: `| POST | http://localhost:8000/user/selfie`
> _Envia a selifie do usuário._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição      |
|------------------|----------------|
| `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/selfie
```

#### Modelo de corpo da requisição:
```json
{
    "file_or_base64": "IMAGEM EM BASE64"
}
```

#### Modelo de resposta:

~~~json
{
    "detail": [
        {
            "msg": "Invalid on boarding step, check your current step on /user/onboarding_user_current_step"
        }
    ]
}
~~~

&nbsp;

### 3.10. `document`
- Rota HTTP: `| POST | http://localhost:8000/user/document`
> _Envia as fotos de frente e verso do documento usado no cadastro do usuário._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição      |
|------------------|----------------|
| `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/document
```

#### Modelo de corpo da requisição:
```json
{
    "document_front": "IMAGEM EM BASE64",
    "document_back": "IMAGEM EM BASE64"
}
```

#### Modelo de resposta:
~~~json
{
    "detail": [
        {
            "msg": "Invalid on boarding step, check your current step on /user/onboarding_user_current_step"
        }
    ]
}
~~~

&nbsp;

### 3.11. `sign_terms`
- Rota HTTP: `| PUT | http://localhost:8000/user/sign_terms`
> _Faz o aceite de algum termo de uso._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição      |
|------------------|----------------|
| `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/sign_terms
```

#### Modelo de corpo da requisição:
```json
{
    "file_types": [

        "term_refusal"
    ]
}
```

#### Modelo de resposta:

~~~json
{
    "jwt": "TOKEN JWT",
    "control_data": {
        "is_blocked_electronic_signature": false,
        "using_suitability_or_refuse_term": "term_refusal",
        "last_modified_date_months_past": 1,
        "suitability_months_past": 0,
        "terms": [
            {
                "name": "term_application"
            },
            {
                "name": "term_open_account"
            },
            {
                "name": "term_refusal",
                "version": 4,
                "date": 1651095506.213,
                "is_deprecated": false
            },
            {
                "name": "term_non_compliance"
            },
            {
                "name": "term_retail_liquid_provider"
            },
            {
                "name": "term_open_account_dw"
            },
            {
                "name": "term_application_dw"
            },
            {
                "name": "term_privacy_policy_dw"
            },
            {
                "name": "term_data_sharing_policy_dw"
            }
        ]
    }
}
~~~

&nbsp;

### 3.12. `signed_term`
- Rota HTTP: `| GET | http://localhost:8000/user/signed_term`
> _Retorna o link para o PDF de um termo que já foi assinado._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro    | Descrição                  |
|--------------|----------------------------|
| `file_type`  | Termo para retornar o PDF. |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/signed_term?file_type=term_refusal
```

#### Modelo de resposta:

~~~json
{
    "link": "https://dtvm-terms-dev.s3.amazonaws.com/term_refusal/term_refusal_v4.pdf?Id"
}
~~~

&nbsp;

### 3.13. `onboarding_user_current_step_br`
- Rota HTTP: `| GET | http://localhost:8000/user/onboarding_user_current_step_br`
> _Retorna o estado das etapas de conclusão do cadastro para operar no Brasil._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/onboarding_user_current_step_br
```

#### Modelo de resposta:

~~~json
{
    "current_onboarding_step": "finished",
    "suitability_step": true,
    "user_identifier_data_step": true,
    "user_selfie_step": true,
    "user_complementary_step": true,
    "user_document_validator": true,
    "user_data_validation": true,
    "user_electronic_signature": true,
    "finished": true
}
~~~

&nbsp;

### 3.14. `onboarding_user_current_step_us`
- Rota HTTP: `| GET | http://localhost:8000/user/onboarding_user_current_step_us`
> _Retorna o estado das etapas de conclusão do cadastro para operar nos Estados Unidos._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/onboarding_user_current_step_us
```

#### Modelo de resposta:

~~~json
{
    "current_onboarding_step": "terms_step",
    "terms_step": false,
    "user_document_validator_step": false,
    "is_politically_exposed_step": false,
    "is_exchange_member_step": false,
    "is_company_director_step": false,
    "time_experience_step": false,
    "finished": false
}
~~~

&nbsp;

### 3.15. `politically_exposed_us`
- Rota HTTP: `| PUT | http://localhost:8000/user/politically_exposed_us`
> _Atualiza o dado de "Politicamente Exposto" no cadastro do cliente nos Estados Unidos.
> Caso o campo `is_politically_exposed` seja verdadeiro, devem ser preenchidos os nomes das pessoas politicamente
> expostas no campo `politically_exposed_names`._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/politically_exposed_us
```

#### Modelo de corpo da requisição:
```json
{
  "is_politically_exposed": true,
  "politically_exposed_names": [
    "Joao"
  ]
}
```

#### Modelo de resposta:

~~~json
{
    "message": "Register Updated."
}
~~~

&nbsp;

### 3.16. `exchange_member_us`
- Rota HTTP: `| PUT | http://localhost:8000/user/exchange_member_us`
> _Atualiza o dado de "membro de uma corretora" no cadastro do cliente nos Estados Unidos._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/exchange_member_us
```

#### Modelo de corpo da requisição:
```json
{
    "is_exchange_member": false
}
```

#### Modelo de resposta:

~~~json
{
    "message": "Register Updated."
}
~~~

&nbsp;

### 3.17. `company_director_us`
- Rota HTTP: `| PUT | http://localhost:8000/user/company_director_us`
> _Atualiza o dado de "diretor de alguma empresa" no cadastro do cliente nos Estados Unidos.
> Caso seja diretor deve informar o nome da empresa e, se estiver presente na bolsa, o Ticker da ação._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/company_director_us
```

#### Modelo de corpo da requisição:
```json
{
    "is_company_director": true,
    "company_name": "Lalau",
    "company_ticker": "LALA4"
}
```

#### Modelo de resposta:

~~~json
{
    "message": "Register Updated."
}
~~~

&nbsp;

### 3.18. `time_experience_us`
- Rota HTTP: `| PUT | http://localhost:8000/user/time_experience_us`
> _Atualiza o dado de "Time Experience" no cadastro do cliente nos Estados Unidos._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/time_experience_us
```

#### Modelo de corpo da requisição:
```json
{
    "time_experience": "YRS_1_2"
}
```

#### Modelo de resposta:
~~~json
{
    "detail": [
        {
            "msg": "We have some issue, please try again."
        }
    ]
}
~~~

&nbsp;

### 3.19. `electronic_signature`
- Rota HTTP: `| PUT | http://localhost:8000/user/electronic_signature`
> _Registra a senha do usuário._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/electronic_signature
```

#### Modelo de corpo da requisição:
```json
{
    "electronic_signature": "Abc123456789"
}
```

#### Modelo de resposta:
~~~json
{
    "message": "Register Updated."
}
~~~

&nbsp;

### 3.20. `forgot_electronic_signature`
- Rota HTTP: `| GET | http://localhost:8000/user/forgot_electronic_signature`
> _Envia um email para a redefinição da senha._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/forgot_electronic_signature
```

#### Modelo de resposta:

~~~json
{
    "message": "We sent an email to login and change your electrionic signature"
}
~~~

&nbsp;

### 3.21. `reset_electronic_signature`
- Rota HTTP: `| PUT | http://localhost:8000/user/reset_electronic_signature`
> _Reseta a senha de um usuário e insere outra._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/reset_electronic_signature
```

#### Modelo de corpo da requisição:
```json
{
    "electronic_signature": "Abc123456789"
}
```

#### Modelo de resposta:
~~~json
{
    "detail": [
        {
            "msg": "User don't have permition to access this route or feature."
        }
    ]
}
~~~

&nbsp;

### 3.22. `change_electronic_signature`
- Rota HTTP: `| PUT | http://localhost:8000/user/change_electronic_signature`
> _Altera a senha do usuário._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
{
    "electronic_signature": "Abc123456789",
    "new_electronic_signature": "Abc123456789"
}
```

#### Modelo de resposta:
~~~json
{
    "message": "Register Updated."
}
~~~

&nbsp;

### 3.23. `customer_registration_data`
- Rota HTTP: `| GET | http://localhost:8000/user/customer_registration_data`
> _Pega os dados de cadastro de um usuário pelo token JWT do cabeçalho da requisição._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição      |
|------------------|----------------|
| `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/customer_registration_data
```

#### Modelo de resposta:
~~~json
{
    "personal": {
        "name": "Teste Almeida",
        "nick_name": "RAST3",
        "birth_date": 750135600.0,
        "gender": "M",
        "father_name": "Arge Ferreira",
        "mother_name": "Vani Silva",
        "email": "email@lionx.com.br",
        "cel_phone": "11952945942",
        "nationality": 1,
        "occupation_activity": 101,
        "company_name": "LionX",
        "company_cnpj": "36923006000188",
        "patrimony": 200000.0,
        "income": 200000.0,
        "tax_residences": [
            {
                "country": "AUT",
                "tax_number": "1212-012"
            },
            {
                "country": "CHE",
                "tax_number": "1212-012"
            }
        ],
        "birth_place_country": "BRA",
        "birth_place_city": 5150,
        "birth_place_state": "SP"
    },
    "marital": {
        "spouse": {
            "spouse_name": "Antonia Gererate",
            "spouse_cpf": "53845387084",
            "nationality": "1"
        },
        "status": 1
    },
    "documents": {
        "cpf": "58038116020",
        "identity_type": "RG",
        "identity_number": "385722594",
        "expedition_date": 1552867200.0,
        "issuer": "SSP",
        "state": "SP"
    },
    "address": {
        "country": "BRA",
        "number": 153,
        "street_name": "RUA IMBUIA",
        "city": 5150,
        "neighborhood": "CIDADE DAS FLORES",
        "zip_code": "06184110",
        "state": "SP",
        "phone": null
    },
    "external_exchange_account_us": {}
}
~~~

&nbsp;

### 3.24. `customer_registration_data`
- Rota HTTP: `| PUT | http://localhost:8000/user/customer_registration_data`
> _Atualiza os dados cadastrais de um usuário._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição      |
|------------------|----------------|
| `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/customer_registration_data
```

#### Modelo de corpo da requisição:
```json
{
    "personal": {
        "name": {
            "value": "Sr Teste",
            "source": "app"
        }
    }
}
```

#### Modelo de resposta:

~~~json
{
    "detail": [
        {
            "msg": "We have some issue, please try again."
        }
    ]
}
~~~

&nbsp;

### 3.25. `customer_validation_data`
- Rota HTTP: `| GET | http://localhost:8000/user/customer_validation_data`
> _Pega os dados de validação de um usuário pelo token JWT do cabeçalho da requisição._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição      |
|------------------|----------------|
| `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/customer_validation_data
```

#### Modelo de resposta:

~~~json
{
    "personal": {
        "name": "Sr Teste",
        "nick_name": "RAST3",
        "birth_date": 750135600.0,
        "gender": "M",
        "father_name": "Arge Ferreira",
        "mother_name": "Vani Silva",
        "email": "nj@lionx.com.br",
        "cel_phone": "11952945942",
        "nationality": 1,
        "occupation_activity": 101,
        "company_name": "LionX",
        "company_cnpj": "36923006000188",
        "patrimony": 200000.0,
        "income": 200000.0,
        "tax_residences": [
            {
                "country": "AUT",
                "tax_number": "1212-012"
            },
            {
                "country": "CHE",
                "tax_number": "1212-012"
            }
        ],
        "birth_place_country": "BRA",
        "birth_place_city": 5150,
        "birth_place_state": "SP"
    },
    "marital": {
        "spouse": {
            "spouse_name": "Antonia Gererate",
            "spouse_cpf": "53845387084",
            "nationality": "1"
        },
        "status": 1
    },
    "documents": {
        "cpf": "58038116020",
        "identity_type": "RG",
        "identity_number": "385722594",
        "expedition_date": 1552867200.0,
        "issuer": "SSP",
        "state": "SP"
    },
    "address": {
        "country": "BRA",
        "number": 153,
        "street_name": "RUA IMBUIA",
        "city": 5150,
        "neighborhood": "CIDADE DAS FLORES",
        "zip_code": "06184110",
        "state": "SP",
        "phone": null
    },
    "external_exchange_account_us": {}
}
~~~

&nbsp;

### 3.26. `customer_validation_data`
- Rota HTTP: `| PUT | http://localhost:8000/user/customer_validation_data`
> _Atualiza os dados de validação de um usuário._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição      |
|------------------|----------------|
| `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/customer_validation_data
```

#### Modelo de corpo da requisição:
```json
{
    "personal": {
        "name": {
            "value": "Silvana Stefany Isi Moraes",
            "source": "app"
        },
        "nick_name": {
            "value": "hso404",
            "source": "app"
        },
        "birth_date": {
            "value": 885175200,
            "source": "app"
        },
        "gender": {
            "value": "F",
            "source": "app"
        },
        "father_name": {
            "value": "Antonio Henrique Nelson Moraes",
            "source": "app"
        },
        "mother_name": {
            "value": "Jéssica Lavínia Renata",
            "source": "app"
        },
        "email": {
            "value": "rorzecerti@vusra.com",
            "source": "app"
        },
        "cel_phone": {
            "value": "+5562986463601",
            "source": "app"
        },
        "nationality": {
            "value": 1,
            "source": "app"
        },
        "occupation_activity": {
            "value": 101,
            "source": "app"
        },
        "company_cnpj": {
            "source": "app",
            "value": "44117745000100"
        },
        "patrimony": {
            "value": 200000,
            "source": "app"
        },
        "income": {
            "value": 200000,
            "source": "app"
        },
        "birth_place_country": {
            "value": "BRA",
            "source": "app"
        },
        "birth_place_city": {
            "value": 932,
            "source": "app"
        },
        "birth_place_state": {
            "value": "GO",
            "source": "app"
        },
        "company_name": {
            "source": "app",
            "value": "Tecnologia"
        },
        "tax_residences": {
            "source": "app",
            "value": [
                {
                    "country": "BRA",
                    "tax_number": "33847255061"
                }
            ]
        }
    },
    "marital": {
        "status": {
            "value": 1,
            "source": "app"
        }
    },
    "documents": {
        "cpf": {
            "value": "73152835019",
            "source": "app"
        },
        "identity_type": {
            "value": "RG",
            "source": "app"
        },
        "identity_number": {
            "value": "346673859",
            "source": "app"
        },
        "expedition_date": {
            "value": 1300417200,
            "source": "app"
        },
        "issuer": {
            "value": "SSP",
            "source": "app"
        },
        "state": {
            "value": "SP",
            "source": "app"
        }
    },
    "address": {
        "country": {
            "value": "BRA",
            "source": "app"
        },
        "number": {
            "value": "651",
            "source": "app"
        },
        "street_name": {
            "value": "Travessa Ipora",
            "source": "app"
        },
        "city": {
            "value": 1151,
            "source": "app"
        },
        "neighborhood": {
            "value": "Vila Nossa Se",
            "source": "app"
        },
        "zip_code": {
            "value": "65590-000",
            "source": "app"
        },
        "state": {
            "value": "MA",
            "source": "app"
        }
    }
}
```

#### Modelo de resposta:
~~~json
{
    "message": "Register Updated."
}
~~~

&nbsp;

### 3.27. `user_admin`
- Rota HTTP: `| POST | http://localhost:8000/user_admin`
> _Cria um usuário de administrador._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição      |
|------------------|----------------|
| `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user_admin
```

#### Modelo de resposta:

~~~json
{
    "detail": [
        {
            "msg": "We have some issue, please try again."
        }
    ]
}
~~~

&nbsp;

### 3.28. `bank_accounts`
- Rota HTTP: `| GET | http://localhost:8000/user/bank_accounts`
> _TRANSFERIDO PARA O EBISU_

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro   | Descrição |
|-------------|-----------|
| `PARAMETRO` | DESCRIÇÃO |
&nbsp; 

#### Modelo de requisição:
```http
REQUISIÇÃO AQUI
```

#### Modelo de resposta:

~~~json
"RESPOSTA AQUI"
~~~

&nbsp;

### 3.29. `bank_accounts`
- Rota HTTP: `| PUT | http://localhost:8000/user/bank_accounts`
> _TRANSFERIDO PARA O EBISU_

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro   | Descrição |
|-------------|-----------|
| `PARAMETRO` | DESCRIÇÃO |
&nbsp; 

#### Modelo de requisição:
```http
REQUISIÇÃO AQUI
```

#### Modelo de resposta:

~~~json
"RESPOSTA AQUI"
~~~

&nbsp;

### 3.30. `bank_accounts`
- Rota HTTP: `| POST | http://localhost:8000/user/bank_accounts`
> _TRANSFERIDO PARA O EBISU_

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro   | Descrição |
|-------------|-----------|
| `PARAMETRO` | DESCRIÇÃO |
&nbsp; 

#### Modelo de requisição:
```http
REQUISIÇÃO AQUI
```

#### Modelo de resposta:

~~~json
"RESPOSTA AQUI"
~~~

&nbsp;

### 3.31. `bank_account`
- Rota HTTP: `| DELETE | http://localhost:8000/user/bank_account`
> _TRANSFERIDO PARA O EBISU_

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro   | Descrição |
|-------------|-----------|
| `PARAMETRO` | DESCRIÇÃO |
&nbsp; 

#### Modelo de requisição:
```http
REQUISIÇÃO AQUI
```

#### Modelo de resposta:

~~~json
"RESPOSTA AQUI"
~~~

&nbsp;

### 3.32. `external_fiscal_tax`
- Rota HTTP: `| GET | http://localhost:8000/user/external_fiscal_tax`
> _Retorna o número fical cadastrado na conta do usuário._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/external_fiscal_tax
```

#### Modelo de resposta:

~~~json
{
    "tax_residences": [
        {
            "country": "BRA",
            "tax_number": "1292-00"
        }
    ]
}
~~~

&nbsp;


### 3.33. `external_fiscal_tax_confirmation`
- Rota HTTP: `| PUT | http://localhost:8000/user/external_fiscal_tax_confirmation`
> _Cadastra ou atualiza o número fical registrado na conta do usuário._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/external_fiscal_tax_confirmation
```

#### Modelo de corpo da requisição:
```json
{
    "tax_residences": [
        {
            "country": "BRA",
            "tax_number": "1292-00"
        }
    ]
}
```

#### Modelo de resposta:

~~~json
{
    "message": "Register Updated."
}
~~~

&nbsp; 

### 3.34. `employ_for_us`
- Rota HTTP: `| PUT | http://localhost:8000/user/employ_for_us`
> _Registra a situação do usário de "Empregado" ou "Desempegado", e a atividade dele caso esteja empregado._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/employ_for_us
```

#### Modelo de corpo da requisição:
```json
{
    "user_employ_status": "EMPLOYED",
    "user_employ_type": "UTILITIES",
    "user_employ_position": "ADMINISTRATOR",
    "user_employ_company_name": "EMPRESA REAL LTDA"
}
```

#### Modelo de resposta:

~~~json
{
    "message": "Register Updated."
}
~~~

&nbsp; 

### 3.35. `w8_form`
- Rota HTTP: `| GET | http://localhost:8000/user/w8_form`
> _Retorna o link do formulário W8, que é o termo que o cliente tem que ler e aceitar, para o pagamento de
> impostos nos Estados Unidos, que serão repassados ao Brasil._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/w8_form
```

#### Modelo de resposta:

~~~json
{

    "w8_link": "https://d1gfu8yyntzl2k.cloudfront.net/cace7ccf-4fc2-4d3a-8a9e-375849fbfb44.pdf?Policy=eyJTdGF0ZW1lbnQiOiBbeyJSZXNvdXJjZSI6Imh0dHBzOi8vZDFnZnU4eXludHpsMmsuY2xvdWRmcm9udC5uZXQvY2FjZTdjY2YtNGZjMi00ZDNhLThhOWUtMzc1ODQ5ZmJmYjQ0LnBkZiIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTY1MTU3NTk0OX0sIklwQWRkcmVzcyI6eyJBV1M6U291cmNlSXAiOiIwLjAuMC4wLzAifX19XX0_&Signature=aQaYZXoFLvcH3D1nYubDfjAF1pJxAz0rDHIJ8Ng3xCTl-zvy09UKBwAHK0NZyJ9SWQCho7ZbIWWP3b8gMZBFjdooB6BGsHt3VZF~MkyH~3CuKqYu~njoJlMcj9pS3-Lv38Q4Y-S2Y99zv0UyOK440JmjlhoaQCUCxqQK8h59fT3jTAH0Cm~eovpSoVdA6A-HhUXaUhOGoT9OVRMz1EQ8qnUxhV5~FTzTmj7lgjwWqo~rMhf581bsUui8fmgWb~hz9ukd5Ifmgckpx2oi7pOwlhlpxn7rCm4uJ0P-n~8UtNW97UF0jeKwwxQIyr6RTDgmGYOZtbH9BcCa9Zh6R~miXw__&Key-Pair-Id=APKAJD7VLH4OKOE2R73Q"

}
~~~

&nbsp;


### 3.36. `w8_form_confirmation`
- Rota HTTP: `| PUT | http://localhost:8000/user/w8_form_confirmation`
> _Cadastra ou atualiza o aceite no formulário W8, que é o termo que o cliente tem que ler e aceitar, para o pagamento de
> impostos nos Estados Unidos, que serão repassados ao Brasil._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/user/w8_form_confirmation
```

#### Modelo de corpo da requisição:
```json
{
    "w8_confirmation": true
}
```

#### Modelo de resposta:

~~~json
{
    "message": "Register Updated."
}
~~~

&nbsp;

### 4. Client update enums
> _Endpoints que retornam as opções de preenchimento possíveis para os dados cadastrais._

### 4.1. `gender`
- Rota HTTP: `| GET | http://localhost:8000/client_update_enums/gender`
> _Pega as opções de gênero possíveis no cadastro._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/client_update_enums/gender
```

#### Modelo de resposta:
~~~json
{
    "enums": [
        {
            "code": "M",
            "value": "Masculino"
        },
        {
            "code": "F",
            "value": "Feminino"
        },
        {
            "code": "O",
            "value": "Outro"
        },
        {
            "code": "NI",
            "value": "Não Desejo Informar"
        }
    ]
}
~~~

&nbsp;

### 4.2. `document_type`
- Rota HTTP: `| GET | http://localhost:8000/client_update_enums/document_type`
> _Retorna os documentos aceitos para o cadastro de clientes._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/client_update_enums/document_type
```

#### Modelo de resposta:

~~~json
{
    "enums": [
        {
            "code": "CH",
            "value": "Carteira Nacional De Habilitacao"
        },
        {
            "code": "RG",
            "value": "Registro Geral"
        }
    ]
}
~~~

&nbsp;

### 4.3. `marital_status`
- Rota HTTP: `| GET | http://localhost:8000/client_update_enums/marital_status`
> _Retorna as opções de estado civil._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/client_update_enums/marital_status
```

#### Modelo de resposta:

~~~json
{
    "enums": [
        {
            "code": 1,
            "value": "Solteiro(A) "
        },
        {
            "code": 2,
            "value": "Casado(A)"
        },
        {
            "code": 3,
            "value": "Separado(A) Judicialmente"
        },
        {
            "code": 4,
            "value": "Divorciado(A) "
        },
        {
            "code": 5,
            "value": "Viúvo(A) "
        },
        {
            "code": 6,
            "value": "União Estável"
        }
    ]
}
~~~

&nbsp;

### 4.4. `nationality`
- Rota HTTP: `| GET | http://localhost:8000/client_update_enums/nationality`
> _Pega as opções de nacionalidade para o cadastro._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/client_update_enums/nationality
```

#### Modelo de resposta:

~~~json
{
    "enums": [
        {
            "code": 1,
            "value": "Brasileiro Nato"
        },
        {
            "code": 2,
            "value": "Brasileiro Naturalizado"
        },
        {
            "code": 3,
            "value": "Estrangeiro"
        }
    ]
}
~~~

&nbsp;

### 4.5. `city`
- Rota HTTP: `| GET | http://localhost:8000/client_update_enums/city`
> _Retorna as cidades disponíveis em determinado estado._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro | Descrição                    |
|-----------|------------------------------|
| `country` | Sigla do país de endereço.   |
| `state`   | Sigla do estado de endereço. |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/client_update_enums/city?country=BRA&state=SP
```

#### Modelo de resposta:

~~~json
{
    "enums": [
        {
            "code": 4761,
            "value": "Adamantina"
        },
        {
            "code": 4762,
            "value": "Adolfo"
        },
        {
            "code": 4763,
            "value": "Aguai"
        },
        {
            "code": 4764,
            "value": "Aguas Da Prata"
        },
      "..."
    ]
}
~~~

&nbsp;

### 4.6. `state`
- Rota HTTP: `| GET | http://localhost:8000/client_update_enums/state`
> _Retorna os estados disponíveis em determinado país._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro | Descrição     |
|-----------|---------------|
| `country` | Sigla do país |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/client_update_enums/state?country=USA
```

#### Modelo de resposta:

~~~json
{
    "enums": [
        {
            "code": "AL",
            "value": "Alabama"
        },
        {
            "code": "MA",
            "value": "Massachusetts"
        }
    ]
}
~~~

&nbsp;

### 4.7. `country`
- Rota HTTP: `| GET | http://localhost:8000/client_update_enums/country`
> _Retorna uma lista de países possíveis._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
ttp://localhost:8000/client_update_enums/country
```

#### Modelo de resposta:

~~~json
{
    "enums": [
        {
            "code": "ANT",
            "value": "Antilhas Holandesas"
        },
        {
            "code": "ARG",
            "value": "Argentina"
        },
        {
            "code": "AUS",
            "value": "Australia"
        },
        "..."
    ]
}
~~~

&nbsp;

### 4.8. `activity_type`
- Rota HTTP: `| GET | http://localhost:8000/client_update_enums/activity_type`
> _Retorna os tipos de atividade disponíveis._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/client_update_enums/activity_type
```

#### Modelo de resposta:
~~~json
{
      "enums": [
            {
              "code": 101,
              "value": "Engenheiro "
            },
            {
              "code": 102,
              "value": "Arquiteto"
            },
            {
              "code": 103,
              "value": "Agronomo "
            },
            {
              "code": 104,
              "value": "Quimico"
            },
            "..."
      ]
}
~~~

&nbsp;

### 4.9. `issuing_body`
- Rota HTTP: `| GET | http://localhost:8000/client_update_enums/issuing_body`
> _Retorna as opções de órgão emissor de documentos._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/client_update_enums/issuing_body
```

#### Modelo de resposta:
~~~json
{
      "enums": [
            {
              "code": "SSP",
              "value": "Secretaria De Seguranca Publica"
            },
            {
              "code": "IFP",
              "value": "Instituto Felix Pacheco"
            },
            {
              "code": "CRA",
              "value": "Conselho Regional De Administração"
            },
            {
              "code": "CREA",
              "value": "Cons. Reg. De Engenharia E Arquitetura"
            },
            "..."
      ]
}
~~~

&nbsp;

### 4.10. `time_experience_us`
- Rota HTTP: `| GET | http://localhost:8000/client_update_enums/time_experience_us`
> _Retorna as opções de tempo disponível para cadastro nos Estados Unidos._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/client_update_enums/time_experience_us
```

#### Modelo de resposta:

~~~json
{
    "enums": {
        "NONE": "N/D",
        "YRS_1_2": "1 a 2 anos",
        "YRS_3_5": "3 a 5 anos",
        "YRS_5_10": "5 a 10 anos",
        "YRS_10_": "Mais de 10 anos"
    }
}
~~~

&nbsp;

### 5. Client register enums
> _Endpoints que retornam as opções de preenchimento possíveis dos dados cadastrais, para uso de terceiros._

### 5.1. `city`
- Rota HTTP: `| GET | http://localhost:8000/client_register_enums/city`
> _Retorna as cidades disponíveis em determinado estado._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro | Descrição                    |
|-----------|------------------------------|
| `country` | Sigla do país de endereço.   |
| `state`   | Sigla do estado de endereço. |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/client_register_enums/city?country=BRA&state=SP
```

#### Modelo de resposta:

~~~json
{
    "enums": [
        {
            "code": 4761,
            "value": "Adamantina"
        },
        {
            "code": 4762,
            "value": "Adolfo"
        },
        {
            "code": 4763,
            "value": "Aguai"
        },
        {
            "code": 4764,
            "value": "Aguas Da Prata"
        },
      "..."
    ]
}
~~~

&nbsp;

### 5.2. `state`
- Rota HTTP: `| GET | http://localhost:8000/client_register_enums/state`
> _Retorna os estados disponíveis em determinado país._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro | Descrição     |
|-----------|---------------|
| `country` | Sigla do país |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/client_register_enums/state?country=USA
```

#### Modelo de resposta:
~~~json
{
    "enums": [
        {
            "code": "AL",
            "value": "Alabama"
        },
        {
            "code": "MA",
            "value": "Massachusetts"
        }
    ]
}
~~~

&nbsp;

### 5.3. `nationality`
- Rota HTTP: `| GET | http://localhost:8000/client_register_enums/nationality`
> _Pega as opções de nacionalidade disponíveis._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/client_register_enums/nationality
```

#### Modelo de resposta:

~~~json
{
    "enums": [
        {
            "code": 1,
            "value": "Brasileiro Nato"
        },
        {
            "code": 2,
            "value": "Brasileiro Naturalizado"
        },
        {
            "code": 3,
            "value": "Estrangeiro"
        }
    ]
}
~~~

&nbsp;

### 5.4. `document_type`
- Rota HTTP: `| GET | http://localhost:8000/client_register_enums/document_type`
> _Pega as opções de nacionalidade para o cadastro._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/client_register_enums/document_type
```

#### Modelo de resposta:

~~~json
{
    "enums": [
        {
            "code": 1,
            "value": "Brasileiro Nato"
        },
        {
            "code": 2,
            "value": "Brasileiro Naturalizado"
        },
        {
            "code": 3,
            "value": "Estrangeiro"
        }
    ]
}
~~~

&nbsp;

### 5.5. `country`
- Rota HTTP: `| GET | http://localhost:8000/client_register_enums/country`
> _Retorna uma lista de países possíveis._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/client_register_enums/country
```

#### Modelo de resposta:

~~~json
{
    "enums": [
        {
            "code": "ANT",
            "value": "Antilhas Holandesas"
        },
        {
            "code": "ARG",
            "value": "Argentina"
        },
        {
            "code": "AUS",
            "value": "Australia"
        },
        "..."
    ]
}
~~~

&nbsp;

### 5.6. `activity_type`
- Rota HTTP: `| GET | http://localhost:8000/client_register_enums/activity_type`
> _Retorna os tipos de atividade disponíveis._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/client_register_enums/activity_type
```

#### Modelo de resposta:
~~~json
{
      "enums": [
            {
              "code": 101,
              "value": "Engenheiro "
            },
            {
              "code": 102,
              "value": "Arquiteto"
            },
            {
              "code": 103,
              "value": "Agronomo "
            },
            {
              "code": 104,
              "value": "Quimico"
            },
            "..."
      ]
}
~~~

&nbsp;

### 5.7. `document_issuing_body`
- Rota HTTP: `| GET | http://localhost:8000/client_register_enums/document_issuing_body`
> _Retorna as opções de órgão emissor de documentos._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/client_register_enums/document_issuing_body
```

#### Modelo de resposta:
~~~json
{
      "enums": [
            {
              "code": "SSP",
              "value": "Secretaria De Seguranca Publica"
            },
            {
              "code": "IFP",
              "value": "Instituto Felix Pacheco"
            },
            {
              "code": "CRA",
              "value": "Conselho Regional De Administração"
            },
            {
              "code": "CREA",
              "value": "Cons. Reg. De Engenharia E Arquitetura"
            },
            "..."
      ]
}
~~~

&nbsp;

### 5.8. `all_in_one`
- Rota HTTP: `| GET | http://localhost:8000/client_register_enums/all_in_one`
> _Retorna um JSON com todos os Enums disponíveis._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/client_register_enums/all_in_one
```

#### Modelo de resposta:

~~~json
{
    "activity_type": [
        "..."
    ],
    "nationality": [
        "..."
    ],
    "document_issuing_body": [
        "..."
    ],
  "..."
}
~~~

&nbsp;

### 6. Features
> _Endpoints para a manipulação de features. As features são as funcionalidades que o cliente terá disponível na conta,
> como, por exemplo: Newsletter, Informes de Mercado, Dados em Tempo Real, etc. As features podem ser relacionadas a uma view._
> 
> _**Observação:** ver o tópico `7. Views` e `8. Views link` para mais detalhes._

### 6.1. `feature`
- Rota HTTP: `| POST | http://localhost:8000/feature`
> _Cria uma nova feature._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/feature
```

#### Modelo de corpo da requisição:
```json
{
    "name": "MinhaFeature",
    "display_name": "Minha Feature"
}
```

#### Modelo de resposta:
~~~json
{
    "message": "Create successed."
}
~~~

&nbsp;

### 6.2. `feature/[feature_id]`
- Rota HTTP: `| PUT | http://localhost:8000/feature/feature_id`
> _Altera uma feature existente._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro    | Descrição                        |
|--------------|----------------------------------|
| `feature_id` | ID da feature que será alterada. |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/feature/MinhaFeature
```

#### Modelo de corpo da requisição:
```json
{
    "name": "AltereiMinhaFeature",
    "display_name": "Feature Alterada"
}
```

#### Modelo de resposta:
~~~json
{
    "message": "Register Updated."
}
~~~

&nbsp;

### 6.3. `feature/[feature_id]`
- Rota HTTP: `| DELETE | http://localhost:8000/feature/feature_id`
> _Deleta uma feature._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro    | Descrição                        |
|--------------|----------------------------------|
| `feature_id` | ID da feature que será deletada. |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/feature/nj
```

#### Modelo de resposta:
~~~json
{
    "message": "Register deleted."
}
~~~

&nbsp;

### 6.4. `features`
- Rota HTTP: `| GET | http://localhost:8000/features`
> _Retorna uma lista das features disponíveis._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/features
```

#### Modelo de resposta:
~~~json
{
    "features": [
        {
            "_id": "njj23",
            "name": "njj23",
            "display_name": "njj23"
        },
        {
            "_id": "njj44",
            "name": "nj5",
            "display_name": "nj5"
        },
        {
            "_id": "nj78787878",
            "name": "nj9999999",
            "display_name": "nj9999999"
        },
        {
            "_id": "nj22",
            "name": "nj22",
            "display_name": "nj22"
        },
        {
            "_id": "MinhaFeature",
            "name": "AltereiMinhaFeature",
            "display_name": "Feature Alterada"
        }
    ]
}
~~~

&nbsp;


### 7. Views
> Endpoints para a manipulação de views. As views são os "pacotes de serviço" disponíveis na conta, como, por exemplo: "Premium",
> "Basic", "Gold", "Silver", "Plus", etc. As views podem ser relacionadas às features a partir de "links", dessa forma um
> "pacote" pode ter determinadas "funcionalidades."
> 
> _**Observação:** ver o tópico `6. Features` e `8. Views link` para mais detalhes._

### 7.1. `view`
- Rota HTTP: `| POST | http://localhost:8000/view`
> _Cria uma nova view._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro       | Descrição     |
|-----------------|---------------|
| `SEM PARÂMETRO` | SEM PARÂMETRO |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/view
```

#### Modelo de corpo da requisição:
```json
{
    "name": "MinhaView",
    "display_name": "Minha View"
}
```

#### Modelo de resposta:

~~~json
{
    "message": "Create successed."
}
~~~

&nbsp;

### 7.2. `id/[view_id]`
- Rota HTTP: `| GET | http://localhost:8000/view/id/view_id`
> _Retorna uma view pelo ID._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro   | Descrição  |
|-------------|------------|
| `view_id`   | ID da view |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/view/id/MinhaView`
```

#### Modelo de resposta:

~~~json
{
    "_id": "MinhaView",
    "name": "MinhaView",
    "display_name": "Minha View"
}
~~~

&nbsp;

### 7.3. `id/[view_id]`
- Rota HTTP: `| PUT | http://localhost:8000/view/id/view_id`
> _Atualiza uma view._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro   | Descrição                   |
|-------------|-----------------------------|
| `view_id`   | ID da view a ser atualizada |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/view/id/MinhaView
```

#### Modelo de corpo da requisição:
```json
{
    "name": "ViewAtualizada",
    "display_name": "Atualizei Minha View"
}
```

#### Modelo de resposta:

~~~json
{
    "message": "Register Updated."
}
~~~

&nbsp;

### 7.4. `id/[view_id]`
- Rota HTTP: `| DELETE | http://localhost:8000/view/id/view_id`
> _Deleta uma view._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro   | Descrição                 |
|-------------|---------------------------|
| `view_id`   | ID da view a ser deletada |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/view/id/nj9999999
```

#### Modelo de resposta:
~~~json
{
    "message": "Register deleted."
}
~~~

&nbsp;

### 7.5. `views`
- Rota HTTP: `| GET | http://localhost:8000/views`
> _Retorna uma lista das views existentes._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição      |
|------------------|----------------|
| `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/views
```

#### Modelo de resposta:

~~~json
{
    "views": [
        {
            "_id": "nj",
            "name": "nj",
            "display_name": "nj",
            "features": []
        },
        {
            "_id": "teste",
            "name": "teste",
            "display_name": "teste",
            "features": [
                "nj"
            ]
        },
        {
            "_id": "teste22",
            "name": "teste22",
            "display_name": "teste22"
        },
        {
            "_id": "teste223",
            "name": "teste223",
            "display_name": "teste223"
        },
        {
            "_id": "MinhaView",
            "name": "ViewAtualizada",
            "display_name": "Atualizei Minha View"
        }
    ]
}
~~~

&nbsp;

### 8. Views link
> Endpoints para a manipulação dos "links" entre as features e as views. Ou seja, das relações entre as views e as features.
> 
> _**Observação:** ver o tópico `6. Features` e `7. Views` para mais detalhes._

### 8.1. `link_feature`
- Rota HTTP: `| PUT | http://localhost:8000/view/link_feature`
> _Relaciona uma feature com uma view, assim a view começa a possuir essa feature._ 

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição      |
|------------------|----------------|
| `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/view/link_feature
```
#### Modelo de corpo da requisição:
```json
{
    "feature_id": "MinhaFeature",
    "view_id": "MinhaView"
}
```
#### Modelo de resposta:

~~~json
{
    "message": "Register Updated."
}
~~~

&nbsp;

### 8.2. `link_feature`
- Rota HTTP: `| DELETE | http://localhost:8000/view/link_feature`
> _Deleta um link entre uma view e uma feature, assim a view deixa de possuir a feature._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição      |
|------------------|----------------|
| `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/view/link_feature
```

#### Modelo de corpo da requisição:
```json
{
    "feature_id": "nj22",
    "view_id": "MinhaView"
} 
```
#### Modelo de resposta:

~~~json
{
    "message": "Register deleted."
}
~~~

&nbsp;

### 8.3. `link`
- Rota HTTP: `| GET | http://localhost:8000/views/link`
> _Retorna uma lista das views com as features que elas possuem._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição      |
|------------------|----------------|
| `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/views/link
```

#### Modelo de resposta:
~~~json
{
    "views": [
        {
            "_id": "nj",
            "name": "nj",
            "display_name": "nj",
            "features": [
                "MinhaFeature"
            ]
        },
        {
            "_id": "nj88",
            "name": "nj88",
            "display_name": "nj88",
            "features": []
        },
        {
            "_id": "nj8899",
            "name": "nj8899",
            "display_name": "nj8899",
            "features": []
        },
        {
            "_id": "teste",
            "name": "teste",
            "display_name": "teste",
            "features": [
                "nj"
            ]
        },
        {
            "_id": "teste22",
            "name": "teste22",
            "display_name": "teste22"
        },
        {
            "_id": "teste223",
            "name": "teste223",
            "display_name": "teste223"
        },
        {
            "_id": "MinhaView",
            "name": "ViewAtualizada",
            "display_name": "Atualizei Minha View",
            "features": [
                "MinhaFeature"
            ]
        }
    ]
}
~~~

&nbsp;

### 9. Term

### 9.1. `term`
- Rota HTTP: `| GET | http://localhost:8000/term`
> _Retorna o link do PDF de um termo de uso especificado._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro   | Descrição                        |
|-------------|----------------------------------|
| `file_type` | O termo que terá o PDF retornado |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/term?file_type=term_refusal
```

#### Modelo de resposta:
~~~json
{
    "link": "https://dtvm-terms-dev.s3.amazonaws.com/term_refusal/term_refusal_v4.pdf?AWSAccessKeyId=AKIATZVFXI25USQWCS5O&Signature=oDzkmb90mHgM%2FZRs8%2BzeVTAb7lg%3D&Expires=1651165695"
}
~~~

&nbsp;

### 10. Terms

### 10.1. `terms`
- Rota HTTP: `| GET | http://localhost:8000/terms`
> _Retorna os termos e políticas de uso disponíveis._

&nbsp; 
#### Parâmetros da requisição:
| Parâmetro        | Descrição      |
|------------------|----------------|
| `SEM PARÂMETROS` | SEM PARÂMETROS |
&nbsp; 

#### Modelo de requisição:
```http
http://localhost:8000/terms
```

#### Modelo de resposta:

~~~json
{
    "terms": [
        "term_application",
        "term_open_account",
        "term_refusal",
        "term_non_compliance",
        "term_retail_liquid_provider",
        "term_open_account_dw",
        "term_application_dw",
        "term_privacy_policy_dw",
        "term_data_sharing_policy_dw"
    ]
}
~~~

&nbsp;

---

## Criação de usuário
__Passo a passo para a criação de uma conta, e gerar os tokens JWT que permitem a utilização dos endpoints:__

1. Crie um usuário com o email e um nickname.
   
    ```http
    http://localhost:8000/user
    ```
   
2. Faça login com o email e pegue o token JWT do link enviado ao email.
   
    ```http
    http://localhost:8000/login
    ```

3. Faça a seguinte requisição com o token JWT em um campo do cabeçalho chamado `x-thebes-answer`, esse campo será necessário
em todas as requisições a partir de agora. Pegue o JWT que for retornado e troque pelo JWT antigo no cabeçalho.
   
    ```http
    http://localhost:8000/thebes_gate
    ```

4. Faça a seguinte requisição para ver as etapas de cadastro que precisam ser concluidas, e realize-as em sequência. 
Conforme a conclusão os campos ficam com o valor `true`, quando todos os valores estiverem `true` 
o cadastro estará concluído.

    **Requisição:**
    ```http
    http://localhost:8000/user/onboarding_user_current_step_br
    ```
    **Resposta:**
    ```json
    {
        "current_onboarding_step": "suitability_step",
        "suitability_step": false,
        "user_identifier_data_step": false,
        "user_selfie_step": false,
        "user_complementary_step": false,
        "user_document_validator": false,
        "user_data_validation": false,
        "user_electronic_signature": false,
        "finished": false
    }
    ```

5. Faça a seguinte requisição para validar a assinatura eletrônica e receber um token de assinatura eletrônica, que é 
utilizado por algumas requisições em um campo do cabeçalho chamado `x-mist`.

    ```http
    http://localhost:8000/validate_electronic_signature
    ```

6. Para realizar cadastro nos Estados Unidos, faça a seguinte requisição e realize as etapas marcadas como `false`:
    
    **Requisição:**
    ```http
    http://localhost:8000/user/onboarding_user_current_step_us
    ```
    **Resposta:**
    ```json
    {
        "current_onboarding_step": "finished",
        "terms_step": true,
        "user_document_validator_step": true,
        "is_politically_exposed_step": true,
        "is_exchange_member_step": true,
        "is_company_director_step": true,
        "external_fiscal_tax_confirmation_step": true,
        "employ_step": true,
        "time_experience_step": true,
        "w8_confirmation_step": true,
        "finished": true
    }
    ```
___

## Erros e exceções

### BadRequestError
- **Código HTTP:** `400 Bad Request `
- Erro lançado quando o servidor não consegue processar a requisição por conta de um problema de sintaxe.

### UnauthorizedError
- **Código HTTP:** `401 Unauthorized`
- Erro lançado quando as credenciais de autenticação estão inválidas.

### ForbiddenError
- **Código HTTP:** `403 Forbidden`
- Erro lançado quando o acesso é proibido.

### InternalServerError
- **Código HTTP:** `500 Internal Server Error`
- Erro lançado quando uma condição inesperada acontece no servidor.

### ExceptionError
- **Código HTTP:** `500 Internal Server Error`
- Erro lançado quando ocorre algum erro que não se encaixa nas condições listadas acima.

___

## Swagger
É possível ver as requisições pelo link abaixo após rodar o projeto, no entanto, elas apresentarão erro por
não possuírem o token de autenticação JWT:
> http://0.0.0.0:8000/docs
>
> http://localhost:8000/docs

| Recomendado utilizar uma plataforma para testes de APIs, como o Postman. |
|--------------------------------------------------------------------------|
