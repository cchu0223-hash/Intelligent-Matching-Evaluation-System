# Backend

FastAPI service for voice recommendation, feedback capture, and recommendation logs.

## API

- `GET /api/health`: service status, voice count, keyword count, DeepSeek availability.
- `POST /api/recommend`: input real dubbing text and return deduped Top5 voice recommendations.
- `POST /api/feedback`: save rating and optional text suggestion for one recommendation.

## Matching Pipeline

1. Load voice records, tag taxonomy, and scene keyword rows from Excel.
2. Build keyword hits from the real dubbing text.
3. Apply rule recall, including marketing backfill, weak-scene fallback, technical freshness preference, service-scene penalty, broad-tag penalty, and marketing focus scoring.
4. Optionally send recalled candidates to DeepSeek for reranking.
5. Merge model score and rule score, then dedupe by normalized speaker name before returning Top5.

## Local Run

```bash
cp .env.example .env
python3 -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

For this local Codex workspace, dependencies were also validated with:

```bash
PYTHONPATH=backend/.deps:backend python3 -m py_compile $(find backend/app -name '*.py' ! -name '._*')
```
