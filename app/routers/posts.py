from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json

memory_db = {}

router = APIRouter()



@router.get("/users/", tags=["users"])
async def get_users():
    return memory_db.values()


@router.post("/users/", tags=["users"])
async def create_user(user: User):
    user = jsonable_encoder(user)
    memory_db[user["id"]] = user
    return user


@router.put("/users/{id}", tags=["users"])
async def update_user(id: int, user: User):
    if id not in memory_db:
        return None
    memory_db[id] = user
    return user


@router.delete("/users/{id}", tags=["users"])
async def delete_user(id: int):
    if id not in memory_db:
        return None
    del memory_db[id]
    # return {"status": "success"} as JSON response

    return JSONResponse(status_code=200, content={"status": "success"})
