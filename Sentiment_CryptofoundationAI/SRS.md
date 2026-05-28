# Software Requirements Specification (SRS)

## 1. Introduction
This SRS defines the technical and functional requirements for the AI Sentiment Intelligence microservice.

## 2. Functional Requirements
- **FR1. Analysis API**: The system MUST provide an endpoint (`POST /api/v1/sentiment/analyze`) accepting raw text or an article ID to compute sentiment.
- **FR2. Emotion Vectors**: The NLP pipeline MUST output scores for 8 dimensions: positive, neutral, negative, fear, panic, uncertainty, optimism, trust.
- **FR3. Fear Index Calculation**: The system MUST calculate the global Fear Index on a periodic schedule (e.g., every 5 minutes) based on recent article data.
- **FR4. Trend Data**: The system MUST provide an endpoint (`GET /api/v1/analytics/trend`) returning aggregated timeseries data for the Fear Index.

## 3. System Validation & Rules
- **Data Validation (Pydantic)**: All incoming API requests must conform strictly to predefined Pydantic v2 schemas. Invalid payloads must return HTTP 422 Unprocessable Entity.
- **Fear Engine Boundaries**: The Fear Index value MUST be mathematically bounded between `0.0` and `100.0`.
- **Text Truncation**: To prevent ML model Out-of-Memory (OOM) errors, the NLP pipeline MUST automatically truncate input text to a maximum of 512 tokens.

## 4. Non-Functional Requirements (NFRs)
- **NFR1. Performance**: Synchronous API calls to the sentiment analyzer should complete in < 200ms when utilizing cache or lightweight heuristics, and < 1500ms when performing full ML inference on CPU.
- **NFR2. Scalability**: The Celery worker architecture must allow horizontal scaling to process thousands of queued articles concurrently.
- **NFR3. Security**: Direct access to the FastAPI service MUST be protected via an internal authentication middleware utilizing the `X-Internal-Token`. Rate limiting MUST be enforced using `slowapi`.

## 5. Error Handling Behavior
- **Missing Models**: If HuggingFace models fail to load or are unavailable, the system MUST seamlessly fallback to the heuristic keyword-based emotion extraction without failing the request.
- **Database Timeouts**: If `asyncpg` encounters connection limits, the application must return an HTTP 503 Service Unavailable and log the incident.
