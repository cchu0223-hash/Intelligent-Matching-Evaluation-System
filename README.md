# Intelligent Matching Evaluation System

内部评测系统，用于采集“配音文本 -> 智能推荐音色”的推荐结果、试听反馈、评分和文字建议。

## Scope

- `frontend/`: 评测网页，支持输入配音文本、展示 Top5 推荐音色、试听、评分和反馈。
- `backend/`: 推荐 API，负责规则召回、DeepSeek 重排、推荐结果记录和反馈记录。
- `docs/`: 产品与技术设计文档。

## Current Status

This repository has been initialized from the existing local demo workspace. The implementation will be built in stages:

1. Backend API scaffold.
2. Recommendation logic extraction from the existing demo.
3. Frontend evaluation page.
4. SQLite feedback storage.
5. Internal deployment setup.

## Data Policy

Large Excel files, generated recommendation outputs, API keys, and local database files should not be committed. Keep source data in the existing workspace or provide paths through environment variables.

