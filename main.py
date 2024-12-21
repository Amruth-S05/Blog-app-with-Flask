from fastapi.staticfiles import StaticFiles
from app import app
import uvicorn

app.mount("/static", StaticFiles(directory="app/static"), name="static")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
