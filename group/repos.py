from models import SQLGroup
from entities import Group


class SQLGroupRepo:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        print("### group / repos / get_all")
        db_groups = SQLGroup.query.all()

        groups_ent_list = []
        for db_group in db_groups:
            group_ent = Group(
                id=db_group.id,
                name=db_group.name,
                created_at=db_group.created_at,
                updated_at=db_group.updated_at
            )
            groups_ent_list.append(group_ent)

        return 200, groups_ent_list

    def insert(self, group_ent):
        print("### group / repos / insert")
        db_group = SQLGroup(
            name=group_ent.name,
            created_at=group_ent.created_at,
            updated_at=group_ent.updated_at,
        )

        self.db.session.add(db_group)
        self.db.session.commit()
        group_ent.id = db_group.id

        return 200, group_ent

    def get_by_name(self, group_name):
        print("### group / repos / get_by_name")
        db_group = SQLGroup.query.filter_by(name=group_name).first()
        if db_group:
            group_ent = Group(
                id=db_group.id,
                name=db_group.name,
                created_at=db_group.created_at,
                updated_at=db_group.updated_at,
            )
            return 200, group_ent
        return 404, None

    def get_by_id(self, group_id):
        print("### group / repos / get_by_id")
        db_group = self.db.session.get(SQLGroup, group_id)
        if db_group:
            group_ent = Group(
                id=db_group.id,
                name=db_group.name,
                created_at=db_group.created_at,
                updated_at=db_group.updated_at,
            )
            return 200, group_ent

        return 404, None

    def delete(self, group_id):
        print("### group / repos / delete")
        db_group = self.db.session.get(SQLGroup, group_id)

        if db_group:
            self.db.session.delete(db_group)
            self.db.session.commit()
            return 200, True

        return 404, False

    def update(self, group_id, group_ent):
        print("### group / repos / update")
        db_group = self.db.session.get(SQLGroup, group_id)
        db_group.name = group_ent.name
        self.db.session.commit()
        return 200, group_ent

    def get_db_group_by_id(self, group_id):
        print("### group / repos / get_db_group_by_id")
        db_group = self.db.session.get(SQLGroup, group_id)
        if db_group:
            return 200, db_group

        return 404, None
