from sqlalchemy import Column, String, Enum, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from database import Base

class CommentsDB(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    content = Column(String(255), nullable=False)
    likes = Column(Integer, nullable=True, default=0)

    user = relationship("UsersDB", back_populates="comments")
    post = relationship("PostsDB", back_populates="comments")
    comment_likes = relationship("LikesDB", back_populates="comment")