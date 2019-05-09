import json
from enum import (
    Enum,
    auto,
)


class UserRole(Enum):
    guest = auto()
    normal = auto()


class MvcEncoder(json.JSONEncoder):
    prefix = "__enum__"

    def default(self, o):
        if isinstance(o, UserRole):
            return {self.prefix: o.name}
        else:
            return super().default(o)


def mvc_decode(d):
    if MvcEncoder.prefix in d:
        name = d[MvcEncoder.prefix]
        return UserRole[name]
    else:
        return d
