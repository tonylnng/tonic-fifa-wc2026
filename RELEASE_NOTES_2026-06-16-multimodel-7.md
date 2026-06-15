# Release Notes — 第三方多模型對照擴充至 7 家（2026-06-16，HKT 清晨）

## 摘要

將第三方多模型對照從 **3 家擴充至 7 家**，新增 OpenAI、Google、xAI、Z.ai 四大廠的最新模型，並回填第 13–20 場小組賽預測批次（`2026-06-15T0904Z`），讓每場皆有完整的七模型對照與重算後的綜合共識。本站主預測仍固定為 **Claude Opus 4.8**，第三方僅作對照基準。

## 新增（Added）

- **第三方對照新增 4 家模型**（經 Vercel AI Gateway 呼叫）：
  - OpenAI GPT-5.1 Thinking（`openai/gpt-5.1-thinking`）
  - Google Gemini 3.1 Pro（`google/gemini-3.1-pro-preview`）
  - xAI Grok 4.20 Reasoning（`xai/grok-4.20-reasoning`）
  - Z.ai GLM-4.7（`zai/glm-4.7`）
  - 連同原有 MiniMax M3、千問 Qwen3.7 Max、DeepSeek V4 Pro，第三方對照共 **7 家**；加上本站 Opus 4.8 主預測，綜合共識 `models_used` 最多達 **8**。

## 變更（Changed）

- **`multimodel_predict.py`**：
  - `MODELS` 清單擴充為 7 家。
  - `max_tokens` 由 600 提高至 **3000**：reasoning 類模型（Gemini／GLM）需在推理後才輸出 JSON，600 會在 `finish_reason: length` 截斷。
  - 新增**退化防護**：模型若未給出合法比分（`^\d+:\d+$`）即視同失敗並重試／略過，避免空回應污染共識。
- **回填 #13–#20**：對 8 場既有預測各跑一次七模型對照，重算頂層 `benchmarks`（kind=ai）與 `consensus`。主 Opus 預測維持不變；部分場次綜合共識與主預測比分略有差異（如 #14／#17 主預測 2:1、共識 2:0），屬正常。
  - 回填後綜合共識：#13 西班牙 3:0（H .866）· #14 比利時 2:0（H .607）· #15 沙烏地 0:2 客（A .598）· #16 伊朗 2:0（H .603）· #17 法國 2:0（H .679）· #18 伊拉克 0:2 客（A .59）· #19 阿根廷 2:0（H .743）· #20 奧地利 2:0（H .731）。
- **文檔同步**：`PREDICTION_METHODOLOGY.md`、`README.md`（§預測方法）、`data/predictions/SCHEMA.md`、`CRON_RUNBOOK.md` 全部更新為 7 家模型、`max_tokens 3000`、`models_used` 上限 8。前端 `PredictionCard` 對照說明列出全部 7 家來源。
- **指標重算**：`accuracy.json`／`calibration.json`／`benchmark_scores.json` 重新計算。新增 4 家模型目前僅出現在尚無結果的 #13–#20 預測中，故暫不出現在已完成比賽的對照排行榜（待相關比賽結束後納入）。

## 備註

- 本次為程式碼／設定調整 + 回填，非新預測批次，故不新增 Notion 頁面。
- 第三方對照透過 `custom-cred:ai-gateway.vercel.sh` 憑證、以 curl 子程序呼叫（代理環境下 requests SSL 會失敗，勿改回）。
