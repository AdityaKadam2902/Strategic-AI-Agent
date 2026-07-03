# Strategic Decision Intelligence Platform

Enterprise-grade multi-agent AI system for strategic business decision analysis. Six specialized AI agents evaluate decisions from multiple perspectives, producing comprehensive recommendations with confidence scoring.

## Architecture

```
User Request
    |
    v
FastAPI Application (Validation, Rate Limiting, Observability)
    |
    v
LangGraph Workflow Orchestrator
    |
    +---> Pro Agent (Parallel)
    +---> Con Agent (Parallel)
    +---> Financial Agent (Parallel)
    +---> Market Agent (Parallel)
    |
    v
Judge Agent (Synthesis)
    |
    v
Confidence Scorer
    |
    v
Structured Response
```

## Technology Stack

**Backend**
- Python 3.11 with FastAPI
- LangGraph for multi-agent orchestration
- Groq AI for high-performance inference
- Pydantic v2 for strict validation
- Structlog for structured logging

**Frontend**
- React 18 with TypeScript
- Tailwind CSS for styling
- Framer Motion for animations
- Lucide React for icons

**Infrastructure**
- Docker with multi-stage builds
- Redis for caching layer
- GitHub Actions for CI/CD

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Groq API key ([console.groq.com](https://console.groq.com))

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Docker Deployment

```bash
export LLM_API_KEY=your_key_here
docker-compose up --build
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- OpenAPI Schema: http://localhost:8000/openapi.json

### Example Request

```bash
curl -X POST http://localhost:8000/api/v1/debate \
  -H "Content-Type: application/json" \
  -d '{
    "decision": "Should we invest $2M in expanding our cloud infrastructure?",
    "industry_context": "SaaS"
  }'
```

## Project Structure

```
strategic-decision-intelligence/
├── backend/
│   ├── app/
│   │   ├── agents/           # AI agent implementations
│   │   ├── core/             # Configuration, logging, exceptions
│   │   ├── services/         # Business logic services
│   │   ├── main.py           # FastAPI application
│   │   ├── models.py         # Pydantic domain models
│   │   └── state.py          # LangGraph state definitions
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── styles/           # CSS/Tailwind
│   │   ├── App.tsx           # Main application
│   │   └── main.tsx          # Entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci.yml
└── README.md
```

## Development

```bash
# Backend formatting
black app/ tests/
isort app/ tests/
mypy app/

# Testing
pytest tests/ -v --cov=app

# Frontend linting
npm run lint
```

## License

MIT License
