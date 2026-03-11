from fastapi import APIRouter
from models.post import PostCreate
from fastapi import Header
from fastapi import Depends
from jose import jwt,JWTError
import pymysql.cursors
import database

def verify_token(authorization:str = Header()):
    token = authorization.replace("Bearer ","")
    payload = jwt.decode(token,'secret',algorithms=['HS256'])
    return payload

router = APIRouter()

# 用户发帖子
@router.post("/posts/")
async def post(postcreate:PostCreate,current_user: dict=Depends(verify_token)):
    connection = database.get_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO posts (user_id,title,content) VALUES(%s,%s,%s)"
            cursor.execute(sql,(postcreate.user_id,postcreate.title,postcreate.content))
        connection.commit()
    return "post successfully"

# 返回所有的帖子
@router.get("/posts/")
async def get_posts():
    connection = database.get_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM posts"
            cursor.execute(sql,)
            result = cursor.fetchall()
    return result

# 返回要看的post
@router.get("/posts/{id}")
async def get_post(id:int):
    connection = database.get_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM posts WHERE id=%s"
            cursor.execute(sql,(id))
            result = cursor.fetchone()
    return result