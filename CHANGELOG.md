# 變更紀錄 CHANGELOG

本檔記錄世界盃 2026 AI 預測中心的版本變更。所有時間以香港時間（HKT）為準。

格式參考 [Keep a Changelog](https://keepachangelog.com/)，版本依語意化版本號。

---

## [資料更新] 2026-06-16T0055Z 3 場冷門和局賽果 #13–#15 + 7 場新預測 #17–#23（HKT 6/16 上午）

### 新增（Added）

- 新增 3 場賽果（**均為冷門和局，AI 三場全數落空**）：#13 西班牙 0:0 佛得角（40 歲門將神撲）、#14 比利時 1:1 埃及（烏龍球扳平）、#15 沙烏地 1:1 烏拉圭（門將神勇）。三場賽後覆盤（postmortem）已生成，verdict 皆為 `miss`。
- 新增 7 場小組賽預測（Claude Opus 4.8 主預測，每場附 7 家第三方模型對照與共識 `models_used=8`）：#17 法國 2:1 主（共識 2:0）·#18 伊拉克 0:3 客（共識 0:2）·#19 阿根廷 2:0 主·#20 奧地利 2:0 主·#21 葡萄牙 2:0 主·#22 英格蘭 2:1 主·#23 迦納 2:1 主（信心 .46）。其中 #22、#23 為首次納入的新場次。
- 來源數：#17 (109)、#18 (104)、#19 (105)、#20 (110)、#21 (74)、#22 (71)、#23 (67)。近 36 小時內開賽者（#17–#20）≥100 處／場，其餘 48 小時窗口 ≥50 處／場。

### 變更（Changed）

- 指標重算（`accuracy.json`／`calibration.json`／`benchmark_scores.json`）：因新增三場失準結果，整體**勝負命中率降至 3/11（27.3%）**、比分完全命中 0/11、Brier 0.3135、ECE 0.3718（仍偏過度自信）。
- 同步至網站、Notion（資料庫新增 7 頁）與 GitHub。仍處小組賽，排程維持每 8 小時。
- 詳見 [`RELEASE_NOTES_2026-06-16T0055Z.md`](RELEASE_NOTES_2026-06-16T0055Z.md)。

---

## [資料更新] 2026-06-15T1710Z 新增 8 場小組賽預測 #14–#21（HKT 6/16 清晨）

### 新增（Added）

- 新增 8 場小組賽預測（Claude Opus 4.8 主預測，每場附 7 家第三方模型對照與共識 `models_used=8`）：#14 比利時 2:1 主·#15 沙烏地 0:2 客·#16 伊朗 2:0 主·#17 法國 2:1 主（共識 2:0）·#18 伊拉克 0:3 客（共識 0:2）·#19 阿根廷 2:0 主·#20 奧地利 2:0 主·#21 葡萄牙 2:0 主。
- 來源數：#14 (180)、#15 (166)、#16 (229)、#17 (109)、#18 (104)、#19 (105)、#20 (153)、#21 (63)。近 36 小時內開賽者 ≥100 處／場。
- 每場含 `top_scorelines`、`scenarios`、`prediction.benchmarks`（公開博彩／模型基準線）與繁中 `reasoning`。

### 變更（Changed）

- 指標重算（`accuracy.json`／`calibration.json`／`benchmark_scores.json`）：本批次比賽尚無結果，整體指標維持不變。
- 同步至網站、Notion（資料庫新增 8 頁）與 GitHub。仍處小組賽，排程維持每 8 小時。
- 詳見 [`RELEASE_NOTES_2026-06-15T1710Z.md`](RELEASE_NOTES_2026-06-15T1710Z.md)。

---

## [變更] 2026-06-16 第三方多模型對照擴充至 7 家（HKT 6/16 清晨）

### 新增（Added）

- 第三方對照新增 4 家最新模型（經 Vercel AI Gateway）：OpenAI GPT-5.1 Thinking、Google Gemini 3.1 Pro、xAI Grok 4.20 Reasoning、Z.ai GLM-4.7。連同原有 MiniMax M3／千問 Qwen3.7 Max／DeepSeek V4 Pro，第三方對照共 7 家；加上本站 Opus 4.8 主預測，綜合共識 `models_used` 最多達 8。

### 變更（Changed）

- `multimodel_predict.py`：`MODELS` 擴充為 7 家；`max_tokens` 600 → 3000（reasoning 模型 Gemini／GLM 需較大上限才能在推理後輸出 JSON）；新增退化防護（比分須符合 `^\d+:\d+$`，否則視同失敗）。
- 回填 #13–#20：對 8 場既有預測各跑一次七模型對照，重算頂層 `benchmarks`（kind=ai）與 `consensus`。主 Opus 預測維持不變。回填後共識：#13 西班牙 3:0 · #14 比利時 2:0 · #15 沙烏地 0:2 客 · #16 伊朗 2:0 · #17 法國 2:0 · #18 伊拉克 0:2 客 · #19 阿根廷 2:0 · #20 奧地利 2:0。
- 文檔同步更新：`PREDICTION_METHODOLOGY.md`、`README.md`（§預測方法）、`data/predictions/SCHEMA.md`、`CRON_RUNBOOK.md` 全部改為 7 家模型、`max_tokens 3000`；前端 `PredictionCard` 對照說明列出 7 家來源。
- 指標重算（`accuracy.json`／`calibration.json`／`benchmark_scores.json`）。新增 4 家模型僅出現在尚無結果的 #13–#20，待相關比賽結束後才納入對照排行榜。
- 詳見 [`RELEASE_NOTES_2026-06-16-multimodel-7.md`](RELEASE_NOTES_2026-06-16-multimodel-7.md)。

---

## [文件] 2026-06-15 新增預測方法說明（HKT 6/15 晚間）

### 新增（Added）

- 新增 [`PREDICTION_METHODOLOGY.md`](PREDICTION_METHODOLOGY.md)：完整預測方法說明，涵蓋主預測引擎（Claude Opus 4.8、來源數分級、關鍵因素、輸出欄位）、第三方多模型對照與共識算法、賽後覆盤、評分與校準機制、設計原則。

### 變更（Changed）

- `README.md` 新增「預測方法（Prediction Methodology）」章節，摘要整條預測與評分邏輯並連結至完整文件；檔案索引表加入 `PREDICTION_METHODOLOGY.md`。

---

## [資料更新] 2026-06-15T0904Z 預測批次（HKT 6/15 下午）

### 新增（Added）— 第 13–20 場小組賽預測（8 場，主模型 Claude Opus 4.8）

- 對即將開賽的 8 場小組賽（#13–#20）產生全新預測批次 `2026-06-15T0904Z`，獨立寫入 `site/data/predictions/match_{13..20}__2026-06-15T0904Z.json`，不覆蓋舊批次。
  - #13 西班牙 3:0 佛得角（信心 0.81，122 源）· #14 比利時 2:1 埃及（0.58，180）· #15 沙烏地阿拉伯 0:2 烏拉圭（0.63，166）· #16 伊朗 2:0 紐西蘭（0.60，229）
  - #17 法國 2:1 塞內加爾（0.60，134）· #18 伊拉克 0:2 挪威（0.78，89）· #19 阿根廷 2:0 阿爾及利亞（0.73，97）· #20 奧地利 2:0 約旦（0.60，55）
  - 來源數分級：近 36h 內開賽者每場 ≥100 源；其餘 48h 窗口每場 ≥50 源。
- 每場預測檔均附**第三方多模型對照**（MiniMax M3／Qwen3.7 Max／DeepSeek V4 Pro）與**頂層共識**。

### 新增（Added）— 1 場比賽結果與 Opus 賽後覆盤

- #12 瑞典 **5:1** 突尼西亞（Ayari 7'&90+6'、Isak 30'、Gyökeres 59'、Svanberg 84'；突尼西亞 Rekik 43'）。原預測 1:0 主勝 → 方向正確、比分大幅偏保守。
- 附 Claude Opus 4.8 繁中賽後覆盤，合併寫入 `postmortems.json`。

### 變更（Changed）— 指標重算

- `accuracy.json`：已評估 8 場，勝負方向 **3/8（37.5%）**、正確比分 **0/8**。
- `calibration.json`：**Brier 0.2436、ECE 0.29、過度自信 0.2625**。
- `benchmark_scores.json`：9 條基準線、涵蓋 8 場（本站 Opus 3/8、Brier 0.2436；MiniMax 3/4；DeepSeek 3/4；Qwen 2/4；Football Meister AI 1/1；博彩 1/4；Opta 1/4；Polymarket 0/1；Kalshi 0/1）。

---

## [資料更新] 2026-06-15T0855Z 預測批次（HKT 6/15 下午）

### 新增（Added）— 第 12–19 場小組賽預測（8 場，主模型 Claude Opus 4.8）

- 對即將開賽的 8 場小組賽（#12–#19）產生全新預測批次 `2026-06-15T0855Z`，獨立寫入 `site/data/predictions/match_{12..19}__2026-06-15T0855Z.json`，不覆蓋舊批次。
  - #12 瑞典 1:0 突尼西亞（信心 0.57，155 源）· #13 西班牙 3:0 佛得角（0.80，106）· #14 比利時 2:1 埃及（0.58，180）· #15 沙烏地阿拉伯 0:2 烏拉圭（0.63，155）
  - #16 伊朗 1:0 紐西蘭（0.60，216）· #17 法國 2:1 塞內加爾（0.60，57）· #18 伊拉克 0:2 挪威（0.78，92）· #19 阿根廷 2:0 阿爾及利亞（0.74，92）
  - 來源數分級：#12–#16 在 36h 內開賽（≥100 源）；#17–#19 在 48h 窗口（≥50 源）。
- 每場預測檔均附**第三方多模型對照**（MiniMax M3／Qwen3.7 Max／DeepSeek V4 Pro）與**頂層共識**。

### 新增（Added）— 3 場比賽結果與 Opus 賽後覆盤

- #9 德國 **7:1** 庫拉索（方向正確、比分偏保守）· #10 荷蘭 **2:2** 日本（逼和 dissent 兌現）· #11 象牙海岸 **1:0** 厄瓜多爾（90' 絕殺，原 1:1 和局落空）。
- 三場各附 Claude Opus 4.8 繁中賽後覆盤，合併寫入 `postmortems.json`。

### 變更（Changed）— 指標重算

- `accuracy.json`：已評估 7 場，勝負方向 **2/7（28.6%）**、正確比分 **0/7**。
- `calibration.json`：**Brier 0.2455、ECE 0.3929、過度自信 0.3614**。
- `benchmark_scores.json`：9 條基準線、涵蓋 7 場（本站 Opus 2/7；MiniMax 2/3；DeepSeek 2/3；Qwen 1/3；Football Meister AI 1/1；博彩 1/4；Opta 1/4）。

---

## [資料更新] 2026-06-14T1655Z 預測批次（HKT 6/15 凌晨）

### 新增（Added）— 第 9–16 場小組賽預測刷新（全部 36h 內開賽，皆 ≥100 源）

- 以 **Claude Opus 4.8** 為本站主預測，對即將開賽的 8 場小組賽（#9–#16）產生全新預測批次 `2026-06-14T1655Z`，獨立寫入 `site/data/predictions/match_{9..16}__2026-06-14T1655Z.json`，不覆蓋舊批次。
  - #9 德國 4:0 庫拉索（信心 0.89，144 源）· #10 荷蘭 2:1 日本（0.56，133）· #11 象牙海岸 1:1 厄瓜多爾（0.42，148）· #12 瑞典 1:0 突尼西亞（0.57，135）
  - #13 西班牙 3:0 佛得角（0.86，140）· #14 比利時 2:1 埃及（0.58，164）· #15 沙烏地阿拉伯 0:2 烏拉圭（0.63，135）· #16 伊朗 1:0 紐西蘭（0.60，189）
  - 8 場皆落在觸發後 36 小時內開賽，故每場來源數 ≥100。
- 每場預測檔均附**第三方多模型對照**（MiniMax M3／Qwen3.7 Max／DeepSeek V4 Pro）與**頂層共識**；#15 DeepSeek 回傳格式異常已自動略過（以 2 個 AI 完成對照）。
- 重算 `accuracy.json`、`calibration.json`（Brier 0.3386、ECE 0.415）、`benchmark_scores.json`（6 基準線、4 場）。
- 本批次無新完成比賽：#9 觸發時剛開賽進行中，餘場未開賽；已嚴格排除網路上 AI 捏造的「賽後比分」偽結果。

### 移除（Removed）

- 清除誤入 `data/predictions/` 與 `site/data/predictions/` 的子代理建置腳本（`build_*.py`／`gen_*.py`／`_*.py`），保持資料目錄純淨。

---

## [資料更新] 2026-06-14T0855Z 預測批次（HKT 6/14 下午）

### 新增（Added）— 第 9–16 場小組賽預測刷新

- 以 **Claude Opus 4.8** 為本站主預測，對即將開賽的 8 場小組賽（#9–#16）產生全新預測批次 `2026-06-14T0855Z`，獨立寫入 `site/data/predictions/match_{9..16}__2026-06-14T0855Z.json`，不覆蓋舊批次。
  - #9 德國 4:0 庫拉索（信心 0.89，137 源）· #10 荷蘭 2:1 日本（0.55，116）· #11 象牙海岸 1:1 厄瓜多爾（0.43，139）· #12 瑞典 1:0 突尼西亞（0.56，111）
  - #13 西班牙 3:0 佛得角（0.85，128）· #14 比利時 2:1 埃及（0.61，121）· #15 沙烏地阿拉伯 0:2 烏拉圭（0.63，70）· #16 伊朗 1:0 紐西蘭（0.50，67）
  - 36 小時內開賽場次（#9–#14）來源數 ≥100；其餘 48 小時窗口場次（#15–#16）≥50。
- 每場預測檔均附**第三方多模型對照**（MiniMax M3／Qwen3.7 Max／DeepSeek V4 Pro，僅比分＋三向勝率＋一句話 take）與**頂層共識**，第三方僅作對照，主預測仍為 Opus 4.8。
- 重算 `accuracy.json`、`calibration.json`、`benchmark_scores.json`（已評估 4 場，維持不變）。

### 移除（Removed）

- 清除誤入 `site/data/predictions/` 的子代理建置腳本（`_*.py`），保持資料目錄純淨。

---

## [1.5.0] — 2026-06-14

### 變更（Changed）— 全站即時讀取按鈕移至頭部條

1. **後端新端點 `/api/live-all`**（`site/server/routes.ts`）
   - 一次並行抓取 GitHub raw 上**所有資料集**：`results`、`accuracy`、`calibration`、`postmortems`、`benchmark_scores`、`fixtures`，以及全部 `predictions`（先讀 `predictions/manifest.json` 取得檔案清單再並行抓取）。
   - predictions 依場次分組、依 `run_timestamp` 由新到舊排序，與 `/api/predictions` 一致。
   - 沿用 **60 秒快取**（`liveAllCache` / `LIVE_TTL_MS`）與 6 秒逾時保護（AbortController）；任一抓取失敗即整體回退本機打包資料並標明 `source`（`github` ／ `local-fallback`）。

2. **頭部條全站即時讀取按鈕**（`site/client/src/components/Header.tsx`）
   - 「即時讀取最新」按鈕移至頁面**頭部條**，**每一個分頁皆可見**（不再只限結果分頁）。
   - 來源／時間徽章：GitHub 即時 ／ 讀取失敗·本機；載入時 `RefreshCw` 圖示旋轉。

3. **點擊一鍵更新全站**（`site/client/src/pages/dashboard.tsx`）
   - 點擊後查詢 `/api/live-all`，並以結果回填（seed）所有相關 query 快取：`/api/fixtures`、`/api/predictions`、`/api/results`、`/api/accuracy`、`/api/calibration`、`/api/postmortems`、`/api/benchmark-scores`，再使 `/api/status` 失效。
   - **每一個分頁同步顯示 GitHub 最新內容**，不必等待下一次重新發布。
   - 移除結果分頁專屬的舊「即時讀取」控制卡（功能整併至頭部）。

4. **預測檔清單 `manifest.json`**（`sync_to_site.py`）
   - `sync_to_site.py` 同步時自動產生 `site/data/predictions/manifest.json`（列出全部 `match_*.json` 檔名），供前端／`/api/live-all` 在 GitHub raw 上枚舉預測檔（raw 無目錄列舉能力）。
   - `/api/predictions` 與 `/api/status` 掃描預測目錄時忽略 `manifest.json`。

---

## [1.4.0] — 2026-06-14（run 2026-06-14T0551Z）

### 新增（Added）— 即時讀取 GitHub 最新結果

1. **後端新端點 `/api/live-results`**（`site/server/routes.ts`）
   - 即時抓取 GitHub raw（`https://raw.githubusercontent.com/tonylnng/tonic-fifa-wc2026/master/site/data/results.json`）的最新比賽結果，不需等待網站重新發布。
   - 內建 **60 秒快取**（`liveCache` / `LIVE_TTL_MS`），避免每次請求都打 GitHub；6 秒逾時保護（AbortController）。
   - 回傳完整結果物件 ＋ `source`（`github` ／ `local-fallback`）＋ `cached` 旗標；GitHub 讀取失敗時自動回退本機打包資料並標明來源。

2. **前端「即時讀取」控制卡**（`site/client/src/pages/dashboard.tsx`）
   - 結果頁新增手動「即時讀取 GitHub 最新結果」按鈕（`RefreshCw` 圖示），點擊後查詢 `/api/live-results`。
   - 狀態徽章：GitHub 即時 ／ 快取 ／ 回退本機 ／ 本機打包，並以**香港時間**顯示資料更新時間（`hktTimestamp()` 輔助函式）。
   - 有即時資料時優先顯示 GitHub 最新結果（`active = live ?? results`），否則使用本機打包資料。

### 新增（Added）— 賽後覆盤改用 Opus 4.8

- 賽後覆盤（postmortems）生成模型由先前流程改為 **Claude Opus 4.8**（與本站主預測一致），確保覆盤分析品質一致。

### 資料更新（Data）

- 新增第 7、8 場最終比分：第 7 場 海地 0:1 蘇格蘭（蘇格蘭勝）、第 8 場 澳洲 2:0 土耳其（澳洲勝，爆冷）。`results.json` 現含 8 場結果。
- 第 7、8 場 Opus 4.8 賽後覆盤（run 2026-06-14T0057Z）：第 7 場勝負命中、比分失準；第 8 場爆冷失準。`postmortems.json` 現含第 5、6、7、8 場共 4 份覆盤。
- 第 9–16 場全新 Opus 4.8 預測（run 2026-06-14T0551Z），含 top_scorelines／scenarios／頂層 benchmarks（含第三方 AI MiniMax／千問／DeepSeek）／consensus，並已同步至 Notion。
- 重算 accuracy／calibration／benchmark_scores（已評估 4 場，勝負 1/4、比分 0/4、Brier 0.3386、ECE 0.415）。

---

## [1.3.0] — 2026-06-14（run 2026-06-14T0057Z）

### 新增（Added）— 第三方多模型 AI 對照 ＋ 綜合共識

本站主預測維持 **Claude Opus 4.8**；新增三家第三方 AI 作為對照基準，並產生跨模型「綜合共識」。

1. **第三方多模型對照（Benchmarks · kind=ai）**
   - 新增 `multimodel_predict.py`：讀取該場最新批次預測檔，經 [Vercel AI Gateway](https://vercel.com/docs/ai-gateway) 同時呼叫三家最新模型——`minimax/minimax-m3`（MiniMax M3）、`alibaba/qwen3.7-max`（千問 Qwen3.7 Max）、`deepseek/deepseek-v4-pro`（DeepSeek V4 Pro）。
   - 每家只回傳「**比分 ＋ 三向勝率 ＋ 一句話 take**」（不寫長篇理由，省用量），以 `kind:"ai"` ＋ `model_id` 追加到預測檔的**頂層** `benchmarks[]`（依 `source` 去重，保留既有 betting／model／market 條目）。
   - SSL 相容性：透過 `curl --cacert /etc/ssl/certs/agent-proxy-ca-2.pem` 子程序呼叫 Gateway（代理環境下 Python `requests`／`urllib` 會 SSL 失敗）。
   - 容錯：任一模型逾時／失敗即略過，其餘照常寫入。

2. **跨模型綜合共識（Consensus）**
   - 新增頂層 `consensus` 欄位：比分採多數決（平手靠近主預測）、勝率採加權平均（主預測 Opus 4.8 權重 2、每個第三方 AI 權重 1），並附繁中一句綜合邏輯。

3. **前端「模型共識」＋「多模型對決」區**
   - `PredictionCard` 新增 `ConsensusBlock`（顯示綜合共識比分／勝負／三向勝率）。
   - 「多模型對決（本站 Opus 4.8 vs 第三方 AI vs 市場/超級電腦）」區並列本站、第三方 AI、博彩、超級電腦、預測市場各自的比分與勝率條，附一句來源說明。
   - `lib/types.ts`：`Benchmark.kind` 加入 `"ai"`、`outcome` 改為選填、新增 `model_id`；新增 `Consensus` 介面與 `Prediction.consensus`。

4. **計分整合**
   - `compute_benchmark_scores.py` 把 `kind:"ai"` 條目一併納入基準線排行榜；條目無 `outcome` 時由 `win_prob` argmax 推導，賽後可在「校準與基準」頁比較本站與第三方 AI 誰更準。

### 憑證（Credentials）

- Vercel AI Gateway 金鑰存於使用者**憑證庫**（vault），供排程跨工作階段重用；腳本以 `api_credentials=["custom-cred:ai-gateway.vercel.sh"]` 取用，金鑰不落地、不入庫於 repo。

### 文檔（Docs）

- `CRON_RUNBOOK.md` 新增「2.5 第三方多模型 AI 對照 + 共識」步驟。
- `site/data/predictions/SCHEMA.md` 新增「頂層 benchmarks[] 與 consensus」章節（含 `kind:"ai"`、`model_id`、`consensus` 結構與一致性規則）。
- `README.md` 更新「這個項目包含什麼」，標註多模型對照與共識。

---

## [1.2.0] — 2026-06-14

### 重大修正（Fixed）

- **修正全部 104 場賽事開賽時間**：先前 `build_fixtures.py` 內建的本地開賽時間基準值有誤（例如第 1 場 MEX–RSA 誤存 16:00、應為墨西哥城 13:00；第 8 場 AUS–TUR 誤存溫哥華 06-14 04:00、實際為太平洋時間 6/13 晚 9 點＝UTC 6/14 04:00），導致 `kickoff_utc` 連帶全部偏移。前端倒數與「進行中」標記因此顯示錯誤。
  - 新增 `fix_fixture_times.py`：以權威來源 [fixturedownload.com](https://fixturedownload.com/feed/json/fifa-world-cup-2026) 校正。小組賽以隊伍對戰組合比對、淘汰賽（73–104）以內部 match# 比對，重算 `kickoff_utc` 並回推正確本地日期與時間。
  - 隊名別名對應：turkey→turkiye、ivory coast→cote divoire、south korea→korea republic、czech republic→czechia、dr congo→congo dr、cape verde→cabo verde、ir iran→iran。
  - 同步修正全部 24 個預測檔內的 `kickoff_utc` 去正規化副本（預測內容本身未更動）。
  - 於 `build_fixtures.py` 加上警告註解，指向 `fix_fixture_times.py`。
  - 已上線驗證：第 8 場澳洲顯示「進行中」、第 9 場德國「11 小時後」、第 13 場西班牙「1 天 10 小時後」皆正確。

### 新增（Added）— 四項進階功能

1. **賽前倒數 ＋ 即將開賽標記**
   - `utils.ts` 新增 `countdown()`；`PredictionCard` 加入 `CountdownBadge` 與 `useNow` 即時刷新。
   - 儀表板排序改為：進行中 → 最快開賽 → 已完成 → 已過往，把近賽置頂。

2. **校準曲線（Calibration）**
   - 新增 `compute_calibration.py`，依信心分桶計算命中率，輸出 `data/calibration.json`（含 Brier score、ECE、過度自信指標）。
   - 新增前端 `CalibrationTab.tsx`，以 recharts 繪製可靠度圖（reliability diagram）。
   - 新增「校準與基準」分頁。

3. **對比基準線（Benchmarks）**
   - `backfill_benchmarks.py` 為預測補上 `benchmarks[]`（博彩／模型／市場／AI 各自隱含勝率）。
   - 新增 `compute_benchmark_scores.py`，輸出 `data/benchmark_scores.json`（各基準線 Brier 計分排行榜）。
   - `PredictionCard` 新增基準線並列顯示。
   - schema 同步擴充（見 `site/data/predictions/SCHEMA.md`）。

4. **賽後自動覆盤（Postmortems）**
   - 新增 `build_postmortems.py`（支援 `--merge-stdin`，鍵＝match＋run_id，不覆蓋舊批次），輸出 `data/postmortems.json`。
   - 新增前端 `PostmortemsTab.tsx`，可搜尋／篩選賽後覆盤。
   - 新增「賽後覆盤」分頁。

### API 端點（Added）

- 新增 `/api/calibration`、`/api/postmortems`、`/api/benchmark-scores` 三個唯讀端點（`site/server/routes.ts`）。

### 文件（Changed）

- `CRON_RUNBOOK.md`：新增 benchmarks／覆盤／calibration 計算與同步步驟。
- `site/data/predictions/SCHEMA.md`：記錄 `benchmarks` 欄位、postmortems、calibration 結構。
- `README.md`：更新「包含什麼」清單（新資料檔、新腳本、新功能、無密碼公開）。
- `push_to_github.py`：同步階段一併複製 `calibration.json`／`postmortems.json`／`benchmark_scores.json`。

---

## [1.1.0] — 2026-06-14（run 2026-06-14T0111Z）

### 新增

- 香港時間開賽顯示。
- Top 比分機率（`top_scorelines`）。
- 多情境預測（`scenarios`）。
- 預測排程改用 Claude Opus 4.8；來源數分級（近 36 小時內 ≥100 處、48 小時窗 ≥50 處）。

---

## [1.0.0] — 初版

- 全自動 FIFA 世界盃 2026 賽事預測系統：雲端研究 → X:X 比分預測 ＋ 理由 → 推送 GitHub ／同步 Notion ／發布 pplx.app。
- 自架版（Docker ＋ Nginx ＋ Certbot）零運算負擔同步展示。
- 全繁體中文介面，比賽時間一律香港時間。
