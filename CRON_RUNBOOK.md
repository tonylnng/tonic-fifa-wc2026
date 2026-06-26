# 世界盃 2026 AI 預測 — 自動排程執行手冊 (Cron Runbook)

每次排程觸發時，依序執行以下步驟。所有使用者可見文字必須為繁體中文。

## 0. 環境
- 專案根目錄：`/home/user/workspace/wc2026/`
- 資料目錄：`data/`（fixtures.json, results.json, accuracy.json, players.json, leaderboards.json, predictions/）
- 網站目錄：`site/`（部署用）
- Notion 設定：`notion_config.json`（data_source_id: 112974c5-2bbd-4e5e-b3b7-28fd2ed96b6a）
- GitHub 同步站：`/home/user/workspace/wc2026/gitsync/`（已 clone 自 private repo tonylnng/tonic-fifa-wc2026，remote=origin）
- pplx.app 發布：site_id `7674b33b-8ee7-4c42-8d99-e3df659afaed`，網址 https://tonic-fifa-wc2026.pplx.app

## 1. 判斷階段與即將開賽的比賽
- 讀取 `data/fixtures.json`，找出當前時間之後 48 小時內、且尚未有結果（results.json 無紀錄）的比賽。
- **淘汰賽識別**：48 隊賽制下，淘汰賽自 **32 強（Round of 32）** 開始，依序 Round of 16 / Quarter-final / Semi-final / Third place / Final。若即將開賽比賽的 stage 屬上述任一淘汰賽階段，**該場預測需額外執行 2.6 點球風險維度**。
- **排程固定為每日一次（香港時間 13:00，即 UTC `0 5 * * *`），直到賽事結束。即使進入 32 強／16 強等淘汰賽亦維持每日一次此頻率，不切換為每日兩次或每 4 小時。**（2026-06-23 成本優化：由每日兩次 07:00/19:00 降為每日一次。）

## 2. 收集最新情況 + 產生預測

**預測使用模型：Anthropic Claude Sonnet 4.6。** 研究子代理請以 `run_subagent(..., model="claude_sonnet_4_6")` 啟動，並在每個預測檔的 `model` 欄位填 `"claude-sonnet-4.6"`。

**合併研究子代理（2026-06-23 成本優化）：** 同一次 run 的所有即將開賽比賽，盡量用「一個」研究子代理一次研究多場（而非每場各起一個），以減少子代理啟動與重複搜尋的固定開銷；場次很多（>3）時可分 2 組，每組一個子代理。

**來源數要求（依開賽時間分級）：**
- **近 36 小時內開賽**的比賽：**收集最少 20 處來源**（≥20）。
- 其餘 48h 窗口內比賽：最少 12 處來源（≥12）。
- **來源須去重：同一域名只計算一個**（例如 bbc.com 出現 5 篇只算 1 處），確保資訊增量。
（2026-06-26 成本優化：由 ≥40/≥25 降為 ≥20/≥12 並加入去重規則；100/50 早於 2026-06-23 廢棄。）
（以 `fixtures.json` 的 `kickoff_utc` 對比觸發時間判斷是否落在 36h 內。）

對每場即將開賽的比賽，研究最新情報（球員狀態、傷兵、評論員意見、官方、論壇、社群、KOL、YouTube、博彩、模型），產生：
- `kickoff_utc`：由 `fixtures.json` 對應場次帶入（ISO 8601 UTC）；另可填 `kickoff_hkt`（香港時間，純顯示）。
- `prediction.score` {home, away}、`scoreline` "X:X"、`outcome`(home/draw/away)
- `win_prob` {home, draw, away}（總和=1）、`confidence`(0-1)
- **`prediction.top_scorelines`**：3-5 個最可能比分 + 各自機率，機率由高到低；第一個須等於主 `scoreline`。
- **`prediction.scenarios`**：2-4 個多角度情境（如「模型共識／博彩盤口／保守情境／進攻火力」），每個含 `name`、`scoreline`、`outcome`、`confidence`、`basis`（繁中一句依據）。
- **`prediction.benchmarks`**：2-4 個公開基準線的隱含機率，用於與 AI 並列對照與計分。每個含 `source`（如「博彩隱含機率」「Opta 超級電腦」「Kalshi 預測市場」）、`kind`（betting/model/market/ai）、`win_prob`{home,draw,away}（總和≈1）、可選 `scoreline`、`note`（繁中一句來源說明）。基準線數值由研究時蒐集到的博彩盤口、Opta／超級電腦、預測市場等推導，**務必與該場 `key_factors` 中的輿論共識一致**。
- `reasoning.summary`（繁體中文，詳細）、`key_factors`（繁體中文清單）、`consensus_lean`、`dissent`
- `sources`（≥25 或 ≥40，含 url/type）、`source_count`
- `run_id` = 觸發時的 UTC 時間戳，格式 `YYYY-MM-DDTHHMMZ`
- 寫入 `data/predictions/match_{N}__{run_id}.json`（**獨立保存，不覆蓋舊批次**）

所有使用者可見文字（summary/key_factors/scenarios.basis 等）必須**繁體中文**。比賽時間一律以**香港時間**為準呈現（前端由 `kickoff_utc` 自動轉換）。

範本見 `data/predictions/SCHEMA.md`。

## 2.5 第三方多模型 AI 對照 + 共識（A+C）

**在每場比賽的 Sonnet 4.6 預測檔寫好之後**，為同一個預測檔補上第三方 AI 對照與綜合共識。第三方 AI 經 Vercel AI Gateway 取得，只回傳「比分 + 三向勝率 + 一句話 take」（不寫長篇理由，省用量）；本站主預測仍以 **Sonnet 4.6** 為準，第三方僅作對照基準。

- 第三方模型（**精簡至 4 家**，各取最新版）：`minimax/minimax-m3`、`alibaba/qwen3.7-max`、`deepseek/deepseek-v4-pro`、`google/gemini-3.1-pro-preview`。
  - **已移除（2026-06-26 成本優化）**：`openai/gpt-5.1-thinking`、`xai/grok-4.20-reasoning`（reasoning 模型 max_tokens=3000，token 消耗最高）、`zai/glm-4.7`（與 DeepSeek 高度重疊）。
  - **max_tokens 設為 1500**：DeepSeek V4 Pro 為 hybrid reasoning 模型，即使不要求推理，輸出前會自動產生 `<think>...</think>` 區塊（平均 500–800 token）；800 會導致 JSON 被截斷。 1500 提供足夠緩衝，同時比原 3000 還是省約 50%。MiniMax / Qwen / Gemini 三家不帶 reasoning 區塊，1500 完全宾裕。
  - **`extract_json()` 自動剥離 `<think>` 區塊**：腳本會先用 `re.sub(r"<think>.*?</think>", "", ...)` 清除整個 think 區塊，再尋找 JSON，避免 think 內有 `{` 時誤抓錯誤位置。
- 對每場即將開賽比賽，於帶憑證的 bash 執行（**必須**用 `api_credentials=["custom-cred:ai-gateway.vercel.sh"]`，Gateway 金鑰存於使用者憑證庫）：
```bash
python3 /home/user/workspace/wc2026/multimodel_predict.py --match {N}
```
  - 此腳本會讀取該場**最新批次**預測檔，呼叫 4 個第三方模型，把結果以 `kind:"ai"` 追加到該檔的**頂層** `benchmarks[]`（依 `source` 去重，保留既有 betting/model/market 條目），並計算頂層 `consensus`（比分多數決、勝率加權平均，主預測權重 2、每個 AI 權重 1）。
  - 重要：腳本透過 `curl --cacert /etc/ssl/certs/agent-proxy-ca-2.pem` 子程序呼叫 Gateway（Python `requests`/`urllib` 在代理下會 SSL 失敗，**請勿改回 requests**）。
  - 若某模型回傳失敗或逾時，腳本會略過該模型，其餘照常寫入；共識以可用模型計算。
  - 若憑證庫該金鑰需核准（`list_credentials` 顯示 `requires_approval=true`），先 `approve_credential` 再執行。
- 前端會讀取頂層 `pred.consensus` 與 `pred.benchmarks`（含 `kind:"ai"`、`model_id`），在卡片詳情顯示「模型共識」區與「多模型對決」區。

## 2.6 淘汰賽點球風險維度（**32 強起每場必做，併入主預測研究子代理**）

**僅淘汰賽階段（stage 含 "Round of 32" / "Round of 16" / "Quarter-final" / "Semi-final" / "Third place" / "Final"）的即將開賽比賽才執行；小組賽完全略過此步驟。** 由於淘汰賽和局會進入加時／點球，預測失準風險升高，故自 **32 強起** 為每場補上點球與心理維度，寫入該場 Sonnet 4.6 預測檔的 `prediction.knockout` 區塊。

**✨ 2026-06-26 成本優化：點球大戰研究不再另起子代理。改為在主預測研究子代理（步驟 2）的 prompt 內，同時要求子代理蒐集點球大戰資料，一次輸出主預測 JSON + `prediction.knockout` 區塊，節省一次子代理啟動。**

對每場淘汰賽即將開賽比賽，主預測研究子代理需針對雙方蒐集：
- **近 5 年（含本屆）大型國際賽事點球大戰數據**：世界盃、洲際國家盃、歐國盃、美洲盃、各洲區資格賽附加賽等。逐隊統計 `shootouts`（場次）、`won`（勝出）、`win_rate`、可選 `conversion_rate`（罰球命中率）、一句 `recent`（近期紀錄，繁中），附 `sources`。**找不到確證的數字寧可保守填 0 並在 recent 說明，切勿杜撰。**
- **球員心理素質分析**（`psychology.home/away`，全繁中）：門將撲點紀錄、隊長／核心大賽經驗、年輕陣容抗壓、主罰順序穩定度等。
- **主要主罰球員**（`key_takers`，選填 2-5 人）：`team`(home/away)、`name_zh`、`record`（命中紀錄繁中）。
- **機率估計**：`draw_after_90_prob`、`extra_time_prob`、`shootout_prob`、`advance_prob`{home,away}（二向總和=1，含加時／點球後最終晉級）。
- **綜合點球風險** `penalty_risk`（high/medium/low）與 `risk_note`（1-3 句繁中提示）。

格式範本見 `data/predictions/SCHEMA.md` 的 `knockout` 區塊；型別見 `site/client/src/lib/types.ts` 的 `KnockoutInfo`。前端 `PredictionCard` 會在卡片角落顯示「點球風險」徽章，並在詳情顯示「淘汰賽點球風險分析」完整區塊（三項機率、晉級條、雙方近 5 年點球戰績、心理素質、主罰球員、風險提示）。**小組賽預測檔不含 `knockout`，前端自動不顯示，互不影響。**

## 3. 結果 + 賽後覆盤 + 球員統計（**合併單一 Sonnet 4.6 子代理**）

**✨ 2026-06-26 成本優化：原步驟 3（覆盤）與步驟 3.5（球員統計）各自啟動 Sonnet 4.6 子代理，改為合併成一個子代理，節省一次子代理啟動與重複搜尋開銷。**

- 搜尋是否有新完成的比賽，將最終比分寫入 `data/results.json`（results 陣列，含 match, scoreline, home, away, date）。
- **有新完成比賽時，啟動一個 Sonnet 4.6 子代理，同時完成兩項任務：**
  1. 搜尋權威來源（FIFA 官方／ESPN／Sky／衛報／賽事中心），找出該場的入球者與紅黃牌球員（烏龍球不計入 `goals`，找不到確證就略過，切勿杜撰）。
  2. 比對該場最新批次預測與實際比分，生成繁體中文賽後覆盤（`headline`/`review`/`lessons`/`vs_benchmarks`/`verdict` 等完整欄位）。
- 子代理輸出兩份 JSON，parent 分別 pipe 到腳本：
```bash
echo '<postmortem json 物件或陣列>' | python3 /home/user/workspace/wc2026/build_postmortems.py --merge-stdin
echo '<players json 物件或陣列>' | python3 /home/user/workspace/wc2026/update_players.py --merge-stdin
```
- **postmortem** 合併鍵為 (match, run_id)，不覆蓋既有不同場次的覆盤。每筆含：`match`、`home`、`away`、`stage`、`predicted`、`predicted_outcome`、`final`、`actual_outcome`、`outcome_correct`、`exact_correct`、`verdict`(exact/outcome/miss)、`run_id`、`model`、`headline`、`review`、`lessons`、`vs_benchmarks`。
- **players** 球員 id 規則：`{隊三碼大寫}-{姓氏小寫}`（與 `data/players.json` 既有 id 一致）。若球員不在名單中，事件物件附帶 `name_en`/`name_zh`/`team`（須與 fixtures 英文隊名逐字一致）/`team_zh`/`position`，腳本會自動建檔。腳本依 `id` 與 `stats.matches_with_events` **冪等累加**，並重算 `data/leaderboards.json`（射手榜／紀律榜）。每場 events 內各球員只記「該場」事件數（勿跨場累加）。完整格式見 `data/PLAYERS_SCHEMA.md`。

## 4. 重算準確率、校準與基準線計分
```bash
python3 /home/user/workspace/wc2026/update_accuracy.py
python3 /home/user/workspace/wc2026/compute_calibration.py
python3 /home/user/workspace/wc2026/compute_benchmark_scores.py
```
- `update_accuracy.py`：勝負／比分命中率（由 results.json 的 scoreline 比對各場最新批次預測）。
- `compute_calibration.py`：把預測信心分桶，對比實際命中率，輸出 `data/calibration.json`（含 Brier、ECE、過度自信 overconfidence）。
- `compute_benchmark_scores.py`：在相同已完成比賽上，把 AI 與各 `benchmarks` 來源並列計分（勝負命中、比分命中、Brier），輸出 `data/benchmark_scores.json` 排行榜。
  - **逐場明細自動維護（每場比賽完結都更新）**：每個來源輸出 `matches[]`（逐場：stage、中英雊名、預測比分與勝負、**當時信心 %**、實際比分與勝負、`outcome_hit`、`exact_hit`），並標記停更來源 `stale`/`latest_match` 與頂層 `max_match_completed`。前端「校準與基準」頁的 AI 列可點擊展開（預設收合）顯示逐場表格與命中圖示（✓ 勝負命中、✗ 未中、金色高亮＝比分命中），並內含「信心」欄；停更來源顯示琥珀「已停更·止於 #N」徽章。**此明細由步驟 4 的 `compute_benchmark_scores.py` 每次自動重算，無需手動維護。**

## 5. 同步資料到網站目錄
```bash
python3 /home/user/workspace/wc2026/sync_to_site.py
```
（會一併複製 fixtures/results/accuracy/predictions 以及 `calibration.json`、`postmortems.json`、`benchmark_scores.json`、`players.json`、`leaderboards.json`。）

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
- **固定每日一次：香港時間 13:00，即 UTC `0 5 * * *`。直到賽事結束。**（2026-06-23 成本優化）
- **進入 32 強／16 強等淘汰賽亦維持此頻率，不切換為每 4 小時。**（使用者明確要求；舊版「每 8 / 每 4 小時」規則已廢止。）

## 維護備註
- `kickoff_utc` 由 `add_kickoff_utc.py`（城市→IANA 時區）產生，已寫入 `fixtures.json`；若日後新增/修改場次，重新執行該腳本即可。
- 前端時間顯示統一經 `client/src/lib/utils.ts` 的 `kickoffHkt()`（轉 Asia/Hong_Kong）。
