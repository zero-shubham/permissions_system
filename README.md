# Permissions Systems
##### _It's plugin for fastapi (but can be used with similar frameworks), that provides a minimal_
##### _setup for maintaining resources and related permissions for user-groups._

#### How to use it?

**application.py**

```python
from fastapi import FastAPI
import databases
import sqlalchemy
import os
from permissions_system.PermissionsSystemDatabases import PermissionsS

app = FastAPI()

DB_URI = os.environ["DB_URI"]

database = databases.Database(DB_URI)
metadata = sqlalchemy.MetaData()
ps = PermissionsS(metadata, database, DB_URI)


app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)

async def startup():
    await database.connect()
    await ps.setup()
```
*Step1 -* __instantiate PermissionsS class.__

*Step2 -* __during startup event after database is connected make a call to setup()__
*_________________________________________________________________________________________*

__*PermissionsS will then detect your tables add them to resources, add super-admin user-group, if there aren't already. Everytime there is a new resource that gets added automatically to resources table. User-group super-admin by default has all CRUD permissions for all resources. To add a new user-group and related permissions use built-in functions add_user_group and add_permissions.*__

*PermissionsSystem is not like djano-admin or flask-admin. It doesn't provide a front-end, it provides a minimal setup to manage resources and permissions. It aims to provide autonomy and more control over to the developer.*