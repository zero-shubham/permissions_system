from core.config import SECRET_KEY
from core.security import pwd_context
from gino.ext.starlette import Gino
from permissions_system.PermissionsSystem import PermissionsS
import os
import sqlalchemy
import databases
from dotenv import load_dotenv
from fastapi import FastAPI
import sys
import pathlib
sys.path.extend([str(pathlib.Path(__file__).parent.parent.absolute())])

# from permissions_system.AuthenticationSystem import AuthenticationSys

load_dotenv(verbose=True)
app = FastAPI(title="React-Admin Backend")

DB_URI = os.environ["DB_URI"]

# db = Gino(app, dsn=DB_URI)
database = databases.Database(DB_URI)
metadata = sqlalchemy.MetaData()
ps = PermissionsS(metadata, DB_URI)

# auth_sys = AuthenticationSys(
#     pwd_context=pwd_context,
#     metadata=metadata,
#     database=database,
#     DB_URL=DB_URI,
#     SECRET_KEY=SECRET_KEY
# )
