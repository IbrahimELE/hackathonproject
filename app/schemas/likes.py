from pydantic import BaseModel
from datetime import datetime
from enum import Enum 

class Like_type(str, Enum):
    post = "post"
    comment = "comment"
    
class Likes(BaseModel):
    id: int
    user_id: int  
    post_id: int 
    comment_id: int
    type: Like_type

