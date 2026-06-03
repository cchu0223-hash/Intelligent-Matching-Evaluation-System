from __future__ import annotations

import asyncio

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.recommender.engine import VoiceRecommender, recommendation_to_dict
from app.schemas import (
    FeedbackRequest,
    FeedbackResponse,
    HealthResponse,
    RecommendRequest,
    RecommendResponse,
)
from app.storage.database import Database

settings = get_settings()
database = Database(settings.database_path)
recommender = VoiceRecommender(
    voice_library_xlsx=settings.voice_library_xlsx,
    voice_taxonomy_xlsx=settings.voice_taxonomy_xlsx,
    voice_keywords_xlsx=settings.voice_keywords_xlsx,
    deepseek_api_key=settings.deepseek_api_key,
    deepseek_api_base_url=settings.deepseek_api_base_url,
    deepseek_model=settings.deepseek_model,
    analysis_max_chars=settings.analysis_max_chars,
)

app = FastAPI(title="Intelligent Matching Evaluation API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins or ["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        voice_count=len(recommender.voices),
        keyword_count=len(recommender.keyword_rows),
        deepseek_enabled=bool(settings.deepseek_api_key),
    )


@app.post("/api/recommend", response_model=RecommendResponse)
async def recommend(payload: RecommendRequest) -> RecommendResponse:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="配音文本不能为空")
    if len(text) > settings.max_input_chars:
        raise HTTPException(status_code=413, detail=f"配音文本不能超过 {settings.max_input_chars} 字")
    if payload.task_type != "voice":
        raise HTTPException(status_code=400, detail="当前版本仅支持 voice 任务")

    top_k = payload.top_k or settings.top_k
    result = await asyncio.to_thread(
        recommender.recommend,
        text=text,
        top_k=top_k,
        candidate_size=settings.candidate_size,
        use_deepseek=payload.use_deepseek,
    )
    recommendations = [recommendation_to_dict(item) for item in result["recommendations"]]
    request_id = database.create_recommendation_request(
        task_type=payload.task_type,
        input_text=text,
        mode=result["mode"],
        stage=result["stage"],
        debug=result["hit_info"],
        recommendations=recommendations,
    )
    return RecommendResponse(
        request_id=request_id,
        task_type=payload.task_type,
        mode=result["mode"],
        stage=result["stage"],
        debug_tags=result["hit_info"],
        recommendations=recommendations,
        llm_error=result["llm_error"],
    )


@app.post("/api/feedback", response_model=FeedbackResponse)
def feedback(payload: FeedbackRequest) -> FeedbackResponse:
    feedback_id = database.create_feedback(
        request_id=payload.request_id,
        vcn=payload.vcn,
        speaker_name=payload.speaker_name,
        rank=payload.rank,
        rating=payload.rating,
        suggestion=payload.suggestion.strip() if payload.suggestion else None,
    )
    return FeedbackResponse(feedback_id=feedback_id, status="saved")
