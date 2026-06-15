# Release Notes — 2026-06-15 預測方法說明文件（HKT 6/15 晚間）

本次為**文件更新**，無資料／預測變動。

## 新增（Added）

- **`PREDICTION_METHODOLOGY.md`** — 完整預測方法說明，內容包括：
  - 總覽：一次排程的完整管線（判斷階段 → 雙引擎預測 → 結果覆盤 → 重算指標 → 多平台同步 → 通知）
  - 主預測引擎 **Claude Opus 4.8**：來源數分級（36h ≥100／48h ≥50）、六大來源類別、六項關鍵判斷因素、預測檔輸出欄位（機率分佈 + 多情境 + 基準線）
  - 第三方多模型對照（MiniMax M3／Qwen3.7 Max／DeepSeek V4 Pro）與綜合共識算法（主預測權重 2、各 AI 權重 1）
  - 結果收錄與 Opus 賽後覆盤（exact/outcome/miss）
  - 評分機制：準確率、校準（Brier／ECE／過度自信）、基準線排行
  - 資料流同步表與六大設計原則

## 變更（Changed）

- **`README.md`** 新增「預測方法（Prediction Methodology）」章節（位於「雲端端（預測引擎）說明」之後），以摘要形式呈現整條預測與評分邏輯，並連結至完整方法文件。
- 檔案索引表新增 `PREDICTION_METHODOLOGY.md` 一列。

## 影響範圍

- 純文件更新，網站功能、資料結構、預測批次皆不受影響。
- 線上：https://tonic-fifa-wc2026.pplx.app
