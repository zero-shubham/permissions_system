from databases import Database
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    String,
    ForeignKey,
    Boolean,
    create_engine
)
from sqlalchemy.dialects.postgresql import (
    UUID
)
from uuid import (
    uuid4,
    UUID as UUIDModel
)
from permissions_system.constants import PermissionTypesEnum
from pydantic import BaseModel
import logging
from typing import List


class ResourceWithPermissions(BaseModel):
    id: UUIDModel
    resource: str
    create: bool
    read: bool
    update: bool
    delete: bool


class PermissionsS():
    def __init__(self,  metadata: MetaData, database: Database, DB_URL: str):
        self.metadata = metadata
        self.DB_URL = DB_URL
        self.database = database
        self.UserGroup = Table(
            "_ps_user_groups",
            self.metadata,
            Column("id", UUID, primary_key=True),
            Column("group", String(length=500), unique=True)
        )

        self.Resource = Table(
            "_ps_resources",
            self.metadata,
            Column("id", UUID, primary_key=True),
            Column("resource_table", String(length=500), unique=True),
            Column("resource_name", String(length=600))
        )

        self.Permission = Table(
            "_ps_permissions",
            self.metadata,
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

        self.User = Table(
            "_ps_users",
            self.metadata,
            Column("id", UUID, primary_key=True),
            Column("user_name", String(
                length=500), unique=True),
            Column("password", String(length=1000)),
            Column("group", ForeignKey(
                "_ps_user_groups.group",
                ondelete="CASCADE"
            ))
        )

    # * ---- ADD RESOURCES -----
    async def add_resources(self, new_resources: list):
        values = [
            {
                "id": uuid4(),
                "resource_name": self.table_to_name(resource),
                "resource_table": resource
            } for resource in new_resources
        ]
        resources = [ResourceWithPermissions(**{
            "id": uuid4(),
            "resource": resource,
            "create": True,
            "read": True,
            "update": True,
            "delete": True
        }) for resource in new_resources]

        query = self.Resource.insert()
        await self.database.execute_many(query=query, values=values)
        await self.add_permissions("super_admin", resources)
        logging.info(f"Resources {new_resources} were added.")

    # * ------- DELETE RESOURCES -------
    async def delete_resources(self, stale_resources: list):
        query = self.Resource.delete().where(
            self.Resource.c.resource_table.in_(stale_resources)
        )
        res = await self.database.execute(query)
        logging.info(f"Resources {stale_resources} were removed.")

# * ------ ADD USER GROUPS ------------
    async def add_user_group(self, user_group: str):
        query = self.UserGroup.insert()
        values = {
            "id": uuid4(),
            "group": user_group
        }
        await self.database.execute(query=query, values=values)
        logging.info(f"UserGroup {user_group} added.")

# * ------ ADD PERMISSIONS ------------
    async def add_permissions(
        self,
        user_group: str,
        resources: List[ResourceWithPermissions]
    ):
        query = self.Permission.insert()
        values = [
            {
                "id": uuid4(),
                "group": user_group,
                "resource": rwp.resource,
                "create": rwp.create,
                "read": rwp.read,
                "update": rwp.update,
                "delete": rwp.delete
            } for rwp in resources
        ]
        await self.database.execute_many(query=query, values=values)
        logging.info(f"Permissons added for {user_group} as {values}")

    # * ----- INIT SUPER ADMIN ------
    async def _init_super_admin(self):
        query = self.UserGroup.select().where(
            self.UserGroup.columns.group == "super_admin")

        super_admin = await self.database.fetch_val(query)
        if not super_admin:
            # add super_admin to user group also add permissions
            await self.add_user_group("super_admin")
            # get all resources and provide super_admin permissions for each
            query = self.Resource.select()
            resources = await self.database.fetch_all(query=query)
            resources = [ResourceWithPermissions(**{
                "id": uuid4(),
                "resource": resource.get("resource_table"),
                "create": True,
                "read": True,
                "update": True,
                "delete": True
            }) for resource in resources]
            await self.add_permissions("super_admin", resources)
            logging.info(f"SuperAdmin was initialised.")

    async def setup(self):
        engine = create_engine(self.DB_URL)
        self.metadata.create_all(engine)
        all_tables = list(self.metadata.tables.keys())

        query = self.Resource.select().with_only_columns(
            [self.Resource.c.resource_table])
        resources = await self.database.fetch_all(query)
        resources = [res.get("resource_table") for res in resources]

        # check if "super_admin" User group exists
        # if not add it
        await self._init_super_admin()

        #  if there are some stale resources get rid of them
        stale_resources = [
            resource for resource in resources if resource not in all_tables]
        if len(stale_resources):
            await self.delete_resources(stale_resources)

        # if there are some new tables add them to resources
        new_tables = [table for table in all_tables if table not in resources]
        if len(new_tables):
            await self.add_resources(new_tables)

        self.current_user_groups = await self.get_user_groups()

    async def create_user(
        self,
        user_id: UUIDModel,
        user_name: str,
        password: str,
        user_group: str
    ):
        query = self.User.insert().values(
            id=user_id,
            user_name=user_name,
            password=password,
            group=user_group
        )
        await self.database.execute(query)
        return user_id

    async def get_user_groups(self):
        query = self.UserGroup.select().with_only_columns(
            [self.UserGroup.c.group]
        )
        user_groups = await self.database.fetch_all(query)
        user_groups = [user_group.get("group") for user_group in user_groups]
        return user_groups

    async def user_has_permissions(
        self,
        user_id: int,
        resource: str,
        permission_type: PermissionTypesEnum
    ):
        query = self.Permission.select().select_from(
            self.Permission.join(self.UserGroup.join(self.User))
        ).where(
            self.Permission.c.resource == resource
        )
        res = await self.database.fetch_one(query)
        res = dict(res.items())
        return res[permission_type]

    @classmethod
    def table_to_name(cls, val: str) -> str:
        tmp = val.split("_")
        tmp = [t.capitalize() for t in tmp]
        return " ".join(tmp)
