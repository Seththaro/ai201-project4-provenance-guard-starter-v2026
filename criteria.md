# Acceptance criteria - Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion - and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False positives: at most 1 in 10 human pieces is labelled high-confidence AI

Test set: 10 pieces of human writing, at least 4 of them deliberately plain
(short sentences, common words, the style of a younger or second-language
writer). Submit each through `POST /submit`. **At most 1 of the 10 comes back
with `guess: "ai"`, and none of the 4 plain ones do.** The target has to hold in
each of 3 separate runs.

**Why this target:** On a writing site a wrong accusation costs one person a
lot and a missed detection costs the site a little, so this is the strictest
target I have. Signal one (`detector.py`, perplexity) scores plain writing as
machine-like, so the plain pieces are exactly where my system is most likely to
accuse the wrong person; I will not let them hide inside an average.

---

## 2. Score spread: clearly-AI text averages at least 0.30 above clearly-human text

Test set: 5 pieces I am sure are AI-generated and 5 I am sure a person wrote.
Take the mean `combined_score` of each group from the `/submit` response. **Mean
of the AI group minus mean of the human group is at least 0.30**, in each of 3
runs.

**Why this target:** If the two groups sit closer than 0.30, the thresholds
(0.35 and 0.70) cannot separate them and the labels are decoration. 0.30 is
not trivial: both signals are weak on short text, so I expect to be near the
edge. I'd rather miss a real target than hit an easy one.

---

## 3. Label coverage: all three labels are reachable and no score falls in a gap

Two checks. (a) Calling `scoring.score_to_label` on every score from 0.00 to
1.00 in steps of 0.01 returns exactly one of `human`, `unsure`, `ai` for all 101
values, and each of the three is returned at least once. (b) Over a set of at
least 20 real submissions through `POST /submit`, **all three** `guess` values
appear at least once, and at least 3 of them are `unsure`.

**Why this target:** An "unsure" label nobody can reach would turn the
system into the 0.5 coin flip the brief warns about, and a "human" label that
can't be reached means the system can only accuse or shrug. My style signal
could only compress scores toward 0.5 if it didn't vary, so (b) tests that it
does.

---

## 4. Appeal path: 10 of 10 appeals change status and are recorded; unknown ids change nothing

Take 10 content_ids from earlier submissions and `POST /appeal` each with a
reason. **All 10 return HTTP 200 and `"status": "under_review"`, and for all 10
`GET /log` shows an `event: "appeal"` entry with the same `content_id` and the
reasoning text.** Then send 3 appeals with made-up content_ids: **all 3 return
404 and add no `under_review` entry** to the log.

**Why this target:** The appeal is the only thing between a wrong accusation and
nothing at all, so it should be 10 of 10, not 9 of 10. The unknown-id case
matters because a typo that silently "succeeds" would tell a real writer their
appeal was received when it was not.

---

## 5. Bad input: 8 malformed requests get a 4xx JSON error, never a 500, and the service stays up

Send these to `POST /submit`: no `text` field; `text` empty; `text` of only
whitespace; `text` a number; `text` of 14 words; `text` of 25,000 characters;
no `creator_id`; a body that is a JSON list. **All 8 return a 400, 413 or 422
with a JSON `error` field, none returns 500, each leaves a `rejected` entry in
the log, and `POST /ping` still answers 200 afterwards.**

**Why this target:** A crash on malformed input is one of the most common real
failures, and the text limits protect the model-loading path: a 25,000
character body should be refused before it reaches a model that only reads 400
tokens. Under 15 words no signal is meaningful, so a verdict there would be
invented.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 - read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
