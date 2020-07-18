from fastapi import (
    HTTPException,
    Security,
    status
)
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError
from schemas.token import TokenPayload
from core.config import SECRET_KEY
from core.jwt import ALGORITHM
from crud.user import find_user_by_id
from crud.token import check_token_in_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(token: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    token_is_valid = await check_token_in_db(token_data.user_id, token)

    if not token_is_valid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    user = await find_user_by_id(user_id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
