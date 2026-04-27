from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    worker_code = Column(String(30), unique=True, nullable=False, index=True)
    name = Column(String(150), nullable=False)
    photo_path = Column(String(255), nullable=False)
    qr_path = Column(String(255), nullable=False)
    contract_start = Column(Date, nullable=False)
    contract_end = Column(Date, nullable=False)

    attendance_logs = relationship("AttendanceLog", back_populates="worker", cascade="all, delete-orphan")
