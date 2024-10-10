from fastapi import status, HTTPException, Depends

from fastapi.security import (
    APIKeyHeader,
)
from sqlalchemy.orm import Session
from db import get_db
from models import User


api_key_header = APIKeyHeader(name="Token", auto_error=False)


async def get_user_by_token(token: str):
    db = next(get_db())

    return db.query(User).filter(
        User.token == token,
    ).first()


async def user_auth(
        api_key: APIKeyHeader | None = Depends(api_key_header),
):
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found",
        )

    user = await get_user_by_token(api_key)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    return user
