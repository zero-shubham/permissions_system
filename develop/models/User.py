from enum import Enum, IntEnum
import sqlalchemy
from application import database, metadata


class UserTypeEnum(str, Enum):
    admin = "Admin"
    user = "User"


User = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(length=250), unique=True),
    sqlalchemy.Column("password", sqlalchemy.String(length=500)),
    sqlalchemy.Column("user_type", sqlalchemy.Enum(UserTypeEnum))
)
