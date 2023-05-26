from usecases_group import GroupSchema
from models import SQLGroup


class SQLGroupRepo:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        groups_list = GroupSchema(many=True).dump(SQLGroup.query.all())
        return 200, groups_list

    def insert(self, group):
        db_group = SQLGroup(
            name=group.name,
            description=group.description,
        )

        self.db.session.add(db_group)
        self.db.session.commit()

        group_serialized = GroupSchema().dump(db_group)
        return 200, group_serialized

    def get_by_name(self, group):
        group_query = SQLGroup.query.filter_by(name=group).first()
        if group_query:
            return 200, group_query
        return 400, None

    def get_by_id(self, group_id):
        group_query = self.db.session.get(SQLGroup, group_id)
        if group_query:
            return 200, group_query
        return 404, None

    def delete(self, group_id):
        group_query = self.db.session.get(SQLGroup, group_id)

        if group_query:
            self.db.session.delete(group_query)
            self.db.session.commit()
            return 200, True

        return 404, False

    def update(self, group_id, group):

        group_query = self.db.session.get(SQLGroup, group_id)
        group_query.name = group.name

        self.db.session.commit()

        group_serialized = GroupSchema().dump(group_query)
        return 200, group_serialized
