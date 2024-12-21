from fastapi import FastAPI
from .auth import router as auth_router
from .blog import router as blog_router
from .db import database

app = FastAPI()

# Include routers
app.include_router(auth_router)
app.include_router(blog_router)

# Lifecycle events
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/hello")
async def hello():
    return {"message": "Hello, World!"}
