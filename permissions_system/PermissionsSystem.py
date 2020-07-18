from sqlalchemy import (
    MetaData,
    create_engine,
    inspect
)
from sqlalchemy.orm import sessionmaker
from uuid import (
    uuid4,
    UUID as UUIDModel
)
from permissions_system.constants import PermissionTypesEnum
from permissions_system.models import (
    get_permissions_table,
    get_resources_table,
    get_user_groups_table,
    get_users_table
)
from pydantic import BaseModel
import logging
from typing import List

logging.basicConfig(level=logging.DEBUG)


class ResourceWithPermissions(BaseModel):
    id: UUIDModel
    resource: str
    create: bool
    read: bool
    update: bool
    delete: bool


class PermissionsS():
    def __init__(self,  metadata: MetaData,  DB_URL: str):
        self.metadata = metadata
        self.DB_URL = DB_URL
        self.Session = sessionmaker()

        self.UserGroup = get_user_groups_table(self.metadata)

        self.Resource = get_resources_table(self.metadata)

        self.Permission = get_permissions_table(self.metadata)

        self.User = get_users_table(self.metadata)

    # * ---- ADD RESOURCES -----

    def add_resources(self, new_resources: list):
        session = self.Session()
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
        session.execute(query=query, values=values)
        session.commit()
        self.add_permissions("super_admin", resources)
        logging.info(f"Resources {new_resources} were added.")

    # * ------- DELETE RESOURCES -------
    def delete_resources(self, stale_resources: list):
        session = self.Session()
        query = self.Resource.delete().where(
            self.Resource.c.resource_table.in_(stale_resources)
        )
        session.execute(query)
        session.commit()
        logging.info(f"Resources {stale_resources} were removed.")

# * ------ ADD USER GROUPS ------------
    def add_user_group(self, user_group: str):
        session = self.Session()
        query = self.UserGroup.insert()
        values = {
            "id": str(uuid4()),
            "group": user_group
        }
        session.execute(query, values)
        session.commit()
        logging.info(f"UserGroup {user_group} added.")

# * ------ ADD PERMISSIONS ------------
    def add_permissions(
        self,
        user_group: str,
        resources: List[ResourceWithPermissions]
    ):
        session = self.Session()
        query = self.Permission.insert()
        values = [
            {
                "id": str(uuid4()),
                "group": user_group,
                "resource": rwp.resource,
                "create": rwp.create,
                "read": rwp.read,
                "update": rwp.update,
                "delete": rwp.delete
            } for rwp in resources
        ]
        session.execute(query, values)
        session.commit()
        logging.info(f"Permissons added for {user_group} as {values}")

    # * ----- INIT SUPER ADMIN ------
    def _init_super_admin(self):
        session = self.Session()
        super_admin = session.query(self.UserGroup).filter_by(
            group="super_admin").first()

        if not super_admin:
            # * add super_admin to user group also add permissions
            self.add_user_group("super_admin")
            # * get all resources and provide super_admin permissions for each
            resources = session.query(self.Resource).all()
            resources = [ResourceWithPermissions(**{
                "id": uuid4(),
                "resource": resource[1],
                "create": True,
                "read": True,
                "update": True,
                "delete": True
            }) for resource in resources]
            self.add_permissions("super_admin", resources)
            logging.info(f"SuperAdmin was initialised.")

    def setup(self, exclude_tables: List[str] = []):
        # * create engine and bind to Session
        engine = create_engine(self.DB_URL)
        self.Session.configure(bind=engine)

        # * get list of tables by inspecting db
        inspector = inspect(engine)
        all_tables = [
            table_name for table_name in inspector.get_table_names(schema="public")]
        all_tables = [
            table
            for table in all_tables if table not in exclude_tables
        ]
        # * once all tables are declared try to create them
        self.metadata.create_all(engine)

        # * list all resource table names
        session = self.Session()
        resources = session.query(self.Resource.c.resource_table).all()
        resources = [res[0] for res in resources]

        # * check if "super_admin" User group exists
        # * if not add it
        self._init_super_admin()

        #  * if there are some stale resources get rid of them
        stale_resources = [
            resource for resource in resources if resource not in all_tables]
        if len(stale_resources):
            self.delete_resources(stale_resources)

        # if there are some new tables add them to resources
        new_tables = [table for table in all_tables if table not in resources]
        if len(new_tables):
            self.add_resources(new_tables)

        self.current_user_groups = self.get_user_groups()

    def create_user(
        self,
        user_id: UUIDModel,
        user_name: str,
        password: str,
        user_group: str
    ):
        session = self.Session()
        query = self.User.insert()
        session.execute(query, {
            "id": str(user_id),
            "user_name": user_name,
            "password": password,
            "group": user_group
        })
        session.commit()
        return user_id

    def get_user_groups(self):
        session = self.Session()
        user_groups = session.query(self.UserGroup.c.group).all()
        user_groups = [user_group[0] for user_group in user_groups]
        return user_groups

    def user_has_permissions(
        self,
        user_id: UUIDModel,
        resource: str,
        permission_type: PermissionTypesEnum
    ):
        session = self.Session()
        res = session.query(
            self.Permission.columns[permission_type]
        ).join(
            self.UserGroup
        ).join(
            self.User
        ).filter(
            self.Permission.c.resource == resource
        ).filter(
            self.User.c.id == user_id
        ).first()
        return res[0]

    @classmethod
    def table_to_name(cls, val: str) -> str:
        tmp = val.split("_")
        tmp = [t.capitalize() for t in tmp]
        return " ".join(tmp)
