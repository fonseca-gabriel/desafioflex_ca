from usecases_cert import CertificateSchema
from models import SQLCertificate


class SQLCertificateRepo:
    def __init__(self, db):
        self.db = db

    def get_all(self, modifiers):

        certificates_query = SQLCertificate.query

        if modifiers:
            if modifiers.get("sort_param") == 'username':
                certificates_query = certificates_query.order_by(SQLCertificate.username.asc())
            if modifiers.get("sort_param") == 'name':
                certificates_query = certificates_query.order_by(SQLCertificate.name.asc())
            if modifiers.get("filter_name_param"):
                certificates_query = certificates_query.filter(
                    SQLCertificate.name.ilike(f'%{modifiers.get("filter_name_param")}%')
                )
            if modifiers.get("filter_username_param"):
                certificates_query = certificates_query.filter(
                    SQLCertificate.username.ilike(f'%{modifiers.get("filter_username_param")}%')
                )

        certificates = certificates_query.all()
        certs_list = CertificateSchema(many=True).dump(certificates)

        # certs_list = CertificateSchema(many=True).dump(SQLCertificate.query.all())
        return 200, certs_list

    def insert(self, cert):
        db_certificate = SQLCertificate(
            username=cert.username,
            name=cert.name,
            description=cert.description,
            expiration=cert.expiration,
            expirated_at=cert.expirated_at,
            groups=cert.groups,
        )

        self.db.session.add(db_certificate)
        self.db.session.commit()

        certificate_serialized = CertificateSchema().dump(db_certificate)
        return 200, certificate_serialized

    def get_by_username(self, cert):
        cert_query = SQLCertificate.query.filter_by(username=cert).first()
        if cert_query:
            return 200, cert_query
        return 400, None

    def get_by_id(self, cert_id):
        cert_query = self.db.session.get(SQLCertificate, cert_id)
        if cert_query:
            return 200, cert_query
        return 404, None

    def delete(self, cert_id):
        cert_query = self.db.session.get(SQLCertificate, cert_id)

        if cert_query:
            self.db.session.delete(cert_query)
            self.db.session.commit()
            return 200, True

        return 404, False

    def update(self, cert_id, cert):

        cert_query = self.db.session.get(SQLCertificate, cert_id)
        cert_query.username = cert.username

        self.db.session.commit()

        certificate_serialized = CertificateSchema().dump(cert_query)
        return 200, certificate_serialized
