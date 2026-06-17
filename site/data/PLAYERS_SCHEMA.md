# 球員資料 Schema（players.json）

世界盃 2026 球員介紹 + 本屆統計（進球、黃牌、紅牌）。所有使用者可見文字為繁體中文。

## 檔案位置

- 權威來源：`data/players.json`
- 同步到網站：`site/data/players.json`（由 `sync_to_site.py` 複製）
- 衍生排行：`data/leaderboards.json`（由 `update_players.py` 計算，含射手榜/紀律榜）

## players.json 結構

```json
{
  "tournament": "FIFA World Cup 2026",
  "last_updated": "2026-06-17T08:40:00Z",
  "note": "每隊重點球員（5-8 人）。統計為本屆累計，由定時任務每場賽後以 AI 研究權威來源更新。",
  "players": [
    {
      "id": "ARG-messi",                  // 唯一鍵：隊三碼-姓氏小寫（手動穩定）
      "name_en": "Lionel Messi",          // 英文全名
      "name_zh": "里安奴·美斯",            // 繁體中文譯名
      "team": "Argentina",                // 必須對應 fixtures groups 內的隊名
      "team_zh": "阿根廷",
      "position": "FW",                    // GK / DF / MF / FW
      "shirt_no": 10,                      // 球衣號碼（未知填 null）
      "age": 38,                           // 年齡（未知填 null）
      "club": "Inter Miami",              // 所屬俱樂部
      "is_key": true,                      // 是否重點球員（種子名單皆 true）
      "bio_zh": "繁體中文球員簡介，一段約 40-80 字，描述特點、角色、本屆看點。",
      "stats": {
        "goals": 0,                        // 本屆累計進球
        "yellow_cards": 0,                 // 本屆累計黃牌
        "red_cards": 0,                    // 本屆累計紅牌（含兩黃變一紅）
        "matches_with_events": []          // 已計入統計的場次編號陣列，用於冪等去重
      },
      "sources": []                        // 最近一次更新引用的來源 URL（選填）
    }
  ]
}
```

## 欄位規則

- **id**：全域唯一、永不變動，作為跨批次合併鍵。格式 `{隊三碼}-{姓氏}`，小寫，去除空白與特殊字元。
- **team**：必須與 `fixtures.json` 的 `groups` 隊名「完全一致」（英文），否則無法跨檔關聯。
- **position**：固定四類 `GK`/`DF`/`MF`/`FW`。
- **stats.matches_with_events**：冪等核心。`update_players.py` 只在「某場次尚未記入該球員」時才累加，避免重複統計。
- **bio_zh / name_zh / team_zh**：必須繁體中文。

## leaderboards.json 結構（衍生，勿手動編輯）

```json
{
  "last_updated": "2026-06-17T08:40:00Z",
  "scorers": [   // 射手榜：goals 由多到少，同分依紅黃牌少者優先，再依姓名
    { "id": "...", "name_zh": "...", "team_zh": "...", "position": "FW", "goals": 3, "yellow_cards": 0, "red_cards": 0 }
  ],
  "discipline": [ // 紀律榜：red 由多到少 → yellow 由多到少
    { "id": "...", "name_zh": "...", "team_zh": "...", "yellow_cards": 2, "red_cards": 1 }
  ],
  "totals": { "players": 0, "goals": 0, "yellow_cards": 0, "red_cards": 0 }
}
```

## 更新流程（併入 cron c53acfd7）

1. 定時任務在記錄完新賽果後，對「每場新完成比賽」用 Sonnet 4.6 研究子代理搜尋權威來源（官方/ESPN/賽事中心），找出該場進球者與紅黃牌名單。
2. 將結果以 JSON 餵入 `python3 update_players.py --merge-stdin`，腳本依 `id` 與 `matches_with_events` 冪等累加統計，並重算 `leaderboards.json`。
3. `sync_to_site.py` 一併複製 `players.json` 與 `leaderboards.json` 到 `site/data/`。

### update_players.py --merge-stdin 輸入格式

```json
{
  "match": 17,                 // 場次編號（冪等鍵）
  "events": [
    { "id": "FRA-mbappe", "goals": 2, "yellow_cards": 0, "red_cards": 0 },
    { "id": "SEN-koulibaly", "goals": 0, "yellow_cards": 1, "red_cards": 0 }
  ],
  "sources": ["https://...", "https://..."]
}
```

可一次傳入多場（陣列）。新球員若不在名單中，腳本會以 events 內附帶的 `name_zh/team/position` 等欄位自動新增（缺欄位則標 TBD）。
