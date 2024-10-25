from pydantic import BaseModel
from datetime import datetime

class Comments(BaseModel):
    id: int
    user_id: int  
    post_id: int  
    created_at: datetime
    content: str
    likes: int

class CommentsCreate(BaseModel):
    user_id: int  
    post_id: int  
    content: str

class CommentsOut(BaseModel):
    id: int
    user_id: int  
    post_id: int  
    created_at: datetime
    content: str
    likes: int