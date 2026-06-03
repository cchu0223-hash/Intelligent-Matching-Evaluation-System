from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class VoiceRecord:
    speaker_name: str
    vcn: str
    gender_code: str
    gender_label: str
    language: str
    scene_l1: list[str]
    scene_l2: list[str]
    tech_desc: str
    sort_value: float


@dataclass(frozen=True)
class KeywordRow:
    scene_l1: str
    scene_l2: str
    keywords: list[str]


@dataclass(frozen=True)
class TagTaxonomy:
    l1_tags: set[str]
    l2_tags: set[str]
    l1_to_l2: dict[str, set[str]]
    l2_to_l1: dict[str, str]


@dataclass(frozen=True)
class Recommendation:
    rank: int
    speaker_name: str
    vcn: str
    gender: str
    language: str
    scene_l1: list[str]
    scene_l2: list[str]
    attributes: list[str]
    tech_desc: str
    audio_url: str | None
    score: float | None
    reason: str | None
    debug: dict[str, Any]
