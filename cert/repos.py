from cert.usecases import CertificateSchema
from models import SQLCertificate
from entities import Certificate


class SQLCertificateRepo:
    def __init__(self, db):
        self.db = db

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
                # groups=db_cert.groups,
                groups=[db_cert.id for db_cert in db_certs.first().groups],
            )
            certs.append(cert)

        # certificates = db_certs.all()
        # certs_list = CertificateSchema(many=True).dump(certificates)

        # return 200, certs_list
        return 200, certs

    def insert(self, cert):
        print("### cert / repos / insert")
        print(f"cert.groups: {cert.groups}")

        db_certificate = SQLCertificate(
            username=cert.username,
            name=cert.name,
            description=cert.description,
            expiration=cert.expiration,
            expirated_at=cert.expirated_at,
            groups=cert.groups,
        )
        print(f"db_certificate: {db_certificate}")
        self.db.session.add(db_certificate)
        self.db.session.commit()

        certificate_serialized = CertificateSchema().dump(db_certificate)
        return 200, certificate_serialized

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
            return 200, cert_query
        return 404, None

    def delete(self, cert_id):
        print("### cert / repos / delete")
        cert_query = self.db.session.get(SQLCertificate, cert_id)

        if cert_query:
            self.db.session.delete(cert_query)
            self.db.session.commit()
            return 200, True

        return 404, False

    def update(self, cert_id, cert):
        print("### cert / repos / update")

        cert_query = self.db.session.get(SQLCertificate, cert_id)
        cert_query.username = cert.username

        self.db.session.commit()

        certificate_serialized = CertificateSchema().dump(cert_query)
        return 200, certificate_serialized
