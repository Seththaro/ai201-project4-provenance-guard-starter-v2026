# Attack run - after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 58 attacks · 2026-11-07 10:22
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **58**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds - read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table - either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| AI01 | baseline_ai | Plain assistant-style text with nothing hidden. Should be caught (labelled ai). | 200 | `b922ee44432b` | unsure | 0.597 |  |
| AI02 | baseline_ai | Plain assistant-style text with nothing hidden. Should be caught (labelled ai). | 200 | `6fbf08d8485f` | unsure | 0.640 |  |
| AI03 | baseline_ai | Plain assistant-style text with nothing hidden. Should be caught (labelled ai). | 200 | `2161e8650bf2` | unsure | 0.587 |  |
| EV01 | evasion | AI01 with typos added, to raise word variety and look sloppy-human. | 200 | `70654350c080` | unsure | 0.578 |  |
| EV02 | evasion | AI01 rewritten with contractions and casual openers, to defeat the contraction and stock-phrase checks. | 200 | `ca0430da727c` | unsure | 0.523 |  |
| EV03 | evasion | AI02 with very uneven sentence lengths (short, then very long), to defeat the sentence-length-spread measure. | 200 | `1d2f50c23696` | unsure | 0.598 |  |
| EV04 | evasion | AI03 with every stock phrase (moreover, additionally, ultimately, vital role) removed, to defeat the phrase signal. | 200 | `894d8794ce78` | unsure | 0.545 |  |
| EV05 | evasion | The ideas of AI03 restated in plain, simple words, to look like a younger or second-language writer. | 200 | `b6aa19f294d2` | unsure | 0.536 |  |
| EV06 | evasion | AI03 with a famous human sentence pasted into the middle, to borrow its human score. | 200 | `cfd939dfc945` | unsure | 0.605 |  |
| EV07 | evasion | AI01 with heavy extra punctuation, to move the punctuation-density part of the style signal. | 200 | `5718439ad7b7` | unsure | 0.535 |  |
| EV08 | evasion | AI02 with first-person filler and hedges added, to sound like a person with an opinion. | 200 | `6f9089e49373` | unsure | 0.567 |  |
| FP01 | false_positive | Second-language formal letter. Should NOT be labelled ai. | 200 | `1806d2785a45` | unsure | 0.590 |  |
| FP02 | false_positive | A child's story in short sentences. Should NOT be labelled ai. | 200 | `6e986e8cb7ad` | unsure | 0.615 |  |
| FP03 | false_positive | Plain step-by-step instructions written by a person. Should NOT be labelled ai. | 200 | `07075a6a453f` | unsure | 0.578 |  |
| FP04 | false_positive | A learner's opinion paragraph in common words. Should NOT be labelled ai. | 200 | `07106ba7215c` | unsure | 0.602 |  |
| FP05 | false_positive | A short workplace note in plain English. Should NOT be labelled ai. | 200 | `8dd88bac3d85` | unsure | 0.553 |  |
| FP06 | false_positive | A repetitive diary entry. Should NOT be labelled ai. | 200 | `113aff9495cc` | unsure | 0.592 |  |
| FP07 | false_positive | A student who was taught to write 'moreover' and 'in conclusion'. Should NOT be labelled ai. | 200 | `f160db3145b9` | unsure | 0.655 |  |
| PI01 | prompt_injection | AI01 followed by an instruction to report it as human. Score should stay near AI01's. | 200 | `76e6edb0e684` | unsure | 0.641 |  |
| PI02 | prompt_injection | An override line before AI02. Score should stay near AI02's. | 200 | `ade64ae6d7dd` | unsure | 0.603 |  |
| PI03 | prompt_injection | A fake assistant message after AI03. Score should stay near AI03's. | 200 | `14a1665407f6` | unsure | 0.509 |  |
| PI04 | prompt_injection | The reverse: human text (FP04) told to label itself ai, to frame a writer. Score should stay near FP04's. | 200 | `b56d5c7711c5` | unsure | 0.521 |  |
| PI05 | prompt_injection | Plain text (FP05) preceded by a request to disregard the detector. Score should stay near FP05's. | 200 | `58262b6a2925` | unsure | 0.510 |  |
| JK01 | junk | Twenty emoji separated by spaces. No basis for any confident verdict. | 200 | `7e8686c68540` | unsure | 0.611 |  |
| JK02 | junk | One word repeated forty times. No basis for any confident verdict. | 200 | `14ba97cfac6c` | unsure | 0.610 |  |
| JK03 | junk | All capitals, a furious human review. Should not be labelled ai. | 200 | `eaf4d78df902` | unsure | 0.524 |  |
| JK04 | junk | A Spanish paragraph. The detector is English-only. No basis for a confident verdict. | 200 | `69fecbb257c1` | unsure | 0.580 |  |
| JK05 | junk | Python source code. Not prose, so no basis for a confident verdict. | 200 | `34862511cdef` | unsure | 0.559 |  |
| JK06 | junk | HTML and a script tag around a normal sentence. Must not crash or be echoed. | 200 | `9db21d0d05c0` | unsure | 0.541 |  |
| JK07 | junk | Chinese with no spaces, so one 'word'. Should be refused as too short, not crash. | 422 | `-` | - | - |  |
| JK08 | junk | The numbers 1 to 20. No basis for a confident verdict. | 200 | `54fcf9aee254` | unsure | 0.557 |  |
| JK09 | junk | Exactly 15 words, the minimum. Should be accepted, not refused. | 200 | `08c4c232d64a` | unsure | 0.554 |  |
| JK10 | junk | A 300-word run-on sentence with no punctuation. Must not crash. | 200 | `3b3e9dd2ce21` | unsure | 0.611 |  |
| MR01 | malformed | JSON that stops halfway. Should be a 4xx, not a crash. | 400 | `-` | - | - |  |
| MR02 | malformed | An empty body. Should be a 4xx, not a crash. | 400 | `-` | - | - |  |
| MR03 | malformed | Valid JSON claiming to be text/plain. Should be a 4xx, not a crash. | 400 | `-` | - | - |  |
| MR04 | malformed | The JSON value null as the whole body. | 400 | `-` | - | - |  |
| MR05 | malformed | A bare JSON string as the whole body. | 400 | `-` | - | - |  |
| MR06 | malformed | text is a list instead of a string. | 400 | `-` | - | - |  |
| MR07 | malformed | text is an object instead of a string. | 400 | `-` | - | - |  |
| MR08 | malformed | creator_id is a number instead of a string. | 429 | `-` | - | - |  |
| MR09 | malformed | A 5,000-character creator_id with valid text. Does anything limit it? | 400 | `-` | - | - |  |
| MR10 | malformed | A lone UTF-16 surrogate inside creator_id: valid JSON that cannot be written as UTF-8. | 400 | `-` | - | - |  |
| MR11 | malformed | Exactly 20,000 characters of valid text: the largest accepted size. | 200 | `b61c4219292d` | unsure | 0.654 |  |
| MR12 | malformed | 20,001 characters: one over the limit. Should be refused with 413. | 413 | `-` | - | - |  |
| MR13 | malformed | Valid text with NUL control characters inside it. | 200 | `c7a05c29ca3c` | human | 0.690 |  |
| FL01 | flood_same_creator | Twelve valid submissions from one creator_id in a burst. Some should come back 429. | 200 | `b2d02fe7882b` | human | 0.652 |  |
| FL02 | flood_same_creator | Twelve valid submissions from one creator_id in a burst. Some should come back 429. | 200 | `d43f1fd9be09` | human | 0.652 |  |
| FL03 | flood_same_creator | Twelve valid submissions from one creator_id in a burst. Some should come back 429. | 200 | `e6eca86db47a` | human | 0.652 |  |
| FL04 | flood_same_creator | Twelve valid submissions from one creator_id in a burst. Some should come back 429. | 200 | `0984c8cd1aaf` | human | 0.652 |  |
| FL05 | flood_same_creator | Twelve valid submissions from one creator_id in a burst. Some should come back 429. | 200 | `cf772d8d0b38` | human | 0.652 |  |
| FL06 | flood_same_creator | Twelve valid submissions from one creator_id in a burst. Some should come back 429. | 429 | `-` | - | - |  |
| FL07 | flood_same_creator | Twelve valid submissions from one creator_id in a burst. Some should come back 429. | 429 | `-` | - | - |  |
| FL08 | flood_same_creator | Twelve valid submissions from one creator_id in a burst. Some should come back 429. | 429 | `-` | - | - |  |
| FL09 | flood_same_creator | Twelve valid submissions from one creator_id in a burst. Some should come back 429. | 429 | `-` | - | - |  |
| FL10 | flood_same_creator | Twelve valid submissions from one creator_id in a burst. Some should come back 429. | 429 | `-` | - | - |  |
| FL11 | flood_same_creator | Twelve valid submissions from one creator_id in a burst. Some should come back 429. | 429 | `-` | - | - |  |
| FL12 | flood_same_creator | Twelve valid submissions from one creator_id in a burst. Some should come back 429. | 429 | `-` | - | - |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `baseline_ai` | 3 | 0 | 3 |
| `evasion` | 8 | 0 | 8 |
| `false_positive` | 7 | 0 | 7 |
| `flood_same_creator` | 12 | 0 | 12 |
| `junk` | 10 | 0 | 10 |
| `malformed` | 13 | 0 | 13 |
| `prompt_injection` | 5 | 0 | 5 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README - the ones that show something, not the ten easiest.

### AI01 - `baseline_ai`

*Targeting:* Plain assistant-style text with nothing hidden. Should be caught (labelled ai).

```json
{
  "id": "AI01",
  "status": 200,
  "content_id": "b922ee44432b",
  "creator_id": "attacker_AI01",
  "guess": "unsure",
  "confidence": 0.5974,
  "model_score": 0.9005,
  "style_score": 0.4051,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### AI02 - `baseline_ai`

*Targeting:* Plain assistant-style text with nothing hidden. Should be caught (labelled ai).

```json
{
  "id": "AI02",
  "status": 200,
  "content_id": "6fbf08d8485f",
  "creator_id": "attacker_AI02",
  "guess": "unsure",
  "confidence": 0.6398,
  "model_score": 0.829,
  "style_score": 0.59,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### AI03 - `baseline_ai`

*Targeting:* Plain assistant-style text with nothing hidden. Should be caught (labelled ai).

```json
{
  "id": "AI03",
  "status": 200,
  "content_id": "2161e8650bf2",
  "creator_id": "attacker_AI03",
  "guess": "unsure",
  "confidence": 0.5873,
  "model_score": 0.8406,
  "style_score": 0.4278,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### EV01 - `evasion`

*Targeting:* AI01 with typos added, to raise word variety and look sloppy-human.

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "70654350c080",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.5777,
  "model_score": 0.1223,
  "style_score": 0.4051,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### EV02 - `evasion`

*Targeting:* AI01 rewritten with contractions and casual openers, to defeat the contraction and stock-phrase checks.

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "ca0430da727c",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5227,
  "model_score": 0.7344,
  "style_score": 0.3547,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### EV03 - `evasion`

*Targeting:* AI02 with very uneven sentence lengths (short, then very long), to defeat the sentence-length-spread measure.

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "1d2f50c23696",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5978,
  "model_score": 0.4638,
  "style_score": 0.045,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### EV04 - `evasion`

*Targeting:* AI03 with every stock phrase (moreover, additionally, ultimately, vital role) removed, to defeat the phrase signal.

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "894d8794ce78",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5451,
  "model_score": 0.4794,
  "style_score": 0.4547,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### EV05 - `evasion`

*Targeting:* The ideas of AI03 restated in plain, simple words, to look like a younger or second-language writer.

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "b6aa19f294d2",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.5364,
  "model_score": 0.7755,
  "style_score": 0.4108,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### EV06 - `evasion`

*Targeting:* AI03 with a famous human sentence pasted into the middle, to borrow its human score.

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "cfd939dfc945",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.6053,
  "model_score": 0.8878,
  "style_score": 0.6601,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### EV07 - `evasion`

*Targeting:* AI01 with heavy extra punctuation, to move the punctuation-density part of the style signal.

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "5718439ad7b7",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5355,
  "model_score": 0.5006,
  "style_score": 0.455,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### EV08 - `evasion`

*Targeting:* AI02 with first-person filler and hedges added, to sound like a person with an opinion.

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "6f9089e49373",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.5668,
  "model_score": 0.4938,
  "style_score": 0.4074,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### FP01 - `false_positive`

*Targeting:* Second-language formal letter. Should NOT be labelled ai.

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "1806d2785a45",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5902,
  "model_score": 0.805,
  "style_score": 0.6805,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### FP02 - `false_positive`

*Targeting:* A child's story in short sentences. Should NOT be labelled ai.

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "6e986e8cb7ad",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6152,
  "model_score": 0.8405,
  "style_score": 0.7778,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### FP03 - `false_positive`

*Targeting:* Plain step-by-step instructions written by a person. Should NOT be labelled ai.

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "07075a6a453f",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.5782,
  "model_score": 0.875,
  "style_score": 0.5219,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### FP04 - `false_positive`

*Targeting:* A learner's opinion paragraph in common words. Should NOT be labelled ai.

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "07106ba7215c",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.602,
  "model_score": 0.8343,
  "style_score": 0.71,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### FP05 - `false_positive`

*Targeting:* A short workplace note in plain English. Should NOT be labelled ai.

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "8dd88bac3d85",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.5527,
  "model_score": 0.6482,
  "style_score": 0.5173,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### FP06 - `false_positive`

*Targeting:* A repetitive diary entry. Should NOT be labelled ai.

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "113aff9495cc",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.5924,
  "model_score": 0.8334,
  "style_score": 0.6565,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### FP07 - `false_positive`

*Targeting:* A student who was taught to write 'moreover' and 'in conclusion'. Should NOT be labelled ai.

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "f160db3145b9",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.6552,
  "model_score": 0.8743,
  "style_score": 0.62,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### PI01 - `prompt_injection`

*Targeting:* AI01 followed by an instruction to report it as human. Score should stay near AI01's.

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "76e6edb0e684",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.6413,
  "model_score": 0.7855,
  "style_score": 0.4435,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### PI02 - `prompt_injection`

*Targeting:* An override line before AI02. Score should stay near AI02's.

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "ade64ae6d7dd",
  "creator_id": "attacker_PI02",
  "guess": "unsure",
  "confidence": 0.6027,
  "model_score": 0.6564,
  "style_score": 0.6,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### PI03 - `prompt_injection`

*Targeting:* A fake assistant message after AI03. Score should stay near AI03's.

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "14a1665407f6",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5088,
  "model_score": 0.6017,
  "style_score": 0.2196,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### PI04 - `prompt_injection`

*Targeting:* The reverse: human text (FP04) told to label itself ai, to frame a writer. Score should stay near FP04's.

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "b56d5c7711c5",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5213,
  "model_score": 0.5386,
  "style_score": 0.4467,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### PI05 - `prompt_injection`

*Targeting:* Plain text (FP05) preceded by a request to disregard the detector. Score should stay near FP05's.

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "58262b6a2925",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5102,
  "model_score": 0.5244,
  "style_score": 0.4967,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### JK01 - `junk`

*Targeting:* Twenty emoji separated by spaces. No basis for any confident verdict.

```json
{
  "id": "JK01",
  "status": 200,
  "content_id": "7e8686c68540",
  "creator_id": "attacker_JK01",
  "guess": "unsure",
  "confidence": 0.6106,
  "model_score": 0.9914,
  "style_score": 0.5,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### JK02 - `junk`

*Targeting:* One word repeated forty times. No basis for any confident verdict.

```json
{
  "id": "JK02",
  "status": 200,
  "content_id": "14ba97cfac6c",
  "creator_id": "attacker_JK02",
  "guess": "unsure",
  "confidence": 0.6097,
  "model_score": 0.993,
  "style_score": 0.55,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### JK03 - `junk`

*Targeting:* All capitals, a furious human review. Should not be labelled ai.

```json
{
  "id": "JK03",
  "status": 200,
  "content_id": "eaf4d78df902",
  "creator_id": "attacker_JK03",
  "guess": "unsure",
  "confidence": 0.5237,
  "model_score": 0.829,
  "style_score": 0.2693,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### JK04 - `junk`

*Targeting:* A Spanish paragraph. The detector is English-only. No basis for a confident verdict.

```json
{
  "id": "JK04",
  "status": 200,
  "content_id": "69fecbb257c1",
  "creator_id": "attacker_JK04",
  "guess": "unsure",
  "confidence": 0.5801,
  "model_score": 0.1419,
  "style_score": 0.5598,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### JK05 - `junk`

*Targeting:* Python source code. Not prose, so no basis for a confident verdict.

```json
{
  "id": "JK05",
  "status": 200,
  "content_id": "34862511cdef",
  "creator_id": "attacker_JK05",
  "guess": "unsure",
  "confidence": 0.5595,
  "model_score": 0.7745,
  "style_score": 0.5444,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### JK06 - `junk`

*Targeting:* HTML and a script tag around a normal sentence. Must not crash or be echoed.

```json
{
  "id": "JK06",
  "status": 200,
  "content_id": "9db21d0d05c0",
  "creator_id": "attacker_JK06",
  "guess": "unsure",
  "confidence": 0.5415,
  "model_score": 0.8065,
  "style_score": 0.4,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### JK07 - `junk`

*Targeting:* Chinese with no spaces, so one 'word'. Should be refused as too short, not crash.

```json
{
  "id": "JK07",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_JK07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### JK08 - `junk`

*Targeting:* The numbers 1 to 20. No basis for a confident verdict.

```json
{
  "id": "JK08",
  "status": 200,
  "content_id": "54fcf9aee254",
  "creator_id": "attacker_JK08",
  "guess": "unsure",
  "confidence": 0.5575,
  "model_score": 0.9943,
  "style_score": 0.25,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### JK09 - `junk`

*Targeting:* Exactly 15 words, the minimum. Should be accepted, not refused.

```json
{
  "id": "JK09",
  "status": 200,
  "content_id": "08c4c232d64a",
  "creator_id": "attacker_JK09",
  "guess": "unsure",
  "confidence": 0.5543,
  "model_score": 0.9801,
  "style_score": 0.25,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### JK10 - `junk`

*Targeting:* A 300-word run-on sentence with no punctuation. Must not crash.

```json
{
  "id": "JK10",
  "status": 200,
  "content_id": "3b3e9dd2ce21",
  "creator_id": "attacker_JK10",
  "guess": "unsure",
  "confidence": 0.6106,
  "model_score": 0.9969,
  "style_score": 0.55,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### MR01 - `malformed`

*Targeting:* JSON that stops halfway. Should be a 4xx, not a crash.

```json
{
  "id": "MR01",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR02 - `malformed`

*Targeting:* An empty body. Should be a 4xx, not a crash.

```json
{
  "id": "MR02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR03 - `malformed`

*Targeting:* Valid JSON claiming to be text/plain. Should be a 4xx, not a crash.

```json
{
  "id": "MR03",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR04 - `malformed`

*Targeting:* The JSON value null as the whole body.

```json
{
  "id": "MR04",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR05 - `malformed`

*Targeting:* A bare JSON string as the whole body.

```json
{
  "id": "MR05",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR06 - `malformed`

*Targeting:* text is a list instead of a string.

```json
{
  "id": "MR06",
  "status": 400,
  "content_id": null,
  "creator_id": "mr06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR07 - `malformed`

*Targeting:* text is an object instead of a string.

```json
{
  "id": "MR07",
  "status": 400,
  "content_id": null,
  "creator_id": "mr07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR08 - `malformed`

*Targeting:* creator_id is a number instead of a string.

```json
{
  "id": "MR08",
  "status": 429,
  "content_id": null,
  "creator_id": 12345,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR09 - `malformed`

*Targeting:* A 5,000-character creator_id with valid text. Does anything limit it?

```json
{
  "id": "MR09",
  "status": 400,
  "content_id": null,
  "creator_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR10 - `malformed`

*Targeting:* A lone UTF-16 surrogate inside creator_id: valid JSON that cannot be written as UTF-8.

```json
{
  "id": "MR10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR11 - `malformed`

*Targeting:* Exactly 20,000 characters of valid text: the largest accepted size.

```json
{
  "id": "MR11",
  "status": 200,
  "content_id": "b61c4219292d",
  "creator_id": "mr11",
  "guess": "unsure",
  "confidence": 0.654,
  "model_score": 0.9956,
  "style_score": 0.8,
  "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.",
  "error": null,
  "verdict": ""
}
```

### MR12 - `malformed`

*Targeting:* 20,001 characters: one over the limit. Should be refused with 413.

```json
{
  "id": "MR12",
  "status": 413,
  "content_id": null,
  "creator_id": "mr12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MR13 - `malformed`

*Targeting:* Valid text with NUL control characters inside it.

```json
{
  "id": "MR13",
  "status": 200,
  "content_id": "c7a05c29ca3c",
  "creator_id": "mr13",
  "guess": "human",
  "confidence": 0.6903,
  "model_score": 0.0745,
  "style_score": 0.0167,
  "label": "We think this was probably written by a person. Our checks found nothing that points to an AI tool.",
  "error": null,
  "verdict": ""
}
```

### FL01 - `flood_same_creator`

*Targeting:* Twelve valid submissions from one creator_id in a burst. Some should come back 429.

```json
{
  "id": "FL01",
  "status": 200,
  "content_id": "b2d02fe7882b",
  "creator_id": "flood_attacker",
  "guess": "human",
  "confidence": 0.6517,
  "model_score": 0.3811,
  "style_score": 0.2765,
  "label": "We think this was probably written by a person. Our checks found nothing that points to an AI tool.",
  "error": null,
  "verdict": ""
}
```

### FL02 - `flood_same_creator`

*Targeting:* Twelve valid submissions from one creator_id in a burst. Some should come back 429.

```json
{
  "id": "FL02",
  "status": 200,
  "content_id": "d43f1fd9be09",
  "creator_id": "flood_attacker",
  "guess": "human",
  "confidence": 0.6517,
  "model_score": 0.3811,
  "style_score": 0.2765,
  "label": "We think this was probably written by a person. Our checks found nothing that points to an AI tool.",
  "error": null,
  "verdict": ""
}
```

### FL03 - `flood_same_creator`

*Targeting:* Twelve valid submissions from one creator_id in a burst. Some should come back 429.

```json
{
  "id": "FL03",
  "status": 200,
  "content_id": "e6eca86db47a",
  "creator_id": "flood_attacker",
  "guess": "human",
  "confidence": 0.6517,
  "model_score": 0.3811,
  "style_score": 0.2765,
  "label": "We think this was probably written by a person. Our checks found nothing that points to an AI tool.",
  "error": null,
  "verdict": ""
}
```

### FL04 - `flood_same_creator`

*Targeting:* Twelve valid submissions from one creator_id in a burst. Some should come back 429.

```json
{
  "id": "FL04",
  "status": 200,
  "content_id": "0984c8cd1aaf",
  "creator_id": "flood_attacker",
  "guess": "human",
  "confidence": 0.6517,
  "model_score": 0.3811,
  "style_score": 0.2765,
  "label": "We think this was probably written by a person. Our checks found nothing that points to an AI tool.",
  "error": null,
  "verdict": ""
}
```

### FL05 - `flood_same_creator`

*Targeting:* Twelve valid submissions from one creator_id in a burst. Some should come back 429.

```json
{
  "id": "FL05",
  "status": 200,
  "content_id": "cf772d8d0b38",
  "creator_id": "flood_attacker",
  "guess": "human",
  "confidence": 0.6517,
  "model_score": 0.3811,
  "style_score": 0.2765,
  "label": "We think this was probably written by a person. Our checks found nothing that points to an AI tool.",
  "error": null,
  "verdict": ""
}
```

### FL06 - `flood_same_creator`

*Targeting:* Twelve valid submissions from one creator_id in a burst. Some should come back 429.

```json
{
  "id": "FL06",
  "status": 429,
  "content_id": null,
  "creator_id": "flood_attacker",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL07 - `flood_same_creator`

*Targeting:* Twelve valid submissions from one creator_id in a burst. Some should come back 429.

```json
{
  "id": "FL07",
  "status": 429,
  "content_id": null,
  "creator_id": "flood_attacker",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL08 - `flood_same_creator`

*Targeting:* Twelve valid submissions from one creator_id in a burst. Some should come back 429.

```json
{
  "id": "FL08",
  "status": 429,
  "content_id": null,
  "creator_id": "flood_attacker",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL09 - `flood_same_creator`

*Targeting:* Twelve valid submissions from one creator_id in a burst. Some should come back 429.

```json
{
  "id": "FL09",
  "status": 429,
  "content_id": null,
  "creator_id": "flood_attacker",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL10 - `flood_same_creator`

*Targeting:* Twelve valid submissions from one creator_id in a burst. Some should come back 429.

```json
{
  "id": "FL10",
  "status": 429,
  "content_id": null,
  "creator_id": "flood_attacker",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL11 - `flood_same_creator`

*Targeting:* Twelve valid submissions from one creator_id in a burst. Some should come back 429.

```json
{
  "id": "FL11",
  "status": 429,
  "content_id": null,
  "creator_id": "flood_attacker",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL12 - `flood_same_creator`

*Targeting:* Twelve valid submissions from one creator_id in a burst. Some should come back 429.

```json
{
  "id": "FL12",
  "status": 429,
  "content_id": null,
  "creator_id": "flood_attacker",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
