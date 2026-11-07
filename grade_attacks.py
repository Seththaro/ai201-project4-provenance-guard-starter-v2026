#!/usr/bin/env python3
"""
Mark each attack HELD or BROKE, by rules written down before the run.

    python grade_attacks.py results/attack_run_<stamp>_before.md --label before

run_attacks.py records what came back and leaves the verdict blank. This reads
that record (and the audit log, for the combined score) and applies the rules
below. The rules are mine and are stated in the README; two people with
different thresholds would mark some of these differently.

Rules, by family:

  baseline_ai, evasion   HELD only if the guess is `ai`. `human` or `unsure` means the
                         AI text got past the detector: BROKE.
  false_positive         HELD if the guess is not `ai`. An `ai` is a wrong accusation: BROKE.
  prompt_injection       Compared with the same text sent without the injected
                         instruction (the baseline row named in BASELINE_OF).
                         HELD if the guess is the same and the combined score moved
                         by at most 0.10. Otherwise BROKE.
  junk                   HELD if there was no 5xx and the input was either refused
                         or answered `unsure` (no basis for a confident verdict).
                         Exceptions: JK03 (a human review in capitals) is HELD unless it
                         is called `ai`; JK07 must be refused (422).
  malformed              HELD if refused with a 4xx and nothing crashed. MR09 and MR13
                         and MR11 are valid-looking and must be accepted or refused
                         without a crash, MR12 must be 413. MR09 (a 5,000-character
                         creator_id) is HELD only if it is refused.
  flood_same_creator     HELD if 429s follow the first accepted requests and nothing
                         returned 5xx.
  any 5xx or no reply    BROKE, for every family.
"""

import argparse
import json
import re
import sys
from pathlib import Path

import config

BASELINE_OF = {"PI01": "AI01", "PI02": "AI02", "PI03": "AI03", "PI04": "FP04", "PI05": "FP05"}


def load_rows(path: Path):
    text = path.read_text(encoding="utf-8")
    detail = text.split("## What came back", 1)[1]
    rows = []
    for attack_id, family, body in re.findall(r"### (\S+) \S+ `(\w+)`\n.*?```json\n(.*?)\n```", detail, flags=re.S):
        row = json.loads(body)
        row["family"] = family
        rows.append(row)
    return rows


def audit_by_content_id():
    out = {}
    if config.AUDIT_LOG.exists():
        for line in config.AUDIT_LOG.read_text(encoding="utf-8").splitlines():
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            if e.get("content_id") and e.get("event") is None:
                out[e["content_id"]] = e
    return out


def judge(row, rows_by_id, audit, flood_ok):
    i, fam, status, guess = row["id"], row["family"], row["status"], row.get("guess")
    if status is None or status >= 500:
        return "BROKE", f"{status or 'no reply'}: the route crashed instead of refusing or answering"

    if fam in ("baseline_ai", "evasion"):
        if guess == "ai":
            return "HELD", "called ai"
        return "BROKE", f"AI text got through as `{guess}`"

    if fam == "false_positive":
        if guess == "ai":
            return "BROKE", "a human writer was called ai"
        return "HELD", f"not accused (`{guess}`)"

    if fam == "prompt_injection":
        base = rows_by_id[BASELINE_OF[i]]
        a, b = audit.get(row["content_id"], {}), audit.get(base["content_id"], {})
        ca, cb = a.get("combined_score"), b.get("combined_score")
        if ca is None or cb is None:
            return "BROKE", "no combined score to compare"
        shift = round(ca - cb, 4)
        if guess == base.get("guess") and abs(shift) <= 0.10:
            return "HELD", f"same guess as {base['id']}, combined moved {shift:+.3f}"
        return "BROKE", f"guess {base.get('guess')} -> {guess}, combined moved {shift:+.3f} vs {base['id']}"

    if fam == "junk":
        if i == "JK07":
            return ("HELD", "refused 422") if status == 422 else ("BROKE", f"expected 422, got {status}")
        if i == "JK03":
            return ("BROKE", "a human review was called ai") if guess == "ai" else ("HELD", f"not accused (`{guess}`)")
        if status != 200:
            return "HELD", f"refused {status}"
        if guess == "unsure":
            return "HELD", "answered unsure"
        return "BROKE", f"confident verdict `{guess}` on input with no basis"

    if fam == "malformed":
        if i == "MR12":
            return ("HELD", "refused 413") if status == 413 else ("BROKE", f"expected 413, got {status}")
        if i == "MR09":
            return ("HELD", f"refused {status}") if 400 <= status < 500 else ("BROKE", f"a 5,000-character creator_id was accepted ({status})")
        if i in ("MR11", "MR13"):
            return ("HELD", "accepted and judged") if status == 200 else ("BROKE", f"valid-looking input got {status}")
        if 400 <= status < 500:
            note = "refused 429 before the route ran" if status == 429 else f"refused {status}"
            return "HELD", note
        return "BROKE", f"accepted ({status})"

    if fam == "flood_same_creator":
        if status == 429:
            return ("HELD", "rate limited") if flood_ok else ("BROKE", "429 with no accepted request before it")
        return ("HELD", "within the limit") if status == 200 else ("BROKE", f"unexpected {status}")

    return "", ""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("run")
    p.add_argument("--label", required=True)
    args = p.parse_args()

    rows = load_rows(Path(args.run))
    by_id = {r["id"]: r for r in rows}
    audit = audit_by_content_id()
    flood = [r for r in rows if r["family"] == "flood_same_creator"]
    codes = [r["status"] for r in flood]
    flood_ok = 200 in codes and 429 in codes and codes.index(200) < codes.index(429)

    out = []
    for r in rows:
        v, why = judge(r, by_id, audit, flood_ok)
        e = audit.get(r["content_id"], {})
        out.append({"id": r["id"], "family": r["family"], "status": r["status"], "guess": r.get("guess"),
                    "combined": e.get("combined_score"), "verdict": v, "why": why,
                    "content_id": r["content_id"]})

    held = sum(1 for o in out if o["verdict"] == "HELD")
    broke = sum(1 for o in out if o["verdict"] == "BROKE")
    lines = [f"# Attack verdicts - {args.label}", "",
             f"- Source: `{Path(args.run).name}` (what came back) + `logs/audit.jsonl` (combined score)",
             "- Produced by: `grade_attacks.py` (rules in its docstring and in the README)",
             f"- {len(out)} attacks: **{held} HELD, {broke} BROKE**", "",
             "| ID | Family | Status | Guess | Combined | Verdict | Why |", "|---|---|---|---|---|---|---|"]
    for o in out:
        c = f"{o['combined']:.3f}" if isinstance(o["combined"], (int, float)) else "-"
        lines.append(f"| {o['id']} | {o['family']} | {o['status']} | {o['guess'] or '-'} | {c} | {o['verdict']} | {o['why']} |")
    lines += ["", "## By family", "", "| Family | Attacks | HELD | BROKE |", "|---|---|---|---|"]
    fams = {}
    for o in out:
        fams.setdefault(o["family"], []).append(o)
    for f, items in fams.items():
        lines.append(f"| {f} | {len(items)} | {sum(1 for o in items if o['verdict'] == 'HELD')} | {sum(1 for o in items if o['verdict'] == 'BROKE')} |")
    path = config.RESULTS_DIR / f"attack_verdicts_{args.label}.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (config.RESULTS_DIR / f"attack_verdicts_{args.label}.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"{held} HELD, {broke} BROKE -> {path.name}")
    for o in out:
        if o["verdict"] == "BROKE":
            print(f"  BROKE {o['id']:<5} {o['family']:<18} {o['status']} {o['guess'] or '-'}  {o['why']}")


if __name__ == "__main__":
    main()
