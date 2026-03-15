from fastapi import APIRouter
from models.comment import CommentCreate
from fastapi import Depends
import pymysql.cursors
import database
from utils import response
from auth import verify_token

router = APIRouter()

# 用户发表评论
@router.post("/posts/{post_id}/comments/")
async def comment(post_id: int,commentcreate:CommentCreate,current_user:dict = Depends(verify_token)):
    connention = database.get_connection()
    with connention:
        with connention.cursor() as cursor:
            sql = "INSERT INTO comments (user_id,post_id,content) VALUES(%s,%s,%s)"
            cursor.execute(sql,(commentcreate.user_id,post_id,commentcreate.content))
        connention.commit()
    return response(201,"comment successfully")

# 返回某个帖子的全部评论
@router.get("/posts/{post_id}/comments/")
async def get_comments(post_id:int):
    connection = database.get_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT users.username, comments.content, comments.created_at FROM comments JOIN users ON comments.user_id = users.id WHERE comments.post_id = %s order by comments.created_at"
            cursor.execute(sql,(post_id,))
            result = cursor.fetchall()
    return response(200,"get comments successfully",result)

# 删除某个评论
@router.delete("/comments/{comment_id}")
async def delete_comment(comment_id:int,current_user: dict = Depends(verify_token)):
    connection = database.get_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT user_id FROM comments WHERE id=%s"
            cursor .execute(sql,(comment_id,))
            result = cursor.fetchone()

        if current_user['user_id']!=result['user_id']:
            return "sorry!you do not have right to delete this comment!"

        with connection.cursor() as cursor:
            sql = "DELETE FROM comments WHERE id=%s"
            cursor.execute(sql,(comment_id,))
        connection.commit()
    return response(200,"delete succcessfully")