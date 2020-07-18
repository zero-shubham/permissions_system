import asyncio
import sys
from email_validator import validate_email
from utils.app_event_funcs import startup, shutdown
from crud.user import create_new_user
from schemas.user import UserInDB


async def create_super_user():
    print("Enter SuperAdmin email: ")
    email = input()
    try:
        email = validate_email(email)["email"]
    except Exception as excep:
        print(excep, "\n Not a valid email.")
        return
    print("Enter SuperAdmin password: ")
    password = input()
    creation_success = await create_new_user(obj_in=UserInDB(**{
        "user_name": email,
        "group": "super_admin",
        "password": password
    }))

    if creation_success:
        print("\n *** Super Admin was successfully created. *** \n")
    else:
        print("\n Something went wrong, get hold of the developer! \n")


async def main():
    arguments = sys.argv
    await startup()
    if arguments[1] == "createsuperadmin":
        await create_super_user()

    await shutdown()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
        loop.run_until_complete(asyncio.sleep(2.0))
    finally:
        loop.close()
