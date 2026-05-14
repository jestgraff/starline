from datetime import datetime, date

from sqlalchemy import Integer, String, Date, DateTime, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    device_id: Mapped[int] = mapped_column(Integer, index=True)

    service_type: Mapped[str] = mapped_column(String(255))
    mileage: Mapped[int] = mapped_column(Integer)

    service_date: Mapped[date] = mapped_column(Date)

    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    next_service_mileage: Mapped[int | None] = mapped_column(Integer, nullable=True)
    next_service_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )