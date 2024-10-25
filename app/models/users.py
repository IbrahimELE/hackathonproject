from sqlalchemy import Column, String, Enum, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from database import Base

class UsersDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email_address = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)

    posts = relationship("PostsDB", back_populates="user")
    comments = relationship("CommentsDB", back_populates="user")
    likes = relationship("LikesDB", back_populates="user")
