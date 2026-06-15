# 世界盃 2026 AI 預測方法說明（Prediction Methodology）

> 本文說明定時任務（cron `c53acfd7`）每次執行時，「如何產生一場比賽的 AI 預測」以及「如何評分與對照」的完整邏輯。供你快速理解預測方法、資料流與評分指標。
>
> **所有使用者可見內容為繁體中文；比賽時間一律以香港時間（HKT）呈現。**

---

## 一、總覽：一次排程做了什麼

定時任務每 8 小時觸發一次（小組賽期間；進入 16 強改每 4 小時）。每次觸發會走一條完整的資料管線：

```
判斷階段
  └─► 找出未來 48h 內、尚無結果的即將開賽比賽
       └─► 對每場：①Opus 4.8 深度研究預測  ②第三方多模型對照+共識
            └─► 收錄新完成比賽結果 + Opus 賽後覆盤
                 └─► 重算 準確率 / 校準 / 基準線排行
                      └─► 同步：網站 → Notion → GitHub → 重新發布 pplx.app
                           └─► 發繁中通知
```

預測的「方法核心」集中在 **步驟①②**（如何得出一場比賽的比分與勝率）與後段的 **評分機制**（如何衡量準不準）。以下分開說明。

---

## 二、預測引擎：本站主預測（Claude Opus 4.8）

**主預測模型固定為 Anthropic Claude Opus 4.8。** 每場比賽由一個獨立的研究子代理（`run_subagent(model="claude_opus_4_8")`）負責，產出一份完整預測檔。

### 2.1 研究強度（來源數分級）

預測不是憑模型記憶，而是要求子代理**即時蒐集大量最新情報**，並依開賽急迫度分級：

| 開賽時間（對比觸發時刻） | 最少來源數 |
|---|---|
| 近 36 小時內開賽 | **≥100 處來源** |
| 其餘 48 小時窗口內 | **≥50 處來源** |

來源涵蓋多元面向，避免單一視角偏誤：

- **官方**：FIFA、各國足協、球隊官網
- **媒體**：ESPN、BBC、Goal、Sky、The Athletic、AS、Marca…
- **博彩／模型**：主流博彩盤口、Opta 超級電腦、Elo 類模型、賠率聚合站
- **論壇／社群**：Reddit（r/worldcup）、各足球論壇
- **KOL／名嘴**：具名分析師、退役球員評論
- **YouTube**：賽前分析／預覽影片

> ⚠️ **防偽規則**：宣稱「尚未開賽比賽最終比分」的 YouTube／網路「賽後 review」內容多為 AI 捏造，**一律不採信為結果**。

### 2.2 研究時考慮的關鍵因素

子代理綜合判斷以下維度（寫入 `reasoning.key_factors`）：

1. **球員狀態**：近期表現、核心球員出賽可能
2. **傷停名單**：傷兵、停賽、體能輪換
3. **近期戰績／狀態**：球隊近況曲線
4. **戰術對位**：陣型相剋、教練風格
5. **主客場／場地**：地點、氣候、草皮、旅途
6. **輿論共識**：博彩盤口、超級電腦、名嘴與社群的整體傾向

### 2.3 預測檔輸出（每場一個 JSON，永不覆蓋）

每場每批次獨立寫入 `data/predictions/match_{場次}__{run_id}.json`（`run_id` = 觸發時 UTC 時間戳，如 `2026-06-15T0904Z`）。**舊批次永遠保留**，方便事後回溯「賽前最後一刻的預測」並稽核整條推理鏈。

核心欄位：

| 欄位 | 意義 |
|---|---|
| `prediction.scoreline` / `score` | 主預測比分（最可能比分） |
| `prediction.outcome` | 勝負向：home / draw / away |
| `prediction.win_prob` {home,draw,away} | 三向勝率，**總和 = 1** |
| `prediction.confidence` | 對主預測的自評信心（0–1） |
| `prediction.top_scorelines[]` | 3–5 個最可能比分 + 各自機率（由高到低；第一個 = 主比分） |
| `prediction.scenarios[]` | 2–4 個多角度情境（如「模型共識／博彩盤口／保守情境／進攻火力」），各含比分、勝負、信心、依據 |
| `prediction.benchmarks[]` | 2–4 條**公開基準線**（博彩隱含機率、Opta 超級電腦、預測市場…）的三向機率，用來與 AI 並列對照 |
| `reasoning` | summary / key_factors / consensus_lean / dissent（全繁中） |
| `sources[]` + `source_count` | 來源清單與計數（須達門檻） |

> 重點設計：預測不是「一個比分」，而是**機率分佈（top_scorelines）+ 多情境（scenarios）+ 外部基準線（benchmarks）**，讓使用者看到不確定性與多種可能，而非單點猜測。

---

## 三、第三方多模型對照 + 綜合共識

主預測寫好後，對**同一份預測檔**補上三家第三方 AI 的對照，再算出綜合共識。第三方**僅作對照基準，本站主預測永遠是 Opus 4.8**。

### 3.1 執行方式

```bash
python3 multimodel_predict.py --match {場次}
# 需帶憑證：api_credentials=["custom-cred:ai-gateway.vercel.sh"]
```

- 經 **Vercel AI Gateway** 呼叫三家模型：
  - `minimax/minimax-m3`
  - `alibaba/qwen3.7-max`
  - `deepseek/deepseek-v4-pro`
- 第三方只回傳精簡內容（省用量）：**比分 + 三向勝率 + 一句話 take**，不寫長篇理由。
- 技術細節：腳本以 `curl --cacert` 子程序呼叫 Gateway（代理環境下 Python requests 會 SSL 失敗，故不用 requests）。某模型逾時／失敗即略過，其餘照常寫入。

### 3.2 結果如何寫回

- 三家 AI 以 `kind:"ai"`（含 `model_id`）追加到預測檔**頂層** `benchmarks[]`（依來源去重，保留既有 betting/model/market 條目）。
- 第三方若回傳整數機率（如 55/25/20），會自動 sum-normalize 為總和 1。

### 3.3 綜合共識（consensus）的算法

腳本把「本站 Opus 主預測 + 可用第三方」合成一個頂層 `consensus`：

- **勝率**：加權平均 — **主預測權重 2，每家第三方權重 1**。
  （例：本站 + 3 家 AI 全到齊 → 權重 2:1:1:1，`models_used = 4`。）
- **比分**：多數決；若平手則靠近主預測。

前端卡片詳情會顯示「模型共識」區與「多模型對決」區，呈現四個模型的比分與勝率對照。

---

## 四、結果收錄與賽後覆盤

- 搜尋新完成比賽，將最終比分寫入 `data/results.json`（含 `scoreline`）。
- 對每場新結果，用 **Opus 4.8** 生成繁中**賽後覆盤**（`postmortems.json`，合併鍵 = match + run_id）：
  - `verdict`：exact（比分全中）/ outcome（方向中）/ miss（落空）
  - `headline`（一句標題）、`review`（詳述為何命中／失準）、`lessons`（教訓清單）、`vs_benchmarks`（AI 與基準線相比的優劣）

> 範例：本輪 #12 瑞典 5:1 突尼西亞 — 原預測 1:0 主勝 → `verdict: outcome`（方向命中、比分偏保守，漏估瑞典爆發力）。

---

## 五、評分機制：如何衡量「準不準」

每輪重算三組指標（依序執行 `update_accuracy.py` → `compute_calibration.py` → `compute_benchmark_scores.py`）。**所有評分都以「該場最新一筆賽前預測」對比實際比分**。

### 5.1 準確率（accuracy.json）

- **勝負命中率（outcome accuracy）**：預測勝負向（1X2）是否等於實際結果。
- **比分命中率（exact accuracy）**：預測比分是否完全相同。
- 另按階段（Group / R16 …）分組統計。

### 5.2 校準（calibration.json）

衡量「信心是否名副其實」，把預測信心分桶對比實際命中率：

- **Brier 分數**：對「所預測勝負向」給出的機率 vs 是否命中（1/0）的均方差，**越低越好**。
- **ECE（期望校準誤差）**：各信心桶「平均信心 − 實際命中率」的加權絕對差。
- **過度自信（overconfidence）**：整體平均信心 − 平均命中率。>0.1 即提示「過度自信傾向」。

### 5.3 基準線排行（benchmark_scores.json）

在**相同的已完成比賽**上，把本站 AI 與所有基準線（博彩、Opta、預測市場、三家第三方 AI…）**並列計分**：

- 各來源計算 outcome 命中、exact 命中、Brier。
- 第三方 AI 若未存 `outcome`，由其 `win_prob` 取最大向推導。
- 產生一張排行榜，看本站 Opus 相對外部基準的強弱。

---

## 六、資料流與同步

| 步驟 | 動作 | 輸出 |
|---|---|---|
| 同步網站 | `sync_to_site.py` | 複製 fixtures/results/accuracy/predictions + calibration/postmortems/benchmark_scores 到 `site/data/` |
| Notion | `notion-create-pages` | 每場新預測建一頁（含比分、勝負、信心、來源數、批次、摘要） |
| GitHub | `push_to_github.py` + `git push` | 推送 `data/` 並附 release note、更新 CHANGELOG/README/SCHEMA/RUNBOOK |
| 發布 | `npm run build` → `deploy_website` → `publish_website` | 沿用 site_id 更新 https://tonic-fifa-wc2026.pplx.app（公開、無密碼） |
| 通知 | `send_notification` | 有新預測/結果才發繁中 in-app 摘要 |

---

## 七、設計原則小結

1. **權威主預測單一化**：本站結論永遠是 Claude Opus 4.8，第三方只作對照，避免「多模型混戰」失去可究責性。
2. **證據驅動，非記憶驅動**：每場強制蒐集 50–100+ 處即時來源，覆蓋官方／媒體／博彩／社群／KOL 多視角。
3. **表達不確定性**：輸出機率分佈、多情境、多基準線，而非單點比分。
4. **可稽核、不可竄改歷史**：每批次預測獨立保存，賽後可回看賽前最後判斷。
5. **持續自我評估**：準確率、校準、基準排行三管齊下，並用 Opus 賽後覆盤累積教訓。
6. **全繁中、香港時間**：所有使用者面向內容一致呈現。

---

## 八、相關檔案索引

| 檔案 | 用途 |
|---|---|
| `CRON_RUNBOOK.md` | 排程逐步執行手冊（權威流程） |
| `data/predictions/SCHEMA.md` | 預測檔完整 JSON Schema |
| `multimodel_predict.py` | 第三方多模型對照 + 共識計算 |
| `update_accuracy.py` | 勝負／比分命中率 |
| `compute_calibration.py` | Brier / ECE / 過度自信 |
| `compute_benchmark_scores.py` | AI vs 基準線排行 |
| `build_postmortems.py` | 賽後覆盤合併寫入 |
| `sync_to_site.py` / `push_to_github.py` | 網站與 GitHub 同步 |

*最後更新：2026-06-15（HKT）*
