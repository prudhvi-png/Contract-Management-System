import secrets
from datetime import date
from pathlib import Path

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.worker import Worker
from app.services.qr_service import generate_worker_qr

PHOTO_DIR = Path("app/static/photos")
QR_DIR = Path("app/static/qrcodes")


def _generate_unique_worker_code(db: Session) -> str:
    for _ in range(10):
        code = f"WRK-{secrets.token_hex(4).upper()}"
        exists = db.query(Worker).filter(Worker.worker_code == code).first()
        if not exists:
            return code
    raise HTTPException(status_code=500, detail="Could not create a unique worker code")


def create_worker(
    db: Session,
    name: str,
    contract_start: date,
    contract_end: date,
    photo: UploadFile,
) -> Worker:
    if contract_end < contract_start:
        raise HTTPException(status_code=400, detail="Contract end date must be after start date")

    if photo.content_type not in {"image/png", "image/jpeg", "image/jpg"}:
        raise HTTPException(status_code=400, detail="Photo must be a PNG or JPG image")

    worker_code = _generate_unique_worker_code(db)

    extension = Path(photo.filename or "photo.jpg").suffix.lower() or ".jpg"
    if extension not in {".png", ".jpg", ".jpeg"}:
        extension = ".jpg"

    photo_filename = f"{worker_code}{extension}"
    photo_path = PHOTO_DIR / photo_filename
    PHOTO_DIR.mkdir(parents=True, exist_ok=True)

    with photo_path.open("wb") as file_obj:
        file_obj.write(photo.file.read())

    qr_filename = f"{worker_code}.png"
    qr_path = QR_DIR / qr_filename
    generate_worker_qr(worker_code=worker_code, output_path=qr_path)

    worker = Worker(
        worker_code=worker_code,
        name=name.strip(),
        photo_path=f"/static/photos/{photo_filename}",
        qr_path=f"/static/qrcodes/{qr_filename}",
        contract_start=contract_start,
        contract_end=contract_end,
    )

    db.add(worker)
    db.commit()
    db.refresh(worker)
    return worker


def list_workers(db: Session):
    return db.query(Worker).order_by(Worker.id.desc()).all()
