from marshmallow import fields, Schema, ValidationError
from marshmallow.validate import Length, And, Regexp, Range
from entities import Certificate
from datetime import datetime, timedelta
from models import SQLGroup  # remover depois


class CertificateSchema(Schema):

    def dump_groups_ids(self, value):
        return [group.id for group in value.groups]

    def load_groups_ids(self, value):
        return list(value)

    id = fields.Integer(dump_only=True)
    username = fields.Str(required=True, validate=And(Length(max=30), Regexp(regex=r'^[a-zA-Z0-9]+$')))
    name = fields.Str(required=True, validate=Length(max=255))
    description = fields.Str(required=True, validate=Length(max=255))
    expiration = fields.Integer(required=True, validate=Range(10, 3650))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    expirated_at = fields.DateTime()
    groups = fields.Method("dump_groups_ids", "load_groups_ids")

    class Meta:
        fields = (
            'id',
            'username',
            'name',
            'description',
            'expiration',
            'created_at',
            'updated_at',
            'expirated_at',
            'groups',
        )


def define_expirated_at(expiration):
    return datetime.utcnow() + timedelta(days=int(expiration))


class CertificateUC:
    def __init__(self, repo):
        self.repo = repo
        # self.grou_uc = group_uc

    def get_all(self, modifiers):
        return self.repo.get_all(modifiers)

    def create(self, data):
        try:
            cert_dict = CertificateSchema().load(data)
        except ValidationError as err:
            return 400, err.messages

        # Verifica se o username já existe
        status, username_existis = self.repo.get_by_username(cert_dict["username"])
        if status == 200:
            return 409, None

        # for group_id in cert_dict["groups"]:
        #     staus, obj = self.group_uc.get_by_id(group_id)
        #     if status == 404:
        #         return 400, "Erro"

        group_ids = [int(group_id) for group_id in cert_dict["groups"]]
        groups = SQLGroup.query.filter(SQLGroup.id.in_(group_ids)).all()  # ajustar, não deve ser usar SQL aqui

        cert_dict["id"] = None
        cert_dict["created_at"] = None
        cert_dict["updated_at"] = None
        cert_dict["expirated_at"] = define_expirated_at(cert_dict["expiration"])
        cert_dict["groups"] = groups
        # cert = Certificate(**cert_dict)

        cert = Certificate(
            # id=None,
            created_at=datetime.now(),
        )

        return self.repo.insert(cert)

    def get_by_id(self, cert_id):
        status, cert_exists = self.repo.get_by_id(cert_id)

        if status == 404:
            return 404, None

        cert = Certificate(username=cert_exists.username, id=cert_exists.id)
        return 200, cert

    def delete(self, cert_id):
        status, cert_exists = self.repo.get_by_id(cert_id)

        if status == 404:
            return 404, None

        return self.repo.delete(cert_id)

    def update(self, cert_id, data):
        cert_dict = CertificateSchema().load(data)

        # Verifica se o username já existe
        status, username_existis = self.repo.get_by_username(cert_dict["username"])
        if status == 200:
            return 409, None

        cert = Certificate(username=cert_dict["username"], id=None)
        return self.repo.update(cert_id, cert)

