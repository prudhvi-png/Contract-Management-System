from datetime import date
from urllib.parse import quote_plus

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.worker_service import create_worker, list_workers

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    workers = list_workers(db)
    today = date.today()
    return templates.TemplateResponse(
        request,
        "workers.html",
        {
            "workers": workers,
            "today": today,
            "message": request.query_params.get("message"),
        },
    )


@router.get("/workers/new")
def add_worker_page(request: Request):
    return templates.TemplateResponse(
        request,
        "add_worker.html",
        {"error": request.query_params.get("error")},
    )


@router.post("/workers/new")
def add_worker_submit(
    name: str = Form(...),
    contract_start: date = Form(...),
    contract_end: date = Form(...),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        create_worker(
            db=db,
            name=name,
            contract_start=contract_start,
            contract_end=contract_end,
            photo=photo,
        )
    except HTTPException as exc:
        return RedirectResponse(url=f"/workers/new?error={quote_plus(exc.detail)}", status_code=303)

    return RedirectResponse(url="/?message=Worker created successfully", status_code=303)
