from sqlalchemy import Integer, String, Column, Boolean, DateTime
from database import Base
import datetime


class User(Base):
    __tablename__ = "app_users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True,)
    password = Column(String,)
    is_active = Column(Boolean, default=True)

    token = Column(String, default=None)
    restore_token = Column(String, default=None)

class UserLoggin(Base):
    __tablename__ = "app_user_loggin"

    id = Column(Integer, primary_key=True)
    email = Column(String, index=True)
    created_at = Column(DateTime,)

    