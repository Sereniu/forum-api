from fastapi import FastAPI
from pydantic import BaseModel
import bcrypt
import database
import pymysql.cursors

# 用户注册
class UserRegister(BaseModel):
    username:str
    password:str

# 用户登录
class UserLogin(BaseModel):
    username:str
    password:str

app = FastAPI()

# 用户注册API
@app.post("/register/")
async def register(userregister:UserRegister):
    pw=userregister.password.encode()
    hashed=bcrypt.hashpw(pw,bcrypt.gensalt())

    connection=database.get_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (username,password) VALUES(%s,%s)"
            cursor.execute(sql,(userregister.username,hashed.decode("utf-8")))
        connection.commit()
    return userregister.username+' '+"register successfully!"

# 用户登录API
@app.post("/login/")
async def login(userlogin:UserLogin):
    connection = database.get_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT password from users where users.username=%s"
            cursor.execute(sql,(userlogin.username,))
            result = cursor.fetchone()
    if bcrypt.checkpw(userlogin.password.encode(),result[0].encode()):
        return "login successfully"
    else :
        return "failed to login"