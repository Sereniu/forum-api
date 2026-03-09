from fastapi import FastAPI
from pydantic import BaseModel
import bcrypt
import database
import pymysql.cursors

class UserRegister(BaseModel):
    username:str
    password:str

app = FastAPI()

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