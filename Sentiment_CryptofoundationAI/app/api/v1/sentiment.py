from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.requests import AnalyzeSentimentRequest
from app.schemas.responses import ResponseApi, SentimentAnalysisData, EmotionScores, EntitySentiment
from app.core.database import get_db
from app.models.analytics import ArticleSentiment
from app.services.nlp_pipeline import nlp_pipeline

router = APIRouter()

@router.post("/analyze", response_model=ResponseApi[SentimentAnalysisData])
async def analyze_sentiment(request: AnalyzeSentimentRequest, db: AsyncSession = Depends(get_db)):
    if not request.article_id and not request.text:
        raise HTTPException(status_code=400, detail="Must provide either article_id or text")

    if request.article_id:
        stmt = select(ArticleSentiment).where(ArticleSentiment.article_id == request.article_id)
        result = await db.execute(stmt)
        existing = result.scalars().first()
        if existing:
            return ResponseApi(
                code=200, message="Retrieved from database",
                data=SentimentAnalysisData(
                    sentiment=existing.overall_sentiment,
                    confidence_score=existing.confidence_score,
                    fear_probability=existing.fear_probability,
                    emotions=EmotionScores(**existing.emotions_json),
                    entities=[EntitySentiment(**e) for e in existing.entities_json] if existing.entities_json else []
                )
            )

    text_to_analyze = request.text or f"Placeholder text for article {request.article_id}"
    analysis = nlp_pipeline.analyze_text(text_to_analyze)
    response_data = SentimentAnalysisData(**analysis)

    if request.article_id:
        new_record = ArticleSentiment(
            article_id=request.article_id,
            overall_sentiment=analysis["sentiment"],
            confidence_score=analysis["confidence_score"],
            fear_probability=analysis["fear_probability"],
            emotions_json=analysis["emotions"].model_dump(),
            entities_json=[e.model_dump() for e in analysis["entities"]]
        )
        db.add(new_record)
        await db.commit()

    return ResponseApi(code=200, message="Sentiment analysis completed successfully", data=response_data)

@router.get("/articles/{article_id}/analyze", response_model=ResponseApi[SentimentAnalysisData])
async def get_article_sentiment(article_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(ArticleSentiment).where(ArticleSentiment.article_id == article_id)
    result = await db.execute(stmt)
    existing = result.scalars().first()

    if existing:
        return ResponseApi(
            code=200, message="Article sentiment retrieved",
            data=SentimentAnalysisData(
                sentiment=existing.overall_sentiment,
                confidence_score=existing.confidence_score,
                fear_probability=existing.fear_probability,
                emotions=EmotionScores(**existing.emotions_json),
                entities=[EntitySentiment(**e) for e in existing.entities_json] if existing.entities_json else []
            )
        )
    raise HTTPException(status_code=404, detail="Analysis not found for this article. Submit via POST first.")
