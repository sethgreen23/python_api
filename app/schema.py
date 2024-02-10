from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    # rating: Optional[int] = None # optional and default to none
    published: bool = True # optional

# request schema model    
class CreatePost(PostBase):
    pass

class UpdatePost(BaseModel):
    title: str
    content: str
    published: bool


# response schema model
class Post(PostBase):
    created_at: datetime
    class Config:
        orm_mode = True
    
