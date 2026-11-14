#!/usr/bin/env python3
"""
Capstone test runner: the five criteria in criteria.md, three trials each.

    python capstone_eval.py --label before            # AI201_WARMUP=0
    python capstone_eval.py --label after --warmup 1

Each trial starts the service fresh with the documented command (`python app.py`),
so criterion 2 measures a real cold start. Order inside one start: cold submit (2),
warm-up, 20 submits (3), 10 submits (5), 8 bad inputs (4), then the 20 mixed
requests (1). logs/requests.jsonl is emptied before each block.
Writes results/capstone_<stamp>_<label>.md and .json.
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
import audit      # noqa: E402
import reqlog     # noqa: E402
import scenarios  # noqa: E402

URL = "http://127.0.0.1:5000"
PIECES = scenarios.HUMAN_CLASSIC + scenarios.AI_TEXTS + scenarios.BORDERLINE + scenarios.HUMAN_PLAIN
STAGES = ("model", "style", "phrase", "combine")


def make_text(i):
    """80-110 words, deterministic, distinct per i."""
    words, k = [], i
    while len(words) < 85:
        words += PIECES[k % len(PIECES)].split()
        k += 3
    return " ".join(words[:110])


def clear_log():
    if reqlog.REQUEST_LOG.exists():
        reqlog.REQUEST_LOG.unlink()


def post(body=None, raw=None):
    if raw is not None:
        return requests.post(f"{URL}/submit", data=raw.encode("utf-8"),
                             headers={"Content-Type": "application/json"}, timeout=120)
    return requests.post(f"{URL}/submit", json=body, timeout=120)


def start(warmup):
    env = dict(os.environ, AI201_DEBUG="0", AI201_WARMUP=warmup, AI201_RATE_LIMITS="1", PYTHONUTF8="1")
    (ROOT / "logs").mkdir(exist_ok=True)
    out = open(ROOT / "logs" / "server_stdout.txt", "w")
    t = time.perf_counter()
    proc = subprocess.Popen([sys.executable, "app.py"], cwd=ROOT, env=env, stdout=out, stderr=subprocess.STDOUT)
    while time.perf_counter() - t < 120:
        try:
            if requests.get(f"{URL}/health", timeout=2).ok:
                return proc, time.perf_counter() - t
        except Exception:
            time.sleep(0.5)
    proc.terminate()
    raise RuntimeError("service did not answer /health in 120s")


def rss_mb(pid):
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-c", f"(Get-Process -Id {pid}).WorkingSet64"],
                           capture_output=True, text=True, timeout=20)
        return round(int(r.stdout.strip()) / 1e6)
    except Exception:
        return None


def audit_score(content_id):
    for e in reversed(audit.read_entries()):
        if e.get("content_id") == content_id and e.get("event") is None:
            return e.get("combined_score")
    return None


BAD = [
    ("no text", dict(body={"creator_id": "b1"})),
    ("text null", dict(body={"text": None, "creator_id": "b2"})),
    ("list body", dict(body=[1, 2, 3])),
    ("empty body", dict(raw="")),
    ("25000 chars", dict(body={"text": "word " * 5000, "creator_id": "b5"})),
    ("5000-char creator_id", dict(body={"text": make_text(1), "creator_id": "x" * 5000})),
    ("numeric creator_id", dict(body={"text": make_text(2), "creator_id": 12345})),
    ("lone surrogate creator_id", dict(raw='{"text": "%s", "creator_id": "\\ud800"}' % make_text(3))),
]


def send_bad(kw):
    return post(kw.get("body"), raw=kw.get("raw"))


def trial(n, warmup, tag):
    res = {"trial": n}
    clear_log()
    proc, health_s = start(warmup)
    try:
        # criterion 2: the cold submit
        r = post({"text": make_text(0), "creator_id": f"{tag}{n}_cold"})
        cold = reqlog.read()[-1]
        res["c2"] = {"health_after_s": round(health_s, 1), "first_submit_ms": cold["duration_ms"],
                     "status": r.status_code,
                     "pass": r.status_code == 200 and cold["duration_ms"] < 5000 and health_s < 60,
                     "record": cold}
        post({"text": make_text(1), "creator_id": f"{tag}{n}_warm"})  # warm-up

        # criterion 3: 20 warm submits
        clear_log()
        codes = [post({"text": make_text(10 + i), "creator_id": f"{tag}{n}_l{i}"}).status_code for i in range(20)]
        rows = reqlog.read()
        d = sorted(x["duration_ms"] for x in rows)
        res["c3"] = {"p95_ms": d[18], "median_ms": d[10], "max_ms": d[-1], "ok": codes.count(200),
                     "pass": d[18] < 2000 and codes.count(200) == 20}
        res["_lat_rows"] = rows

        # criterion 5: 10 submits, compare log, response and audit log
        clear_log()
        ok_a = ok_b = both = 0
        rows = []
        for i in range(10):
            r = post({"text": make_text(40 + i), "creator_id": f"{tag}{n}_f{i}"}).json()
            rec = reqlog.read()[-1]
            a = rec["output"].get("combined_score") == r.get("combined_score") == audit_score(r.get("content_id"))
            st = rec["stage_ms"]
            b = sum(st.get(k, 0) for k in STAGES) >= 0.9 * rec["duration_ms"]
            ok_a += a
            ok_b += b
            both += (a and b)
            rows.append(rec)
        dur = [x["duration_ms"] for x in rows]
        cpu = [x["cpu_ms"] for x in rows]
        res["c5"] = {"a_ok": ok_a, "b_ok": ok_b, "both": both, "pass": both == 10,
                     "mean_duration_ms": round(sum(dur) / 10, 1), "mean_cpu_ms": round(sum(cpu) / 10, 1),
                     "rss_mb": rss_mb(proc.pid), "sample": rows[:2]}
        res["_fid_rows"] = rows

        # criterion 4: bad inputs
        clear_log()
        good, detail = 0, []
        for name, kw in BAD:
            try:
                r = send_bad(kw)
                try:
                    j = r.json()
                except Exception:
                    j = None
                recs = reqlog.read()
                rec = recs[-1] if recs else {}
                ok = (400 <= r.status_code < 500 and isinstance(j, dict) and "error" in j
                      and rec.get("status") == r.status_code and rec.get("error") == j.get("error"))
                detail.append({"case": name, "status": r.status_code, "error": (j or {}).get("error"),
                               "logged_status": rec.get("status"), "logged_error": rec.get("error"), "ok": ok})
            except Exception as exc:
                ok = False
                detail.append({"case": name, "exception": repr(exc), "ok": False})
            good += ok
        res["c4"] = {"good": good, "pass": good == 8, "detail": detail}

        # criterion 1: 20 mixed requests
        clear_log()
        sent = 0
        for i in range(10):
            post({"text": make_text(70 + i), "creator_id": f"{tag}{n}_m{i}"})
            sent += 1
        for _, kw in BAD[:6]:
            send_bad(kw)
            sent += 1
        for _ in range(2):
            requests.get(f"{URL}/health")
            sent += 1
        for _ in range(2):
            requests.get(f"{URL}/nope")
            sent += 1
        recs = reqlog.read()
        need = ("timestamp", "request_id", "route", "status", "input", "output", "duration_ms")
        complete = sum(all(x.get(k) is not None for k in need) for x in recs)
        res["c1"] = {"sent": sent, "lines": len(recs), "complete": complete,
                     "pass": len(recs) == 20 and complete == 20,
                     "records": [{k: x.get(k) for k in ("route", "status", "error", "duration_ms")} for x in recs]}
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=15)
        except Exception:
            proc.kill()
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--warmup", default="0")
    ap.add_argument("--trials", type=int, default=3)
    a = ap.parse_args()
    tag = a.label[:3]
    T = []
    for n in range(1, a.trials + 1):
        print(f"trial {n} ...", flush=True)
        t = trial(n, a.warmup, tag)
        T.append(t)
        print(f"  c1 {t['c1']['lines']}/20 complete {t['c1']['complete']} | c2 {t['c2']['first_submit_ms']} ms | "
              f"c3 p95 {t['c3']['p95_ms']} | c4 {t['c4']['good']}/8 | c5 {t['c5']['both']}/10", flush=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    out = ROOT / "results" / f"capstone_{stamp}_{a.label}"
    keep = lambda rows: [{k: r.get(k) for k in ("duration_ms", "cpu_ms", "stage_ms")} for r in rows]
    for t in T:
        t["_lat_rows"] = keep(t["_lat_rows"])
        t["_fid_rows"] = keep(t["_fid_rows"])
    out.with_suffix(".json").write_text(json.dumps({"label": a.label, "warmup": a.warmup, "trials": T}, indent=1),
                                        encoding="utf-8")
    v = lambda k: "MET" if all(t[k]["pass"] for t in T) else "MISSED"

    def row(name, target, cells, verdict):
        return f"| {name} | {target} | " + " | ".join(cells) + f" | {verdict} |"

    L = [f"# Capstone run log - {a.label} (AI201_WARMUP={a.warmup})", "",
         "Produced by `capstone_eval.py`. Service started fresh per trial with `python app.py`.", "",
         "| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |", "|---|---|---|---|---|---|",
         row("1. Every request leaves a complete record", "20 of 20",
             [f"{t['c1']['complete']}/20 ({t['c1']['lines']} lines)" for t in T], v("c1")),
         row("2. Cold first submit under 5 s", "< 5000 ms, health < 60 s",
             [f"{t['c2']['first_submit_ms']:.0f} ms, health {t['c2']['health_after_s']} s" for t in T], v("c2")),
         row("3. Warm p95 of 20 under 2 s", "p95 < 2000 ms, 20/20 OK",
             [f"p95 {t['c3']['p95_ms']:.0f} ms, med {t['c3']['median_ms']:.0f}, {t['c3']['ok']}/20 OK" for t in T], v("c3")),
         row("4. Bad input: JSON 4xx, logged with error", "8 of 8", [f"{t['c4']['good']}/8" for t in T], v("c4")),
         row("5. Log matches response, stages add up", "10 of 10",
             [f"{t['c5']['both']}/10 (a {t['c5']['a_ok']}, b {t['c5']['b_ok']})" for t in T], v("c5")), "",
         "## Cost (criterion 5's 10 warm submits per trial)", "",
         "| Trial | mean duration_ms | mean cpu_ms | resident memory MB |", "|---|---|---|---|"]
    for t in T:
        L.append(f"| {t['trial']} | {t['c5']['mean_duration_ms']} | {t['c5']['mean_cpu_ms']} | {t['c5']['rss_mb']} |")
    L += ["", "## Real output (trial 1)", "",
          "**Criterion 2, record of the first submit** (`app.py::_log_request`)", "```json",
          json.dumps(T[0]["c2"]["record"]), "```",
          "**Criterion 5, two records** (`app.py::_log_request`)", "```json"]
    L += [json.dumps(r) for r in T[0]["c5"]["sample"]]
    L += ["```", "**Criterion 4, per case** (`app.py::_check_text`, `_log_request`)", "```json",
          json.dumps(T[0]["c4"]["detail"], indent=1), "```",
          "**Criterion 1, the 20 records** (route, status, error, duration_ms)", "```json",
          json.dumps(T[0]["c1"]["records"]), "```", "",
          "Criterion 3 durations, trial 1 (ms): " + str(sorted(r["duration_ms"] for r in T[0]["_lat_rows"]))]
    out.with_suffix(".md").write_text("\n".join(L), encoding="utf-8")
    print("wrote", out.with_suffix(".md"))


if __name__ == "__main__":
    main()
