class Certificate:
    def __init__(self, id, username, name, description, expiration, expirated_at, groups, created_at, updated_at):
        self.id = id
        self.username = username
        self.name = name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        self.expiration = expiration
        self.expirated_at = expirated_at
        self.groups = groups


class Group:
    def __init__(self, id, name, created_at, updated_at):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
