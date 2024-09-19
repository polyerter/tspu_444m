from sqlalchemy import Integer, String, Column, Boolean
from database import Base


class User(Base):
    __tablename__ = "app_users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True,)
    password = Column(String,)
    is_active = Column(Boolean, default=True)
