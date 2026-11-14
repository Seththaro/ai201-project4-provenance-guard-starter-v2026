#!/usr/bin/env python3
"""
Run my five criteria three times and count what each trial measured.

    python app.py                                  # in one terminal
    python check_criteria.py --label before        # in another
    python check_criteria.py --label after

run_eval.py saves the raw output of the /submit scenarios. This script does the
counting for the run log, using the same lists from scenarios.py, and it covers
the two things run_eval.py cannot: criterion 4 (an appeal needs a content_id
from an earlier submission) and criterion 3(a), the sweep of score_to_label.

It measures. It does not decide MET or MISSED; the verdict is written by hand
against the target in criteria_unit7.md.
"""

import argparse
import datetime as dt
import json
import sys

import requests

import config
import scenarios
import scoring

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass

URL = f"http://{config.HOST}:{config.PORT}"
PLAIN = len(scenarios.HUMAN_PLAIN)


def submit(text, creator_id):
    r = requests.post(f"{URL}/submit", json={"text": text, "creator_id": creator_id}, timeout=120)
    try:
        body = r.json()
    except ValueError:
        body = {}
    return r.status_code, body


def rejected_count():
    entries = requests.get(f"{URL}/log", timeout=30).json()["entries"]
    return sum(1 for e in entries if e.get("event") == "rejected")


def one_trial(t):
    out = {}
    tag = f"{dt.datetime.now():%H%M%S}"

    # One batch of 20 submissions feeds criteria 1, 2 and 3(b).
    texts = scenarios.CRITERION_3_TEXTS
    results = []
    for i, text in enumerate(texts):
        status, body = submit(text, f"crit_t{t}_{tag}_{i}")
        results.append({"i": i, "status": status, **{k: body.get(k) for k in (
            "content_id", "guess", "model_score", "style_score", "phrase_score", "combined_score")}})
    plain = results[:PLAIN]
    classic = results[PLAIN:PLAIN + 5]
    ai = results[PLAIN + 5:PLAIN + 10]
    human10 = plain + classic

    # Criterion 1: false positives among the 10 human pieces, and among the plain ones.
    ai_flags = [r["i"] for r in human10 if r["guess"] == "ai"]
    plain_flags = [r["i"] for r in plain if r["guess"] == "ai"]
    out["c1"] = {"ai_of_10": len(ai_flags), "plain_ai_of_5": len(plain_flags),
                 "flagged_indexes": ai_flags,
                 "pass": len(ai_flags) <= 1 and not plain_flags}

    # Criterion 2: mean combined score, AI group minus human group (5 vs 5).
    mean_ai = sum(r["combined_score"] for r in ai) / 5
    mean_h = sum(r["combined_score"] for r in classic) / 5
    out["c2"] = {"mean_ai": round(mean_ai, 4), "mean_human": round(mean_h, 4),
                 "gap": round(mean_ai - mean_h, 4), "pass": mean_ai - mean_h >= 0.30}

    # Criterion 3: (a) sweep score_to_label over 0.00..1.00, (b) guesses over 20 submissions.
    sweep = [scoring.score_to_label(s / 100)[0] for s in range(101)]
    a_ok = all(g in ("human", "unsure", "ai") for g in sweep) and len(set(sweep)) == 3
    guesses = [r["guess"] for r in results]
    b_ok = set(guesses) >= {"human", "unsure", "ai"} and guesses.count("unsure") >= 3
    out["c3"] = {"sweep_labels_seen": sorted(set(sweep)), "guess_counts": {
        g: guesses.count(g) for g in ("human", "unsure", "ai")}, "n": len(results),
        "pass": a_ok and b_ok}

    # Criterion 4: 10 appeals recorded, 3 made-up ids get 404 and add nothing.
    ids = [r["content_id"] for r in results if r["content_id"]][:10]
    appeal_ok = 0
    for n, cid in enumerate(ids):
        reason = f"trial {t} appeal {n}: I wrote this myself."
        r = requests.post(f"{URL}/appeal", json={"content_id": cid, "reasoning": reason}, timeout=30)
        entries = requests.get(f"{URL}/log", timeout=30).json()["entries"]
        logged = any(e.get("event") == "appeal" and e.get("content_id") == cid
                     and e.get("reasoning") == reason for e in entries)
        if r.status_code == 200 and r.json().get("status") == "under_review" and logged:
            appeal_ok += 1
    fake = [f"doesnotexist{t}{n}" for n in range(3)]
    fake_404 = 0
    for cid in fake:
        r = requests.post(f"{URL}/appeal", json={"content_id": cid, "reasoning": "made up"}, timeout=30)
        if r.status_code == 404:
            fake_404 += 1
    entries = requests.get(f"{URL}/log", timeout=30).json()["entries"]
    fake_added = sum(1 for e in entries if e.get("content_id") in fake and e.get("status") == "under_review")
    out["c4"] = {"appeals_ok_of_10": appeal_ok, "unknown_404_of_3": fake_404,
                 "unknown_entries_added": fake_added,
                 "pass": appeal_ok == 10 and fake_404 == 3 and fake_added == 0}

    # Criterion 5: 8 malformed requests -> 400/413/422 with a JSON error, rejected entries logged, /ping still 200.
    before = rejected_count()
    sent = []
    bodies = list(scenarios.BAD_BODIES)
    for b in bodies:
        r = requests.post(f"{URL}/submit", json=b, timeout=60)
        try:
            j = r.json()
        except ValueError:
            j = None
        sent.append({"status": r.status_code, "error": (j or {}).get("error") if isinstance(j, dict) else None})
    r = requests.post(f"{URL}/submit", json=["not", "an", "object"], timeout=60)
    try:
        j = r.json()
    except ValueError:
        j = None
    sent.append({"status": r.status_code, "error": (j or {}).get("error") if isinstance(j, dict) else None})
    added = rejected_count() - before
    ping = requests.post(f"{URL}/ping", json={"message": "hi"}, timeout=30).status_code
    codes_ok = all(s["status"] in (400, 413, 422) and s["error"] for s in sent)
    out["c5"] = {"statuses": [s["status"] for s in sent], "errors": [s["error"] for s in sent],
                 "rejected_entries_added": added, "ping": ping,
                 "pass": codes_ok and added == 8 and ping == 200}

    out["raw_submissions"] = results
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--label", default="")
    p.add_argument("--trials", type=int, default=3)
    args = p.parse_args()

    requests.get(f"{URL}/health", timeout=5)
    trials = []
    for t in range(1, args.trials + 1):
        print(f"trial {t} ...", flush=True)
        trials.append(one_trial(t))
        c = trials[-1]
        print(f"  c1 {c['c1']['ai_of_10']}/10 (plain {c['c1']['plain_ai_of_5']}/5)  "
              f"c2 gap {c['c2']['gap']}  c3 {c['c3']['guess_counts']}  "
              f"c4 {c['c4']['appeals_ok_of_10']}/10+{c['c4']['unknown_404_of_3']}/3  "
              f"c5 {c['c5']['statuses']} +{c['c5']['rejected_entries_added']} log", flush=True)

    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    config.RESULTS_DIR.mkdir(exist_ok=True)
    path = config.RESULTS_DIR / f"criteria_{stamp}{label}.md"

    def row(name, target, cells, verdict_pass):
        return f"| {name} | {target} | " + " | ".join(cells) + " | |"

    lines = [
        f"# Criteria run{f' - {args.label}' if args.label else ''}",
        "",
        "- Produced by: `check_criteria.py::main` (texts from `scenarios.py`)",
        f"- {args.trials} trials, nothing changed in between, {dt.datetime.now():%Y-%m-%d %H:%M}",
        f"- Limits in force: {config.RATE_LIMIT_PER_MINUTE}/minute, {config.RATE_LIMIT_PER_DAY}/day per creator_id",
        "",
        "| Criterion | Target | " + " | ".join(f"Run {i}" for i in range(1, args.trials + 1)) + " | Verdict |",
        "|---|---|" + "|".join(["---"] * args.trials) + "|---|",
        row("1. My own writing flagged as AI", "<= 1 of 10, none of the plain 5",
            [f"{c['c1']['ai_of_10']}/10 (plain {c['c1']['plain_ai_of_5']}/5)" for c in trials], None),
        row("2. Score spread", "gap >= 0.30",
            [f"{c['c2']['gap']:.3f}" for c in trials], None),
        row("3. Label coverage", "3 of 3 labels, >= 3 unsure",
            [f"{c['c3']['guess_counts']['human']}h/{c['c3']['guess_counts']['unsure']}u/{c['c3']['guess_counts']['ai']}ai" for c in trials], None),
        row("4. Appeal path", "10/10 + 3/3 unknown 404",
            [f"{c['c4']['appeals_ok_of_10']}/10 + {c['c4']['unknown_404_of_3']}/3" for c in trials], None),
        row("5. Bad input", "8/8 4xx JSON, 8 logged, ping 200",
            [f"{sum(1 for s in c['c5']['statuses'] if s in (400, 413, 422))}/8, {c['c5']['rejected_entries_added']} logged" for c in trials], None),
        "",
        "Per-trial detail (real output):",
        "",
        "```json",
        json.dumps([{k: v for k, v in c.items() if k != "raw_submissions"} for c in trials], indent=2),
        "```",
        "",
        "Raw `/submit` results for trial 1 (index 0-4 plain human, 5-9 classic human, 10-14 AI, 15-19 borderline):",
        "",
        "```json",
        json.dumps(trials[0]["raw_submissions"], indent=2),
        "```",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
