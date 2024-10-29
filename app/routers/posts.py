from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

posts_db = {}

router = APIRouter()


class Post(BaseModel):
    id: int
    title: str
    content: str
    user_id: int


class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int


@router.get("/posts/", tags=["posts"])
async def get_posts():
    return list(posts_db.values())


@router.post("/posts/", tags=["posts"])
async def create_post(post: PostCreate):
    post = Post(id=len(posts_db) + 1, **post.dict())
    posts_db[post.id] = post
    return post


@router.get("/posts/{id}", tags=["posts"])
async def get_post(id: int):
    if id not in posts_db:
        return JSONResponse(status_code=404, content={"error": f"Post id {id} not found"})
    return posts_db[id]


@router.put("/posts/{id}", tags=["posts"])
async def update_post(id: int, post: PostCreate):
    if id not in posts_db:
        return JSONResponse(status_code=404, content={"error": f"Post id {id} not found"})
    post = Post(id=id, **post.dict())
    posts_db[id] = post
    return post


@router.delete("/posts/{id}", tags=["posts"])
async def delete_post(id: int):
    if id not in posts_db:
        return JSONResponse(status_code=404, content={"error": f"Post id {id} not found"})
    del posts_db[id]
    return JSONResponse(status_code=204, content={"status": "success"})