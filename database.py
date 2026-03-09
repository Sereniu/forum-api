import pymysql
from pymysql.cursors import DictCursor
def get_connection():
    connection = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="tohr3o#Wn",
        database="forum_api",
        charset="utf8mb4",
        cursorclass=DictCursor
    )
    return connection