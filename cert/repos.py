from models import SQLCertificate
from entities import Certificate


class SQLCertificateRepo:
    def __init__(self, db, group_repo):
        self.db = db
        self.group_repo = group_repo

    def get_all(self, modifiers):
        print("### cert / repos / get_all")
        db_certs = SQLCertificate.query

        if modifiers:
            if modifiers.get("sort_param") == 'username':
                db_certs = db_certs.order_by(SQLCertificate.username.asc())
            if modifiers.get("sort_param") == 'name':
                db_certs = db_certs.order_by(SQLCertificate.name.asc())
            if modifiers.get("filter_name_param"):
                db_certs = db_certs.filter(
                    SQLCertificate.name.ilike(f'%{modifiers.get("filter_name_param")}%')
                )
            if modifiers.get("filter_username_param"):
                db_certs = db_certs.filter(
                    SQLCertificate.username.ilike(f'%{modifiers.get("filter_username_param")}%')
                )

        certs = []
        for db_cert in db_certs:
            cert = Certificate(
                id=db_cert.id,
                username=db_cert.username,
                name=db_cert.name,
                created_at=db_cert.created_at,
                updated_at=db_cert.updated_at,
                expiration=db_cert.expiration,
                expirated_at=db_cert.expirated_at,
                description=db_cert.description,
                groups=[db_cert.id for db_cert in db_certs.first().groups],
            )
            certs.append(cert)

        return 200, certs

    def insert(self, cert_ent):
        print("### cert / repos / insert")
        print(f"cert_ent.groups: {cert_ent.groups}")

        db_groups = []
        for group in cert_ent.groups:
            status, group_sql = self.group_repo.get_db_group_by_id(group)
            if status == 404:
                return 400, f"Erro, grupo {group} não existe"
            db_groups.append(group_sql)

        db_certificate = SQLCertificate(
            username=cert_ent.username,
            name=cert_ent.name,
            description=cert_ent.description,
            expiration=cert_ent.expiration,
            expirated_at=cert_ent.expirated_at,
            groups=db_groups,
            created_at=cert_ent.created_at,
            updated_at=cert_ent.updated_at
        )

        self.db.session.add(db_certificate)
        self.db.session.commit()

        return 200, cert_ent

    def get_by_username(self, cert):
        print("### cert / repos / get_by_username")
        cert_query = SQLCertificate.query.filter_by(username=cert).first()
        if cert_query:
            return 200, cert_query
        return 400, None

    def get_by_id(self, cert_id):
        print("### cert / repos / get_by_id")
        cert_query = self.db.session.get(SQLCertificate, cert_id)
        if cert_query:
            cert_ent = Certificate(
                id=cert_query.id,
                username=cert_query.username,
                name=cert_query.name,
                description=cert_query.description,
                expiration=cert_query.expiration,
                expirated_at=cert_query.expirated_at,
                groups=[group.id for group in cert_query.groups],
                created_at=cert_query.created_at,
                updated_at=cert_query.updated_at
            )
            return 200, cert_ent
        return 404, None

    def delete(self, cert_id):
        print("### cert / repos / delete")
        cert_query = self.db.session.get(SQLCertificate, cert_id)

        if cert_query:
            self.db.session.delete(cert_query)
            self.db.session.commit()
            return 200, True

        return 404, False

    def update(self, cert_id, cert_ent):
        print("### cert / repos / update")

        db_groups = []
        for group in cert_ent.groups:
            status, group_sql = self.group_repo.get_db_group_by_id(group)
            if status == 404:
                return 404, f"Erro, grupo {group} não existe"
            db_groups.append(group_sql)

        cert_query = self.db.session.get(SQLCertificate, cert_id)
        if cert_ent.name:
            cert_query.name = cert_ent.name
        if cert_ent.description:
            cert_query.description = cert_ent.description
        if cert_ent.groups:
            cert_query.groups = db_groups  # aqui preciso informar objs SQLGroup

        self.db.session.commit()

        return 200, cert_ent
