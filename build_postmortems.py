#!/usr/bin/env python3
"""賽後覆盤（postmortem）合併工具。

用法一（合併單筆，供 cron 用 Opus 生成內容後寫入）：
    echo '<postmortem-json>' | python3 build_postmortems.py --merge-stdin

用法二（程式內呼叫 merge_postmortem(dict)）。

維護 data/postmortems.json：{tournament,last_updated,postmortems:[...]}
以 (match, run_id) 為鍵去重；同鍵以新內容覆蓋（允許重生覆盤）。
所有使用者可見文字應為繁體中文。
"""
import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
PM_PATH = os.path.join(DATA, "postmortems.json")

REQUIRED = ["match", "home", "away", "stage", "predicted", "predicted_outcome",
            "final", "actual_outcome", "verdict", "run_id", "headline", "review"]


def load():
    if os.path.exists(PM_PATH):
        with open(PM_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {"tournament": "FIFA World Cup 2026", "last_updated": "", "postmortems": []}


def verdict_of(pm):
    if pm.get("exact_correct"):
        return "exact"
    if pm.get("outcome_correct"):
        return "outcome"
    return "miss"


def merge_postmortem(pm: dict):
    for k in REQUIRED:
        if k not in pm:
            raise ValueError(f"postmortem missing field: {k}")
    pm.setdefault("outcome_correct", pm["predicted_outcome"] == pm["actual_outcome"])
    pm.setdefault("exact_correct", pm["predicted"] == pm["final"])
    pm.setdefault("verdict", verdict_of(pm))
    pm.setdefault("generated_at", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))

    db = load()
    key = (pm["match"], pm["run_id"])
    db["postmortems"] = [p for p in db["postmortems"]
                         if (p["match"], p["run_id"]) != key]
    db["postmortems"].append(pm)
    db["postmortems"].sort(key=lambda p: p["match"])
    db["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(PM_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    return db


def main():
    if "--merge-stdin" in sys.argv:
        raw = sys.stdin.read().strip()
        pm = json.loads(raw)
        # 支援單筆或陣列
        items = pm if isinstance(pm, list) else [pm]
        for it in items:
            merge_postmortem(it)
        print(f"merged {len(items)} postmortem(s); total={len(load()['postmortems'])}")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
