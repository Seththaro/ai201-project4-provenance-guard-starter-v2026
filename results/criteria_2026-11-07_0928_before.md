# Criteria run - before

- Produced by: `check_criteria.py::main` (texts from `scenarios.py`)
- 3 trials, nothing changed in between, 2026-11-07 09:28
- Limits in force: 5/minute, 50/day per creator_id

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing flagged as AI | <= 1 of 10, none of the plain 5 | 0/10 (plain 0/5) | 0/10 (plain 0/5) | 0/10 (plain 0/5) | |
| 2. Score spread | gap >= 0.30 | 0.083 | 0.083 | 0.083 | |
| 3. Label coverage | 3 of 3 labels, >= 3 unsure | 1h/19u/0ai | 1h/19u/0ai | 1h/19u/0ai | |
| 4. Appeal path | 10/10 + 3/3 unknown 404 | 10/10 + 3/3 | 10/10 + 3/3 | 10/10 + 3/3 | |
| 5. Bad input | 8/8 4xx JSON, 8 logged, ping 200 | 8/8, 8 logged | 8/8, 8 logged | 7/8, 8 logged | |

Per-trial detail (real output):

```json
[
  {
    "c1": {
      "ai_of_10": 0,
      "plain_ai_of_5": 0,
      "flagged_indexes": [],
      "pass": true
    },
    "c2": {
      "mean_ai": 0.6072,
      "mean_human": 0.5246,
      "gap": 0.0826,
      "pass": false
    },
    "c3": {
      "sweep_labels_seen": [
        "ai",
        "human",
        "unsure"
      ],
      "guess_counts": {
        "human": 1,
        "unsure": 19,
        "ai": 0
      },
      "n": 20,
      "pass": false
    },
    "c4": {
      "appeals_ok_of_10": 10,
      "unknown_404_of_3": 3,
      "unknown_entries_added": 0,
      "pass": true
    },
    "c5": {
      "statuses": [
        400,
        400,
        400,
        400,
        422,
        413,
        400,
        400
      ],
      "errors": [
        "missing_text",
        "missing_text",
        "missing_text",
        "missing_text",
        "text_too_short",
        "text_too_long",
        "missing_creator_id",
        "missing_creator_id"
      ],
      "rejected_entries_added": 8,
      "ping": 200,
      "pass": true
    }
  },
  {
    "c1": {
      "ai_of_10": 0,
      "plain_ai_of_5": 0,
      "flagged_indexes": [],
      "pass": true
    },
    "c2": {
      "mean_ai": 0.6072,
      "mean_human": 0.5246,
      "gap": 0.0826,
      "pass": false
    },
    "c3": {
      "sweep_labels_seen": [
        "ai",
        "human",
        "unsure"
      ],
      "guess_counts": {
        "human": 1,
        "unsure": 19,
        "ai": 0
      },
      "n": 20,
      "pass": false
    },
    "c4": {
      "appeals_ok_of_10": 10,
      "unknown_404_of_3": 3,
      "unknown_entries_added": 0,
      "pass": true
    },
    "c5": {
      "statuses": [
        400,
        400,
        400,
        400,
        422,
        413,
        400,
        400
      ],
      "errors": [
        "missing_text",
        "missing_text",
        "missing_text",
        "missing_text",
        "text_too_short",
        "text_too_long",
        "missing_creator_id",
        "missing_creator_id"
      ],
      "rejected_entries_added": 8,
      "ping": 200,
      "pass": true
    }
  },
  {
    "c1": {
      "ai_of_10": 0,
      "plain_ai_of_5": 0,
      "flagged_indexes": [],
      "pass": true
    },
    "c2": {
      "mean_ai": 0.6072,
      "mean_human": 0.5246,
      "gap": 0.0826,
      "pass": false
    },
    "c3": {
      "sweep_labels_seen": [
        "ai",
        "human",
        "unsure"
      ],
      "guess_counts": {
        "human": 1,
        "unsure": 19,
        "ai": 0
      },
      "n": 20,
      "pass": false
    },
    "c4": {
      "appeals_ok_of_10": 10,
      "unknown_404_of_3": 3,
      "unknown_entries_added": 0,
      "pass": true
    },
    "c5": {
      "statuses": [
        400,
        400,
        400,
        400,
        422,
        413,
        400,
        429
      ],
      "errors": [
        "missing_text",
        "missing_text",
        "missing_text",
        "missing_text",
        "text_too_short",
        "text_too_long",
        "missing_creator_id",
        "rate_limited"
      ],
      "rejected_entries_added": 8,
      "ping": 200,
      "pass": false
    }
  }
]
```

Raw `/submit` results for trial 1 (index 0-4 plain human, 5-9 classic human, 10-14 AI, 15-19 borderline):

```json
[
  {
    "i": 0,
    "status": 200,
    "content_id": "43159a26c662",
    "guess": "unsure",
    "model_score": 0.8775,
    "style_score": 0.6294,
    "phrase_score": 0.4,
    "combined_score": 0.5976
  },
  {
    "i": 1,
    "status": 200,
    "content_id": "e7ba62d9abf3",
    "guess": "unsure",
    "model_score": 0.7638,
    "style_score": 0.71,
    "phrase_score": 0.4,
    "combined_score": 0.5861
  },
  {
    "i": 2,
    "status": 200,
    "content_id": "65252b2d6729",
    "guess": "unsure",
    "model_score": 0.8255,
    "style_score": 0.6167,
    "phrase_score": 0.0,
    "combined_score": 0.5437
  },
  {
    "i": 3,
    "status": 200,
    "content_id": "e06107371c16",
    "guess": "unsure",
    "model_score": 0.7961,
    "style_score": 0.6435,
    "phrase_score": 0.4,
    "combined_score": 0.5817
  },
  {
    "i": 4,
    "status": 200,
    "content_id": "5aed1d893a83",
    "guess": "unsure",
    "model_score": 0.548,
    "style_score": 0.6053,
    "phrase_score": 0.4,
    "combined_score": 0.5385
  },
  {
    "i": 5,
    "status": 200,
    "content_id": "20a076b0f186",
    "guess": "unsure",
    "model_score": 0.6999,
    "style_score": 0.5702,
    "phrase_score": 0.4,
    "combined_score": 0.5945
  },
  {
    "i": 6,
    "status": 200,
    "content_id": "f220eabc8903",
    "guess": "unsure",
    "model_score": 0.6233,
    "style_score": 0.6363,
    "phrase_score": 0.4,
    "combined_score": 0.5832
  },
  {
    "i": 7,
    "status": 200,
    "content_id": "35b912f5e06e",
    "guess": "human",
    "model_score": 0.4254,
    "style_score": 0.09,
    "phrase_score": 0.4,
    "combined_score": 0.3029
  },
  {
    "i": 8,
    "status": 200,
    "content_id": "4031b7e35860",
    "guess": "unsure",
    "model_score": 0.6779,
    "style_score": 0.4451,
    "phrase_score": 0.4,
    "combined_score": 0.5408
  },
  {
    "i": 9,
    "status": 200,
    "content_id": "1a8d9f375d25",
    "guess": "unsure",
    "model_score": 0.957,
    "style_score": 0.55,
    "phrase_score": 0.4,
    "combined_score": 0.6016
  },
  {
    "i": 10,
    "status": 200,
    "content_id": "268c520d588b",
    "guess": "unsure",
    "model_score": 0.8081,
    "style_score": 0.4065,
    "phrase_score": 0.6923,
    "combined_score": 0.5722
  },
  {
    "i": 11,
    "status": 200,
    "content_id": "9dbeb4abd073",
    "guess": "unsure",
    "model_score": 0.88,
    "style_score": 0.5,
    "phrase_score": 0.9714,
    "combined_score": 0.6326
  },
  {
    "i": 12,
    "status": 200,
    "content_id": "923c87a4f747",
    "guess": "unsure",
    "model_score": 0.8174,
    "style_score": 0.4605,
    "phrase_score": 1.0,
    "combined_score": 0.6145
  },
  {
    "i": 13,
    "status": 200,
    "content_id": "2f866d858351",
    "guess": "unsure",
    "model_score": 0.6017,
    "style_score": 0.3553,
    "phrase_score": 1.0,
    "combined_score": 0.5476
  },
  {
    "i": 14,
    "status": 200,
    "content_id": "7ca84e709f7f",
    "guess": "unsure",
    "model_score": 0.7445,
    "style_score": 0.56,
    "phrase_score": 0.6899,
    "combined_score": 0.669
  },
  {
    "i": 15,
    "status": 200,
    "content_id": "12f3dc5b1cf1",
    "guess": "unsure",
    "model_score": 0.5214,
    "style_score": 0.3263,
    "phrase_score": 0.4,
    "combined_score": 0.4288
  },
  {
    "i": 16,
    "status": 200,
    "content_id": "12287a7ea987",
    "guess": "unsure",
    "model_score": 0.6522,
    "style_score": 0.4311,
    "phrase_score": 0.4,
    "combined_score": 0.5244
  },
  {
    "i": 17,
    "status": 200,
    "content_id": "99b94fbfabfd",
    "guess": "unsure",
    "model_score": 0.6383,
    "style_score": 0.4929,
    "phrase_score": 0.4,
    "combined_score": 0.5398
  },
  {
    "i": 18,
    "status": 200,
    "content_id": "3a7a40aea6a4",
    "guess": "unsure",
    "model_score": 0.8284,
    "style_score": 0.4314,
    "phrase_score": 0.4,
    "combined_score": 0.5519
  },
  {
    "i": 19,
    "status": 200,
    "content_id": "857f9ddfecff",
    "guess": "unsure",
    "model_score": 0.5918,
    "style_score": 0.3586,
    "phrase_score": 0.4,
    "combined_score": 0.4718
  }
]
```
