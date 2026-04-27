from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.connection import Base


class AttendanceLog(Base):
    __tablename__ = "attendance_logs"

    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    type = Column(String(3), nullable=False)  # IN / OUT

    worker = relationship("Worker", back_populates="attendance_logs")
