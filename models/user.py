from pydantic import BaseModel

# 用户注册
class UserRegister(BaseModel):
    username:str
    password:str

# 用户登录
class UserLogin(BaseModel):
    username:str
    password:str