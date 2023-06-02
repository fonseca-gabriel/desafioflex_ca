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

## Observações

- Estou considerando que o atributo groups da entidade Certificate irá receber apenas inteiros das requisições.
- Na atualização do certificado, estou considerando que somente o nome, a descrição e os grupos podem ser alterados.
- Na atualização do grupo, estou considerando que somente a descrição pode ser alterada.