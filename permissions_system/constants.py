from enum import Enum


class PermissionTypesEnum(str, Enum):
    create = "create"
    read = "read"
    update = "update"
    delete = "delete"


class InternalTables(str, Enum):
    User = "_ps_users"
    UserGroup = "_ps_user_groups"
    Resource = "_ps_resources"
    Permission = "_ps_permissions"

    class Config:
        allow_mutation = False
