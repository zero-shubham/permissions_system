import sqlalchemy
from application import metadata


Token = sqlalchemy.Table(
    "tokens",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey(
        '_ps_users.id', ondelete="CASCADE"), primary_key=True),
    sqlalchemy.Column("token", sqlalchemy.String(length=1000),
                      nullable=False)
)

# class Token(db.Model):
#     __tablename__ = "tokens"
#     user_id = db.Column(db.ForeignKey(
#         '_ps_users.id', ondelete="CASCADE"), primary_key=True)
#     token = db.Column(db.String(length=1000), nullable=False)
