from pydantic import BaseModel

# comment发表
class CommentCreate(BaseModel):
    user_id:int
    content:str
