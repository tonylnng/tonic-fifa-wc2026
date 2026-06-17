# Release Notes — 主預測模型切換 Opus 4.8 → Sonnet 4.6（2026-06-17 HKT）

## 摘要

依使用者指示，將**定時任務的 AI 預測主模型**由 Claude Opus 4.8 切換為 **Claude Sonnet 4.6（最新型號）**。此變更**僅影響未來的預測批次**；所有歷史預測檔、賽後覆盤與舊版發行紀錄一律保留不動。

## 變更（Changed）

- **主預測模型**：`Claude Opus 4.8` → `Claude Sonnet 4.6`
  - 研究子代理啟動參數：`run_subagent(model="claude_opus_4_8")` → `run_subagent(model="claude_sonnet_4_6")`
  - 預測檔 `model` 欄位字串：`"claude-opus-4.8"` → `"claude-sonnet-4.6"`
  - 賽後覆盤（post-mortem）生成模型同步改為 Sonnet 4.6
- **定時任務定義（cron `c53acfd7`）**：任務文字中所有 Opus 4.8 引用更新為 Sonnet 4.6；排程時間（每 8 小時 `55 0,8,16 * * *` UTC）與其餘步驟不變。
- **技能 `wc2026-prediction-automation`**：`SKILL.md` 與 `references/runbook.md` 的模型引用更新為 Sonnet 4.6，並重新驗證、存回使用者技能庫。
- **執行手冊 `CRON_RUNBOOK.md`**：模型引用更新為 Sonnet 4.6。
- **網站基準計分標籤**：`compute_benchmark_scores.py` 中主預測來源標籤由「AI（本站 Opus）」改為**「AI（本站主預測）」**（模型中立，歷史與未來批次均正確顯示）。
- **`multimodel_predict.py`**：新增 `friendly_main_label()`，依各預測檔 `model` 欄位動態推導繁中標籤（Sonnet 4.6／Opus 4.8／主預測），共識說明文字 `logic` 改為動態顯示實際主模型，使歷史與未來批次的對照敘述皆正確。

## 不變（Unchanged）

- 所有歷史預測檔（`data/predictions/match_*.json`）、`results.json`、賽後覆盤與既有發行紀錄保持原樣。
- 第三方七家模型僅作對照基準的設計不變；主預測仍為本站單一模型。
- 來源數分級（近 36h ≥100／其餘 48h ≥50）、每批次獨立保存、繁體中文 + 香港時間呈現等規則不變。

## 影響範圍

- 自下一次定時觸發起，新預測批次將以 Sonnet 4.6 產生並標示。
- 網站、Notion、GitHub 的呈現自動沿用上述標籤。
