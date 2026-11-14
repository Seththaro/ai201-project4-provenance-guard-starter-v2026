#!/usr/bin/env python3
"""
Provenance Guard - the web service.

    python app.py

Then, in another terminal:

    curl -X POST http://127.0.0.1:5000/ping \
      -H "Content-Type: application/json" \
      -d '{"message": "hello"}'

That's the example route. It works right now, before you've written anything.
**Leave it alone** - it's your control. When something breaks later, check that
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself.

Routes:

    POST /ping        the worked example. Already works. Don't edit it
    POST /submit      text in, guess + confidence + label out
    POST /appeal      a writer pushes back; item goes to under_review
    GET  /content/<id>  one item's current status (stretch)
    POST /verify      earn a verified-human credential (stretch)
    GET  /log         the audit log. Already works
    GET  /health      is the service up, and is the model loaded
"""

import time
import uuid

from flask import Flask, g, jsonify, request
from werkzeug.exceptions import HTTPException

import audit
import config
import detector
import phrases
import reqlog
import scoring
import stylometry

app = Flask(__name__)


# ── Rate limiting - UNIT 8 ────────────────────────────────────────────────────
# Off until you turn it on. In unit 8, Milestone 1:
#
#   1. Set RATE_LIMITING_ENABLED = True in config.py (or AI201_RATE_LIMITS=1)
#   2. Choose your numbers there
#   3. Uncomment the @limiter.limit(...) line on /submit below
#
# The order doesn't matter. While limiting is off, that decorator is a no-op
# that quietly does nothing, so uncommenting it early costs you nothing - but
# it also means no 429 until you've done step 1.
#
# The storage backend is preconfigured, which stops Flask-Limiter printing a
# warning on every start. In-memory is right for one laptop and wrong for
# anything real - a restart forgets every count.

class _LimiterOff:
    """
    Stands in for the real limiter while rate limiting is off.

    It makes @limiter.limit(...) a decorator that returns the route
    untouched, so uncommenting the line before you flip the setting is
    harmless instead of a crash on startup.
    """

    def limit(self, *args, **kwargs):
        return lambda view: view


limiter = _LimiterOff()
if config.RATE_LIMITING_ENABLED:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    def rate_limit_key():
        """
        Who a request counts against.

        Falling back to the caller's address is the easy version. Unit 8's
        stretch asks about per-creator limits instead - and the difference
        matters: one script can look like a thousand callers, and one household
        can look like one.
        """
        payload = request.get_json(silent=True)
        # A body that parses as JSON but isn't an object - a bare list or
        # string - has no .get. Without this guard the key function raises
        # BEFORE the route runs, and a malformed request becomes a 500 that
        # looks like your handler crashed when your handler never ran.
        if not isinstance(payload, dict):
            return get_remote_address()
        creator = payload.get("creator_id")
        return creator if isinstance(creator, str) and creator.strip() else get_remote_address()

    limiter = Limiter(
        key_func=rate_limit_key,
        app=app,
        storage_uri=config.RATE_LIMIT_STORAGE,
        default_limits=[],
    )

    @app.errorhandler(429)
    def rate_limited(exc):
        """
        A rejected request still leaves a trace.

        ⚠️ An attack that shows up only as an absence is one you'll never find.
        """
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            payload = {}
        audit.log_rejection(
            creator_id=payload.get("creator_id", "unknown"),
            reason="rate_limited",
            limit=str(exc.description),
        )
        return jsonify({
            "error": "rate_limited",
            "message": "Too many submissions. Try again shortly.",
            "limit": str(exc.description),
        }), 429



# ── Request log - CAPSTONE (shape A) ──────────────────────────────────────────
# One structured record per request, written after the response is built, so a
# refused, rate-limited or crashed request leaves a trace too. See reqlog.py.

@app.before_request
def _start_timer():
    g.t0 = time.perf_counter()
    g.cpu0 = time.process_time()
    g.request_id = uuid.uuid4().hex[:12]
    g.stage_ms = {}
    g.error = None


@app.after_request
def _log_request(response):
    try:
        status = response.status_code
        body = response.get_json(silent=True) if response.is_json else None
        error = getattr(g, "error", None)
        if error is None and status >= 400:
            error = (body or {}).get("error") if isinstance(body, dict) else None
            error = error or f"http_{status}"
        record = {
            "timestamp": audit._now(),
            "request_id": getattr(g, "request_id", None),
            "method": request.method,
            "route": request.path,
            "status": status,
            "input": reqlog.summarize_input(request.get_json(silent=True)) if request.method == "POST" else {},
            "output": reqlog.summarize_output(status, body),
            "duration_ms": round((time.perf_counter() - g.t0) * 1000, 1),
            "cpu_ms": round((time.process_time() - g.cpu0) * 1000, 1),
            "stage_ms": getattr(g, "stage_ms", {}),
            "error": error,
        }
        reqlog.write(record)
        response.headers["X-Request-ID"] = record["request_id"]
    except Exception:  # noqa: BLE001 - never let logging break a response
        pass
    return response


@app.errorhandler(Exception)
def _unhandled(exc):
    """A crash answers in JSON and is recorded with its error, not just a bare 500."""
    if isinstance(exc, HTTPException):
        return exc
    g.error = f"{type(exc).__name__}: {str(exc)[:120]}"
    return jsonify({"error": "internal_error", "message": "The service hit an unexpected error."}), 500


# ── The worked example. Already works. Don't edit. ────────────────────────────

@app.post("/ping")
def ping():
    """
    Everything a route needs, in six lines.

    JSON arrives as a dict. You pull things out of it. You return a dict and
    the framework turns it into a response. That's the whole idea.
    """
    payload = request.get_json(silent=True) or {}
    return jsonify({
        "ok": True,
        "you_sent": payload.get("message"),
        "service": "provenance-guard",
    })


@app.get("/health")
def health():
    """Is the service up, and has the model been downloaded yet?"""
    import detector

    loaded = detector._model is not None
    return jsonify({
        "ok": True,
        "detector_model": config.DETECTOR_MODEL,
        "detector_loaded": loaded,
        "rate_limiting": config.RATE_LIMITING_ENABLED,
        "log_entries": len(audit.read_entries()),
    })


# ── The routes you build ──────────────────────────────────────────────────────

def _error(status: int, code: str, message: str, creator_id=None):
    """Refuse an input, leave a trace in the log, answer in JSON."""
    audit.log_rejection(
        creator_id=creator_id if isinstance(creator_id, str) else "unknown",
        reason=code,
    )
    return jsonify({"error": code, "message": message}), status


def _payload() -> dict:
    """The JSON body as a dict. A bare list or string counts as empty."""
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


_verified_ids = None   # capstone improvement 1: built once, not re-read per request


def _is_verified(creator_id: str) -> bool:
    """
    Has this writer earned the verified-human credential (stretch)?

    Capstone improvement 1: this used to re-parse the whole audit log on every
    submission (5 ms at 1,600 entries, growing with the log). The set of
    verified creators is now read once and updated when /verify grants one.
    """
    global _verified_ids
    if _verified_ids is None:
        _verified_ids = {
            e.get("creator_id") for e in audit.read_entries()
            if e.get("event") == "verification" and e.get("status") == "verified"
        }
    return creator_id in _verified_ids


def _score_text(text: str) -> dict:
    """Run all three signals and combine. Models load once and stay loaded."""
    stage = getattr(g, "stage_ms", {})
    t = time.perf_counter()
    model_score = detector.model_signal(text)
    stage["model"] = round((time.perf_counter() - t) * 1000, 1)
    t = time.perf_counter()
    style_score = stylometry.style_signal(text)
    stage["style"] = round((time.perf_counter() - t) * 1000, 1)
    t = time.perf_counter()
    phrase_score = phrases.phrase_signal(text)
    stage["phrase"] = round((time.perf_counter() - t) * 1000, 1)
    t = time.perf_counter()
    combined = scoring.combine_signals(model_score, style_score, phrase_score)
    guess, label = scoring.score_to_label(combined)
    stage["combine"] = round((time.perf_counter() - t) * 1000, 1)
    return {
        "model_score": model_score,
        "style_score": style_score,
        "phrase_score": phrase_score,
        "combined_score": combined,
        "confidence": scoring.confidence_of(combined),
        "guess": guess,
        "label": label,
    }


def _check_text(text, creator_id, min_words):
    """Validate text + creator_id. Returns an error response or None."""
    if not isinstance(creator_id, str) or not creator_id.strip():
        return _error(400, "missing_creator_id", "creator_id is required and must be a non-empty string.")
    # creator_id is a log field and a rate-limit key, so it must be short and
    # writable as UTF-8 before anything else touches it. It is passed to _error
    # as None because logging the bad value itself is what crashed the route.
    if len(creator_id) > config.MAX_CREATOR_ID_CHARS:
        return _error(400, "creator_id_too_long",
                      f"creator_id is over {config.MAX_CREATOR_ID_CHARS} characters.")
    try:
        creator_id.encode("utf-8")
    except UnicodeEncodeError:
        return _error(400, "invalid_creator_id", "creator_id contains characters that cannot be stored.")
    if not isinstance(text, str) or not text.strip():
        return _error(400, "missing_text", "text is required and must be a non-empty string.", creator_id)
    if len(text) > config.MAX_TEXT_CHARS:
        return _error(413, "text_too_long",
                      f"text is over {config.MAX_TEXT_CHARS} characters; please send a shorter piece.", creator_id)
    if len(text.split()) < min_words:
        return _error(422, "text_too_short",
                      f"text needs at least {min_words} words to be checked.", creator_id)
    return None


@app.post("/submit")
# Unit 8 improvement 2: only requests that were accepted count against the limit.
# A refused request (a 4xx) costs almost nothing to answer, and before this change
# every request with no usable creator_id shared one per-address bucket, so a few
# malformed requests locked out the next ones with a 429 before _check_text ran.
@limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day", deduct_when=lambda response: response.status_code < 400)
def submit():
    """
    Take a piece of text, decide about it, log the decision, answer.

    Expects JSON:  {"text": "...", "creator_id": "..."}
    Returns JSON:  content_id, guess, confidence, label, model_score,
                   style_score, phrase_score, combined_score, status,
                   verified_human.

    Bad input (missing/empty/non-string text, missing creator_id, under
    MIN_WORDS, over MAX_TEXT_CHARS) is refused with 400/413/422 and logged as
    a rejection; it never reaches a signal.
    """
    data = _payload()
    text, creator_id = data.get("text"), data.get("creator_id")

    problem = _check_text(text, creator_id, config.MIN_WORDS)
    if problem:
        return problem

    try:
        result = _score_text(text)
    except detector.DetectorUnavailable as exc:
        return _error(503, "detector_unavailable", str(exc).splitlines()[0], creator_id)

    verified = _is_verified(creator_id)
    if verified:
        result["label"] += " This writer holds a verified-human credential."
        if result["guess"] == "ai":
            # A credentialed writer is never auto-labelled high-confidence AI;
            # the item is downgraded to "unsure" instead.
            result["guess"], result["label"] = "unsure", scoring.LABELS["unsure"] + (
                " This writer holds a verified-human credential.")

    content_id = uuid.uuid4().hex[:12]
    audit.log_decision(
        content_id=content_id,
        creator_id=creator_id,
        guess=result["guess"],
        model_score=result["model_score"],
        style_score=result["style_score"],
        combined_score=result["combined_score"],
        label=result["label"],
        status="decided",
        phrase_score=result["phrase_score"],
        confidence=result["confidence"],
        verified_human=verified,
        word_count=len(text.split()),
    )

    return jsonify({
        "content_id": content_id,
        "guess": result["guess"],
        "confidence": result["confidence"],
        "label": result["label"],
        "model_score": result["model_score"],
        "style_score": result["style_score"],
        "phrase_score": result["phrase_score"],
        "combined_score": result["combined_score"],
        "verified_human": verified,
        "status": "decided",
    })


@app.post("/appeal")
def appeal():
    """
    A writer says we got it wrong.

    Expects JSON:  {"content_id": "...", "reasoning": "..."}
    Records the appeal beside the original decision, moves the item to
    under_review, and confirms. No automatic re-checking.
    """
    data = _payload()
    content_id, reasoning = data.get("content_id"), data.get("reasoning")

    if not isinstance(content_id, str) or not content_id.strip():
        return _error(400, "missing_content_id", "content_id is required.")
    if not isinstance(reasoning, str) or not reasoning.strip():
        return _error(400, "missing_reasoning", "Please tell us why you think this was wrong.")
    if len(reasoning) > config.MAX_REASONING_CHARS:
        return _error(413, "reasoning_too_long",
                      f"reasoning is over {config.MAX_REASONING_CHARS} characters.")

    decisions = [e for e in audit.entries_for(content_id) if e.get("event") is None]
    if not decisions:
        return _error(404, "unknown_content_id", f"No submission found with content_id '{content_id}'.")

    audit.log_appeal(content_id, decisions[0]["creator_id"], reasoning.strip())
    return jsonify({
        "content_id": content_id,
        "status": "under_review",
        "message": "Thank you. Your appeal has been recorded and a person will review it.",
    })


@app.get("/content/<content_id>")
def get_content(content_id):
    """Current status of one item (stretch): decision, status, appeals."""
    entries = audit.entries_for(content_id)
    decisions = [e for e in entries if e.get("event") is None]
    if not decisions:
        return jsonify({"error": "unknown_content_id",
                        "message": f"No submission found with content_id '{content_id}'."}), 404
    d = decisions[0]
    appeals = [e for e in entries if e.get("event") == "appeal"]
    return jsonify({
        "content_id": content_id,
        "creator_id": d["creator_id"],
        "guess": d["guess"],
        "combined_score": d["combined_score"],
        "verified_human": d.get("verified_human", False),
        "status": entries[-1]["status"],
        "appeals": [{"timestamp": a["timestamp"], "reasoning": a["reasoning"]} for a in appeals],
    })


@app.post("/verify")
def verify():
    """
    Verified-human path (stretch). The extra step: the writer sends a fresh
    writing sample of at least VERIFY_MIN_WORDS words, written on the spot.
    If our checks don't call it high-confidence AI, the writer earns the
    credential, and it shows on every later submission and in GET /content.

    Expects JSON:  {"creator_id": "...", "sample": "..."}
    """
    data = _payload()
    creator_id, sample = data.get("creator_id"), data.get("sample")

    problem = _check_text(sample, creator_id, config.VERIFY_MIN_WORDS)
    if problem:
        return problem

    try:
        result = _score_text(sample)
    except detector.DetectorUnavailable as exc:
        return _error(503, "detector_unavailable", str(exc).splitlines()[0], creator_id)

    granted = result["guess"] != "ai"
    if granted and _verified_ids is not None:
        _verified_ids.add(creator_id)
    audit.log_verification(
        creator_id=creator_id,
        granted=granted,
        combined_score=result["combined_score"],
        guess=result["guess"],
    )
    if not granted:
        return jsonify({
            "creator_id": creator_id,
            "verified_human": False,
            "message": "We couldn't verify this sample automatically. Try a longer, more personal "
                       "sample, or contact a reviewer.",
        }), 200
    return jsonify({
        "creator_id": creator_id,
        "verified_human": True,
        "message": "You now hold a verified-human credential. It will show on your future work.",
    })


# ── Already works ─────────────────────────────────────────────────────────────

@app.get("/log")
def get_log():
    """
    The audit log, most recent last.

        curl "http://127.0.0.1:5000/log?limit=10"

    You need this in unit 8 to paste entries into your README, and you need it
    now to see whether your logging is actually working.
    """
    limit = request.args.get("limit", type=int)
    entries = audit.read_entries(limit=limit)
    return jsonify({"count": len(entries), "entries": entries})


def main():
    print(f"Provenance Guard on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(f"  rate limiting:   {'ON' if config.RATE_LIMITING_ENABLED else 'off (unit 8)'}")
    print(f"  audit log:       {config.AUDIT_LOG}")
    print(f"  request log:     {reqlog.REQUEST_LOG}")
    if config.WARMUP_ON_START:
        import time as _t
        t = _t.perf_counter()
        print(f"  warming up:      {detector.warm_up()} ({_t.perf_counter() - t:.1f}s)")
    else:
        print("  warm-up:         off (first /submit loads the model)")
    print()
    print("Check it's alive:")
    print(f'  curl -X POST http://{config.HOST}:{config.PORT}/ping \\')
    print('    -H "Content-Type: application/json" \\')
    print("    -d '{\"message\": \"hello\"}'")
    print()
    # debug=True hands out an interactive debugger, so it's local-only - see config.py
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()
