from fastapi import Header
from jose import jwt,JWTError

def verify_token(authorization:str = Header()):
    token = authorization.replace("Bearer ","")
    payload = jwt.decode(token,'secret',algorithms=['HS256'])
    return payload