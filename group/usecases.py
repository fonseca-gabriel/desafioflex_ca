from datetime import datetime
from marshmallow import fields, Schema, ValidationError
from marshmallow.validate import Length
from entities import Group


class GroupSchema(Schema):

    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    name = fields.String(required=True, validate=Length(max=30))

    class Meta:
        fields = ('id', 'name', 'created_at', 'updated_at')


class GroupUC:
    def __init__(self, repo):
        self.repo = repo

    def get_all(self):
        print("### group / usecases / get_all")
        return self.repo.get_all()

    def create(self, data):
        print("### group / usecases / create")
        try:
            group_dict = GroupSchema().load(data)
        except ValidationError as err:
            return 400, err.messages

        status, group_ent = self.repo.get_by_name(group_dict.get("name"))
        if status == 200:
            return 409, None

        group = Group(
            id=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            name=group_dict.get("name"),
        )

        return self.repo.insert(group)

    def get_by_id(self, group_id):
        print("### group / usecases / get_by_id")
        status, group_ent = self.repo.get_by_id(group_id)

        if status == 404:
            return 404, None

        return 200, group_ent

    def delete(self, group_id):
        print("### group / usecases / delete")
        status, group_exists = self.repo.get_by_id(group_id)

        if status == 404:
            return 404, None

        return self.repo.delete(group_id)

    def update(self, group_id, data):
        print("### group / usecases / update")
        try:
            group_dict = GroupSchema().load(data)
        except ValidationError as err:
            return 400, err.messages

        status, group = self.repo.get_by_name(group_dict.get("name"))
        if status == 200:
            return 409, None

        status, group_ent = self.repo.get_by_id(group_id)

        if status == 200:
            group_ent.name = group_dict.get("name")
            group_ent.updates_at = datetime.now()
            return self.repo.update(group_id, group_ent)

        return 409, None
