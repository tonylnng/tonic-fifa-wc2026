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
    ],

    "benchmarks": [                               // 【新】公開基準線隱含機率（2-4 個），用於與 AI 並列對照與計分
      {
        "source": "博彩隱含機率",                  // 來源名（繁中）
        "kind": "betting",                         // betting | model | market | ai
        "win_prob": { "home": 0.79, "draw": 0.14, "away": 0.07 },  // 三向隱含機率，總和≈1
        "scoreline": "3:0",                        // 選填：該來源最可能比分
        "note": "主流博彩讓球與大小盤推導"          // 一句來源說明（繁中）
      },
      {
        "source": "Opta 超級電腦",
        "kind": "model",
        "win_prob": { "home": 0.74, "draw": 0.17, "away": 0.09 },
        "note": "Opta/ESPN Elo 等模型平均"
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
- `benchmarks[*].win_prob` 三向機率總和 ≈ 1.0；基準線數值須與 `key_factors` 輿論共識一致，不可自造。`compute_benchmark_scores.py` 會讀取這些基準線與 AI 並列計分。
- `kickoff_utc` 必須與 `fixtures.json` 對應場次一致。

## 賽後覆盤（postmortems.json）
結果出爐後，每場產生一筆覆盤，合併鍵為 (match, run_id)，寫入 `data/postmortems.json`。欄位：`match`、`home`、`away`、`stage`、`predicted`、`predicted_outcome`、`final`、`actual_outcome`、`outcome_correct`、`exact_correct`、`verdict`(exact/outcome/miss)、`run_id`、`model`、`headline`、`review`、`lessons`(陣列)、`vs_benchmarks`。以 `echo '<json>' | python3 build_postmortems.py --merge-stdin` 寫入。

## 校準與基準線計分
- `data/calibration.json`：由 `compute_calibration.py` 產生，信心分桶 vs 實際命中率，含 Brier、ECE、overconfidence。
- `data/benchmark_scores.json`：由 `compute_benchmark_scores.py` 產生，AI 與各基準線在相同已完成比賽上的排行榜。

## 頂層 benchmarks[] 與 consensus（第三方多模型 A+C）

除了 `prediction.benchmarks`（由 Opus 研究時寫入的博彩/模型/市場基準線）之外，`multimodel_predict.py` 會在預測檔的**頂層**寫入兩個欄位，供前端「模型共識」與「多模型對決」區使用：

```json
{
  // ...上述所有預測欄位...

  "benchmarks": [                               // 【頂層】所有基準線（betting/model/market + 第三方 ai）合並於此
    {
      "source": "博彩隱含機率",
      "kind": "betting",                          // betting | model | market | ai
      "win_prob": { "home": 0.95, "draw": 0.04, "away": 0.01 },
      "scoreline": "4:0",
      "note": "德國 1/25 至 1/20（隱含 95-97%）"
    },
    {
      "source": "MiniMax M3",                     // 第三方 AI
      "kind": "ai",
      "model_id": "minimax/minimax-m3",           // 【新】用於 AI 條目的 Gateway 模型 ID
      "win_prob": { "home": 0.92, "draw": 0.06, "away": 0.02 },
      "scoreline": "4:0",
      "note": "德國實力碾壓庫拉索，應輕鬆取勝。"   // 第三方只回「一句話 take」，不寫長篇理由
    }
    // 另 alibaba/qwen3.7-max、deepseek/deepseek-v4-pro、openai/gpt-5.1-thinking、
    // google/gemini-3.1-pro-preview、xai/grok-4.20-reasoning、zai/glm-4.7 同格式（共 7 家）
  ],

  "consensus": {                                  // 【新頂層】本站主預測 + 多家第三方的綜合共識
    "scoreline": "4:0",                           // 比分多數決（平手靠近主預測）
    "outcome": "home",
    "win_prob": { "home": 0.924, "draw": 0.056, "away": 0.02 },  // 加權平均（主預測權重 2，每個 AI 權重 1）
    "models_used": 8,                             // 參與共識的模型數（主預測 + 可用第三方；7 家全到齊為 8）
    "logic": "綜合 8 個模型（本站 Opus 4.8 + 7 家第三方）：勝率採主預測加權平均、比分採多數決。"  // 繁中一句綜合邏輯
  }
}
```

說明：
- **主預測仍為 Opus 4.8**；第三方 AI 僅作對照基準（`kind:"ai"`）。
- 頂層 `benchmarks[]` 依 `source` 去重；AI 條目多帶 `model_id`（Gateway 模型 ID）。第三方 `win_prob` 可能是整數（如 55/25/20），會被 sum-normalize 為總和 1。
- `consensus.win_prob` 由主預測（權重 2）與各 AI（權重 1）加權平均；`scoreline` 為多數決，平手時靠近主預測。
- `compute_benchmark_scores.py` 會把 `kind:"ai"` 條目一併納入基準線排行榜；若條目無 `outcome`，會由 `win_prob` argmax 推導。
