from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database.connection import Base, engine
from app.models import attendance_log, worker  # noqa: F401
from app.routes import api, web

app = FastAPI(title="Contract Worker Management System")

# Ensure static directories exist.
Path("app/static/photos").mkdir(parents=True, exist_ok=True)
Path("app/static/qrcodes").mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(web.router)
app.include_router(api.router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
