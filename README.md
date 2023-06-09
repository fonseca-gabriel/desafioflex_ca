# Desafioflex com Clean Architecture

## Descrição
API REST para gerenciamento de certificados, contendo cadastro, listagem, edição e deleção dos certificados e grupos associados.

A API utiliza Python 3.10 e Flask na versão 2.3.1 e banco SQLite 3. Foi utilizado o SQLAlchemy como ORM.

Outras bibliotecas, dependências e respectivas versões podem ser verificadas no arquivo `requirements.txt` contida neste projeto.

## Estrutura de arquivos

Segue a árvore de arquivos do projeto:

```
.
├── app.py
├── cert
│   ├── apis.py
│   ├── repos.py
│   └── usecases.py
├── create_test_database.py
├── entities.py
├── group
│   ├── apis.py
│   ├── repos.py
│   └── usecases.py
├── instance
│   └── database.db
├── models.py
├── README.md
├── requirements.txt
└── setup.py
```

## Estrutura da base de dados

Para efeitos de melhor compreensão, segue a estrutura da base de dados utilizada no projeto:

```
CREATE TABLE certificates (
        id INTEGER NOT NULL, 
        username VARCHAR(30) NOT NULL, 
        name VARCHAR(255) NOT NULL, 
        description VARCHAR(255), 
        expiration INTEGER NOT NULL, 
        created_at DATETIME, 
        updated_at DATETIME, 
        expirated_at DATETIME, 
        PRIMARY KEY (id), 
        UNIQUE (username)
);

CREATE TABLE groups (
        id INTEGER NOT NULL, 
        name VARCHAR(30) NOT NULL, 
        description VARCHAR(255), 
        created_at DATETIME, 
        updated_at DATETIME, 
        PRIMARY KEY (id), 
        UNIQUE (name)
);

CREATE TABLE certificate_group (
        certificate_id INTEGER NOT NULL, 
        group_id INTEGER NOT NULL, 
        PRIMARY KEY (certificate_id, group_id), 
        FOREIGN KEY(certificate_id) REFERENCES certificates (id), 
        FOREIGN KEY(group_id) REFERENCES groups (id)
);
```

## Execução em CLI

O arquivo `cert_infra/run.py` é responsável pelo gerenciamento dos certificados via CLI, interagindo diretamente com o sistema operacional, sem qualquer relação com as informações presentes no banco de dados.

Através do comando `python run.py -h` é possível obter as informações de ajuda para execução.

O comando permite a criação, revogação e listagem dos certificados, para isso utiliza-se dos seguintes argumentos posicionais:

- **create**
- **revoke**
- **show**

Para obter informações de ajuda de cada uma das opções, basta executar o comando `python run.py [opção] -h`, conforme o exemplo que segue:

```python run.py create -h```

### Listagem de certificados

É possível listar os certificados existentes, diretamente do arquivo de banco de dados (index.txt) da VPN, através da opção **show**.

São três as possibilidades de listagem, em todas elas é necessário informar o nome do servidor através do argumento `--server [nome-do-servidor]`:

- **all**: lista todos os certificados do servidor informado
- **valid**: lista somente os certificados válidos do servidor informado
- **revoked**: lista somente os certificados revogados do servidor informado

O uso da opção em questão se dá da seguinte forma:

 ```python run.py show --server [nome-do-servidor] --type [opcao-de-listagem]```


### Criação de certificados

A criação de novos certificados se utiliza da opção **create**, da seguinte forma:

```python run.py create --server [nome-do-servidor] --username [username-do-certificado] --expiration [validade-em-dias]```

### Revogação de certificado

A criação de novos certificados se utiliza da opção **revoke**, da seguinte forma:

```python run.py revoke --server [nome-do-servidor] --username [username-do-certificado]```


## Observações

- Estou considerando que o atributo groups da entidade Certificate irá receber apenas inteiros das requisições.
- Na atualização do certificado, estou considerando que somente o nome, a descrição e os grupos podem ser alterados.
- Na atualização do grupo, estou considerando que somente a descrição pode ser alterada.