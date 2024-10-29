from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json

memory_db = {}

router = APIRouter()

class Post(BaseModel):
    id: int
    title: str
    content: str
    user_id: int

@router.get("/posts/", tags=["posts"])
async def get_posts():
    return list(memory_db.values())

@router.post("/posts/", tags=["posts"])
async def create_post(post: Post):
    post = jsonable_encoder(post)
    if post["user_id"] not in memory_db:
        return JSONResponse(status_code=400, content={"error": "user_id not found"})
    memory_db[post["id"]] = post
    return post

@router.get("/posts/{id}", tags=["posts"])
async def get_post(id: int):
    if id not in memory_db:
        return JSONResponse(status_code=404, content={"error": "post not found"})
    return memory_db[id]

@router.put("/posts/{id}", tags=["posts"])
async def update_post(id: int, post: Post):
    if id not in memory_db:
        return JSONResponse(status_code=404, content={"error": "post not found"})
    if post["user_id"] not in memory_db:
        return JSONResponse(status_code=400, content={"error": "user_id not found"})
    memory_db[id] = post
    return post

@router.delete("/posts/{id}", tags=["posts"])
async def delete_post(id: int):
    if id not in memory_db:
        return JSONResponse(status_code=404, content={"error": "post not found"})
    del memory_db[id]
    return JSONResponse(status_code=204, content={"status": "success"})
