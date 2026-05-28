from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from datetime import datetime, timedelta, timezone
from app.schemas.responses import ResponseApi, AnalyticsTrendData, TrendDataPoint
from app.core.database import get_db
from app.models.analytics import FearIndexHistory

router = APIRouter()

@router.get("/trend", response_model=ResponseApi[AnalyticsTrendData])
async def get_analytics_trend(
    timeframe: str = Query("7d", description="Timeframe like 24h, 7d, 30d"),
    db: AsyncSession = Depends(get_db)
):
    now = datetime.now(timezone.utc)
    days = 7
    if timeframe == "24h": days = 1
    elif timeframe == "30d": days = 30

    lookback = now - timedelta(days=days)

    stmt = (
        select(FearIndexHistory)
        .where(FearIndexHistory.timestamp >= lookback)
        .order_by(FearIndexHistory.timestamp)
    )
    result = await db.execute(stmt)
    history_records = result.scalars().all()

    points = [TrendDataPoint(
        timestamp=record.timestamp.isoformat() if record.timestamp else now.isoformat(),
        fear_index=round(record.index_value, 1),
        average_sentiment=round(record.average_sentiment, 2)
    ) for record in history_records]

    return ResponseApi(code=200, message="Success", data=AnalyticsTrendData(timeframe=timeframe, datapoints=points))
