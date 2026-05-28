from typing import TypeVar, Generic, Optional, Any, List, Dict
from pydantic import BaseModel, Field

T = TypeVar("T")

class ResponseApi(BaseModel, Generic[T]):
    code: int
    message: str
    data: Optional[T] = None

class EmotionScores(BaseModel):
    positive: float
    neutral: float
    negative: float
    fear: Optional[float] = 0.0
    panic: Optional[float] = 0.0
    uncertainty: Optional[float] = 0.0
    optimism: Optional[float] = 0.0
    trust: Optional[float] = 0.0

class EntitySentiment(BaseModel):
    entity: str
    sentiment: str

class SentimentAnalysisData(BaseModel):
    sentiment: str
    confidence_score: float
    fear_probability: float
    emotions: EmotionScores
    entities: List[EntitySentiment] = Field(default_factory=list)

class FearIndexData(BaseModel):
    index_value: float
    classification: str
    trend: str
    last_updated: str

class TrendDataPoint(BaseModel):
    timestamp: str
    fear_index: float
    average_sentiment: float

class AnalyticsTrendData(BaseModel):
    timeframe: str
    datapoints: List[TrendDataPoint]
