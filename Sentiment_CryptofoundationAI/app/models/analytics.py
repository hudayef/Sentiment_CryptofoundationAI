from sqlalchemy import Column, String, Float, DateTime, JSON, BigInteger
from sqlalchemy.sql import func
from app.models.base import Base

class ArticleSentiment(Base):
    __tablename__ = "article_sentiments"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    article_id = Column(String, unique=True, index=True, nullable=False)

    overall_sentiment = Column(String, nullable=False)
    confidence_score = Column(Float, nullable=False)
    fear_probability = Column(Float, nullable=False)

    emotions_json = Column(JSON, nullable=False)
    entities_json = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class FearIndexHistory(Base):
    __tablename__ = "fear_index_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    index_value = Column(Float, nullable=False)
    classification = Column(String, nullable=False)
    average_sentiment = Column(Float, nullable=False)

    calculation_metrics = Column(JSON, nullable=True)

    timestamp = Column(DateTime(timezone=True), default=func.now(), index=True)
