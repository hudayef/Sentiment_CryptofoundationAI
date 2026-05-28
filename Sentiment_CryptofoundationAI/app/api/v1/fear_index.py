from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.schemas.responses import ResponseApi, FearIndexData
from datetime import datetime, timezone
from app.core.database import get_db
from app.models.analytics import FearIndexHistory
from app.services.fear_engine import calculate_and_store_fear_index

router = APIRouter()

@router.get("/latest", response_model=ResponseApi[FearIndexData])
async def get_latest_fear_index(db: AsyncSession = Depends(get_db)):
    stmt = select(FearIndexHistory).order_by(desc(FearIndexHistory.timestamp)).limit(1)
    result = await db.execute(stmt)
    latest = result.scalars().first()

    if not latest:
        fear_val = await calculate_and_store_fear_index(db)
        stmt = select(FearIndexHistory).order_by(desc(FearIndexHistory.timestamp)).limit(1)
        result = await db.execute(stmt)
        latest = result.scalars().first()

    trend = "increasing" if latest.index_value > 50 else "decreasing"
    data = FearIndexData(
        index_value=round(latest.index_value, 1),
        classification=latest.classification,
        trend=trend,
        last_updated=latest.timestamp.isoformat() if latest.timestamp else datetime.now(timezone.utc).isoformat()
    )
    return ResponseApi(code=200, message="Success", data=data)
