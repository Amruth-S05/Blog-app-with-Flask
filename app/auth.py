from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND
from starlette.templating import Jinja2Templates
from passlib.hash import bcrypt
from sqlalchemy.exc import IntegrityError
from .db import get_db
from .session import create_session, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/register")
async def register_form(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post("/register")
async def register_user(
    username: str = Form(...), password: str = Form(...), db=Depends(get_db)
):
    hashed_password = bcrypt.hash(password)
    try:
        await db.execute(
            "INSERT INTO user (username, password) VALUES (:username, :password)",
            {"username": username, "password": hashed_password},
        )
    except IntegrityError:
        raise HTTPException(status_code=400, detail=f"User {username} already exists")
    return RedirectResponse(url="/auth/login", status_code=HTTP_302_FOUND)


@router.get("/login")
async def login_form(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login")
async def login_user(
    username: str = Form(...), password: str = Form(...), db=Depends(get_db)
):
    user = await db.fetch_one(
        "SELECT * FROM user WHERE username = :username", {"username": username}
    )
    if not user or not bcrypt.verify(password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    response = RedirectResponse(url="/", status_code=HTTP_302_FOUND)
    create_session(response, user["id"])
    return response


@router.get("/logout")
async def logout(response: RedirectResponse):
    response = RedirectResponse(url="/", status_code=HTTP_302_FOUND)
    response.delete_cookie("session")
    return response


@router.get("/profile")
async def profile(user=Depends(get_current_user)):
    return {"username": user["username"], "id": user["id"]}
