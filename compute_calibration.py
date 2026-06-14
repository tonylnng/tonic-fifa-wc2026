#!/usr/bin/env python3
"""校準曲線（可靠度）計算腳本。

讀取 data/predictions/ 與 data/results.json，對每場已完成且有賽前預測的比賽，
取「最新一筆 run_timestamp」的預測（與 update_accuracy.py 一致），依其 confidence
分桶，計算各桶實際勝負命中率，並輸出整體 Brier 分數、ECE 與過度自信指標。

輸出：data/calibration.json
所有 notes 文字使用繁體中文。
"""
import json
import os
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
PRED_DIR = os.path.join(DATA, "predictions")

BUCKETS = [
    (0.0, 0.5, "<50%"),
    (0.5, 0.6, "50-60%"),
    (0.6, 0.7, "60-70%"),
    (0.7, 0.8, "70-80%"),
    (0.8, 0.9, "80-90%"),
    (0.9, 1.01, "90-100%"),
]


def load_results():
    p = os.path.join(DATA, "results.json")
    with open(p, encoding="utf-8") as f:
        return {r["match"]: r for r in json.load(f)["results"]}


def latest_pred_per_match():
    """每場取 run_timestamp 最新的預測檔。"""
    best = {}
    if not os.path.isdir(PRED_DIR):
        return best
    for fn in os.listdir(PRED_DIR):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(PRED_DIR, fn), encoding="utf-8") as f:
            try:
                pred = json.load(f)
            except Exception:
                continue
        m = pred.get("match")
        if m is None:
            continue
        ts = pred.get("run_timestamp", "")
        if m not in best or ts > best[m].get("run_timestamp", ""):
            best[m] = pred
    return best


def main():
    results = load_results()
    preds = latest_pred_per_match()

    # 收集已完成且有預測的場次評估點
    points = []  # (confidence, hit:bool)
    brier_terms = []
    for m, r in results.items():
        pred = preds.get(m)
        if not pred:
            continue
        pp = pred["prediction"]
        conf = float(pp.get("confidence", 0))
        hit = pp.get("outcome") == r.get("outcome")
        points.append((conf, hit))
        # Brier：以對「預測之勝負向」所給的機率 vs 是否命中（1/0）
        wp = pp.get("win_prob", {})
        p_pred_outcome = float(wp.get(pp.get("outcome"), conf))
        brier_terms.append((p_pred_outcome - (1.0 if hit else 0.0)) ** 2)

    total = len(points)

    buckets_out = []
    ece_num = 0.0
    for lo, hi, label in BUCKETS:
        pts = [(c, h) for c, h in points if lo <= c < hi]
        cnt = len(pts)
        if cnt:
            hit_rate = sum(1 for _, h in pts if h) / cnt
            avg_conf = sum(c for c, _ in pts) / cnt
            ece_num += cnt * abs(avg_conf - hit_rate)
        else:
            hit_rate = None
            avg_conf = None
        buckets_out.append({
            "bucket": label,
            "lower": lo,
            "upper": min(hi, 1.0),
            "mid": round((lo + min(hi, 1.0)) / 2, 3),
            "count": cnt,
            "hit_rate": round(hit_rate, 4) if hit_rate is not None else None,
            "avg_confidence": round(avg_conf, 4) if avg_conf is not None else None,
        })

    brier = round(sum(brier_terms) / len(brier_terms), 4) if brier_terms else None
    ece = round(ece_num / total, 4) if total else None
    if total:
        avg_c = sum(c for c, _ in points) / total
        avg_h = sum(1 for _, h in points if h) / total
        overconf = round(avg_c - avg_h, 4)
    else:
        overconf = None

    if total == 0:
        notes = "尚無已完成且具賽前預測的比賽，校準曲線將在累積比賽後自動生成。"
    elif total < 5:
        notes = f"目前僅 {total} 場樣本，校準結果僅供參考，樣本越多越可靠。"
    else:
        if overconf is not None and overconf > 0.1:
            notes = f"已評估 {total} 場：AI 平均信心高於實際命中率約 {round(overconf*100)} 個百分點，呈現過度自信傾向。"
        elif overconf is not None and overconf < -0.1:
            notes = f"已評估 {total} 場：AI 平均信心低於實際命中率，略為保守（低估自身準確度）。"
        else:
            notes = f"已評估 {total} 場：AI 信心與實際命中率大致吻合，校準良好。"

    out = {
        "tournament": "FIFA World Cup 2026",
        "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_evaluated": total,
        "buckets": buckets_out,
        "brier_score": brier,
        "ece": ece,
        "overconfidence": overconf,
        "notes": notes,
    }
    with open(os.path.join(DATA, "calibration.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"calibration.json written: total={total} brier={brier} ece={ece} overconf={overconf}")


if __name__ == "__main__":
    main()
