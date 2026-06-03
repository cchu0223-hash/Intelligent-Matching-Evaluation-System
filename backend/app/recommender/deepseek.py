from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any


def normalize_text(text: str) -> str:
    return " ".join((text or "").replace("\u3000", " ").split()).strip()


def trim_script_text(text: str, max_chars: int) -> str:
    normalized = normalize_text(text)
    if len(normalized) <= max_chars:
        return normalized
    head = normalized[: max(0, max_chars - 300)]
    tail = normalized[-250:]
    return f"{head} ... {tail}"


def rerank_with_deepseek(
    *,
    api_key: str,
    api_base_url: str,
    model: str,
    timeout_seconds: float,
    max_script_chars: int,
    script_text: str,
    candidates: list[dict[str, Any]],
) -> dict[str, Any]:
    url = api_base_url.rstrip("/") + "/chat/completions"
    compact_candidates = [
        {
            "candidate_index": c["candidate_index"],
            "speaker_name": c["speaker_name"],
            "vcn": c["vcn"],
            "gender": c["gender"],
            "language": c["language"],
            "scene_l1": c["scene_l1"],
            "scene_l2": c["scene_l2"],
            "tech_desc": c["tech_desc"],
            "rule_score": c["rule_score"],
        }
        for c in candidates
    ]

    payload = {
        "model": model,
        "temperature": 0.2,
        "messages": [
            {
                "role": "system",
                "content": (
                    "你是配音音色推荐引擎。用户输入是实际配音正文，不是对音色的要求。"
                    "请根据正文内容、场景、语气和候选音色标签，只在候选集内重排。"
                    "输出严格JSON，不要markdown。"
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "task": "script_text_to_voice_rerank",
                        "script_text": trim_script_text(script_text, max_script_chars),
                        "candidate_count": len(compact_candidates),
                        "candidates": compact_candidates,
                        "output_schema": {
                            "ranked": [
                                {
                                    "candidate_index": "int",
                                    "score": "0-1 float",
                                    "reason": "short Chinese string",
                                }
                            ]
                        },
                    },
                    ensure_ascii=False,
                ),
            },
        ],
    }

    request = urllib.request.Request(
        url=url,
        method="POST",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            body = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"DeepSeek HTTP {exc.code}: {detail}") from exc
    except Exception as exc:
        raise RuntimeError(f"DeepSeek request failed: {exc}") from exc

    parsed = json.loads(body)
    content = parsed["choices"][0]["message"]["content"]
    start = content.find("{")
    end = content.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise RuntimeError(f"Invalid model JSON content: {content[:200]}")
    result = json.loads(content[start : end + 1])
    ranked = result.get("ranked", [])
    if not isinstance(ranked, list):
        raise RuntimeError("DeepSeek ranked field is not a list")
    return {"ranked": ranked, "raw_content": content}
