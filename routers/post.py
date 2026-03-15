from fastapi import APIRouter
from models.post import PostCreate
from fastapi import Depends
from jose import jwt,JWTError
from auth import verify_token
import pymysql.cursors
import database
from utils import response

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
    return response(201,"post successfully")

# 返回所有的帖子
@router.get("/posts/")
async def get_posts():
    connection = database.get_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM posts order by views DESC"
            cursor.execute(sql,)
            result = cursor.fetchall()
    return response(200,"get posts successfully",result)

# 返回要看的post
@router.get("/posts/{id}")
async def get_post(id:int):
    connection = database.get_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "UPDATE posts SET views=views+1 WHERE id=%s"
            cursor.execute(sql,(id,))
            sql = "SELECT * FROM posts WHERE id=%s"
            cursor.execute(sql,(id,))
            result = cursor.fetchone()
        connection.commit()
    return response(200,"get post successfully",result)