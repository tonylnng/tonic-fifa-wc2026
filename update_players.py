#!/usr/bin/env python3
"""更新球員本屆統計（進球/黃牌/紅牌）並重算射手榜與紀律榜。

讀取 data/players.json，依賽後事件冪等累加統計，輸出回 players.json，
並計算 data/leaderboards.json。

用法：
  # 從 stdin 合併賽後事件（單場或多場陣列）
  echo '<json>' | python3 update_players.py --merge-stdin

  # 只重算排行榜（不合併新事件）
  python3 update_players.py --recompute-only

stdin 格式（單場物件或多場陣列）：
  {"match": 17,
   "events": [
     {"id": "FRA-mbappe", "goals": 2, "yellow_cards": 0, "red_cards": 0},
     {"id": "SEN-newguy", "goals": 1, "name_en": "...", "name_zh": "...",
      "team": "Senegal", "team_zh": "塞內加爾", "position": "FW"}
   ],
   "sources": ["https://..."]}

冪等：每名球員的 stats.matches_with_events 記錄已計入的場次編號；
同一場再次餵入不會重複累加。
"""
import json
import os
import sys
import argparse
from datetime import datetime, timezone

BASE = "/home/user/workspace/wc2026/data"
PLAYERS = os.path.join(BASE, "players.json")
LEADER = os.path.join(BASE, "leaderboards.json")

POS_ORDER = {"FW": 0, "MF": 1, "DF": 2, "GK": 3}


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_players():
    if not os.path.exists(PLAYERS):
        return {
            "tournament": "FIFA World Cup 2026",
            "last_updated": now_iso(),
            "note": "每隊重點球員。統計為本屆累計，由定時任務每場賽後以 AI 研究權威來源更新。",
            "players": [],
        }
    with open(PLAYERS, encoding="utf-8") as f:
        return json.load(f)


def ensure_stats(p):
    s = p.setdefault("stats", {})
    s.setdefault("goals", 0)
    s.setdefault("yellow_cards", 0)
    s.setdefault("red_cards", 0)
    s.setdefault("matches_with_events", [])
    return s


def index_by_id(doc):
    return {p["id"]: p for p in doc.get("players", []) if p.get("id")}


def merge_match(doc, idx, match_no, events, sources):
    """冪等累加單場事件。回傳本場新計入的球員數。"""
    if match_no is None:
        sys.stderr.write("[WARN] 略過缺少 match 編號的事件批次\n")
        return 0
    applied = 0
    for ev in events:
        pid = ev.get("id")
        if not pid:
            sys.stderr.write(f"[WARN] 略過缺少 id 的事件：{ev}\n")
            continue
        p = idx.get(pid)
        if p is None:
            # 新球員：以事件附帶欄位建檔
            p = {
                "id": pid,
                "name_en": ev.get("name_en", "TBD"),
                "name_zh": ev.get("name_zh", "待補"),
                "team": ev.get("team", "TBD"),
                "team_zh": ev.get("team_zh", "待補"),
                "position": ev.get("position", "MF"),
                "shirt_no": ev.get("shirt_no"),
                "age": ev.get("age"),
                "club": ev.get("club", ""),
                "is_key": False,
                "bio_zh": ev.get("bio_zh", ""),
                "stats": {"goals": 0, "yellow_cards": 0, "red_cards": 0, "matches_with_events": []},
                "sources": [],
            }
            doc["players"].append(p)
            idx[pid] = p
        s = ensure_stats(p)
        if match_no in s["matches_with_events"]:
            continue  # 已計入，冪等略過
        s["goals"] += int(ev.get("goals", 0) or 0)
        s["yellow_cards"] += int(ev.get("yellow_cards", 0) or 0)
        s["red_cards"] += int(ev.get("red_cards", 0) or 0)
        s["matches_with_events"].append(match_no)
        s["matches_with_events"] = sorted(set(s["matches_with_events"]))
        if sources:
            p["sources"] = sources[:8]
        applied += 1
    return applied


def compute_leaderboards(doc):
    players = doc.get("players", [])

    def row(p):
        s = p.get("stats", {})
        return {
            "id": p.get("id"),
            "name_zh": p.get("name_zh"),
            "name_en": p.get("name_en"),
            "team_zh": p.get("team_zh"),
            "team": p.get("team"),
            "position": p.get("position"),
            "shirt_no": p.get("shirt_no"),
            "goals": s.get("goals", 0),
            "yellow_cards": s.get("yellow_cards", 0),
            "red_cards": s.get("red_cards", 0),
        }

    rows = [row(p) for p in players]

    # 射手榜：進球>0；goals desc, 紅黃牌少者優先, 姓名
    scorers = [r for r in rows if r["goals"] > 0]
    scorers.sort(key=lambda r: (-r["goals"], r["red_cards"], r["yellow_cards"], r["name_en"] or ""))

    # 紀律榜：有紅或黃；red desc, yellow desc, 姓名
    discipline = [r for r in rows if r["red_cards"] > 0 or r["yellow_cards"] > 0]
    discipline.sort(key=lambda r: (-r["red_cards"], -r["yellow_cards"], r["name_en"] or ""))

    totals = {
        "players": len(players),
        "goals": sum(r["goals"] for r in rows),
        "yellow_cards": sum(r["yellow_cards"] for r in rows),
        "red_cards": sum(r["red_cards"] for r in rows),
    }
    return {
        "last_updated": now_iso(),
        "scorers": scorers,
        "discipline": discipline,
        "totals": totals,
    }


def sort_players(doc):
    """穩定排序：隊名 → 位置 → 球衣號 → 姓名，方便前端分組顯示。"""
    doc["players"].sort(
        key=lambda p: (
            p.get("team", ""),
            POS_ORDER.get(p.get("position", "MF"), 9),
            p.get("shirt_no") if isinstance(p.get("shirt_no"), int) else 999,
            p.get("name_en", ""),
        )
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--merge-stdin", action="store_true", help="從 stdin 讀入賽後事件並合併")
    ap.add_argument("--recompute-only", action="store_true", help="只重算排行榜")
    args = ap.parse_args()

    doc = load_players()
    idx = index_by_id(doc)
    total_applied = 0

    if args.merge_stdin:
        raw = sys.stdin.read().strip()
        if not raw:
            sys.stderr.write("[ERROR] --merge-stdin 但 stdin 為空\n")
            sys.exit(1)
        payload = json.loads(raw)
        batches = payload if isinstance(payload, list) else [payload]
        for b in batches:
            total_applied += merge_match(
                doc, idx, b.get("match"), b.get("events", []), b.get("sources", [])
            )

    sort_players(doc)
    doc["last_updated"] = now_iso()
    with open(PLAYERS, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)

    lb = compute_leaderboards(doc)
    with open(LEADER, "w", encoding="utf-8") as f:
        json.dump(lb, f, ensure_ascii=False, indent=2)

    print(
        f"players.json: {len(doc['players'])} 人，本次新計入 {total_applied} 筆事件；"
        f"射手榜 {len(lb['scorers'])} 人，紀律榜 {len(lb['discipline'])} 人。"
    )


if __name__ == "__main__":
    main()
