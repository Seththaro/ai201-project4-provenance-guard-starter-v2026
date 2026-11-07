# Per-creator limit: what it does not catch

- Produced by: a short script run from this repo against `app.py::submit` (2026-11-07 09:24)
- 15 submissions from ONE address, each under a DIFFERENT creator_id (`rotator_1` ... `rotator_15`)
- Limit in force: 5 per minute and 50 per day, per creator_id

```
200 200 200 200 200 200 200 200 200 200 200 200 200 200 200
```

Every request got through because each creator_id has its own counter. The flood test in `flood_*.md` (one creator_id, 15 requests) was cut off after 5. A caller who rotates creator_id is not limited by a per-creator key.
