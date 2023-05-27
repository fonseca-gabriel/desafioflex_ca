from group.usecases import GroupSchema
from models import SQLGroup
from entities import Group


class SQLGroupRepo:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        print("### group / repos / get_all")
        db_groups = SQLGroup.query.all()
        groups = []
        for db_group in db_groups:
            group = Group(
                id=db_group.id,
                name=db_group.name,
                created_at=db_group.created_at,
                updated_at=db_group.updated_at
            )
            groups.append(group)

        return 200, groups

    def insert(self, group):
        print("### group / repos / insert")
        db_group = SQLGroup(
            name=group.name,
        )

        self.db.session.add(db_group)
        self.db.session.commit()
        group.id = db_group.id

        return 200, group

    def get_by_name(self, group):
        print("### group / repos / get_by_name")
        db_group = SQLGroup.query.filter_by(name=group).first()
        if db_group:
            group_ent = Group(
                id=db_group.id,
                name=db_group.name,
                created_at=db_group.created_at,
                updated_at=db_group.updated_at,
            )
            return 200, group_ent
        return 400, None

    def get_by_id(self, group_id):
        print("### group / repos / get_by_id")
        group_query = self.db.session.get(SQLGroup, group_id)
        if group_query:
            group_ent = Group(
                id=group_query.id,
                name=group_query.name,
                created_at=group_query.created_at,
                updated_at=group_query.updated_at,
            )
            return 200, group_ent

        return 404, None

    def delete(self, group_id):
        print("### group / repos / delete")
        group_query = self.db.session.get(SQLGroup, group_id)

        if group_query:
            self.db.session.delete(group_query)
            self.db.session.commit()
            return 200, True

        return 404, False

    def update(self, group_id, group_ent):
        print("### group / repos / update")

        group_query = self.db.session.get(SQLGroup, group_id)
        group_query.name = group_ent.name

        self.db.session.commit()

        return 200, group_ent
