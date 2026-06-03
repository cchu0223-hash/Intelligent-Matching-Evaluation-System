from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _resolve_path(value: str | None, default: Path) -> Path:
    raw = (value or "").strip()
    path = Path(raw) if raw else default
    if path.is_absolute():
        return path
    return (_repo_root() / path).resolve()


def _int_env(name: str, default: int) -> int:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    repo_root: Path
    voice_library_xlsx: Path
    voice_taxonomy_xlsx: Path
    voice_keywords_xlsx: Path
    voice_audio_csv: Path | None
    voice_rules_json: Path | None
    database_path: Path
    deepseek_api_key: str
    deepseek_api_base_url: str
    deepseek_model: str
    cors_origins: list[str]
    max_input_chars: int
    analysis_max_chars: int
    candidate_size: int
    top_k: int


def get_settings() -> Settings:
    repo = _repo_root()
    load_dotenv(repo / ".env")
    origins = [
        item.strip()
        for item in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
        if item.strip()
    ]
    return Settings(
        repo_root=repo,
        voice_library_xlsx=_resolve_path(
            os.getenv("VOICE_LIBRARY_XLSX"), repo / "backend/config/voice-library.xlsx"
        ),
        voice_taxonomy_xlsx=_resolve_path(
            os.getenv("VOICE_TAXONOMY_XLSX"), repo / "backend/config/voice-taxonomy.xlsx"
        ),
        voice_keywords_xlsx=_resolve_path(
            os.getenv("VOICE_KEYWORDS_XLSX"), repo / "backend/config/voice-keywords.xlsx"
        ),
        voice_audio_csv=_resolve_path(
            os.getenv("VOICE_AUDIO_CSV"), repo / "backend/config/voice-audio-map.csv"
        ),
        voice_rules_json=_resolve_path(
            os.getenv("VOICE_RULES_JSON"), repo / "backend/config/local_rules.json"
        ),
        database_path=_resolve_path(os.getenv("DATABASE_PATH"), repo / "backend/data/evaluation.db"),
        deepseek_api_key=os.getenv("DEEPSEEK_API_KEY", "").strip(),
        deepseek_api_base_url=os.getenv("DEEPSEEK_API_BASE_URL", "https://api.deepseek.com"),
        deepseek_model=os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash"),
        cors_origins=origins,
        max_input_chars=_int_env("MAX_INPUT_CHARS", 15000),
        analysis_max_chars=_int_env("ANALYSIS_MAX_CHARS", 1000),
        candidate_size=_int_env("CANDIDATE_SIZE", 20),
        top_k=_int_env("TOP_K", 5),
    )
