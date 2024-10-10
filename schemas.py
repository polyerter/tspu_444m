from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    username: str
    password: str


class WalletCreate(BaseModel):
    user_id: int | None = None
    currency: str