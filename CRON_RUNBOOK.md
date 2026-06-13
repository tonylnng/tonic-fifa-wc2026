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

## 2. 收集最新情況 + 產生預測（每場 ≥50 來源）
對每場即將開賽的比賽，研究最新情報（球員狀態、傷兵、評論員意見、官方、論壇、社群、KOL、YouTube、博彩、模型），**收集最少 50 處來源**，產生：
- `prediction.score` {home, away}、`scoreline` "X:X"、`outcome`(home/draw/away)
- `win_prob` {home, draw, away}、`confidence`(0-1)
- `reasoning.summary`（繁體中文，詳細）、`key_factors`（繁體中文清單）、`consensus_lean`、`dissent`
- `sources`（≥50，含 url/type）、`source_count`
- `run_id` = 觸發時的 UTC 時間戳，格式 `YYYY-MM-DDTHHMMZ`
- 寫入 `data/predictions/match_{N}__{run_id}.json`（**獨立保存，不覆蓋舊批次**）

範本見 `data/predictions/SCHEMA.md`。

## 3. 更新已完成比賽的結果
- 搜尋是否有新完成的比賽，將最終比分寫入 `data/results.json`（results 陣列，含 match, scoreline, home, away, date）。

## 4. 重算準確率
```bash
python3 /home/user/workspace/wc2026/update_accuracy.py
```

## 5. 同步資料到網站目錄
```bash
python3 /home/user/workspace/wc2026/sync_to_site.py
```

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
