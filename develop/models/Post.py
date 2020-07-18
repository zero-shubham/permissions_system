import sqlalchemy
from application import database, metadata


Post = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey(
        '_ps_users.id', ondelete="CASCADE"), primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(length=500)),
    sqlalchemy.Column("content", sqlalchemy.TEXT())
)
