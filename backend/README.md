# Backend

FastAPI service for voice recommendation, feedback capture, and recommendation logs.

## API

- `GET /api/health`: service status, voice count, keyword count, DeepSeek availability.
- `POST /api/recommend`: input real dubbing text and return deduped Top5 voice recommendations.
- `POST /api/feedback`: save rating and optional text suggestion for one recommendation.

## Matching Pipeline

1. Load voice records, tag taxonomy, and scene keyword rows from Excel.
2. Load sample audio URLs from `VOICE_AUDIO_CSV`, keyed by VCN.
3. Load local matching rules from `VOICE_RULES_JSON`.
4. Build keyword hits from the real dubbing text.
5. Apply rule recall, including configured backfills, weak-scene fallback, technical freshness preference, service-scene penalty, broad-tag penalty, and focus scoring.
6. Optionally send recalled candidates to DeepSeek for reranking.
7. Merge model score and rule score, then dedupe by normalized speaker name before returning Top5.

## Local Rules

Use `backend/config/local_rules.example.json` as a schema reference. The real rules file should be supplied through `VOICE_RULES_JSON` and must not be committed.

## Audio URL Mapping

The current audio CSV is encoded as `gb18030` and uses these fields:

```text
speaker_no,vcn,speaker_name,audio_url,audio_text,img_url,mv_url
```

Rows without `vcn` or `audio_url` are ignored. If one VCN has multiple audio rows, the backend selects one deterministically using local rules:

1. Prefer words configured in `audio_preferred_words`.
2. Deprioritize words configured in `audio_deprioritized_words`.
3. Use lower `speaker_no` as the final tie-breaker.

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
