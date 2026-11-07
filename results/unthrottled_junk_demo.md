# What improvement 2 costs: refused requests are no longer throttled

- Produced by: a short script against the running service (2026-11-07 10:27), improvement 2 in force
- 30 requests from ONE creator_id (`junk_flooder`), each with empty text (always refused)

```
400 400 400 400 400 400 400 400 400 400 400 400 400 400 400 400 400 400 400 400 400 400 400 400 400 400 400 400 400 400
```

- Audit log entries before: 1257, after: 1287 (+30, one `rejected` entry per refused request)

None of the 30 got a 429, because a request that returns 4xx no longer counts against the limit. Before improvement 2 this creator would have been cut off after 5. The refusals are cheap to answer (no model runs), but each one writes a log line, so an attacker can grow `logs/audit.jsonl` without limit.
