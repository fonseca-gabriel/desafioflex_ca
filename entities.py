class Certificate:
    def __init__(self, id, username, name, description, created_at, updated_at, expiration, expirated_at, groups):
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
    def __init__(self, id, created_at, updated_at, name, description):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
