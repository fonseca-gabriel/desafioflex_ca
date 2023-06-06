from datetime import datetime, timedelta
from marshmallow import fields, Schema, ValidationError
from marshmallow.validate import Length, And, Regexp, Range
from entities import Certificate


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

    def create(self, cert_data):
        print("### cert / usecases / create")
        try:
            cert_dict = CertificateSchema().load(cert_data)
        except ValidationError as err:
            return 400, err.messages

        status, cert_ent_or_error = self.repo.get_by_username(cert_dict.get("username"))
        if status == 200:
            return 409, None

        groups_id = []
        for group_id in cert_dict.get("groups"):
            status, group_ent = self.group_uc.get_by_id(group_id)
            if status == 404:
                return 400, f"Erro, grupo com ID {group_id} não existe"
            groups_id.append(group_ent.id)

        cert_ent = Certificate(
            id=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            username=cert_dict.get("username"),
            name=cert_dict.get("name"),
            description=cert_dict.get("description"),
            expiration=cert_dict.get("expiration"),
            expirated_at=define_expirated_at(cert_dict.get("expiration")),
            groups=groups_id
        )

        status, cert_ent_inserted_or_error = self.repo.insert(cert_ent)
        if status == 404:
            return status, f"Erro, grupo {cert_ent_inserted_or_error} não existe"

        # Adicionar chamada para infra aqui

        return status, cert_ent

    def get_by_id(self, cert_id):
        print("### cert / usecases / get_by_id")

        status, cert_ent = self.repo.get_by_id(cert_id)

        if status == 404:
            return 404, None

        return 200, cert_ent

    def delete(self, cert_id):
        status, cert_ent = self.repo.get_by_id(cert_id)

        if status == 404:
            return 404, None

        # Adicionar chamada para infra aqui

        return self.repo.delete(cert_id)

    def update(self, cert_id, cert_data):
        print("### cert / usecases / update")

        try:
            cert_dict = CertificateSchema(partial=True).load(cert_data)
        except ValidationError as err:
            return 400, err.messages

        status, cert_ent = self.repo.get_by_id(cert_id)

        if status == 404:
            return 404, f"certificado com ID {cert_id} não existe"

        if status == 200:
            if cert_dict.get("name"):
                cert_ent.name = cert_dict.get("name")
            if cert_dict.get("description"):
                cert_ent.description = cert_dict.get("description")
            if cert_dict.get("groups"):
                cert_ent.groups = cert_dict.get("groups")
            cert_ent.updates_at = datetime.now()

            status, cert_ent_or_error = self.repo.update(cert_id, cert_ent)
            if status == 404:
                return 404, f"grupo {cert_ent_or_error} não existe"

            return status, cert_ent

        return 409, None


