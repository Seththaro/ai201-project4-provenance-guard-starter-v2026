"""
Request log (capstone, shape A): one structured record per HTTP request.

The audit log (audit.py) records decisions. This records *requests*: every
request the service handled, whether it became a decision, was refused, was
rate limited or crashed. Each line of logs/requests.jsonl is one JSON object:

    timestamp    UTC, ISO 8601
    request_id   12 hex chars, also returned in the X-Request-ID header
    method, route, status
    input        what came in: creator_id, text_chars, text_words, text_preview
    output       what went out: guess, label, combined_score, content_id, or error
    duration_ms  wall time for the whole request
    cpu_ms       process CPU time spent during the request (compute cost)
    stage_ms     {model, style, phrase, combine} for scored requests
    error        short error string for any 4xx/5xx, else null

Logging must never break a request, so every public function swallows its own
failures.
"""

import json
import threading

import config

REQUEST_LOG = config.LOG_DIR / "requests.jsonl"
_lock = threading.Lock()


def summarize_input(payload) -> dict:
    """What came in, without storing the whole text."""
    if not isinstance(payload, dict):
        return {"body": type(payload).__name__}
    out = {}
    creator = payload.get("creator_id")
    if isinstance(creator, str):
        out["creator_id"] = creator[:100]
    elif creator is not None:
        out["creator_id"] = f"<{type(creator).__name__}>"
    for key in ("text", "sample", "reasoning"):
        value = payload.get(key)
        if isinstance(value, str):
            out["text_chars"] = len(value)
            out["text_words"] = len(value.split())
            out["text_preview"] = value[:60]
            break
        if value is not None:
            out["text_chars"] = f"<{type(value).__name__}>"
            break
    if "content_id" in payload:
        out["content_id"] = str(payload["content_id"])[:40]
    return out


def summarize_output(status: int, body) -> dict:
    if not isinstance(body, dict):
        return {}
    keep = ("content_id", "guess", "label", "combined_score", "status", "error", "ok")
    out = {k: body[k] for k in keep if k in body}
    if "label" in out and isinstance(out["label"], str):
        out["label"] = out["label"][:60]
    return out


def write(record: dict) -> None:
    """Append one record. ensure_ascii keeps a lone surrogate from killing the write."""
    try:
        config.LOG_DIR.mkdir(parents=True, exist_ok=True)
        line = json.dumps(record, ensure_ascii=True)
        with _lock:
            with REQUEST_LOG.open("a", encoding="utf-8") as f:
                f.write(line + "\n")
    except Exception:  # noqa: BLE001 - logging must not break the request
        pass


def read(limit: int | None = None) -> list[dict]:
    if not REQUEST_LOG.exists():
        return []
    rows = []
    for line in REQUEST_LOG.read_text(encoding="utf-8").splitlines():
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows[-limit:] if limit else rows
