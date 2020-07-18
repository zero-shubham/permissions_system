from models.Token import Token
from application import database
from uuid import UUID


async def check_token_in_db(user_id: UUID, token: str):
    query = Token.select().where(Token.columns.user_id ==
                                 user_id).where(
                                     Token.columns.token == token)
    token_in_db = await database.fetch_one(query)
    return token_in_db


async def find_token_by_user_id(user_id: UUID):
    query = Token.select().where(Token.columns.user_id ==
                                 user_id)
    token_in_db = await database.fetch_one(query)
    return token_in_db


async def add_token_in_db(user_id: UUID, token: str):
    token_in_db = await find_token_by_user_id(user_id)
    if token_in_db:
        query = Token.update().values(token=token)
    else:
        query = Token.insert().values(user_id=user_id, token=token)
    await database.execute(query)
    return user_id


async def remove_token_in_db(user_id: UUID):
    query = Token.delete().where(Token.columns.user_id == user_id)
    user_id = await database.execute(query)
    return user_id
