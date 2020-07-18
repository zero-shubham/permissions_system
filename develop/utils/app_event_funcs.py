from application import database, ps


async def startup():
    await database.connect()
    ps.setup()


async def shutdown():
    await database.disconnect()
