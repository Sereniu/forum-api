import pymysql
def get_connection():
    connection = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="tohr3o#Wn",
        database="forum_api",
        charset="utf8mb4"
    )
    return connection