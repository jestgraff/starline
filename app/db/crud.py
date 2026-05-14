from datetime import date

from sqlalchemy import select

from app.db.database import AsyncSessionLocal
from app.db.models import MaintenanceRecord


async def create_maintenance_record(
    device_id: int,
    service_type: str,
    mileage: int,
    comment: str | None = None,
    next_service_mileage: int | None = None,
    next_service_date: date | None = None,
):
    async with AsyncSessionLocal() as session:
        record = MaintenanceRecord(
            device_id=device_id,
            service_type=service_type,
            mileage=mileage,
            service_date=date.today(),
            comment=comment,
            next_service_mileage=next_service_mileage,
            next_service_date=next_service_date,
        )

        session.add(record)
        await session.commit()

        return record


async def get_maintenance_history(device_id: int, limit: int = 10):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(MaintenanceRecord)
            .where(MaintenanceRecord.device_id == device_id)
            .order_by(MaintenanceRecord.service_date.desc())
            .limit(limit)
        )

        return result.scalars().all()