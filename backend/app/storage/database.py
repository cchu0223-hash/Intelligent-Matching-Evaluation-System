from __future__ import annotations

import json
import sqlite3
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Database:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self.path, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
        self._lock = threading.Lock()
        self.init_schema()

    def init_schema(self) -> None:
        with self._lock:
            self._connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS recommendation_requests (
                    id TEXT PRIMARY KEY,
                    task_type TEXT NOT NULL,
                    input_text TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    stage TEXT NOT NULL,
                    debug_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS recommendation_results (
                    id TEXT PRIMARY KEY,
                    request_id TEXT NOT NULL,
                    rank INTEGER NOT NULL,
                    speaker_name TEXT NOT NULL,
                    vcn TEXT NOT NULL,
                    gender TEXT,
                    language TEXT,
                    scene_l1_json TEXT NOT NULL,
                    scene_l2_json TEXT NOT NULL,
                    attributes_json TEXT NOT NULL,
                    tech_desc TEXT,
                    audio_url TEXT,
                    score REAL,
                    reason TEXT,
                    debug_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(request_id) REFERENCES recommendation_requests(id)
                );

                CREATE TABLE IF NOT EXISTS feedback (
                    id TEXT PRIMARY KEY,
                    request_id TEXT NOT NULL,
                    vcn TEXT NOT NULL,
                    speaker_name TEXT NOT NULL,
                    rank INTEGER NOT NULL,
                    rating INTEGER NOT NULL,
                    suggestion TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(request_id) REFERENCES recommendation_requests(id)
                );

                CREATE TABLE IF NOT EXISTS scene_feedback (
                    id TEXT PRIMARY KEY,
                    request_id TEXT NOT NULL,
                    suggested_scene_l1 TEXT,
                    suggested_scene_l2 TEXT,
                    suggested_keywords TEXT NOT NULL,
                    suggestion TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(request_id) REFERENCES recommendation_requests(id)
                );

                CREATE TABLE IF NOT EXISTS asset_url_overrides (
                    id TEXT PRIMARY KEY,
                    asset_type TEXT NOT NULL DEFAULT 'voice',
                    asset_key TEXT NOT NULL,
                    url TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                """
            )
            self._connection.commit()

    def create_recommendation_request(
        self,
        *,
        task_type: str,
        input_text: str,
        mode: str,
        stage: str,
        debug: dict[str, Any],
        recommendations: list[dict[str, Any]],
    ) -> str:
        request_id = str(uuid.uuid4())
        created_at = utc_now()
        with self._lock:
            self._connection.execute(
                """
                INSERT INTO recommendation_requests
                (id, task_type, input_text, mode, stage, debug_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    request_id,
                    task_type,
                    input_text,
                    mode,
                    stage,
                    json.dumps(debug, ensure_ascii=False),
                    created_at,
                ),
            )
            for item in recommendations:
                self._connection.execute(
                    """
                    INSERT INTO recommendation_results
                    (id, request_id, rank, speaker_name, vcn, gender, language,
                     scene_l1_json, scene_l2_json, attributes_json, tech_desc,
                     audio_url, score, reason, debug_json, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        str(uuid.uuid4()),
                        request_id,
                        item["rank"],
                        item["speaker_name"],
                        item["vcn"],
                        item["gender"],
                        item["language"],
                        json.dumps(item["scene_l1"], ensure_ascii=False),
                        json.dumps(item["scene_l2"], ensure_ascii=False),
                        json.dumps(item["attributes"], ensure_ascii=False),
                        item.get("tech_desc"),
                        item.get("audio_url"),
                        item.get("score"),
                        item.get("reason"),
                        json.dumps(item.get("debug", {}), ensure_ascii=False),
                        created_at,
                    ),
                )
            self._connection.commit()
        return request_id

    def create_feedback(
        self,
        *,
        request_id: str,
        vcn: str,
        speaker_name: str,
        rank: int,
        rating: int,
        suggestion: str | None,
    ) -> str:
        feedback_id = str(uuid.uuid4())
        with self._lock:
            self._connection.execute(
                """
                INSERT INTO feedback
                (id, request_id, vcn, speaker_name, rank, rating, suggestion, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    feedback_id,
                    request_id,
                    vcn,
                    speaker_name,
                    rank,
                    rating,
                    suggestion,
                    utc_now(),
                ),
            )
            self._connection.commit()
        return feedback_id

    def create_scene_feedback(
        self,
        *,
        request_id: str,
        suggested_scene_l1: list[str],
        suggested_scene_l2: list[str],
        suggested_keywords: str,
        suggestion: str | None,
    ) -> str:
        feedback_id = str(uuid.uuid4())
        with self._lock:
            self._connection.execute(
                """
                INSERT INTO scene_feedback
                (id, request_id, suggested_scene_l1, suggested_scene_l2,
                 suggested_keywords, suggestion, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    feedback_id,
                    request_id,
                    json.dumps(suggested_scene_l1, ensure_ascii=False),
                    json.dumps(suggested_scene_l2, ensure_ascii=False),
                    suggested_keywords,
                    suggestion,
                    utc_now(),
                ),
            )
            self._connection.commit()
        return feedback_id
