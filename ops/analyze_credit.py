#!/usr/bin/env python3
"""每日成本監控分析。

讀 credit_log.json 的 readings（每筆 = 某時刻 UI 上的累計 Credit Used）。
- 用「最新讀數」與「約 24 小時前最近一筆讀數」之差，估算過去 24h 消耗。
- 用過去 8 天的讀數推出前 7 個完整日的每日消耗，算 7 日均。
- 過去 24h 消耗 高於 7 日均 20% 以上 -> 異常。

輸出單一 JSON 到 stdout，供 cron 代理判讀是否通知 / 寫 Notion。
所有面向使用者文字為繁體中文。時間以香港時間（HKT）呈現。
"""
import json, sys
from datetime import datetime, timedelta
import zoneinfo

HKT = zoneinfo.ZoneInfo("Asia/Hong_Kong")
LOG = "/home/user/workspace/cron_tracking/c53acfd7/credit_log.json"
THRESHOLD = 0.20  # 高於 7 日均 20%

def parse(ts):
    # at_hkt 形如 2026-06-23T09:14（無時區）-> 視為 HKT
    return datetime.fromisoformat(ts).replace(tzinfo=HKT)

def main():
    with open(LOG) as f:
        data = json.load(f)
    readings = sorted(data.get("readings", []), key=lambda r: r["at_hkt"])
    now = datetime.now(HKT)
    out = {
        "checked_at_hkt": now.strftime("%Y-%m-%dT%H:%M"),
        "date_label": now.strftime("%Y-%m-%d"),
        "status": None,
        "latest_reading": None,
        "consumed_24h": None,
        "avg_7d": None,
        "diff_pct": None,
        "abnormal": False,
        "note": "",
        "notify": False,
    }

    if not readings:
        out["status"] = "資料不足"
        out["note"] = "尚無任何讀數。"
        print(json.dumps(out, ensure_ascii=False)); return

    latest = readings[-1]
    out["latest_reading"] = latest["credit_used"]
    latest_t = parse(latest["at_hkt"])

    # 若最新讀數距今超過 30 小時，視為今天還沒補讀數
    if (now - latest_t) > timedelta(hours=30):
        out["status"] = "待補讀數"
        out["note"] = f"最新讀數停在 {latest['at_hkt']} HKT，距今超過 30 小時，今日尚未提供新讀數。"
        out["notify"] = True
        print(json.dumps(out, ensure_ascii=False)); return

    # 過去 24h 消耗：最新 - 最接近「24h 前」的較早讀數
    target = latest_t - timedelta(hours=24)
    prior = [r for r in readings if parse(r["at_hkt"]) <= latest_t - timedelta(hours=12)]
    if not prior:
        out["status"] = "資料不足"
        out["note"] = "只有單一近期讀數，無法計算 24 小時消耗。需累積至少兩日讀數。"
        print(json.dumps(out, ensure_ascii=False)); return
    # 取最接近 24h 前的那筆
    ref = min(prior, key=lambda r: abs((parse(r["at_hkt"]) - target).total_seconds()))
    ref_t = parse(ref["at_hkt"])
    hours = (latest_t - ref_t).total_seconds() / 3600.0
    raw = latest["credit_used"] - ref["credit_used"]
    consumed_24h = raw / hours * 24.0 if hours > 0 else raw  # 正規化為每 24h
    out["consumed_24h"] = round(consumed_24h, 2)

    # 7 日均：用過去 ~8 天的讀數，取每對相鄰日的差，正規化為日消耗，再平均
    window_start = latest_t - timedelta(days=8)
    win = [r for r in readings if parse(r["at_hkt"]) >= window_start]
    daily_rates = []
    for a, b in zip(win, win[1:]):
        ta, tb = parse(a["at_hkt"]), parse(b["at_hkt"])
        h = (tb - ta).total_seconds() / 3600.0
        if h <= 0:
            continue
        d = (b["credit_used"] - a["credit_used"]) / h * 24.0
        daily_rates.append(d)
    # 排除最後一段（即過去24h本身），讓基準=之前7日
    base_rates = daily_rates[:-1] if len(daily_rates) >= 2 else daily_rates

    if len(base_rates) < 2:
        out["status"] = "資料不足"
        out["avg_7d"] = round(sum(base_rates)/len(base_rates), 2) if base_rates else None
        out["note"] = f"歷史讀數不足（目前可用日消耗樣本 {len(base_rates)} 筆），需累積約 3 日以上讀數才能做 7 日均異常比對。本次僅記錄。"
        print(json.dumps(out, ensure_ascii=False)); return

    avg_7d = sum(base_rates) / len(base_rates)
    out["avg_7d"] = round(avg_7d, 2)
    diff = (consumed_24h - avg_7d) / avg_7d if avg_7d > 0 else 0.0
    out["diff_pct"] = round(diff, 4)

    if diff > THRESHOLD:
        out["status"] = "異常↑"
        out["abnormal"] = True
        out["notify"] = True
        out["note"] = (f"過去 24 小時消耗 {consumed_24h:.0f} 點，較前 7 日均 {avg_7d:.0f} 點高出 "
                       f"{diff*100:.1f}%，超過 20% 警戒線。")
    else:
        out["status"] = "正常"
        out["note"] = (f"過去 24 小時消耗 {consumed_24h:.0f} 點，較前 7 日均 {avg_7d:.0f} 點 "
                       f"{'+' if diff>=0 else ''}{diff*100:.1f}%，在正常範圍內。")
    print(json.dumps(out, ensure_ascii=False))

if __name__ == "__main__":
    main()
