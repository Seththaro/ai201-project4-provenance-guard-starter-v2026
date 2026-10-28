# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 - THE BUILD ═══════════════════════ -->

## Stretch features I'm adding

Declared here, in the README, as the brief asks. All three are in the repo.

1. **A third signal** - `phrases.py::phrase_signal` (stock phrases and contractions). Weighting note is under *The combining rule*.
2. **`GET /content/<id>`** - returns one item's current status. Request and response are under *Sample Run*.
3. **A verified-human path** - `POST /verify`. Described and shown under *Sample Run*.

---

## What This Does

Provenance Guard is a small Flask service a writing site could plug into. Text comes in; a guess, a confidence number, a plain-English label, and an appeal route go back out.

The path one submission takes:

1. **`POST /submit` arrives** with `{"text", "creator_id"}` (`app.py::submit`). It adds nothing yet.
2. **Input check** (`app.py::_check_text`). Missing, empty, non-string or under-15-word text is refused with 400/422, over 20,000 characters with 413, and a missing `creator_id` with 400. Each refusal is logged as a `rejected` entry, so bad input never reaches a signal.
3. **Signal one** (`detector.py::model_signal`) adds `model_score`: how predictable a local gpt2 finds the text.
4. **Signal two** (`stylometry.py::style_signal`) adds `style_score`: the shape of the text (sentence-length spread, word variety, punctuation).
5. **Signal three** (`phrases.py::phrase_signal`, stretch) adds `phrase_score`: stock phrases and contractions.
6. **Combine** (`scoring.py::combine_signals`) turns the three scores into one `combined_score` from 0 (human) to 1 (AI). `scoring.confidence_of` turns that into a `confidence` of 0.5–1.0.
7. **Label** (`scoring.py::score_to_label`) maps the score to `human`, `unsure` or `ai` and the sentence a reader sees. A writer with a verified-human credential gets a note on the label, and an `ai` result is downgraded to `unsure`.
8. **Log, then answer.** `audit.log_decision` writes one JSON line to `logs/audit.jsonl` with all three signal scores, then the response goes back with a `content_id`.

If the writer disagrees, `POST /appeal` takes the `content_id` and their reasoning, checks the id exists, appends an `appeal` entry beside the original decision, and sets the status to `under_review`.

**The false positive I designed around.** A student writing plainly submits their own homework. Signal one sees common words in short sentences and scores it as machine-like (0.91 in my test), and signal two agrees (0.70). That writer's combined score was 0.62. Because the AI threshold is 0.70 rather than 0.65, they get the *unsure* label, which says no conclusion has been drawn and nothing is needed from them, and not the accusation. If they ever do get the AI label, it tells them it can be wrong and how to appeal.

**The two endpoints' shapes**

| | In | Out |
|---|---|---|
| `POST /submit` | `text` (string, 15 to 20,000 chars), `creator_id` (non-empty string) | `content_id`, `guess` (`ai`/`human`/`unsure`), `confidence`, `label`, `model_score`, `style_score`, `phrase_score`, `combined_score`, `verified_human`, `status` |
| `POST /appeal` | `content_id` (must exist), `reasoning` (non-empty, at most 2,000 chars) | `content_id`, `status: "under_review"`, `message`. 404 for an unknown id, 400 for missing fields |

---

## Signals and Scoring

### Signal one - the model signal

**What it measures:** Perplexity under gpt2, run locally: how predictable the text is, squashed to 0–1 (`detector.py::model_signal`, midpoint 45, steepness 1.6). I left the midpoint where the starter put it.

**Why that might differ between human and AI writing:** A language model writes by picking likely next words, so its own output tends to be easy for another model to predict. People wander: odd word choices, specific details, abrupt turns.

**What it can't see:** Authorship. It rewards common words in short, ordinary sentences, and plenty of real people write that way: second-language writers, younger writers, anyone writing plainly. My plain-human test paragraph scored 0.91 here, higher than my clearly-AI paragraph (0.74). Ornate human prose can go the other way and look human.

### Signal two - the style signal

**What it measures:** The text as text, with no understanding of it (`stylometry.py::style_signal`). Three parts, each rescaled so higher means more AI-like:

- Sentence-length spread: standard deviation over mean of words per sentence (`sentence_length_spread`). Low spread means AI. Weight 0.50. A single-sentence text has no spread and returns a neutral 0.5.
- Type-token ratio: unique words over total words in moving 50-word windows (`type_token_ratio`), so long texts aren't punished for repeating "the". Low variety means AI. Weight 0.30.
- Punctuation density: mid-sentence marks (commas, semicolons, dashes, brackets, quotes, `!`, `?`) per word (`punctuation_density`). Scored as distance from a "tidy" 0.09, because both very sparse and very busy punctuation read as a person. Weight 0.20.

**Why that might differ between human and AI writing:** Generated prose tends toward even, mid-length sentences and a narrower vocabulary. Human writing is lumpier.

**What it can't see:** Meaning. Anything that changes the shape without changing the substance moves it: typos, broken-up sentences, a pasted quotation. My lightly-edited AI paragraph scored 0.13 here, the most human of anything I tested, only because I wrote it with varied sentence lengths. Of the three parts, the punctuation one is the weakest; the direction I chose is a guess.

### Signal three (stretch) - the phrase signal

**What it measures:** Stock phrases per 100 words ("furthermore", "it is important to note", "delve", ...) at weight 0.6, and the absence of contractions at weight 0.4 (`phrases.py::phrase_signal`).

**Why that might differ between human and AI writing:** Assistants reach for the same connectives, and formal assistant prose avoids contractions.

**What it can't see:** It is a word list. A student taught to write "furthermore" looks like a model; an AI told to be casual doesn't. Deleting a handful of words defeats it. It also does nothing on text without those habits, so it carries the least weight.

### The combining rule

**The rule:** A weighted average of the three signals, then a disagreement rule. If the highest and lowest signal are more than 0.35 apart, the average is pulled halfway back toward 0.5.

**The numbers:** (all in `config.py`)

| Setting | Value |
|---|---|
| `WEIGHT_MODEL_SIGNAL` | 0.45 |
| `WEIGHT_STYLE_SIGNAL` | 0.35 |
| `WEIGHT_PHRASE_SIGNAL` | 0.20 |
| `DISAGREE_GAP` | 0.35 |
| `DISAGREE_SHRINK` | 0.5 (halfway to 0.5) |
| `HUMAN_THRESHOLD` | 0.35 (score at or below is *human*) |
| `AI_THRESHOLD` | 0.70 (score at or above is *ai*) |

Without the phrase signal the other two weights are renormalised, so the rule still works with two signals.

**How the three are weighted (stretch note):** Signal one gets the most (0.45) because it is the only one that reads the text, but not a majority, because it is also the one that wrongly accuses plain writers. Signal two gets 0.35: it measures something different, but it cannot read and is easy to fool. Signal three gets 0.20 because it is narrow and quiet on most text. No signal can accuse on its own: the disagreement rule shrinks a lone confident signal toward *unsure*. The AI threshold (0.70) is further from 0.5 than the human one (0.35 is 0.15 away, 0.70 is 0.20 away) on purpose, because a wrong accusation costs more than a missed detection.

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:** The lightly-edited AI paragraph (varied sentence lengths, still plain AI-flavoured ideas) got model 0.742, style 0.129, phrase 0.144. The gap is 0.61, over 0.35, so the weighted average (0.54) is pulled halfway to 0.5 and it lands at 0.454 (*unsure*). That is the right label: the system truly doesn't know. The cost is that this edited AI text gets through; that is the trade I chose.

**What I measured** (calibration run, before logging to the service; `scoring.combine_signals`, rounded):

| Input | model | style | phrase | combined | guess |
|---|---|---|---|---|---|
| clearly AI | 0.736 | 0.669 | 1.000 | 0.765 | ai |
| clearly human (grandmother's kitchen) | 0.529 | 0.363 | 0.000 | 0.432 | unsure |
| clearly human (Dayton / Ray) | 0.335 | 0.093 | 0.106 | 0.204 | human |
| formal human (constitution) | 0.445 | 0.619 | 0.400 | 0.497 | unsure |
| lightly-edited AI | 0.742 | 0.129 | 0.144 | 0.454 | unsure |
| plain human (store on Saturday) | 0.908 | 0.704 | 0.400 | 0.617 | unsure |

Clearly-AI and clearly-human text land 0.33 to 0.56 apart. No signal discriminates on all of them: signal one cannot separate plain human writing from AI (0.91 vs 0.74), and signal two cannot see the edited AI. That is a finding, not a bug I hid.

---

## Label Variants

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | We think this was probably written by a person. Our checks found nothing that points to an AI tool. |
| unsure | 0.35 – 0.70 | We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you. |
| high-confidence AI | 0.70 – 1.00 | Our checks suggest this may have been written with an AI tool. Automated checks can be wrong, especially for plain or second-language writing. If you wrote it yourself, you can appeal and a person will review it. |

All three are reachable through the service: the Dayton text scored 0.204 (*human*), the clearly-AI text 0.765 (*ai*), and most other things landed in *unsure*. `python scoring.py` prints the ranges straight from `config.py`.

**Why I worded the "unsure" one this way:** The person reading it may have written every word. So it says "we can't tell", blames the checks ("aren't reliable enough") instead of the writer, says no conclusion has been drawn, and ends by saying nothing is needed. It never uses a number or the word "suspect".

---

## Sample Run

**A submission**

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I went to the store on Saturday to buy some food for the week. The store was very busy and there were a lot of people there. I got milk, bread, eggs, and some fruit. Then I went home and made lunch. After lunch I cleaned my room and did my homework. It was a good day and I was happy that I got everything done before the evening.", "creator_id": "sample_writer"}'
```

```json
{"combined_score":0.6174,"confidence":0.6174,"content_id":"5e6a08f497af","guess":"unsure","label":"We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.","model_score":0.9078,"phrase_score":0.4,"status":"decided","style_score":0.7037,"verified_human":false}
```

This is the plain-writing false-positive case from the trace above, a real human paragraph that signal one scored 0.91. It landed in *unsure*, not *ai*.

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "5e6a08f497af", "reasoning": "I wrote this myself for an English class. I am still learning English so I use simple words."}'
```

```json
{"content_id":"5e6a08f497af","message":"Thank you. Your appeal has been recorded and a person will review it.","status":"under_review"}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{"count":2,"entries":[{"combined_score":0.6174,"confidence":0.6174,"content_id":"5e6a08f497af","creator_id":"sample_writer","guess":"unsure","label":"We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you.","model_score":0.9078,"phrase_score":0.4,"status":"decided","style_score":0.7037,"timestamp":"2026-10-28T23:16:39+00:00","verified_human":false,"word_count":69},{"content_id":"5e6a08f497af","creator_id":"sample_writer","event":"appeal","reasoning":"I wrote this myself for an English class. I am still learning English so I use simple words.","status":"under_review","timestamp":"2026-10-28T23:16:43+00:00"}]}
```

The original decision stays where it was (`"status":"decided"`); the appeal is appended after it with `"status":"under_review"`. The log is append-only on purpose.

**Stretch: `GET /content/<id>`**

```bash
$ curl http://127.0.0.1:5000/content/5e6a08f497af
```

```json
{"appeals":[{"reasoning":"I wrote this myself for an English class. I am still learning English so I use simple words.","timestamp":"2026-10-28T23:16:43+00:00"}],"combined_score":0.6174,"content_id":"5e6a08f497af","creator_id":"sample_writer","guess":"unsure","status":"under_review","verified_human":false}
```

It reports the *latest* status, so it moved from `decided` to `under_review` after the appeal. An unknown id returns 404.

**Stretch: the verified-human path**

The extra step is `POST /verify` with a fresh writing sample of at least 80 words. If the three signals don't call that sample high-confidence AI, the writer earns the credential. It is recorded as a `verification` entry in the log. From then on, every one of that writer's submissions carries `"verified_human": true`, the label gets an extra sentence, and a result that would have been *ai* is downgraded to *unsure*. The credential is also returned by `GET /content/<id>`.

```bash
$ curl -X POST http://127.0.0.1:5000/verify -H "Content-Type: application/json" \
  -d '{"creator_id": "writer_plain_human", "sample": "Honestly I never planned to write about my uncle's garage. ... (97 words, abridged here)"}'
```

```json
{"creator_id":"writer_plain_human","message":"You now hold a verified-human credential. It will show on your future work.","verified_human":true}
```

Then the same writer's next submission (plain-writing paragraph):

```json
{"combined_score": 0.6174, "guess": "unsure", "verified_human": true,
 "label": "We can't tell for certain whether this was written by a person or with an AI tool. Our automated checks aren't reliable enough to say, so no conclusion has been drawn about this piece. If you wrote it yourself, nothing is needed from you. This writer holds a verified-human credential.", ...}
```

Limits I know about: the credential is self-serve with one sample, so someone could paste AI text as the sample; it softens the label but is not proof, which is why a credentialed writer's AI-looking work goes to *unsure* for review and is not cleared.

**Bad input** (criterion 5), all refused as JSON, none a 500:

```
missing text   400 missing_text       empty text     400 missing_text
whitespace     400 missing_text       text = 42      400 missing_text
14 words       422 text_too_short     25,000 chars   413 text_too_long
no creator_id  400 missing_creator_id list body      400
```

`POST /ping` still answered 200 afterwards.

---

## How I Used AI

I used Claude Code in my editor to build this from the project brief. Two specific moments:

**Moment 1 - my first "clearly human" test text could not reach the human label**

- *What I asked for:* The full build from the brief, including signals, scoring and routes, then a table of all my test inputs through every signal.
- *What came back:* Working code, and a table where my first "clearly human" paragraph (grandmother's kitchen) scored 0.432, which is *unsure*. With only that text, the *human* label looked unreachable.
- *What I changed:* I did not lower `HUMAN_THRESHOLD` to make it fit. I tested more human texts instead. The Dayton paragraph scored 0.204 (*human*), so the label is reachable and the cost is that gentle human writing mostly lands in *unsure*. I kept the threshold at 0.35 and recorded the result in the table above.

**Moment 2 - which way punctuation should point**

- *What I asked for:* A punctuation measure for the style signal, scaled so higher means more AI-like.
- *What came back:* Mid-sentence punctuation per word, scored as distance from a "tidy" 0.09, so very sparse and very busy punctuation both read as human.
- *What I changed:* A straight line (less punctuation means more AI) had no good reason behind it, so I kept the U-shape, gave this part the lowest weight (0.20) and wrote in the README that it is the weakest of the three and its direction is a guess.

---

<!-- ═══════════════════════ UNIT 8 - THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently - one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run - Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** - the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety - so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run - After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST - unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted - WRITE IT DOWN

     SUBMISSION CHECKLIST - unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack - stage AND mechanism
       [ ] One improvement, with Attack Run - After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
