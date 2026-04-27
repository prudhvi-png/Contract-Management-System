from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.attendance_log import AttendanceLog
from app.models.worker import Worker

COOLDOWN_SECONDS = 15


def scan_worker(db: Session, worker_code: str) -> AttendanceLog:
    worker = db.query(Worker).filter(Worker.worker_code == worker_code).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    now = datetime.now(timezone.utc)
    latest_log = (
        db.query(AttendanceLog)
        .filter(AttendanceLog.worker_id == worker.id)
        .order_by(AttendanceLog.timestamp.desc())
        .first()
    )

    if latest_log and (now - latest_log.timestamp) < timedelta(seconds=COOLDOWN_SECONDS):
        raise HTTPException(
            status_code=429,
            detail=f"Please wait {COOLDOWN_SECONDS} seconds before scanning again",
        )

    next_type = "IN"
    if latest_log and latest_log.type == "IN":
        next_type = "OUT"

    log = AttendanceLog(worker_id=worker.id, timestamp=now, type=next_type)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
