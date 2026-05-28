from pydantic import BaseModel, Field
from typing import Optional

class AnalyzeSentimentRequest(BaseModel):
    article_id: Optional[str] = Field(None, description="UUID of the article if already in DB")
    text: Optional[str] = Field(None, description="Raw text to analyze if article_id is not provided")
    language: str = Field("en", description="Language of the text")
