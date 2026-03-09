from pydantic import BaseModel

# post发布
class PostCreate(BaseModel):
    user_id:int
    title:str
    content:str
