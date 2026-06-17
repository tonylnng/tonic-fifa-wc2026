# Release Notes — 新增「球員介紹」功能 + 定時更新球員統計

**日期**：2026-06-17（HKT）
**類型**：新功能（Feature）
**影響範圍**：網站新增頁面、資料結構、定時任務新增步驟、技能與文檔

---

## 摘要

世界盃 2026 AI 預測中心新增**球員介紹**功能。網站新增「球員」分頁，展示重點球員的基本資料與繁體中文簡介、本屆統計（進球／黃牌／紅牌），並提供**射手榜**與**紀律榜**。定時任務在每場賽後自動以 Claude Sonnet 4.6 研究入球者與紅黃牌球員，冪等累加更新球員統計並重算榜單，與現有預測流程同步。

---

## 新增（Added）

### 資料層
- **`site/data/players.json`**：球員名單（48 隊重點球員，初始約 6 人／隊 + 賽後自動建檔的得分／領牌球員，目前共 346 人）。每位含 `id`（`{隊三碼}-{姓氏}`）、中英文姓名、球衣號碼、位置、所屬球會、年齡、繁中簡介 `bio_zh`，及本屆統計 `stats`（`goals`／`yellow_cards`／`red_cards`／`matches_with_events`）。
- **`site/data/leaderboards.json`**：由 `players.json` 自動計算的射手榜（依進球遞減）與紀律榜（紅牌→黃牌遞減），含賽事累計總數。
- **`data/PLAYERS_SCHEMA.md`**：球員資料結構與 `update_players.py --merge-stdin` 合併格式說明。

### 後端
- **`/api/players`**：回傳 `players.json`。
- **`/api/leaderboards`**：回傳 `leaderboards.json`。

### 前端
- **「球員」分頁**（`PlayersTab.tsx`）：頂部射手榜／紀律榜，下方依球隊分組的球員卡片（國旗、中英文名、號碼、位置徽章、球會、年齡、繁中簡介、進球／黃牌／紅牌數據），支援姓名搜尋與球隊篩選。

### 自動化
- **`update_players.py`**：球員統計合併引擎。`--merge-stdin` 依 `id` 與 `stats.matches_with_events` **冪等累加**單場進球／紅黃牌事件，名單外球員可自動建檔；同時重算 `leaderboards.json`。`--recompute-only` 可僅重算榜單。
- 定時任務 `c53acfd7` 新增**步驟 (3.5)**：每場新出爐結果後，用 Sonnet 4.6 研究權威來源找出入球者與紅黃牌球員，合併進球員統計（烏龍球不計入任何球員進球）。排程維持每 8 小時不變。

---

## 變更（Changed）
- **`sync_to_site.py`**：複製清單加入 `players.json`、`leaderboards.json`。
- **`push_to_github.py`**：data 同步清單加入 `players.json`、`leaderboards.json`。
- **`CRON_RUNBOOK.md`**：環境清單與步驟 5 補列球員資料；新增「## 3.5 更新球員本屆統計」段落。
- **技能 `wc2026-prediction-automation`**（SKILL.md + references/runbook.md）：管線新增球員統計步驟，已重新驗證並存回使用者技能庫。

---

## 備註
- 球員統計只記錄**有確證**的事件；找不到權威來源即略過，絕不杜撰。
- 本功能不影響既有預測、指標、賽後覆盤與歷史批次。
- 網站維持公開、無密碼；所有使用者可見文字為繁體中文，比賽時間以香港時間呈現。
