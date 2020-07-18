from sqlalchemy import (
    MetaData,
    Table,
    Column,
    String,
    ForeignKey,
    Boolean
)
from sqlalchemy.dialects.postgresql import (
    UUID
)
from permissions_system.constants import InternalTables


def get_permissions_table(metadata: MetaData):
    return Table(
        f"{InternalTables.Permission}",
        metadata,
        Column("id", UUID, primary_key=True),
        Column("group", ForeignKey(
            "_ps_user_groups.group",
            ondelete="CASCADE"
        )),
        Column("resource", ForeignKey(
            "_ps_resources.resource_table",
            ondelete="CASCADE"
        )),
        Column("create", Boolean, default=False),
        Column("read", Boolean, default=False),
        Column("update", Boolean, default=False),
        Column("delete", Boolean, default=False),
    )


def get_user_groups_table(metadata: MetaData):
    return Table(
        f"{InternalTables.UserGroup}",
        metadata,
        Column("id", UUID, primary_key=True),
        Column("group", String(length=500), unique=True)
    )


def get_resources_table(metadata: MetaData):
    return Table(
        f"{InternalTables.Resource}",
        metadata,
        Column("id", UUID, primary_key=True),
        Column("resource_table", String(length=500), unique=True),
        Column("resource_name", String(length=600))
    )


def get_users_table(metadata: MetaData):
    return Table(
        f"{InternalTables.User}",
        metadata,
        Column("id", UUID, primary_key=True),
        Column("user_name", String(
            length=500), unique=True),
        Column("password", String(length=1000)),
        Column("group", ForeignKey(
            "_ps_user_groups.group",
            ondelete="CASCADE"
        ))
    )
