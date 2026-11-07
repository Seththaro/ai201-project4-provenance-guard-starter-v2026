# Attack verdicts - before

- Source: `attack_run_2026-11-07_1017_before.md` (what came back) + `logs/audit.jsonl` (combined score)
- Produced by: `grade_attacks.py` (rules in its docstring and in the README)
- 58 attacks: **44 HELD, 14 BROKE**

| ID | Family | Status | Guess | Combined | Verdict | Why |
|---|---|---|---|---|---|---|
| AI01 | baseline_ai | 200 | unsure | 0.597 | BROKE | AI text got through as `unsure` |
| AI02 | baseline_ai | 200 | unsure | 0.640 | BROKE | AI text got through as `unsure` |
| AI03 | baseline_ai | 200 | unsure | 0.587 | BROKE | AI text got through as `unsure` |
| EV01 | evasion | 200 | unsure | 0.422 | BROKE | AI text got through as `unsure` |
| EV02 | evasion | 200 | unsure | 0.477 | BROKE | AI text got through as `unsure` |
| EV03 | evasion | 200 | unsure | 0.402 | BROKE | AI text got through as `unsure` |
| EV04 | evasion | 200 | unsure | 0.455 | BROKE | AI text got through as `unsure` |
| EV05 | evasion | 200 | unsure | 0.536 | BROKE | AI text got through as `unsure` |
| EV06 | evasion | 200 | unsure | 0.605 | BROKE | AI text got through as `unsure` |
| EV07 | evasion | 200 | unsure | 0.465 | BROKE | AI text got through as `unsure` |
| EV08 | evasion | 200 | unsure | 0.433 | BROKE | AI text got through as `unsure` |
| FP01 | false_positive | 200 | unsure | 0.590 | HELD | not accused (`unsure`) |
| FP02 | false_positive | 200 | unsure | 0.615 | HELD | not accused (`unsure`) |
| FP03 | false_positive | 200 | unsure | 0.578 | HELD | not accused (`unsure`) |
| FP04 | false_positive | 200 | unsure | 0.602 | HELD | not accused (`unsure`) |
| FP05 | false_positive | 200 | unsure | 0.553 | HELD | not accused (`unsure`) |
| FP06 | false_positive | 200 | unsure | 0.592 | HELD | not accused (`unsure`) |
| FP07 | false_positive | 200 | unsure | 0.655 | HELD | not accused (`unsure`) |
| PI01 | prompt_injection | 200 | unsure | 0.641 | HELD | same guess as AI01, combined moved +0.044 |
| PI02 | prompt_injection | 200 | unsure | 0.603 | HELD | same guess as AI02, combined moved -0.037 |
| PI03 | prompt_injection | 200 | unsure | 0.491 | HELD | same guess as AI03, combined moved -0.096 |
| PI04 | prompt_injection | 200 | unsure | 0.479 | BROKE | guess unsure -> unsure, combined moved -0.123 vs FP04 |
| PI05 | prompt_injection | 200 | unsure | 0.490 | HELD | same guess as FP05, combined moved -0.063 |
| JK01 | junk | 200 | unsure | 0.611 | HELD | answered unsure |
| JK02 | junk | 200 | unsure | 0.610 | HELD | answered unsure |
| JK03 | junk | 200 | unsure | 0.524 | HELD | not accused (`unsure`) |
| JK04 | junk | 200 | unsure | 0.420 | HELD | answered unsure |
| JK05 | junk | 200 | unsure | 0.559 | HELD | answered unsure |
| JK06 | junk | 200 | unsure | 0.541 | HELD | answered unsure |
| JK07 | junk | 422 | - | - | HELD | refused 422 |
| JK08 | junk | 200 | unsure | 0.557 | HELD | answered unsure |
| JK09 | junk | 200 | unsure | 0.554 | HELD | answered unsure |
| JK10 | junk | 200 | unsure | 0.611 | HELD | answered unsure |
| MR01 | malformed | 400 | - | - | HELD | refused 400 |
| MR02 | malformed | 400 | - | - | HELD | refused 400 |
| MR03 | malformed | 400 | - | - | HELD | refused 400 |
| MR04 | malformed | 400 | - | - | HELD | refused 400 |
| MR05 | malformed | 400 | - | - | HELD | refused 400 |
| MR06 | malformed | 400 | - | - | HELD | refused 400 |
| MR07 | malformed | 400 | - | - | HELD | refused 400 |
| MR08 | malformed | 429 | - | - | HELD | refused 429 before the route ran |
| MR09 | malformed | 200 | human | 0.348 | BROKE | a 5,000-character creator_id was accepted (200) |
| MR10 | malformed | 500 | - | - | BROKE | 500: the route crashed instead of refusing or answering |
| MR11 | malformed | 200 | unsure | 0.654 | HELD | accepted and judged |
| MR12 | malformed | 413 | - | - | HELD | refused 413 |
| MR13 | malformed | 200 | human | 0.310 | HELD | accepted and judged |
| FL01 | flood_same_creator | 200 | human | 0.348 | HELD | within the limit |
| FL02 | flood_same_creator | 200 | human | 0.348 | HELD | within the limit |
| FL03 | flood_same_creator | 200 | human | 0.348 | HELD | within the limit |
| FL04 | flood_same_creator | 200 | human | 0.348 | HELD | within the limit |
| FL05 | flood_same_creator | 200 | human | 0.348 | HELD | within the limit |
| FL06 | flood_same_creator | 429 | - | - | HELD | rate limited |
| FL07 | flood_same_creator | 429 | - | - | HELD | rate limited |
| FL08 | flood_same_creator | 429 | - | - | HELD | rate limited |
| FL09 | flood_same_creator | 429 | - | - | HELD | rate limited |
| FL10 | flood_same_creator | 429 | - | - | HELD | rate limited |
| FL11 | flood_same_creator | 429 | - | - | HELD | rate limited |
| FL12 | flood_same_creator | 429 | - | - | HELD | rate limited |

## By family

| Family | Attacks | HELD | BROKE |
|---|---|---|---|
| baseline_ai | 3 | 0 | 3 |
| evasion | 8 | 0 | 8 |
| false_positive | 7 | 7 | 0 |
| prompt_injection | 5 | 4 | 1 |
| junk | 10 | 10 | 0 |
| malformed | 13 | 11 | 2 |
| flood_same_creator | 12 | 12 | 0 |
