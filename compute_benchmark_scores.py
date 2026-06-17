#!/usr/bin/env python3
"""對比基準線計分：AI vs 博彩 vs Opta/超級電腦 誰更準。

對每場已完成且有賽前預測的比賽，取最新預測檔，將 AI 預測與其 benchmarks
一同對照最終結果計分（勝負命中、精準比分、Brier）。彙整成排行榜。

輸出：data/benchmark_scores.json
"""
import json
import os
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
PRED_DIR = os.path.join(DATA, "predictions")


def load_results():
    with open(os.path.join(DATA, "results.json"), encoding="utf-8") as f:
        return {r["match"]: r for r in json.load(f)["results"]}


def latest_pred_per_match():
    best = {}
    if not os.path.isdir(PRED_DIR):
        return best
    for fn in os.listdir(PRED_DIR):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(PRED_DIR, fn), encoding="utf-8") as f:
            try:
                p = json.load(f)
            except Exception:
                continue
        m = p.get("match")
        if m is None:
            continue
        if m not in best or p.get("run_timestamp", "") > best[m].get("run_timestamp", ""):
            best[m] = p
    return best


def parse_scoreline(s):
    try:
        h, a = s.split(":")
        return int(h), int(a)
    except Exception:
        return None


def main():
    results = load_results()
    preds = latest_pred_per_match()

    # 累加器：source -> {evaluated, outcome_correct, exact_correct, brier_sum, brier_n}
    agg = {}

    def acc(src, kind, outcome, scoreline, win_prob, r):
        a = agg.setdefault(src, {
            "source": src, "kind": kind, "evaluated": 0,
            "outcome_correct": 0, "exact_correct": 0,
            "brier_sum": 0.0, "brier_n": 0,
        })
        a["evaluated"] += 1
        if outcome == r["outcome"]:
            a["outcome_correct"] += 1
        if scoreline:
            ps = parse_scoreline(scoreline)
            if ps and ps[0] == r["score"]["home"] and ps[1] == r["score"]["away"]:
                a["exact_correct"] += 1
        if win_prob and outcome in win_prob:
            p = float(win_prob[outcome])
            hit = 1.0 if outcome == r["outcome"] else 0.0
            a["brier_sum"] += (p - hit) ** 2
            a["brier_n"] += 1

    for m, r in results.items():
        pred = preds.get(m)
        if not pred:
            continue
        pp = pred["prediction"]
        acc("AI（本站主預測）", "ai", pp.get("outcome"), pp.get("scoreline"),
            pp.get("win_prob"), r)
        for b in pred.get("benchmarks", []):
            wp = b.get("win_prob")
            # 第三方 AI 基準線可能未存 outcome，由 win_prob 取最大向推導。
            outcome = b.get("outcome")
            if not outcome and wp:
                outcome = max(wp, key=wp.get)
            acc(b["source"], b.get("kind", "model"), outcome,
                b.get("scoreline"), wp, r)

    leaderboard = []
    for a in agg.values():
        ev = a["evaluated"] or 1
        leaderboard.append({
            "source": a["source"],
            "kind": a["kind"],
            "evaluated": a["evaluated"],
            "outcome_correct": a["outcome_correct"],
            "outcome_accuracy": round(a["outcome_correct"] / ev, 4),
            "exact_correct": a["exact_correct"],
            "exact_accuracy": round(a["exact_correct"] / ev, 4),
            "brier_score": round(a["brier_sum"] / a["brier_n"], 4) if a["brier_n"] else None,
        })
    # 排序：勝負命中率高者在前，其次比分命中率，其次 Brier 低者
    leaderboard.sort(key=lambda x: (
        -x["outcome_accuracy"], -x["exact_accuracy"],
        x["brier_score"] if x["brier_score"] is not None else 1.0,
    ))

    out = {
        "tournament": "FIFA World Cup 2026",
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_matches_scored": len([m for m in results if m in preds]),
        "leaderboard": leaderboard,
        "notes": "AI 與各公開基準線在相同已完成比賽上的對照計分；僅納入該來源有提供預測的場次。",
    }
    with open(os.path.join(DATA, "benchmark_scores.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"benchmark_scores.json written: {len(leaderboard)} sources, "
          f"{out['total_matches_scored']} matches")
    for l in leaderboard:
        print(f"  {l['source']}: outcome {l['outcome_correct']}/{l['evaluated']} "
              f"exact {l['exact_correct']}/{l['evaluated']} brier={l['brier_score']}")


if __name__ == "__main__":
    main()
