# System Design Document (SDD)

## 1. Architectural Overview
The system employs a decoupled, asynchronous microservices architecture. It acts as an auxiliary intelligence layer to the primary transactional Rust (`crypto-hub`) platform.
- **API Layer**: FastAPI handles synchronous HTTP requests and REST API contracts.
- **Worker Layer**: Celery handles asynchronous ML inference, pulling tasks from Redis.
- **Data Layer**: PostgreSQL (via SQLAlchemy `asyncpg`) handles permanent storage; Redis handles transient queues and caching.

## 2. Database Design
- **Table: `article_sentiments`**
  - `id` (BigInt, PK)
  - `article_id` (String, Indexed, Unique)
  - `overall_sentiment` (String)
  - `confidence_score` (Float)
  - `fear_probability` (Float)
  - `emotions_json` (JSONB)
  - `entities_json` (JSONB)
- **Table: `fear_index_history`**
  - `id` (BigInt, PK)
  - `index_value` (Float)
  - `classification` (String)
  - `average_sentiment` (Float)
  - `timestamp` (DateTime, Indexed)

## 3. Backend Structure & APIs
The Python backend strictly follows Clean Architecture:
- `app/api/v1/`: Routing and controller logic.
- `app/core/`: Application settings, database connections, and middleware (auth, logging).
- `app/schemas/`: Pydantic Request/Response validation.
- `app/models/`: SQLAlchemy ORM definitions.
- `app/services/`: Core business logic (`nlp_pipeline.py`, `fear_engine.py`).
- `app/workers/`: Celery task definitions.

### Key API Endpoints
1. `POST /api/v1/sentiment/analyze` -> Triggers analysis on arbitrary text.
2. `GET /api/v1/fear-index/latest` -> Returns the most recently computed Fear Index.
3. `GET /api/v1/analytics/trend?timeframe=7d` -> Returns historical arrays for charting.

## 4. UI/UX Flow (Dashboard Integration)
To prevent developers from guessing UI logic, the frontend implementation must follow these rules:
1. **Fear Gauge Component**:
   - Must use `SWR` or `React Query` to poll `/api/v1/fear-index/latest` every 60 seconds.
   - Must implement a skeleton loader during the initial data fetch.
   - UI Colors must map to classification: Safe (Green), Low Concern (Teal), Alert (Yellow), High Fear (Orange), Extreme Panic (Red).
2. **Trend Chart Component**:
   - Must plot `fear_index` and `average_sentiment` on a dual-axis line chart over `timestamp`.
   - Tooltips must show the exact date and score.
   - Responsive sizing required (via `ResponsiveContainer` if using Recharts).
