import re
from typing import Dict, Any, List
from app.schemas.responses import EmotionScores, EntitySentiment

def extract_crypto_entities(text: str) -> List[EntitySentiment]:
    entities = []
    text_lower = text.lower()
    if "bitcoin" in text_lower or "btc" in text_lower:
        entities.append(EntitySentiment(entity="Bitcoin", sentiment="neutral"))
    if "ethereum" in text_lower or "eth" in text_lower:
        entities.append(EntitySentiment(entity="Ethereum", sentiment="neutral"))
    if "solana" in text_lower or "sol" in text_lower:
        entities.append(EntitySentiment(entity="Solana", sentiment="neutral"))
    return entities

def compute_emotion_scores(sentiment_val: str, text: str) -> EmotionScores:
    text_lower = text.lower()
    pos = 0.8 if sentiment_val == "positive" else 0.1
    neu = 0.8 if sentiment_val == "neutral" else 0.1
    neg = 0.8 if sentiment_val == "negative" else 0.1

    fear, panic, uncertainty, optimism, trust = 0.1, 0.0, 0.2, 0.1, 0.1

    if neg > 0.5:
        if any(w in text_lower for w in ["crash", "hancur", "rugpull", "scam", "hack"]):
            fear, panic = 0.8, 0.9
        elif any(w in text_lower for w in ["drop", "turun", "sell"]):
            fear, panic = 0.5, 0.2

    if pos > 0.5:
        if any(w in text_lower for w in ["moon", "pump", "naik", "bullish"]):
            optimism, trust = 0.9, 0.6

    if any(w in text_lower for w in ["maybe", "unsure", "volatile", "mungkin"]):
        uncertainty = 0.8

    return EmotionScores(
        positive=pos, neutral=neu, negative=neg,
        fear=fear, panic=panic, uncertainty=uncertainty,
        optimism=optimism, trust=trust
    )

class NLPPipeline:
    def __init__(self):
        try:
            from transformers import pipeline
            self.sentiment_analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-xlm-roberta-base-sentiment")
            self.model_loaded = True
        except Exception:
            self.model_loaded = False

    def analyze_text(self, text: str) -> Dict[str, Any]:
        clean_text = re.sub(r'http\S+', '', text).strip()
        sentiment_val, confidence = "neutral", 0.5

        if self.model_loaded and clean_text:
            result = self.sentiment_analyzer(clean_text[:512])[0]
            label = result['label'].lower()
            confidence = result['score']
            if "positive" in label or "pos" in label: sentiment_val = "positive"
            elif "negative" in label or "neg" in label: sentiment_val = "negative"
        else:
            clean_lower = clean_text.lower()
            if any(w in clean_lower for w in ["bullish", "moon", "great", "pump", "naik", "bagus"]):
                sentiment_val, confidence = "positive", 0.8
            elif any(w in clean_lower for w in ["bearish", "crash", "rugpull", "scam", "turun", "jelek"]):
                sentiment_val, confidence = "negative", 0.8

        emotions = compute_emotion_scores(sentiment_val, clean_text)
        entities = extract_crypto_entities(clean_text)
        for e in entities: e.sentiment = sentiment_val

        fear_prob = emotions.fear or 0.0
        if emotions.panic and emotions.panic > fear_prob: fear_prob = emotions.panic

        return {
            "sentiment": sentiment_val,
            "confidence_score": confidence,
            "fear_probability": fear_prob,
            "emotions": emotions,
            "entities": entities
        }

nlp_pipeline = NLPPipeline()
