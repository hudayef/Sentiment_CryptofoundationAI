from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.analytics import ArticleSentiment, FearIndexHistory
from app.core.config import settings

async def calculate_and_store_fear_index(db: AsyncSession) -> float:
    now = datetime.now(timezone.utc)
    day_ago = now - timedelta(hours=24)

    stmt = select(ArticleSentiment).where(ArticleSentiment.created_at >= day_ago)
    result = await db.execute(stmt)
    articles = result.scalars().all()

    total_articles = len(articles)
    if total_articles == 0: return 50.0

    negative_count = sum(1 for a in articles if a.overall_sentiment == "negative")
    c_neg = (negative_count / total_articles) * 100

    total_fear_prob = sum(a.fear_probability for a in articles)
    c_fear = (total_fear_prob / total_articles) * 100

    total_panic_score = 0.0
    for a in articles:
        emotions = a.emotions_json
        if isinstance(emotions, dict) and "panic" in emotions:
             total_panic_score += float(emotions["panic"])
    c_kw = (total_panic_score / total_articles) * 100

    half_day_ago = now - timedelta(hours=12)
    recent_neg = sum(1 for a in articles if a.created_at >= half_day_ago and a.overall_sentiment == "negative")
    older_neg = negative_count - recent_neg
    rate_of_change = ((recent_neg - older_neg) / older_neg) * 100 if older_neg > 0 else 0.0
    c_acc = min(100.0, max(0.0, rate_of_change))

    c_vol = min(100.0, (total_articles / 100.0) * 100)

    fear_index = min(100.0, max(0.0, (
        (settings.WEIGHT_NEGATIVE_RATIO * c_neg) +
        (settings.WEIGHT_FEAR_PROB * c_fear) +
        (settings.WEIGHT_PANIC_KEYWORDS * c_kw) +
        (settings.WEIGHT_TREND_ACCELERATION * c_acc) +
        (settings.WEIGHT_VOLUME_SPIKE * c_vol)
    )))

    classification = "Alert"
    if fear_index <= 20: classification = "Safe"
    elif fear_index <= 40: classification = "Low Concern"
    elif fear_index <= 60: classification = "Alert"
    elif fear_index <= 80: classification = "High Fear"
    else: classification = "Extreme Panic"

    score_map = {"positive": 1.0, "neutral": 0.0, "negative": -1.0}
    avg_sent = sum(score_map.get(a.overall_sentiment, 0.0) for a in articles) / total_articles

    history_record = FearIndexHistory(
        index_value=fear_index,
        classification=classification,
        average_sentiment=avg_sent,
        calculation_metrics={
            "c_neg": c_neg, "c_fear": c_fear, "c_kw": c_kw,
            "c_acc": c_acc, "c_vol": c_vol, "total_articles": total_articles
        }
    )
    db.add(history_record)
    await db.commit()
    return fear_index
