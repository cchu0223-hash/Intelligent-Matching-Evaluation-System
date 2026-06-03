# Intelligent Matching Evaluation System

内部评测系统，用于采集“配音文本 -> 智能推荐音色”的推荐结果、试听反馈、评分和文字建议。

## Scope

- `frontend/`: 评测网页，支持输入配音文本、展示 Top5 推荐音色、试听、评分和反馈。
- `backend/`: 推荐 API，负责规则召回、DeepSeek 重排、推荐结果记录和反馈记录。
- `docs/`: 产品与技术设计文档。

## Current Status

The first runnable version is in place:

1. Backend FastAPI service with rule recall, optional DeepSeek rerank, speaker dedupe, and SQLite logging.
2. Frontend React evaluation page with 15000 character input limit, Top5 recommendations, debug tags, audio placeholders, rating, and optional text feedback.
3. Extensible data model with `task_type` and asset URL override table for future avatar matching and audio URL integration.

## Quick Start

Backend:

```bash
cd backend
cp .env.example .env
python3 -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Environment

Set these in `backend/.env` or your deployment environment:

- `DEEPSEEK_API_KEY`: enables online DeepSeek rerank. If empty, the service falls back to rule-only ranking.
- `DEEPSEEK_API_BASE_URL`: default `https://api.deepseek.com`.
- `DEEPSEEK_MODEL`: default `deepseek-v4-flash`.
- `VOICE_LIBRARY_XLSX`: default `../音库（已标注）.xlsx`.
- `VOICE_TAXONOMY_XLSX`: default `../音色标签体系.xlsx`.
- `VOICE_KEYWORDS_XLSX`: default `../音色场景关键词库.xlsx`.
- `DATABASE_PATH`: default `backend/data/evaluation.db`.
- `CORS_ORIGINS`: default `http://localhost:5173`.

## Data Policy

Large Excel files, generated recommendation outputs, API keys, and local database files should not be committed. Keep source data in the existing workspace or provide paths through environment variables.
