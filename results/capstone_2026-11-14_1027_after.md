# Capstone run log - after (AI201_WARMUP=0)

Produced by `capstone_eval.py`. Service started fresh per trial with `python app.py`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Every request leaves a complete record | 20 of 20 | 20/20 (20 lines) | 20/20 (20 lines) | 20/20 (20 lines) | MET |
| 2. Cold first submit under 5 s | < 5000 ms, health < 60 s | 4750 ms, health 0.5 s | 5318 ms, health 0.5 s | 4851 ms, health 0.5 s | MISSED |
| 3. Warm p95 of 20 under 2 s | p95 < 2000 ms, 20/20 OK | p95 271 ms, med 208, 20/20 OK | p95 245 ms, med 207, 20/20 OK | p95 239 ms, med 217, 20/20 OK | MET |
| 4. Bad input: JSON 4xx, logged with error | 8 of 8 | 8/8 | 8/8 | 8/8 | MET |
| 5. Log matches response, stages add up | 10 of 10 | 10/10 (a 10, b 10) | 10/10 (a 10, b 10) | 10/10 (a 10, b 10) | MET |

## Cost (criterion 5's 10 warm submits per trial)

| Trial | mean duration_ms | mean cpu_ms | resident memory MB |
|---|---|---|---|
| 1 | 234.1 | 2289.1 | 999 |
| 2 | 214.1 | 2251.6 | 1000 |
| 3 | 194.7 | 2379.7 | 999 |

## Real output (trial 1)

**Criterion 2, record of the first submit** (`app.py::_log_request`)
```json
{"timestamp": "2026-11-14T15:26:49+00:00", "request_id": "dfb1da5d2150", "method": "POST", "route": "/submit", "status": 200, "input": {"creator_id": "aft1_cold", "text_chars": 496, "text_words": 91, "text_preview": "Four score and seven years ago our fathers brought forth on "}, "output": {"content_id": "3310776d43a8", "guess": "unsure", "label": "We can't tell for certain whether this was written by a pers", "combined_score": 0.5945, "status": "decided"}, "duration_ms": 4750.2, "cpu_ms": 7937.5, "stage_ms": {"model": 4738.7, "style": 1.2, "phrase": 0.1, "combine": 0.0}, "error": null}
```
**Criterion 5, two records** (`app.py::_log_request`)
```json
{"timestamp": "2026-11-14T15:26:54+00:00", "request_id": "815f64410efe", "method": "POST", "route": "/submit", "status": 200, "input": {"creator_id": "aft1_f0", "text_chars": 496, "text_words": 91, "text_preview": "Four score and seven years ago our fathers brought forth on "}, "output": {"content_id": "c60b57774a7c", "guess": "unsure", "label": "We can't tell for certain whether this was written by a pers", "combined_score": 0.5945, "status": "decided"}, "duration_ms": 158.4, "cpu_ms": 1937.5, "stage_ms": {"model": 156.7, "style": 0.4, "phrase": 0.1, "combine": 0.0}, "error": null}
{"timestamp": "2026-11-14T15:26:55+00:00", "request_id": "d3dc3492c9ce", "method": "POST", "route": "/submit", "status": 200, "input": {"creator_id": "aft1_f1", "text_chars": 533, "text_words": 110, "text_preview": "I went to the woods because I wished to live deliberately, t"}, "output": {"content_id": "26b968805c95", "guess": "unsure", "label": "We can't tell for certain whether this was written by a pers", "combined_score": 0.6038, "status": "decided"}, "duration_ms": 226.3, "cpu_ms": 2593.8, "stage_ms": {"model": 224.5, "style": 0.4, "phrase": 0.1, "combine": 0.0}, "error": null}
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
[{"route": "/submit", "status": 200, "error": null, "duration_ms": 122.1}, {"route": "/submit", "status": 200, "error": null, "duration_ms": 185.9}, {"route": "/submit", "status": 200, "error": null, "duration_ms": 206.2}, {"route": "/submit", "status": 200, "error": null, "duration_ms": 197.7}, {"route": "/submit", "status": 200, "error": null, "duration_ms": 216.6}, {"route": "/submit", "status": 200, "error": null, "duration_ms": 155.2}, {"route": "/submit", "status": 200, "error": null, "duration_ms": 226.4}, {"route": "/submit", "status": 200, "error": null, "duration_ms": 229.4}, {"route": "/submit", "status": 200, "error": null, "duration_ms": 189.0}, {"route": "/submit", "status": 200, "error": null, "duration_ms": 215.6}, {"route": "/submit", "status": 400, "error": "missing_text", "duration_ms": 0.8}, {"route": "/submit", "status": 400, "error": "missing_text", "duration_ms": 0.6}, {"route": "/submit", "status": 400, "error": "missing_creator_id", "duration_ms": 0.6}, {"route": "/submit", "status": 400, "error": "missing_creator_id", "duration_ms": 0.6}, {"route": "/submit", "status": 413, "error": "text_too_long", "duration_ms": 1.3}, {"route": "/submit", "status": 400, "error": "creator_id_too_long", "duration_ms": 0.8}, {"route": "/health", "status": 200, "error": null, "duration_ms": 19.7}, {"route": "/health", "status": 200, "error": null, "duration_ms": 7.9}, {"route": "/nope", "status": 404, "error": "http_404", "duration_ms": 0.2}, {"route": "/nope", "status": 404, "error": "http_404", "duration_ms": 0.2}]
```

Criterion 3 durations, trial 1 (ms): [160.5, 169.9, 180.0, 184.4, 185.5, 196.6, 200.0, 200.1, 201.9, 204.2, 208.4, 209.1, 209.7, 233.2, 246.6, 248.3, 251.3, 257.9, 271.2, 350.5]