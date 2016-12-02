from sys import maxsize


class Project:

    def __init__(self, name, id=None, status=None, inherit=None, view=None, description=None, enabled=None):
        self.name = name
        self.id = id
        self.status = status
        self.inherit = inherit
        self.view = view
        self.description = description
        self.enabled = enabled

    def __repr__(self):
        return '%s : %s: %s: %s: %s: %s: %s' % (self.id, self.name, self.status, self.inherit, self.view, self.description, self.enabled)

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.name == other.name

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize
