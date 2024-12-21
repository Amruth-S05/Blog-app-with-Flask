from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND
from starlette.templating import Jinja2Templates
from sqlalchemy import text
from .db import get_db
from .session import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def index(request: Request, db=Depends(get_db)):
    query = text(
        """
        SELECT p.id, title, body, created, author_id, username
        FROM post p JOIN user u ON p.author_id = u.id
        ORDER BY created DESC
        """
    )
    posts = await db.fetch_all(query)
    return templates.TemplateResponse("blog/index.html", {"request": request, "posts": posts})


@router.get("/create")
async def create_form(request: Request):
    return templates.TemplateResponse("blog/create.html", {"request": request})


@router.post("/create")
async def create_post(
    title: str = Form(...),
    body: str = Form(...),
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")

    query = text(
        "INSERT INTO post (title, body, author_id) VALUES (:title, :body, :author_id)"
    )
    await db.execute(query, {"title": title, "body": body, "author_id": user["id"]})
    return RedirectResponse(url="/", status_code=HTTP_302_FOUND)


@router.get("/{id}/update")
async def update_form(
    id: int, request: Request, db=Depends(get_db), user=Depends(get_current_user)
):
    query = text(
        """
        SELECT p.id, title, body, created, author_id, username
        FROM post p JOIN user u ON p.author_id = u.id
        WHERE p.id = :id
        """
    )
    post = await db.fetch_one(query, {"id": id})
    if not post:
        raise HTTPException(status_code=404, detail=f"Post id {id} does not exist")
    if post["author_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    return templates.TemplateResponse("blog/update.html", {"request": request, "post": post})


@router.post("/{id}/update")
async def update_post(
    id: int,
    title: str = Form(...),
    body: str = Form(...),
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    query = text(
        """
        UPDATE post SET title = :title, body = :body WHERE id = :id
        """
    )
    await db.execute(query, {"title": title, "body": body, "id": id})
    return RedirectResponse(url="/", status_code=HTTP_302_FOUND)


@router.post("/{id}/delete")
async def delete_post(id: int, db=Depends(get_db), user=Depends(get_current_user)):
    query = text(
        """
        DELETE FROM post WHERE id = :id
        """
    )
    await db.execute(query, {"id": id})
    return RedirectResponse(url="/", status_code=HTTP_302_FOUND)
