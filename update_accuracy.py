#!/usr/bin/env python3
"""Recompute accuracy.json by comparing the latest pre-match prediction
for each completed match against results.json. Also stamps results into
prediction-derived evaluation list. Run after results.json is updated.
"""
import json, glob, os, re
from datetime import datetime, timezone

BASE = "/home/user/workspace/wc2026/data"
SITE = "/home/user/workspace/wc2026/site/data"

def load(p):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None

def parse_score(s):
    m = re.match(r"\s*(\d+)\s*[:\-]\s*(\d+)\s*", str(s))
    return (int(m.group(1)), int(m.group(2))) if m else None

def outcome(h, a):
    return "home" if h > a else ("away" if a > h else "draw")

# Gather latest prediction per match
preds = {}  # match -> (run_ts, dict)
for f in glob.glob(os.path.join(BASE, "predictions", "match_*.json")):
    d = load(f)
    if not d: continue
    m = d["match"]
    ts = d.get("run_timestamp", "")
    if m not in preds or ts > preds[m][0]:
        preds[m] = (ts, d)

# Results
rj = load(os.path.join(BASE, "results.json")) or {}
results = rj.get("results", rj if isinstance(rj, list) else [])

evals = []
by_stage = {}
oc = sc = total = 0
for r in results:
    if not isinstance(r, dict): continue
    m = r.get("match")
    fin = parse_score(r.get("scoreline", ""))
    if m not in preds or not fin: continue
    pd = preds[m][1]
    ps = pd["prediction"]
    pscore = (ps["score"]["home"], ps["score"]["away"])
    pout = ps.get("outcome")
    aout = outcome(*fin)
    o_hit = (pout == aout)
    s_hit = (pscore == fin)
    total += 1
    oc += 1 if o_hit else 0
    sc += 1 if s_hit else 0
    stage = pd.get("stage", "Group")
    skey = stage.split()[0] if stage else "Group"
    bs = by_stage.setdefault(skey, {"evaluated": 0, "outcome_correct": 0, "exact_correct": 0})
    bs["evaluated"] += 1
    bs["outcome_correct"] += 1 if o_hit else 0
    bs["exact_correct"] += 1 if s_hit else 0
    evals.append({
        "match": m, "home": pd["home"], "away": pd["away"],
        "predicted": ps.get("scoreline"), "predicted_outcome": pout,
        "final": r.get("scoreline"), "actual_outcome": aout,
        "outcome_correct": o_hit, "exact_correct": s_hit,
        "run_id": pd.get("run_id"),
    })

acc = {
    "tournament": "FIFA World Cup 2026",
    "description": "Rolling AI prediction accuracy. Computed after each match by comparing the latest pre-match prediction against the recorded final result.",
    "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "metrics": {
        "total_evaluated": total,
        "outcome_correct": oc,
        "outcome_accuracy": round(oc / total, 4) if total else 0.0,
        "exact_score_correct": sc,
        "exact_score_accuracy": round(sc / total, 4) if total else 0.0,
    },
    "definitions": {
        "outcome_accuracy": "Share of matches where the predicted winner/draw (1X2) matched the actual outcome.",
        "exact_score_accuracy": "Share of matches where the predicted X:X scoreline exactly matched the actual scoreline.",
    },
    "by_stage": by_stage,
    "evaluations": sorted(evals, key=lambda e: e["match"]),
}

for out in [os.path.join(BASE, "accuracy.json"), os.path.join(SITE, "accuracy.json")]:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(acc, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print(f"Accuracy updated: {total} evaluated, outcome {oc}/{total}, exact {sc}/{total}")
