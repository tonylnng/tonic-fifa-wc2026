# Release v1.5.0 — 全站即時讀取 GitHub 最新內容（頭部條按鈕）

發布日期：2026-06-14（HKT）

## 重點摘要

把原本只更新「結果」分頁的 GitHub 即時讀取功能，升級為**全站一鍵更新**，並將按鈕移至頁面**頭部條**，讓**每一個分頁都看得到、按得到**。

## 變更內容

### 後端
- 新增 `GET /api/live-all`：一次並行抓取 GitHub raw 上所有資料集（`results`、`accuracy`、`calibration`、`postmortems`、`benchmark_scores`、`fixtures`）與全部 `predictions`（透過 `predictions/manifest.json` 枚舉）。
- predictions 依場次分組、依 `run_timestamp` 由新到舊排序，與 `/api/predictions` 行為一致。
- 60 秒快取（`liveAllCache`）＋ 6 秒逾時保護；任一抓取失敗整體回退本機打包資料並標明 `source`。

### 前端
- `Header.tsx`：頭部條新增「即時讀取最新」按鈕＋來源／時間徽章（GitHub 即時 ／ 讀取失敗·本機），載入時圖示旋轉。
- `dashboard.tsx`：點擊後查詢 `/api/live-all`，回填所有相關 query 快取，使六個分頁（AI 預測、預測演變、賽程、結果與準確率、校準與基準、賽後覆盤）同步更新。
- 移除結果分頁專屬的舊控制卡。

### 資料同步
- `sync_to_site.py` 自動產生 `predictions/manifest.json`（供 GitHub raw 枚舉預測檔）。
- `/api/predictions`、`/api/status` 掃描時忽略 `manifest.json`。

## 驗證
- 本地建置通過；Playwright 驗證六個分頁皆顯示頭部按鈕，點擊觸發 `/api/live-all`（HTTP 200）且無 console error。
- 正式站推送 manifest 後，徽章顯示「GitHub 即時」。

## 相容性
- 純讀取功能，無破壞性變更；既有 API 端點維持不變。
