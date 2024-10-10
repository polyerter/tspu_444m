from sqlalchemy import Integer, String, Column, Boolean, DateTime, Float, ForeignKey
from database import Base
import datetime
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "app_users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True,)
    password = Column(String,)
    is_active = Column(Boolean, default=True)

    token = Column(String, default=None)
    restore_token = Column(String, default=None)
    wallets = relationship("Wallet", back_populates="user")


class UserLoggin(Base):
    __tablename__ = "app_user_loggin"

    id = Column(Integer, primary_key=True)
    email = Column(String, index=True)
    created_at = Column(DateTime,)


class Wallet(Base):
    __tablename__ = "app_wallets"

    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Float)
    currency = Column(String, default="USD")
    user_id = Column(Integer, ForeignKey("app_users.id"))

    user = relationship("User", back_populates="wallets")