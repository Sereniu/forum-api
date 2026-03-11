from fastapi import APIRouter,HTTPException
import bcrypt
import database
import pymysql.cursors
from models.user import UserLogin,UserRegister
from jose import jwt
from utils import response

router = APIRouter()

# 用户注册API
@router.post("/register/")
async def register(userregister:UserRegister):
    pw=userregister.password.encode()
    hashed=bcrypt.hashpw(pw,bcrypt.gensalt())

    connection=database.get_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO users (username,password) VALUES(%s,%s)"
            cursor.execute(sql,(userregister.username,hashed.decode("utf-8")))
        connection.commit()
    return response(200,"register successfully")

# 用户登录API
@router.post("/login/")
async def login(userlogin:UserLogin):
    connection = database.get_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT password,id from users where users.username=%s"
            cursor.execute(sql,(userlogin.username,))
            result = cursor.fetchone()
    if result is None:
        raise HTTPException(status_code=404,detail="用户不存在")
    elif bcrypt.checkpw(userlogin.password.encode(),result['password'].encode()):
        token = jwt.encode({'user_id':result['id']},'secret',algorithm='HS256')
        return response(200,"login successfully",token)
    else :
        return response(401,"password error")