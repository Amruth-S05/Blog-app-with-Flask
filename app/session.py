from fastapi import Request, HTTPException
from fastapi.responses import Response

COOKIE_NAME = "session"

def create_session(response: Response, user_id: int):
    response.set_cookie(key=COOKIE_NAME, value=str(user_id), httponly=True)

def get_current_user(request: Request):
    user_id = request.cookies.get(COOKIE_NAME)
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"id": user_id}
