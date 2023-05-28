from marshmallow import fields, Schema, ValidationError
from marshmallow.validate import Length, And, Regexp, Range
from entities import Certificate
from datetime import datetime, timedelta


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
    def __init__(self, repo, group_uc):
        self.repo = repo
        self.group_uc = group_uc

    def get_all(self, modifiers):
        print("### cert / usecases / get_all")
        return self.repo.get_all(modifiers)

    def create(self, data):
        print("### cert / usecases / create")
        try:
            cert_dict = CertificateSchema().load(data)
        except ValidationError as err:
            return 400, err.messages

        # Verifica se o username já existe
        status, username_existis = self.repo.get_by_username(cert_dict["username"])
        if status == 200:
            return 409, None

        groups_id = []
        for group_id in cert_dict["groups"]:
            status, group_ent = self.group_uc.get_by_id(group_id)
            if status == 404:
                return 400, f"Erro, grupo com ID {group_id} não existe"
            groups_id.append(group_ent.id)

        cert_ent = Certificate(
            id=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            username=cert_dict["username"],
            name=cert_dict["name"],
            description=cert_dict["description"],
            expiration=cert_dict["expiration"],
            expirated_at=define_expirated_at(cert_dict["expiration"]),
            groups=groups_id
        )

        return self.repo.insert(cert_ent)

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

