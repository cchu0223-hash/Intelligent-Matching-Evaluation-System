from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class RecommendRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=15000)
    task_type: str = Field(default="voice")
    top_k: Optional[int] = Field(default=None, ge=1, le=10)
    use_deepseek: bool = True


class RecommendationItem(BaseModel):
    rank: int
    speaker_name: str
    vcn: str
    gender: str
    language: str
    scene_l1: list[str]
    scene_l2: list[str]
    attributes: list[str]
    tech_desc: str
    audio_url: Optional[str]
    score: Optional[float]
    reason: Optional[str]
    debug: dict[str, Any]


class RecommendResponse(BaseModel):
    request_id: str
    task_type: str
    mode: str
    stage: str
    debug_tags: dict[str, Any]
    recommendations: list[RecommendationItem]
    llm_error: Optional[str] = None


class FeedbackRequest(BaseModel):
    request_id: str
    vcn: str
    speaker_name: str
    rank: int = Field(..., ge=1)
    rating: int = Field(..., ge=1, le=5)
    suggestion: Optional[str] = Field(default=None, max_length=2000)


class FeedbackResponse(BaseModel):
    feedback_id: str
    status: str


class HealthResponse(BaseModel):
    status: str
    voice_count: int
    keyword_count: int
    deepseek_enabled: bool
