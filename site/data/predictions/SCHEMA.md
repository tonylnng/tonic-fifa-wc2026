# Prediction JSON Schema

Each prediction run writes ONE file per match per run:
`data/predictions/match_{NUM}__{RUN_TIMESTAMP}.json`

Every run is preserved independently (never overwritten) so accuracy can be
re-evaluated against the latest pre-match prediction and the whole reasoning
trail is auditable.

```json
{
  "match": 9,
  "stage": "Group E",
  "home": "Germany",
  "away": "Curacao",
  "kickoff_utc": "2026-06-14T22:00:00Z",        // ISO 8601 UTC（由 fixtures.json 帶入；前端統一轉 HKT 顯示）
  "kickoff_hkt": "2026-06-15 06:00",            // 香港時間（純顯示用，選填）
  "run_id": "2026-06-14T0057Z",
  "run_timestamp": "2026-06-14T00:57:00Z",
  "model": "claude-opus-4.8",                    // 排程預測使用 Opus 4.8
  "prediction": {
    "score": { "home": 4, "away": 0 },          // 主預測（最可能比分）
    "scoreline": "4:0",
    "outcome": "home",                           // home | draw | away
    "win_prob": { "home": 0.93, "draw": 0.05, "away": 0.02 },
    "confidence": 0.88,                           // 0..1 對主預測的自評信心

    "top_scorelines": [                           // 【新】多個可能比分 + 各自機率（3-5 個，機率由高到低）
      { "scoreline": "4:0", "prob": 0.18 },
      { "scoreline": "3:0", "prob": 0.16 },
      { "scoreline": "2:0", "prob": 0.14 },
      { "scoreline": "5:0", "prob": 0.10 },
      { "scoreline": "3:1", "prob": 0.08 }
    ],

    "scenarios": [                                // 【新】多情境/多角度預測（2-4 個），各自比分+勝負+信心
      {
        "name": "模型共識",                        // 例：模型共識 / 博彩盤口 / 保守防守 / 進攻火力
        "scoreline": "4:0",
        "outcome": "home",
        "confidence": 0.9,
        "basis": "Opta/ESPN Elo 等超級電腦平均"     // 此情境的依據（繁中，一句）
      },
      {
        "name": "博彩盤口",
        "scoreline": "3:0",
        "outcome": "home",
        "confidence": 0.85,
        "basis": "主流博彩讓球與大小盤隱含比分"
      },
      {
        "name": "保守情境",
        "scoreline": "2:0",
        "outcome": "home",
        "confidence": 0.6,
        "basis": "古拉索深度防守、德國開幕場慢熱"
      }
    ]
  },
  "reasoning": {
    "summary": "Short 2-3 sentence rationale in Traditional Chinese.",
    "key_factors": [
      "球員狀態：...",
      "傷停名單：...",
      "近期狀態/戰績：...",
      "戰術對位：...",
      "主客場/場地：...",
      "輿論共識：..."
    ],
    "consensus_lean": "home",
    "dissent": "Notable contrarian view, if any."
  },
  "sources": [
    { "type": "official", "name": "FIFA.com", "url": "..." },
    { "type": "forum", "name": "r/worldcup", "url": "..." },
    { "type": "kol", "name": "...", "url": "..." },
    { "type": "youtube", "name": "...", "url": "..." },
    { "type": "media", "name": "ESPN", "url": "..." }
  ],
  "source_count": 105
}
```

## 來源數目標
- **近 36 小時內開賽的比賽：≥100 處來源**
- 其餘即將開賽（48h 窗口內）比賽：≥50 處來源

## Source mix target
- Official: FIFA, federations, club/national team sites
- Media: ESPN, BBC, Goal, Sky, Athletic, AS, Marca, etc.
- Betting/model: Opta, FiveThirtyEight-style, odds aggregators
- Forums/Community: Reddit, sports forums
- KOL / Pundits: named analysts, ex-players
- YouTube: preview/analysis videos

## Source type taxonomy
`official | media | model | betting | forum | kol | youtube | social`

## 欄位一致性規則
- `top_scorelines` 機率總和不必等於 1（只是前幾個最可能比分）；`prediction.scoreline` 應等於 `top_scorelines[0].scoreline`。
- `scenarios[0]` 通常對應主預測（同 `prediction.scoreline`）。
- `win_prob` 三向機率總和 = 1.0。
- `kickoff_utc` 必須與 `fixtures.json` 對應場次一致。
