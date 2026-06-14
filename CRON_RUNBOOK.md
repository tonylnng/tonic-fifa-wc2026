# 世界盃 2026 AI 預測 — 自動排程執行手冊 (Cron Runbook)

每次排程觸發時，依序執行以下步驟。所有使用者可見文字必須為繁體中文。

## 0. 環境
- 專案根目錄：`/home/user/workspace/wc2026/`
- 資料目錄：`data/`（fixtures.json, results.json, accuracy.json, predictions/）
- 網站目錄：`site/`（部署用）
- Notion 設定：`notion_config.json`（data_source_id: 112974c5-2bbd-4e5e-b3b7-28fd2ed96b6a）
- GitHub 同步站：`/home/user/workspace/wc2026/gitsync/`（已 clone 自 private repo tonylnng/tonic-fifa-wc2026，remote=origin）
- pplx.app 發布：site_id `7674b33b-8ee7-4c42-8d99-e3df659afaed`，網址 https://tonic-fifa-wc2026.pplx.app

## 1. 判斷階段與即將開賽的比賽
- 讀取 `data/fixtures.json`，找出當前時間之後 48 小時內、且尚未有結果（results.json 無紀錄）的比賽。
- 若已進入 16 強（任何 stage 為 "Round of 16" 之後的比賽即將開賽），代表進入 4 小時排程。

## 2. 收集最新情況 + 產生預測

**預測使用模型：Anthropic Claude Opus 4.8。** 研究子代理請以 `run_subagent(..., model="claude_opus_4_8")` 啟動，並在每個預測檔的 `model` 欄位填 `"claude-opus-4.8"`。

**來源數要求（依開賽時間分級）：**
- **近 36 小時內開賽**的比賽：**收集最少 100 處來源**（≥100）。
- 其餘 48h 窗口內比賽：最少 50 處來源（≥50）。
（以 `fixtures.json` 的 `kickoff_utc` 對比觸發時間判斷是否落在 36h 內。）

對每場即將開賽的比賽，研究最新情報（球員狀態、傷兵、評論員意見、官方、論壇、社群、KOL、YouTube、博彩、模型），產生：
- `kickoff_utc`：由 `fixtures.json` 對應場次帶入（ISO 8601 UTC）；另可填 `kickoff_hkt`（香港時間，純顯示）。
- `prediction.score` {home, away}、`scoreline` "X:X"、`outcome`(home/draw/away)
- `win_prob` {home, draw, away}（總和=1）、`confidence`(0-1)
- **`prediction.top_scorelines`**：3-5 個最可能比分 + 各自機率，機率由高到低；第一個須等於主 `scoreline`。
- **`prediction.scenarios`**：2-4 個多角度情境（如「模型共識／博彩盤口／保守情境／進攻火力」），每個含 `name`、`scoreline`、`outcome`、`confidence`、`basis`（繁中一句依據）。
- **`prediction.benchmarks`**：2-4 個公開基準線的隱含機率，用於與 AI 並列對照與計分。每個含 `source`（如「博彩隱含機率」「Opta 超級電腦」「Kalshi 預測市場」）、`kind`（betting/model/market/ai）、`win_prob`{home,draw,away}（總和≈1）、可選 `scoreline`、`note`（繁中一句來源說明）。基準線數值由研究時蒐集到的博彩盤口、Opta／超級電腦、預測市場等推導，**務必與該場 `key_factors` 中的輿論共識一致**。
- `reasoning.summary`（繁體中文，詳細）、`key_factors`（繁體中文清單）、`consensus_lean`、`dissent`
- `sources`（≥50 或 ≥100，含 url/type）、`source_count`
- `run_id` = 觸發時的 UTC 時間戳，格式 `YYYY-MM-DDTHHMMZ`
- 寫入 `data/predictions/match_{N}__{run_id}.json`（**獨立保存，不覆蓋舊批次**）

所有使用者可見文字（summary/key_factors/scenarios.basis 等）必須**繁體中文**。比賽時間一律以**香港時間**為準呈現（前端由 `kickoff_utc` 自動轉換）。

範本見 `data/predictions/SCHEMA.md`。

## 3. 更新已完成比賽的結果 + 賽後覆盤
- 搜尋是否有新完成的比賽，將最終比分寫入 `data/results.json`（results 陣列，含 match, scoreline, home, away, date）。
- **對每場新出爐結果，產生賽後覆盤 postmortem**（用 Opus 4.8，繁體中文）：比對該場最新批次預測與實際比分，生成「為何命中／失準」短評。每筆含 `match`、`home`、`away`、`stage`、`predicted`、`predicted_outcome`、`final`、`actual_outcome`、`outcome_correct`、`exact_correct`、`verdict`(exact/outcome/miss)、`run_id`、`model`、`headline`（繁中標題一句）、`review`（繁中詳述）、`lessons`（繁中清單）、`vs_benchmarks`（繁中：AI 與基準線相比的優劣）。以 stdin 合併寫入：
```bash
echo '<postmortem json 物件或陣列>' | python3 /home/user/workspace/wc2026/build_postmortems.py --merge-stdin
```
  合併鍵為 (match, run_id)，不會覆蓋既有不同場次的覆盤。

## 4. 重算準確率、校準與基準線計分
```bash
python3 /home/user/workspace/wc2026/update_accuracy.py
python3 /home/user/workspace/wc2026/compute_calibration.py
python3 /home/user/workspace/wc2026/compute_benchmark_scores.py
```
- `update_accuracy.py`：勝負／比分命中率（由 results.json 的 scoreline 比對各場最新批次預測）。
- `compute_calibration.py`：把預測信心分桶，對比實際命中率，輸出 `data/calibration.json`（含 Brier、ECE、過度自信 overconfidence）。
- `compute_benchmark_scores.py`：在相同已完成比賽上，把 AI 與各 `benchmarks` 來源並列計分（勝負命中、比分命中、Brier），輸出 `data/benchmark_scores.json` 排行榜。

## 5. 同步資料到網站目錄
```bash
python3 /home/user/workspace/wc2026/sync_to_site.py
```
（會一併複製 fixtures/results/accuracy/predictions 以及 `calibration.json`、`postmortems.json`、`benchmark_scores.json`。）

## 6. 同步到 Notion
- 對每場新預測，呼叫 `notion-create-pages`（parent.data_source_id = 112974c5-2bbd-4e5e-b3b7-28fd2ed96b6a）。
- 屬性對應見 `notion_config.json`。
- 已完成比賽：更新該場最新預測頁的「最終比分/勝負命中/比分命中」。
- 可用 `build_notion_pages.py` 產生頁面屬性。

## 7. 推送 data/ 到 GitHub（供使用者自架伺服器 git pull）
在同一個 bash 呼叫使用 `api_credentials=["github"]` 執行：
```bash
python3 /home/user/workspace/wc2026/push_to_github.py
cd /home/user/workspace/wc2026/gitsync && git push -q origin master
```
`push_to_github.py` 會把工作區最新的 `data/`（fixtures/results/accuracy + 全部 predictions 批次）複製進 gitsync repo 並 commit；若無變更會印出 `NOCHANGE` 並跳過。push 需帶 github 憑證。

## 8. 重新建置並重新發布 pplx.app 網站（僅 foreground 排程可用）
```bash
cd /home/user/workspace/wc2026/site && npm run build
```
然後依序：
1. `deploy_website(project_path="/home/user/workspace/wc2026/site/dist/public", site_name="世界盃 2026 AI 預測中心", entry_point="index.html")`
2. `publish_website(project_path="/home/user/workspace/wc2026/site", dist_path="/home/user/workspace/wc2026/site/dist/public", run_command="NODE_ENV=production node dist/index.cjs", install_command="npm ci --omit=dev", port=5000, app_name="世界盃 2026 AI 預測中心", site_id="7674b33b-8ee7-4c42-8d99-e3df659afaed")`
   - 注意：必須沿用 site_id `7674b33b-8ee7-4c42-8d99-e3df659afaed` 才會更新同一個 tonic-fifa-wc2026.pplx.app，而非建立新站。
   - 若最近一次 deploy_website 輸出已不含 site_id/app_slug（代表使用者手動取消發布），則只更新 GitHub 與 Notion，不要重新發布。

## 9. 通知
- 若有新預測或新結果，發送繁體中文 in-app 通知摘要（新預測場次、命中率變化、網址 https://tonic-fifa-wc2026.pplx.app）。
- 若無新事件，靜默結束（不發通知）。

## 排程
- 小組賽期間：每 8 小時（UTC 0/8/16 = HKT 08:00/16:00/00:00）。
- 進入 16 強後：改為每 4 小時。屆時更新 cron 為 `0 0,4,8,12,16,20 * * *`。

## 維護備註
- `kickoff_utc` 由 `add_kickoff_utc.py`（城市→IANA 時區）產生，已寫入 `fixtures.json`；若日後新增/修改場次，重新執行該腳本即可。
- 前端時間顯示統一經 `client/src/lib/utils.ts` 的 `kickoffHkt()`（轉 Asia/Hong_Kong）。
