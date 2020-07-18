# Permissions Systems

##### _It's plugin for ~~fastapi (but can be used with similar frameworks)~~ any frameworks, that provides a minimal_

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
    ps.setup()
```

> for Flask app you will call ps.setup() after db.init(app), assuming you are using flask_sqlalchemy

_Step1 -_ **instantiate PermissionsS class.**

_Step2 -_ **during startup event after database is connected make a call to setup()**
_********\*\*\*\*********\*\*\*\*********\*\*\*\*********\_********\*\*\*\*********\*\*\*\*********\*\*\*\*********_

**\_PermissionsS will then detect your tables add them to resources, add super-admin user-group, if there isn't already one. Everytime there is a new resource that gets added automatically to resources table. User-group super-admin by default has all CRUD permissions for all resources. To add a new user-group and related permissions use built-in functions add_user_group and add_permissions. To get whether a particular user has CRUD permissions for a particular resource you will call**
**> ps.user_has_permissions(user_id:UUID,resource:str,permission_type:PermissionTypesEnum) -> bool\***

_PermissionsSystem is not like django-admin or flask-admin. It doesn't provide a front-end admin dashboard, but a minimal setup to manage resources and permissions. It aims to provide autonomy and more control over to the developer. For front-end you will end up using something more custom or [React-admin](https://marmelab.com/react-admin/) or [vue-element-admin](https://github.com/PanJiaChen/vue-element-admin)_

#### What's next?

- Provide examples.

## PermissionsSystem now only uses sqlalchemy and is completely sync.
