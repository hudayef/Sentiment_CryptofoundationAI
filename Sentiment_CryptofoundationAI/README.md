# 🧠 CryptoFoundation AI: Sentiment & Fear Intelligence System

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)

## 📖 Overview
The **Sentiment & Fear Intelligence System** is an independent, asynchronous Python microservice designed to integrate directly with the `hub.cryptofoundation.io` platform. It provides NLP-powered market sentiment analysis, entity extraction, and a dynamic mathematical **Fear Index** to gauge public crypto market psychology.

This service is designed to run alongside the core Rust backend, communicating via REST APIs and Redis event queues.

---

## 📚 Essential Documentation

Before developing, please read the core project specifications:
- 🎯 **[Product Requirements Document (PRD)](PRD.md)**: Goals, target audience, and key features.
- ⚙️ **[Software Requirements Specification (SRS)](SRS.md)**: Technical constraints, validation rules, and error handling.
- 🏗️ **[System Design Document (SDD)](SDD.md)**: Architectural layout, database schemas, and UI/UX developer guidelines.

**Additional Guides:**
- [Integration Strategy](INTEGRATION_PLAN.md)
- [Machine Learning Pipeline](ML_PIPELINE.md)
- [Fear Engine Mathematics](FEAR_ENGINE.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)

---

## 🚀 Quickstart (Local Development)

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- A running instance of PostgreSQL & Redis (Provided via Docker Compose)

### 1. Run via Docker Compose (Recommended)
This will spin up the FastAPI server, PostgreSQL, Redis, Celery Worker, and Celery Beat scheduler.
```bash
docker-compose up -d --build
```
*API will be available at: `http://localhost:8000/api/v1/openapi.json`*

### 2. Run Locally (Virtual Environment)
```bash
# Create virtual environment manually
# Activate it
# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🔧 Environment Variables (`.env`)
Create a `.env` file in the root directory based on the following variables:

```ini
PROJECT_NAME="Sentiment & Fear Intelligence API"
API_V1_STR="/api/v1"

# Database & Cache Links (Match the Rust Platform)
DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/hub_cf"
REDIS_URL="redis://localhost:6379/0"

# Security
INTERNAL_API_KEY="super_secret_internal_key"

# Fear Engine Tuning Weights (Must equal 1.0)
WEIGHT_NEGATIVE_RATIO=0.35
WEIGHT_FEAR_PROB=0.25
WEIGHT_PANIC_KEYWORDS=0.15
WEIGHT_TREND_ACCELERATION=0.15
WEIGHT_VOLUME_SPIKE=0.10
```

---

## 📂 Project Structure

```text
.
├── app/
│   ├── api/v1/        # FastAPI route handlers (Controllers)
│   ├── core/          # Configs, middlewares, and async db connections
│   ├── models/        # SQLAlchemy database models
│   ├── schemas/       # Pydantic validation schemas (DTOs)
│   ├── services/      # Core Business Logic (NLP, Fear Engine)
│   └── workers/       # Celery background tasks
├── tests/             # Pytest test suite
├── alembic/           # Database migration scripts
├── docker-compose.yml # Local development orchestration
└── requirements.txt   # Python dependencies
```

---

## 🛡️ Testing & Quality Assurance
Run the automated test suite to verify the API endpoints, ML mocking, and database dependencies.
```bash
pytest tests/
```

For detailed security rules and observability setups, refer to:
- [Security Guide](SECURITY.md)
- [Observability Guide](OBSERVABILITY.md)
