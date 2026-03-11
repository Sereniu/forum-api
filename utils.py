def response(code:int,message:str,data=None):
    return {
        "code":code,
        "message":message,
        "data":data
    }