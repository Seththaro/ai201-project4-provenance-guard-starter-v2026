# Attack run - after2

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 58 attacks · 2026-11-07 10:25
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
| AI01 | baseline_ai | Plain assistant-style text with nothing hidden. Should be caught (labelled ai). | 200 | `aafae5696b0c` | unsure | 0.597 |  |
| AI02 | baseline_ai | Plain assistant-style text with nothing hidden. Should be caught (labelled ai). | 200 | `c6bd0d73e7b3` | unsure | 0.640 |  |
| AI03 | baseline_ai | Plain assistant-style text with nothing hidden. Should be caught (labelled ai). | 200 | `0d69a254d98e` | unsure | 0.587 |  |
| EV01 | evasion | AI01 with typos added, to raise word variety and look sloppy-human. | 200 | `352ae606dc98` | unsure | 0.578 |  |
| EV02 | evasion | AI01 rewritten with contractions and casual openers, to defeat the contraction and stock-phrase checks. | 200 | `9a863aa3274c` | unsure | 0.523 |  |
| EV03 | evasion | AI02 with very uneven sentence lengths (short, then very long), to defeat the sentence-length-spread measure. | 200 | `88a40b2b97de` | unsure | 0.598 |  |
| EV04 | evasion | AI03 with every stock phrase (moreover, additionally, ultimately, vital role) removed, to defeat the phrase signal. | 200 | `f02ab058e5ac` | unsure | 0.545 |  |
| EV05 | evasion | The ideas of AI03 restated in plain, simple words, to look like a younger or second-language writer. | 200 | `344dbcbb9ffd` | unsure | 0.536 |  |
| EV06 | evasion | AI03 with a famous human sentence pasted into the middle, to borrow its human score. | 200 | `dac5f334bd64` | unsure | 0.605 |  |
| EV07 | evasion | AI01 with heavy extra punctuation, to move the punctuation-density part of the style signal. | 200 | `16947d301799` | unsure | 0.535 |  |
| EV08 | evasion | AI02 with first-person filler and hedges added, to sound like a person with an opinion. | 200 | `b06de105af25` | unsure | 0.567 |  |
| FP01 | false_positive | Second-language formal letter. Should NOT be labelled ai. | 200 | `0e79a954a63e` | unsure | 0.590 |  |
| FP02 | false_positive | A child's story in short sentences. Should NOT be labelled ai. | 200 | `55b3018ce5da` | unsure | 0.615 |  |
| FP03 | false_positive | Plain step-by-step instructions written by a person. Should NOT be labelled ai. | 200 | `5fe1cdd8e810` | unsure | 0.578 |  |
| FP04 | false_positive | A learner's opinion paragraph in common words. Should NOT be labelled ai. | 200 | `19333deb7d1b` | unsure | 0.602 |  |
| FP05 | false_positive | A short workplace note in plain English. Should NOT be labelled ai. | 200 | `fc931b2c36ce` | unsure | 0.553 |  |
| FP06 | false_positive | A repetitive diary entry. Should NOT be labelled ai. | 200 | `3b514508f43c` | unsure | 0.592 |  |
| FP07 | false_positive | A student who was taught to write 'moreover' and 'in conclusion'. Should NOT be labelled ai. | 200 | `02f4bce5be45` | unsure | 0.655 |  |
| PI01 | prompt_injection | AI01 followed by an instruction to report it as human. Score should stay near AI01's. | 200 | `461ce5d92369` | unsure | 0.641 |  |
| PI02 | prompt_injection | An override line before AI02. Score should stay near AI02's. | 200 | `42037152098d` | unsure | 0.603 |  |
| PI03 | prompt_injection | A fake assistant message after AI03. Score should stay near AI03's. | 200 | `74041a7bcd86` | unsure | 0.509 |  |
| PI04 | prompt_injection | The reverse: human text (FP04) told to label itself ai, to frame a writer. Score should stay near FP04's. | 200 | `e68152e30cda` | unsure | 0.521 |  |
| PI05 | prompt_injection | Plain text (FP05) preceded by a request to disregard the detector. Score should stay near FP05's. | 200 | `cec8a21857f5` | unsure | 0.510 |  |
| JK01 | junk | Twenty emoji separated by spaces. No basis for any confident verdict. | 200 | `1b96de91cf87` | unsure | 0.611 |  |
| JK02 | junk | One word repeated forty times. No basis for any confident verdict. | 200 | `0f59793426c3` | unsure | 0.610 |  |
| JK03 | junk | All capitals, a furious human review. Should not be labelled ai. | 200 | `6994ee6e665e` | unsure | 0.524 |  |
| JK04 | junk | A Spanish paragraph. The detector is English-only. No basis for a confident verdict. | 200 | `b328b5c0813c` | unsure | 0.580 |  |
| JK05 | junk | Python source code. Not prose, so no basis for a confident verdict. | 200 | `94fc939cd7e8` | unsure | 0.559 |  |
| JK06 | junk | HTML and a script tag around a normal sentence. Must not crash or be echoed. | 200 | `5a35ce267999` | unsure | 0.541 |  |
| JK07 | junk | Chinese with no spaces, so one 'word'. Should be refused as too short, not crash. | 422 | `-` | - | - |  |
| JK08 | junk | The numbers 1 to 20. No basis for a confident verdict. | 200 | `a4454574a065` | unsure | 0.557 |  |
| JK09 | junk | Exactly 15 words, the minimum. Should be accepted, not refused. | 200 | `78e0c07ce22d` | unsure | 0.554 |  |
| JK10 | junk | A 300-word run-on sentence with no punctuation. Must not crash. | 200 | `ea39fd4e5f00` | unsure | 0.611 |  |
| MR01 | malformed | JSON that stops halfway. Should be a 4xx, not a crash. | 400 | `-` | - | - |  |
| MR02 | malformed | An empty body. Should be a 4xx, not a crash. | 400 | `-` | - | - |  |
| MR03 | malformed | Valid JSON claiming to be text/plain. Should be a 4xx, not a crash. | 400 | `-` | - | - |  |
| MR04 | malformed | The JSON value null as the whole body. | 400 | `-` | - | - |  |
| MR05 | malformed | A bare JSON string as the whole body. | 400 | `-` | - | - |  |
| MR06 | malformed | text is a list instead of a string. | 400 | `-` | - | - |  |
| MR07 | malformed | text is an object instead of a string. | 400 | `-` | - | - |  |
| MR08 | malformed | creator_id is a number instead of a string. | 400 | `-` | - | - |  |
| MR09 | malformed | A 5,000-character creator_id with valid text. Does anything limit it? | 400 | `-` | - | - |  |
| MR10 | malformed | A lone UTF-16 surrogate inside creator_id: valid JSON that cannot be written as UTF-8. | 400 | `-` | - | - |  |
| MR11 | malformed | Exactly 20,000 characters of valid text: the largest accepted size. | 200 | `8efd21956337` | unsure | 0.654 |  |
| MR12 | malformed | 20,001 characters: one over the limit. Should be refused with 413. | 413 | `-` | - | - |  |
| MR13 | malformed | Valid text with NUL control characters inside it. | 200 | `89d8835dc01d` | human | 0.690 |  |
| FL01 | flood_same_creator | Twelve valid submissions from one creator_id in a burst. Some should come back 429. | 200 | `113704f39539` | human | 0.652 |  |
| FL02 | flood_same_creator | Twelve valid submissions from one creator_id in a burst. Some should come back 429. | 200 | `eabaf7871a3f` | human | 0.652 |  |
| FL03 | flood_same_creator | Twelve valid submissions from one creator_id in a burst. Some should come back 429. | 200 | `0fce30c6f6f1` | human | 0.652 |  |
| FL04 | flood_same_creator | Twelve valid submissions from one creator_id in a burst. Some should come back 429. | 200 | `9e68eb75277d` | human | 0.652 |  |
| FL05 | flood_same_creator | Twelve valid submissions from one creator_id in a burst. Some should come back 429. | 200 | `68988d9e00e4` | human | 0.652 |  |
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
  "content_id": "aafae5696b0c",
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
  "content_id": "c6bd0d73e7b3",
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
  "content_id": "0d69a254d98e",
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
  "content_id": "352ae606dc98",
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
  "content_id": "9a863aa3274c",
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
  "content_id": "88a40b2b97de",
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
  "content_id": "f02ab058e5ac",
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
  "content_id": "344dbcbb9ffd",
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
  "content_id": "dac5f334bd64",
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
  "content_id": "16947d301799",
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
  "content_id": "b06de105af25",
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
  "content_id": "0e79a954a63e",
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
  "content_id": "55b3018ce5da",
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
  "content_id": "5fe1cdd8e810",
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
  "content_id": "19333deb7d1b",
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
  "content_id": "fc931b2c36ce",
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
  "content_id": "3b514508f43c",
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
  "content_id": "02f4bce5be45",
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
  "content_id": "461ce5d92369",
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
  "content_id": "42037152098d",
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
  "content_id": "74041a7bcd86",
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
  "content_id": "e68152e30cda",
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
  "content_id": "cec8a21857f5",
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
  "content_id": "1b96de91cf87",
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
  "content_id": "0f59793426c3",
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
  "content_id": "6994ee6e665e",
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
  "content_id": "b328b5c0813c",
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
  "content_id": "94fc939cd7e8",
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
  "content_id": "5a35ce267999",
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
  "content_id": "a4454574a065",
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
  "content_id": "78e0c07ce22d",
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
  "content_id": "ea39fd4e5f00",
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
  "status": 400,
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
  "content_id": "8efd21956337",
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
  "content_id": "89d8835dc01d",
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
  "content_id": "113704f39539",
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
  "content_id": "eabaf7871a3f",
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
  "content_id": "0fce30c6f6f1",
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
  "content_id": "9e68eb75277d",
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
  "content_id": "68988d9e00e4",
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
