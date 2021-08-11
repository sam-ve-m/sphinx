# Sphinx 
## _Autenticação e autorização de usuários_
---
Projeto destinado a manter as informações dos usuários (usuário, cliente) e autentica/autorizar o acesso aos demais serviços.

### **Passo 1**
Iniciar o virtual ENV do projeto.

### **Passo 2**
Instalar os pacotes dentro do virtual `ENV` listados no `requirements.txt`.

```bash
pip install -r requirements.txt
```

### **Passo 3**
Efetuar o Download dos binários de conexão com o banco oracle.

https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html

> Versão 19

### **Passo 4**
Exportar a variável de ambiente para a pasta onde foi feito o download dos binários

```bash
export LD_LIBRARY_PATH=CAMINHO_PARA_OS_BINARIOS
```

### **Passo 5**
Instalando o pacote libaio1

```bash
sudo apt-get install libaio1
```

### **Passo 6**
Usar o `.env.example` para criar o arquivo com as credencias no caminho `/opt/envs/sphinx.lionx.com.br/.env`

> Rodar o main.py