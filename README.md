# SciSciNet Agent Backend

Multi-agent LLM framework for automated data analysis and visualization using LangChain, LangGraph, and Vega-Lite.

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

3. Run the server:
```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## Usage

Send a query to the API:
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me the number of papers by year"}'
```

## Testing

Run all tests:
```bash
uv run pytest
```

Run specific test file:
```bash
uv run pytest tests/test_database.py -v
```

Run with coverage:
```bash
uv run pytest --cov=src
```

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation.
