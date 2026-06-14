# 變更紀錄 CHANGELOG

本檔記錄世界盃 2026 AI 預測中心的版本變更。所有時間以香港時間（HKT）為準。

格式參考 [Keep a Changelog](https://keepachangelog.com/)，版本依語意化版本號。

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
