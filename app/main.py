from fastapi import FastAPI
import logging
from .routers import users

app = FastAPI()

app.include_router(users.router)

@app.get('/')
async def root():
    return {'message': 'API'}

