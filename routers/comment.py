from fastapi import APIRouter
from models.comment import CommentCreate
import pymysql.cursors
import database

router = APIRouter()

# 用户发表评论
@router.post("/posts/{post_id}/comments/")
async def comment(post_id: int,commentcreate:CommentCreate):
    connention = database.get_connection()
    with connention:
        with connention.cursor() as cursor:
            sql = "INSERT INTO comments (user_id,post_id,content) VALUES(%s,%s,%s)"
            cursor.execute(sql,(commentcreate.user_id,post_id,commentcreate.content))
        connention.commit()
    return "comment successfully"

# 返回某个帖子的全部评论
@router.get("/posts/{post_id}/comments/")
async def get_comments(post_id:int):
    connection = database.get_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT users.username, comments.content, comments.created_at FROM comments JOIN users ON comments.user_id = users.id WHERE comments.post_id = %s"
            cursor.execute(sql,(post_id,))
            result = cursor.fetchall()
    return result

# 删除某个评论
@router.delete("/comments/{comment_id}")
async def delete_comment(comment_id:int):
    connection = database.get_connection()
    with connection:
        with connection.cursor() as cursor:
            sql = "DELETE FROM comments WHERE id=%s"
            cursor.execute(sql,(comment_id,))
        connection.commit()
    return "delete succcessfully"