# Acceptance criteria - Provenance Guard capstone (unit 9)

Shape A, deploy and instrument. Written before any capstone results exist. The
unit 7 criteria are kept in `criteria_unit7.md`. Criteria 1, 2, 3 and 5 are about
this unit's work (the request log, the run path, the numbers that come out of
it); criterion 4 is the bad path.

Setup common to all five: the service is started with the one command in
`RUNNING.md` (`python app.py`) with `AI201_RATE_LIMITS=1` (the default), each
trial starts from an empty `logs/requests.jsonl`, and every request in a trial
uses its own `creator_id` unless said otherwise. "Warm" means after at least one
successful `/submit`. Targets must hold in each of 3 trials.

---

## 1. Every request leaves a complete record: 20 of 20

Send 20 requests to the running service in one trial: 10 valid `POST /submit`
(about 100 words each), 6 invalid `POST /submit` bodies (see criterion 4), 2
`GET /health`, and 2 requests to routes that do not exist (`GET /nope`). Read
`logs/requests.jsonl` afterwards. **Exactly 20 new lines appear, and every line
has non-null `timestamp`, `request_id`, `route`, `status`, `input`, `output` and
`duration_ms`.** Nine of 10 is a miss.

**Why this target:** The point of this unit is that an attack or a failure that
leaves no trace cannot be diagnosed (the unit 8 lesson). A log that records 19 of
20 requests silently drops exactly the ones nobody noticed, so there is no
acceptable fraction below all of them. I include refused and nonexistent routes
because those are the requests most likely to skip a hook.

---

## 2. Cold start: the first submission after starting answers in under 5 seconds

Start the service from nothing with the documented command, wait until
`GET /health` answers, then send one valid `POST /submit`. **The `duration_ms`
the request log records for that first submission is under 5000, and `/health`
answered within 60 seconds of launching the command.** One cold start per trial,
so three in all. This is the cold request, not a warm one.

**Why this target:** My unit 7 README says the first submission "takes 10+
seconds" because gpt2 loads inside the request. A writer, or a health check with
a short timeout, who hits a freshly started service would see a hang that looks
like an outage. 5 seconds is the point where a browser user gives up and a
typical proxy timeout starts to bite. A looser target (30 s) would be met by the
system as it already is, and teach me nothing. I expect to miss this.

---

## 3. Warm latency: 95th percentile of 20 valid submissions is under 2000 ms

After a warm-up submission, send 20 valid `POST /submit` of 80 to 130 words,
sequentially, each under its own `creator_id`. Take `duration_ms` from the 20
request-log lines. **The 95th percentile (the 19th value when sorted) is under
2000 ms, and all 20 return 200.**

**Why this target:** My unit 7 note says a warm submission takes "a second or
two" because gpt2 runs on CPU inside the request. 2 seconds at p95 is a person
waiting for a label after pasting a paragraph. I chose p95 rather than the mean
because the slow requests are the ones a user remembers, and a mean of 900 ms
would hide a tail of 4 s. Under 1000 ms would need a smaller model; I did not
scope that in.

---

## 4. The bad path: 8 of 8 bad inputs get a JSON 4xx, never a 500, and are logged with their error

Send 8 bad requests to `POST /submit`: no `text`; `text: null`; a bare JSON list
as the body; an empty body; text of 25,000 characters; a `creator_id` of 5,000
characters; a numeric `creator_id`; a `creator_id` containing a lone surrogate
(`"\ud800"`). **All 8 return a status from 400 to 499 with a JSON body that has
an `error` field, none returns 500 or HTML, and for all 8 the request-log line
has `status` equal to the response and `error` equal to the response's `error`
code.** The bad inputs cover what broke in unit 8 (the surrogate was a 500) and
what could break in the new logging code (a value that cannot be written).

**Why this target:** The new log hooks run on every request, so a request that
makes them throw is a new way to crash that did not exist before this unit. A
500 on bad input is also the case where the unit 8 audit log stayed silent about
a decision, so 8 of 8 and not 7 of 8.

---

## 5. The log tells the truth: 10 of 10 records match the response and the stage timings add up

After warm-up, send 10 valid `POST /submit`. For each, compare three things.
**(a)** `output.combined_score` in the request log equals `combined_score` in the
HTTP response and in the audit-log entry for the same `content_id`. **(b)**
`stage_ms.model + style + phrase + combine` is at least 90% of `duration_ms`.
All 10 satisfy both (a) and (b).

**Why this target:** A log that disagrees with what the user was told, or timings
that leave a quarter of the request unexplained, is worse than no log because I
would trust it when diagnosing. (a) catches a hook that logs a stale or wrong
body. (b) checks that my stage timers cover the work; if the model stage is the
only one I timed and something else is slow, the stages will not add up and the
latency breakdown stretch would be wrong. I picked 90% because JSON encoding and
the audit-log write sit outside the four timed stages and should be small.
