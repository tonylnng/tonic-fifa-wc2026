#!/usr/bin/env python3
"""回填 benchmarks（對比基準線）至 0057Z 批次預測檔。

依各場 reasoning 內已記錄的 Opta 超級電腦 / 博彩隱含機率 / 預測市場數據，
為前端「對比基準線」並列顯示提供結構化資料。機率為依公開來源整理之估計值。
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
PRED_DIR = os.path.join(ROOT, "data", "predictions")
RUN = "2026-06-14T0057Z"


def mk(source, kind, h, d, a, scoreline=None, note=None):
    probs = {"home": h, "draw": d, "away": a}
    outcome = max(probs, key=probs.get)
    b = {"source": source, "kind": kind, "win_prob": probs, "outcome": outcome}
    if scoreline:
        b["scoreline"] = scoreline
    if note:
        b["note"] = note
    return b


# 各場基準線（home, draw, away 機率；依 reasoning 內記載整理）
BENCH = {
    5: [  # Qatar vs Switzerland
        mk("Opta 超級電腦", "model", 0.10, 0.15, 0.75, "0:2", "Opta 預測瑞士 2-0 勝出"),
        mk("博彩隱含機率", "betting", 0.11, 0.16, 0.73, "0:1", "瑞士賠率 -310 至 -426"),
        mk("Kalshi 預測市場", "market", 0.10, 0.11, 0.794, None, "瑞士勝率 79.4%"),
    ],
    6: [  # Brazil vs Morocco
        mk("Opta 超級電腦", "model", 0.58, 0.24, 0.18, "2:0", "Opta 看好巴西但摩洛哥防守頂級"),
        mk("博彩隱含機率", "betting", 0.55, 0.25, 0.20, "2:1", "巴西勝率約 55-60%"),
    ],
    7: [  # Haiti vs Scotland
        mk("Opta 超級電腦", "model", 0.16, 0.20, 0.64, "0:2", "Opta 模擬海地小組賽全敗"),
        mk("博彩隱含機率", "betting", 0.18, 0.20, 0.62, "0:2", "蘇格蘭賠率 -188 至 -200"),
        mk("Football Meister AI", "model", 0.18, 0.18, 0.64, None, "蘇格蘭 64% 勝率"),
    ],
    8: [  # Australia vs Turkey
        mk("Opta 超級電腦", "model", 0.205, 0.241, 0.553, "1:2", "土耳其 55.3% 勝率（10,000 次模擬）"),
        mk("博彩隱含機率", "betting", 0.24, 0.24, 0.52, "1:2", "土耳其約 -140 至 -160"),
        mk("Polymarket 預測市場", "market", 0.20, 0.225, 0.575, None, "土耳其 57.5%"),
    ],
    9: [  # Germany vs Curacao
        mk("Opta / ESPN Elo", "model", 0.96, 0.03, 0.01, "5:0", "ESPN Elo 預測 5-0；Opta 96.1% 出線"),
        mk("博彩隱含機率", "betting", 0.95, 0.04, 0.01, "4:0", "德國 1/25 至 1/20（隱含 95-97%）"),
        mk("Kalshi 預測市場", "market", 0.97, 0.02, 0.01, None, "德國 97% 勝"),
    ],
    10: [  # Netherlands vs Japan
        mk("博彩隱含機率", "betting", 0.50, 0.24, 0.26, "2:1", "荷蘭賠率約 1.95-2.01"),
        mk("模型/媒體共識", "model", 0.52, 0.23, 0.25, "2:1", "多家媒體看好荷蘭，惟提示日本爆冷力"),
    ],
    11: [  # Ivory Coast vs Ecuador
        mk("博彩隱含機率", "betting", 0.30, 0.31, 0.39, None, "厄瓜多爾為大熱、平局 +194 受推薦"),
        mk("NerdyTips 模型", "model", 0.28, 0.32, 0.40, "1:2", "主推 2.5 球以下、低比分"),
    ],
    12: [  # Sweden vs Tunisia
        mk("Dimers 模型", "model", 0.499, 0.254, 0.247, "2:0", "瑞典 49.9% 勝率"),
        mk("博彩隱含機率", "betting", 0.52, 0.25, 0.23, "2:0", "瑞典 -110、進攻火力佔優"),
    ],
    13: [  # Spain vs Cape Verde
        mk("Opta / AI 模型", "model", 0.89, 0.07, 0.04, "3:0", "AI 模型預測 2-0 或 3-0"),
        mk("博彩隱含機率", "betting", 0.88, 0.08, 0.04, "3:0", "西班牙一面倒大熱、全勝預期"),
    ],
}


def main():
    n = 0
    for match, benches in BENCH.items():
        path = os.path.join(PRED_DIR, f"match_{match}__{RUN}.json")
        if not os.path.exists(path):
            print(f"skip (missing): {path}")
            continue
        with open(path, encoding="utf-8") as f:
            pred = json.load(f)
        pred["benchmarks"] = benches
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pred, f, ensure_ascii=False, indent=2)
        n += 1
        print(f"match {match}: +{len(benches)} benchmarks")
    print(f"done; {n} files updated")


if __name__ == "__main__":
    main()
