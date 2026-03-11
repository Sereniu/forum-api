from fastapi import Header,HTTPException
from jose import jwt,JWTError

def verify_token(authorization:str = Header()):
    try:
        token = authorization.replace("Bearer ","")
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
        return payload
    except JWTError:
        raise HTTPException(status_code=401,detail="token 有误")

