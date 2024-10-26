from sqlalchemy import Column, String, Enum, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from database import Base

class Like_type(str, PyEnum):
    post = "post"
    comment = "comment"

class LikesDB(Base):
    __tablename__ = "likes"
    __table_args__ = {'schema': 'baza'}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("baza.users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("baza.posts.id"), nullable=True)
    comment_id = Column(Integer, ForeignKey("baza.comments.id"), nullable=True)
    type = Column(Enum(Like_type), nullable=False)

    user = relationship("UsersDB", back_populates="likes")
    post = relationship("PostsDB", back_populates="post_likes")
    comment = relationship("CommentsDB", back_populates="comment_likes")