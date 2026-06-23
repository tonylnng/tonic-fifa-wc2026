# To-Do（暫緩 / On Hold — 未經指示不要執行）

## 任務：預測覆盤稽核頁（Prediction Audit Page）

**狀態：** ⏸️ On hold — 使用者明確指示「先不要做」。等使用者下令啟動才執行。

**登記時間：** 2026-06-23 09:28 HKT

### 目標
比對「過去 72 小時內最嚴重的 3 個 AI 預測失誤」，對照實際比賽影像與賽後專家分析，判定每個失誤的根因屬於下列哪一類：
1. 缺漏傷兵資料（missing injury data）
2. 過度依賴單一媒體來源（over-reliance on a specific media outlet）
3. 博彩賠率權重失當（faulty betting odds weighting）

### 產出
- 一頁式報告（one-page report），用於調整淘汰賽（knockout rounds）的框架權重。
- 每個失誤需含：實際比分 vs 預測、根因分類、佐證（影像/專家分析來源連結）、對應的權重調整建議。

### 啟動時的資料來源（備忘）
- 預測批次：data/predictions/match_{N}__{run_id}.json
- 實際結果：data/results.json（最近 72h 完結比賽）
- 賽後覆盤：data/postmortems（既有 headline/review/lessons/vs_benchmarks/verdict）
- 基準對照：compute_benchmark_scores.py 產出的逐場明細
- 失誤排序：以 outcome 未命中 + 信心度高者優先（信心高卻錯 = 最嚴重）
- 框架權重調整對象：淘汰賽 R32+ 的 prediction 流程

### 備註
- 所有使用者可見內容：繁體中文；比賽時間：香港時間（HKT）。
- 「實際比賽影像」可能需要影片/新聞來源檢索（YouTube/ESPN/官方）佐證。
