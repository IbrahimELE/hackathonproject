from pydantic import BaseModel
from datetime import datetime
from enum import Enum 

class Like_type(str, Enum):
    post = "post"
    comment = "comment"
    
class Likes(BaseModel):
    id: int
    user_id: int 
    post_id: int | None
    comment_id: int | None
    type: Like_type

class LikesCreate(BaseModel):
    user_id: int  
    post_id: int | None = None
    comment_id: int | None = None  
    type: Like_type

class LikesOut(BaseModel):
    id: int
    user_id: int  
    post_id: int | None
    comment_id: int | None
    type: Like_type
    created_at: datetime
