# Product Requirements Document (PRD)

## 1. Product Title
Public Sentiment & Fear Intelligence System

## 2. Product Goal
To provide real-time, AI-powered intelligence regarding public sentiment, market fear, and emotion trends within the cryptocurrency ecosystem. This system extends the `crypto-hub` platform by supplying actionable analytics derived from NLP classification of news, articles, and user comments.

## 3. Target Audience / Users
- **Crypto Researchers / Analysts**: Need precise data on market sentiment to understand macro trends.
- **Retail Investors (Dashboard Users)**: Look at the "Fear Index" widget to make informed psychological assessments of the market.
- **Platform Admins / Content Curators**: Use sentiment data to filter out extreme panic-inducing FUD or flag overly manipulative positive articles.

## 4. Key Features
1. **Real-time Fear Index Gauge**: A computed 0-100 metric indicating the current psychological state of the market (Safe vs. Extreme Panic).
2. **Automated Article Sentiment Analysis**: Automatically processes incoming articles through an NLP pipeline to determine if they are bullish, bearish, neutral, or panic-inducing.
3. **Sentiment Trend Analytics**: Historical visualization charting the Fear Index vs. Average Sentiment over time (e.g., 24h, 7d, 30d).
4. **Entity Extraction**: Identify which specific cryptocurrencies (BTC, ETH, SOL) are tied to specific emotional contexts.

## 5. High-Level User Flow
1. **Ingestion Flow**:
   - Core Rust backend ingests a news article.
   - Core Rust backend triggers an event to the AI Intelligence queue (Redis).
   - AI Worker (Python/Celery) picks up the article, runs NLP inference, and stores the sentiment vectors.
2. **Consumption Flow (End-User)**:
   - User logs into the `crypto-hub` dashboard.
   - Dashboard UI makes an API call to the Intelligence Service (via the Rust Gateway).
   - The Fear Gauge widget renders the latest Fear Index score.
   - The Trend Chart renders the 7-day historical sentiment data.
