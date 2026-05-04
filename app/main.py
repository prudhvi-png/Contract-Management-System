from pathlib import Path
from fastapi import Request
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

#from app.database.connection import Base, engine
from app.models import attendance_log, worker  # noqa: F401
from app.routes import api, web

app = FastAPI(title="Contract Worker Management System")
templates = Jinja2Templates(directory="app/templates")

# Ensure static directories exist.
Path("app/static/photos").mkdir(parents=True, exist_ok=True)
Path("app/static/qrcodes").mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(web.router)
# app.include_router(api.router)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "base.html",
        {"request": request, "workers": []}
    )