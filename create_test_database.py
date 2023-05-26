from flask import Flask
from app import db
from models import SQLGroup, SQLCertificate
from datetime import datetime, timedelta
from entities import Certificate, Group

# app = Flask(__name__)

print('Apagando dados do banco...')
db.drop_all()

print('Criando novo banco de dados...')
db.create_all()

print('Criando grupos...')
group1 = SQLGroup(name="RH", description="Grupo RH")
group2 = SQLGroup(name="Comercial", description="Grupo Comercial")
group3 = SQLGroup(name="Suporte", description="Grupo Suporte")
group4 = SQLGroup(name="Vendas", description="Grupo Vendas")

print('Adicionando grupos...')
db.session.add_all([group1, group2, group3, group4])

print('Criando certificados...')
exp1 = 365
exp2 = 30
exp3 = 60
exp4 = 15

cert1 = SQLCertificate(
    username="joao",
    name="João Silva",
    description="JS",
    expiration=exp1,
    expirated_at=datetime.utcnow() + timedelta(days=int(exp1)),
    groups=[group1, group2]
)

cert2 = SQLCertificate(
    username="pedro",
    name="Pedro Souza",
    description="PS",
    expiration=exp2,
    expirated_at=datetime.utcnow() + timedelta(days=int(exp2)),
    groups=[group2, group3]
)

cert3 = SQLCertificate(
    username="maria",
    name="Maria Oliveira",
    description="MO",
    expiration=exp3,
    expirated_at=datetime.utcnow() + timedelta(days=int(exp3)),
    groups=[group2]
)

cert4 = SQLCertificate(
    username="joana",
    name="Joana Rodrigues",
    description="JR",
    expiration=exp4,
    expirated_at=datetime.utcnow() + timedelta(days=int(exp4)),
    groups=[group2, group3, group4]
)

print('Adicionando certificados...')
db.session.add_all([cert1, cert2, cert3, cert4])

print('Salvando dados no banco de dados...')
db.session.commit()

print('Dados populados com sucesso!')
exit(0)
