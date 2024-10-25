from sqlalchemy import Column, String, Enum, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from database import Base

class Post_status(str, PyEnum):
    hidden = "hidden"
    friends_only = "friends"
    public = "public"

class PostsDB(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    post_status = Column(Enum(Post_status), nullable=False)
    likes = Column(Integer, nullable=True, default=0)
    comments = Column(Integer, nullable=True, default=0)

    user = relationship("UsersDB", back_populates="posts")
    comments = relationship("CommentsDB", back_populates="post")
    post_likes = relationship("LikesDB", back_populates="post")
