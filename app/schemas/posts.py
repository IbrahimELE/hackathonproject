from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum
from datetime import datetime
from typing import List
from likes import Likes
from comments import Comments


class Post_status(str, Enum):
    hidden = "hidden"
    friends_only = "Friends only"
    public = "public"

class PostCreate(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    created_at: datetime
    post_status: Post_status = Post_status.hidden

    model_config = ConfigDict(arbitrary_types_allowed=True)

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        from_atributes = True

class Post(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    created_at: datetime
    post_status: Post_status = Post_status.hidden
    likes: List[Likes] = []  
    comments: List[Comments] = []  

    model_config = ConfigDict(arbitrary_types_allowed=True)