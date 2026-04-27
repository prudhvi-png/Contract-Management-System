from datetime import date

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.worker import Worker
from app.services.attendance_service import scan_worker

router = APIRouter(tags=["API"])


class ScanRequest(BaseModel):
    worker_code: str = Field(..., min_length=5, max_length=30)


def _scan_logic(payload: ScanRequest, db: Session):
    log = scan_worker(db=db, worker_code=payload.worker_code.strip())
    worker = db.query(Worker).filter(Worker.id == log.worker_id).first()
    expired = worker.contract_end < date.today()
    return {
        "worker_code": worker.worker_code,
        "name": worker.name,
        "timestamp": log.timestamp.isoformat(),
        "type": log.type,
        "contract_expired": expired,
    }


@router.post("/scan")
def scan(payload: ScanRequest, db: Session = Depends(get_db)):
    return _scan_logic(payload, db)


@router.post("/api/scan")
def scan_alias(payload: ScanRequest, db: Session = Depends(get_db)):
    return _scan_logic(payload, db)
