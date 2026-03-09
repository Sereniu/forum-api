from fastapi import FastAPI
from routers import user
from routers import post

app = FastAPI()
app.include_router(user.router)
app.include_router(post.router)