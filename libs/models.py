from enum import unique
from tokenize import String
from xmlrpc.client import Boolean
from libs.database import Base
from sqlalchemy import Column, Integer, Boolean, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
