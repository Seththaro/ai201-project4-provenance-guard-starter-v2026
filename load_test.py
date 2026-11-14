#!/usr/bin/env python3
"""
Load observation (capstone stretch): the service at about ten times a normal rate.

    python load_test.py --label load

"Normal" is one writer pasting a piece every 10 seconds (6 a minute). Ten times
that is 60 a minute, one arrival a second, held for 60 seconds, each arrival
under its own creator_id and sent whether or not the last one has finished
(open loop, like real users). Starts the service with the documented command,
warm-up on, then runs a normal phase and a 10x phase and compares them using
the service's own request log and the client's view.
"""
import argparse
import datetime as dt
import json
import os
import statistics
import subprocess
import sys
import threading
import time
from pathlib import Path

import requests

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))
import capstone_eval as ce  # noqa: E402
import reqlog               # noqa: E402


def phase(name, per_minute, seconds, tag):
    ce.clear_log()
    interval = 60.0 / per_minute
    n = int(seconds / interval)
    client = []
    lock = threading.Lock()

    def one(i):
        t = time.perf_counter()
        try:
            r = requests.post(f"{ce.URL}/submit", json={"text": ce.make_text(i), "creator_id": f"{tag}_{name}_{i}"}, timeout=180)
            code = r.status_code
        except Exception as exc:  # noqa: BLE001
            code = type(exc).__name__
        with lock:
            client.append((code, (time.perf_counter() - t) * 1000))

    threads = []
    t0 = time.perf_counter()
    for i in range(n):
        target = t0 + i * interval
        time.sleep(max(0, target - time.perf_counter()))
        th = threading.Thread(target=one, args=(i,))
        th.start()
        threads.append(th)
    for th in threads:
        th.join()
    wall = time.perf_counter() - t0
    recs = [r for r in reqlog.read() if r["route"] == "/submit"]
    d = sorted(r["duration_ms"] for r in recs)
    c = sorted(ms for _, ms in client)
    codes = {}
    for code, _ in client:
        codes[str(code)] = codes.get(str(code), 0) + 1
    p = lambda xs, q: xs[min(len(xs) - 1, int(q * len(xs)))]
    return {"phase": name, "rate_per_min": per_minute, "sent": n, "wall_s": round(wall, 1), "status_counts": codes,
            "server_duration_ms": {"median": round(statistics.median(d), 1), "p95": p(d, 0.95), "max": d[-1]},
            "client_latency_ms": {"median": round(statistics.median(c), 1), "p95": round(p(c, 0.95), 1), "max": round(c[-1], 1)},
            "mean_cpu_ms": round(statistics.mean(r["cpu_ms"] for r in recs), 1),
            "logged_requests": len(recs)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", default="load")
    a = ap.parse_args()
    proc, health = ce.start("1")
    try:
        requests.post(f"{ce.URL}/submit", json={"text": ce.make_text(999), "creator_id": "load_warm"}, timeout=120)
        normal = phase("normal", 6, 60, a.label[:4])
        heavy = phase("ten_times", 60, 60, a.label[:4])
        rss = ce.rss_mb(proc.pid)
    finally:
        ce.stop(proc)
    out = {"label": a.label, "rss_mb_after": rss, "phases": [normal, heavy]}
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    path = ROOT / "results" / f"load_{stamp}_{a.label}.json"
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))
    print("wrote", path)


if __name__ == "__main__":
    main()
