from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional

Base = declarative_base()


class User(Base):
    """
    User model representing a registered user in the system.
    
    Attributes:
        id (int): Unique identifier for the user (primary key).
        email (str): User's email address (must be unique and non-null).
        hashed_password (str): Hashed password for authentication (non-null).
    """
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)