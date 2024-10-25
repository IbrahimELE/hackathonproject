from sqlalchemy import Column, String, Enum, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from database import Base

class UsersDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True)  
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email_address = Column(String(255), unique=True, index=True)  
    password = Column(String(255), nullable=False)  

    posts = relationship("PostsDB", back_populates="user")
    comments = relationship("CommentsDB", back_populates="user")
    likes = relationship("LikesDB", back_populates="user")
