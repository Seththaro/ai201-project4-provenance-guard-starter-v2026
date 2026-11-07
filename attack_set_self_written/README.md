# Self-written attack set

This is NOT the staff attack set. The staff set (`attack_set.zip`) was not available, so I wrote this one in the same two-file format that `run_attacks.py` reads, before running anything against my service and without looking at how my service scores any of it.

- `attacks.csv`: 33 text attacks in six families: `baseline_ai` (3), `evasion` (8), `false_positive` (7), `prompt_injection` (5), `junk` (10).
- `attacks_malformed_requests.csv`: 25 requests: 13 `malformed` and 12 `flood_same_creator`.

Everything in it was written by me for this test. The "human" texts (`false_positive` family) are stand-ins in a plain, second-language or student voice, not samples from real people. If the staff set arrives, run it the same way (`python run_attacks.py --set <folder> --label ...`) and treat its results as the real measurement.
