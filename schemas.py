from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    username: str
    password: str


class WalletCreate(BaseModel):
    user_id: Optional[int] = None
    currency: str