# Capstone run log - before (AI201_WARMUP=0)

Produced by `capstone_eval.py`. Service started fresh per trial with `python app.py`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every request leaves a complete record | 20 of 20 | 20/20 (20 lines) | 20/20 (20 lines) | 20/20 (20 lines) | MET |
| 2. Cold first submit under 5 s | < 5000 ms, health < 60 s | 4739 ms, health 0.5 s | 4776 ms, health 0.5 s | 4562 ms, health 0.5 s | MET |
| 3. Warm p95 of 20 under 2 s | p95 < 2000 ms, 20/20 OK | p95 314 ms, med 216, 20/20 OK | p95 228 ms, med 220, 20/20 OK | p95 256 ms, med 215, 20/20 OK | MET |
| 4. Bad input: JSON 4xx, logged with error | 8 of 8 | 8/8 | 8/8 | 8/8 | MET |
| 5. Log matches response, stages add up | 10 of 10 | 9/10 (a 10, b 9) | 9/10 (a 10, b 9) | 9/10 (a 10, b 9) | MISSED |

## Cost (criterion 5's 10 warm submits per trial)

| Trial | mean duration_ms | mean cpu_ms | resident memory MB |
|---|---|---|---|
| 1 | 242.4 | 2414.1 | None |
| 2 | 200.7 | 2409.4 | None |
| 3 | 197.8 | 2370.3 | None |

## Real output (trial 1)

**Criterion 2, record of the first submit** (`app.py::_log_request`)
```json
{"timestamp": "2026-11-14T15:25:05+00:00", "request_id": "d3c5041635e3", "method": "POST", "route": "/submit", "status": 200, "input": {"creator_id": "bef1_cold", "text_chars": 496, "text_words": 91, "text_preview": "Four score and seven years ago our fathers brought forth on "}, "output": {"content_id": "ee1203a6f9c4", "guess": "unsure", "label": "We can't tell for certain whether this was written by a pers", "combined_score": 0.5945, "status": "decided"}, "duration_ms": 4739.2, "cpu_ms": 7312.5, "stage_ms": {"model": 4729.7, "style": 1.2, "phrase": 0.1, "combine": 0.0}, "error": null}
```
**Criterion 5, two records** (`app.py::_log_request`)
```json
{"timestamp": "2026-11-14T15:25:10+00:00", "request_id": "46134c0c2f82", "method": "POST", "route": "/submit", "status": 200, "input": {"creator_id": "bef1_f0", "text_chars": 496, "text_words": 91, "text_preview": "Four score and seven years ago our fathers brought forth on "}, "output": {"content_id": "81c8569a2a96", "guess": "unsure", "label": "We can't tell for certain whether this was written by a pers", "combined_score": 0.5945, "status": "decided"}, "duration_ms": 265.1, "cpu_ms": 2546.9, "stage_ms": {"model": 234.0, "style": 0.6, "phrase": 0.1, "combine": 0.0}, "error": null}
{"timestamp": "2026-11-14T15:25:11+00:00", "request_id": "8b8c642a0dda", "method": "POST", "route": "/submit", "status": 200, "input": {"creator_id": "bef1_f1", "text_chars": 533, "text_words": 110, "text_preview": "I went to the woods because I wished to live deliberately, t"}, "output": {"content_id": "7d2bac4a14ef", "guess": "unsure", "label": "We can't tell for certain whether this was written by a pers", "combined_score": 0.6038, "status": "decided"}, "duration_ms": 401.3, "cpu_ms": 2812.5, "stage_ms": {"model": 385.6, "style": 0.5, "phrase": 0.1, "combine": 0.0}, "error": null}
```
**Criterion 4, per case** (`app.py::_check_text`, `_log_request`)
```json
[
 {
  "case": "no text",
  "status": 400,
  "error": "missing_text",
  "logged_status": 400,
  "logged_error": "missing_text",
  "ok": true
 },
 {
  "case": "text null",
  "status": 400,
  "error": "missing_text",
  "logged_status": 400,
  "logged_error": "missing_text",
  "ok": true
 },
 {
  "case": "list body",
  "status": 400,
  "error": "missing_creator_id",
  "logged_status": 400,
  "logged_error": "missing_creator_id",
  "ok": true
 },
 {
  "case": "empty body",
  "status": 400,
  "error": "missing_creator_id",
  "logged_status": 400,
  "logged_error": "missing_creator_id",
  "ok": true
 },
 {
  "case": "25000 chars",
  "status": 413,
  "error": "text_too_long",
  "logged_status": 413,
  "logged_error": "text_too_long",
  "ok": true
 },
 {
  "case": "5000-char creator_id",
  "status": 400,
  "error": "creator_id_too_long",
  "logged_status": 400,
  "logged_error": "creator_id_too_long",
  "ok": true
 },
 {
  "case": "numeric creator_id",
  "status": 400,
  "error": "missing_creator_id",
  "logged_status": 400,
  "logged_error": "missing_creator_id",
  "ok": true
 },
 {
  "case": "lone surrogate creator_id",
  "status": 400,
  "error": "invalid_creator_id",
  "logged_status": 400,
  "logged_error": "invalid_creator_id",
  "ok": true
 }
]
```
**Criterion 1, the 20 records** (route, status, error, duration_ms)
```json
[{"route": "/submit", "status": 200, "error": null, "duration_ms": 146.5}, {"route": "/submit", "status": 200, "error": null, "duration_ms": 196.8}, {"route": "/submit", "status": 200, "error": null, "duration_ms": 196.3}, {"route": "/submit", "status": 200, "error": null, "duration_ms": 238.5}, {"route": "/submit", "status": 200, "error": null, "duration_ms": 208.7}, {"route": "/submit", "status": 200, "error": null, "duration_ms": 167.3}, {"route": "/submit", "status": 200, "error": null, "duration_ms": 233.3}, {"route": "/submit", "status": 200, "error": null, "duration_ms": 230.2}, {"route": "/submit", "status": 200, "error": null, "duration_ms": 204.8}, {"route": "/submit", "status": 200, "error": null, "duration_ms": 232.6}, {"route": "/submit", "status": 400, "error": "missing_text", "duration_ms": 0.8}, {"route": "/submit", "status": 400, "error": "missing_text", "duration_ms": 0.9}, {"route": "/submit", "status": 400, "error": "missing_creator_id", "duration_ms": 0.8}, {"route": "/submit", "status": 400, "error": "missing_creator_id", "duration_ms": 0.7}, {"route": "/submit", "status": 413, "error": "text_too_long", "duration_ms": 1.0}, {"route": "/submit", "status": 400, "error": "creator_id_too_long", "duration_ms": 1.0}, {"route": "/health", "status": 200, "error": null, "duration_ms": 17.6}, {"route": "/health", "status": 200, "error": null, "duration_ms": 7.4}, {"route": "/nope", "status": 404, "error": "http_404", "duration_ms": 0.3}, {"route": "/nope", "status": 404, "error": "http_404", "duration_ms": 0.2}]
```

Criterion 3 durations, trial 1 (ms): [183.5, 188.5, 199.3, 202.0, 204.7, 205.5, 207.3, 207.9, 212.9, 213.5, 216.1, 225.5, 231.0, 233.1, 234.1, 240.9, 249.5, 251.4, 313.5, 328.8]