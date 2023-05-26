from marshmallow import fields, Schema, ValidationError
from marshmallow.validate import Length
from entities import Group


class GroupSchema(Schema):

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    name = fields.String(required=True, validate=Length(max=30))
    description = fields.String(required=True, validate=Length(max=255))

    class Meta:
        fields = ('id', 'name', 'description', 'created_at', 'updated_at')


class GroupUC:
    def __init__(self, repo):
        self.repo = repo

    def get_all(self):
        return self.repo.get_all()

    def create(self, data):
        try:
            group_dict = GroupSchema().load(data)
        except ValidationError as err:
            return 400, err.messages

        # Verifica se o name já existe
        status, name_existis = self.repo.get_by_name(group_dict["name"])
        if status == 200:
            return 409, None

        group_dict["id"] = None
        group_dict["created_at"] = None
        group_dict["updated_at"] = None
        group = Group(**group_dict)

        return self.repo.insert(group)

    def get_by_id(self, group_id):
        status, group_exists = self.repo.get_by_id(group_id)

        if status == 404:
            return 404, None

        group = Group(name=group_exists.name, id=group_exists.id)
        return 200, group

    def delete(self, group_id):
        status, group_exists = self.repo.get_by_id(group_id)

        if status == 404:
            return 404, None

        return self.repo.delete(group_id)

    def update(self, group_id, data):
        group_dict = GroupSchema().load(data)

        # Verifica se o name já existe
        status, name_existis = self.repo.get_by_name(group_dict["name"])
        if status == 200:
            return 409, None

        group = Group(name=group_dict["name"], id=None)
        return self.repo.update(group_id, group)
