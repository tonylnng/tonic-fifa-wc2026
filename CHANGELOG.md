# 變更紀錄 CHANGELOG

本檔記錄世界盃 2026 AI 預測中心的版本變更。所有時間以香港時間（HKT）為準。

格式參考 [Keep a Changelog](https://keepachangelog.com/)，版本依語意化版本號。

---

## [資料更新] 2026-06-20 00:55 UTC（HKT 08:55）第 20 次定時批次

### 新增（Added）

- **2 場新預測**（Sonnet 4.6，批次 `2026-06-20T0055Z`）：
  - #38 比利時 **2:1** 伊朗（主勝，信心 0.62，69 源）｜香港時間 06-22 03:00，G 組。雙方首輪均平局、同積 1 分；伊朗遭傷兵與除名重創。第三方 7 AI 共識 2:0 主勝。
  - #39 烏拉圭 **1:0** 佛得角（主勝，信心 0.72，74 源）｜香港時間 06-22 06:00，H 組。烏拉圭傷兵不少但實力佔優；佛得角首戰逼平西班牙。第三方 7 AI 共識 2:0 主勝。
- **2 場新結果 + 賽後覆盤**：
  - #29 美國 **2:0** 澳洲（主勝）——伯吉斯烏龍球 11′、弗里曼頭槌 43′（VAR 確認）。AI 預測 2:1，勝負方向命中、澳洲未進球。
  - #30 蘇格蘭 **0:1** 摩洛哥（客勝）——賽巴里 2′閃電破門（本屆最快入球）。AI 預測 1:2 客勝，準確押中爆冷方向。
- **球員統計更新**：弗里曼、賽巴里各 +1 球；多名球員 +1 黃（共 10 筆事件）。射手榜 71 人、紀律榜 76 人。

### 變更（Changed）

- 重算 `accuracy.json`（已評 26 場、勝負 15/26、比分 1/26）、`calibration.json`（AI Brier 0.2515、ECE 0.1508）、`benchmark_scores.json`。結果增至 30 場、覆盤增至 26 篇、球員增至 374 人。
- Notion 追蹤庫新增 2 筆預測頁（批次 `2026-06-20T0055Z`）。預測檔增至 115 個。

---

## [資料更新] 2026-06-19 16:55 UTC（HKT 06-20 00:55）第 19 次定時批次

### 新增（Added）

- **1 場新預測**（Sonnet 4.6，批次 `2026-06-19T1655Z`，95 源）：
  - #37 西班牙 **2:0** 沙烏地阿拉伯（主勝，信心 0.83）｜香港時間 06-22 00:00，H 組。西班牙（2024 歐國盃冠軍級陣容）首輪 0:0 悶平後求反彈，亞馬爾、尼科·威廉斯雙翼預計首發；沙國新帥僅上任 7 週、依賴低位防反。
  - 附第三方 7 個 AI 多模型對照（綜合共識 3:0 主勝，七模型一致看好西班牙）。

### 變更（Changed）

- 本輪無新完賽比賽（#29 美國 vs 澳洲於觸發後 2 小時開賽，順延至下輪），結果/覆盤/球員統計不變；指標維持已評 24 場、勝負 13/24、比分 1/24、AI Brier 0.2547、ECE 0.155。
- Notion 追蹤庫新增 1 筆預測頁（批次 `2026-06-19T1655Z`）。預測檔增至 113 個。

---

## [資料更新] 2026-06-19 08:55 UTC（HKT 16:55）第 18 次定時批次

### 新增（Added）

- **1 場新預測**（Sonnet 4.6，批次 `2026-06-19T0855Z`，104 源）：
  - #36 突尼西亞 **0:2** 日本（客勝，信心 0.72）｜香港時間 06-21 12:00，F 組。日本傷兵潮（久保建英、三笘薰、遠藤航、南野拓實）但深度仍佔優；突尼西亞首戰0-5慘敗後緊急換帥雷納爾。
  - 附第三方 7 個 AI 多模型對照（綜合共識 0:1 客勝，七模型一致看好日本）。
- **1 場新結果 + 賽後覆盤**：
  - #28 墨西哥 **1:0** 南韓（主勝）——羅莫（Luis Romo）50′ 趁南韓門將金承奎失誤射入空門，墨西哥成為本屆首支晋級淘汰賽的球隊。AI 預測 2:1，勝負方向命中、低估雙方防守強度（比分失準）。
- **球員統計更新**：羅莫 +1 球；南韓李剛仁、白昇浩各 +1 黃。射手榜／紀律榜重算。

### 變更（Changed）

- 重算 `accuracy.json`（已評 24 場、勝負 13/24、比分 1/24）、`calibration.json`（AI Brier 0.2547、ECE 0.155）、`benchmark_scores.json`。結果增至 28 場、覆盤增至 24 篇、球員增至 370 人。
- Notion 追蹤庫新增 1 筆預測頁（批次 `2026-06-19T0855Z`）。

---

## [資料更新] 2026-06-19 00:55 UTC（HKT 08:55）第 17 次定時批次

### 新增（Added）

- **2 場新預測**（Sonnet 4.6，批次 `2026-06-19T0055Z`，均 ≥50 源）：
  - #34 德國 **2:1** 象牙海岸（主勝，信心 0.68，69 源）｜香港時間 06-21 04:00，E 組
  - #35 厄瓜多 **3:0** 庫拉索（主勝，信心 0.78，53 源）｜香港時間 06-21 08:00，E 組
  - 每場附第三方 7 個 AI 多模型對照與共識（#34 2:0、#35 2:0）。
- **3 場新結果 + 賽後覆盤**：
  - #25 捷克 **1:1** 南非（和局）——薩迪萊克 6′ 閃電領先，南非莫科耶納 83′ 十二碼逆平。AI 預測 2:0 主勝落空（爆冷平局）。
  - #26 瑞士 **4:1** 波黑（主勝）——曼贊比梅開二度、巴加斯、查卡十二碼；波黑穆哈雷莫維奇 80′ 染紅。AI 預測 2:1，勝負命中、低估末段大爆發。
  - #27 加拿大 **6:0** 卡達（主勝）——大衛帽子戲法（三球）、拉林、薩利巴任意球＋卡達烏龍；卡達雙紅以 9 人完賽。AI 預測 2:0，主勝與零封命中、大幅低估進球。
- **球員統計更新**：大衛 +3 球（帽子戲法）、曼贊比 +2；薩迪萊克、莫科耶納、巴加斯、查卡、拉林、薩利巴、馬赫米奇各 +1 球。波黑穆哈雷莫維奇、卡達阿爾阿明與馬迪博各 +1 紅。射手榜／紀律榜重算。

### 變更（Changed）

- 重算 `accuracy.json`（已評 23 場，勝負 12/23、比分 1/23）、`calibration.json`（AI Brier 0.254、ECE 0.1383）、`benchmark_scores.json`。結果增至 27 場、覆盤增至 23 篇、球員增至 367 人。
- Notion 追蹤庫新增 2 筆預測頁（批次 `2026-06-19T0055Z`）。

---

## [資料更新] 2026-06-18 16:55 UTC（HKT 06-19 00:55）第 16 次定時批次

### 新增（Added）

- **1 場新預測**（Sonnet 4.6，批次 `2026-06-18T1655Z`，107 源，超 ≥50 標準）：
  - #33 荷蘭 **2:1** 瑞典（主勝，信心 0.62，勝平負 55%/24%/21%）｜香港時間 06-21 01:00，F 組第二輪
  - 附第三方 7 個 AI 多模型對照與共識（2:1 主勝，H0.556）。

### 備註（Notes）

- #25 捷克 vs 南非 於觸發時（UTC 17:03）仍進行中（約第 48 分，捷克暫領先），多個權威來源皆無完賽確證，依規本輪不記錄結果，留待下輪處理。
- 本輪無新完賽比賽，指標（accuracy 20 場、勝負 10/20、AI Brier 0.2655）維持不變；預測檔增至 109。

---

## [資料更新] 2026-06-18 08:55 UTC（HKT 16:55）第 15 次定時批次

### 新增（Added）

- **2 場新預測**（Sonnet 4.6，批次 `2026-06-18T0855Z`，均 ≥50 源/場）：
  - #31 巴西 **3:0** 海地（主勝，信心 0.82，98 源）
  - #32 土耳其 **1:0** 巴拉圭（主勝，信心 0.42，67 源）
  - 每場均附第三方多模型對照與共識（#31 4:0 主勝、#32 1:0 主勝）。
- **2 場新結果 + 賽後覆盤**：
  - #23 迦納 **1:0** 巴拿馬（主勝）——伊倫恩基 90+5′ 補時頭槌絕殺。AI 預測 1:0，勝負與比分全中（低信心 0.40 命中緊湊低分賽況）。
  - #24 烏茲別克 **1:3** 哥倫比亞（客勝）——穆尼奧斯 40′、迪亞斯 65′、坎帕斯 90+9′建功，法烏拉耶夫 60′ 追回一球。AI 預測 0:2，勝負命中、低估雙方進球。
- **球員統計更新**：迪亞斯、穆尼奧斯、坎帕斯、伊倫恩基、法烏拉耶夫各 +1 球；伊倫恩基、布萊克曼、哈維、莫希卡、胡薩諾夫、阿里亞斯、迪亞斯各 +1 黃。射手榜／紀律榜同步重算。

### 變更（Changed）

- 重算 `accuracy.json`（已評 20 場，勝負 10/20、比分 1/20）、`calibration.json`（AI Brier 0.2655，ECE 0.1615）、`benchmark_scores.json`。結果增至 24 場、覆盤增至 20 篇。
- Notion 追蹤庫新增 2 筆預測頁（批次 `2026-06-18T0855Z`）。

---

## [資料更新] 2026-06-18 00:55 UTC（HKT 08:55）第 14 次定時批次

### 新增（Added）

- **2 場新預測**（Sonnet 4.6，批次 `2026-06-18T0055Z`，均 ≥50 源/場）：
  - #29 美國 **2:1** 澳洲（主勝，信心 0.62，78 源）
  - #30 蘇格蘭 **1:2** 摩洛哥（客勝，信心 0.42，79 源）
  - 每場均附第三方多模型對照與共識（#29 2:1 主勝、#30 1:2 客勝）。
- **2 場新結果 + 賽後覆盤**：
  - #21 葡萄牙 **1:1** 剛果民主（和局，爆冷）——若昂·尼維斯 6′、韋薩 45+5′頭槌扈平（剛果史上首個世界盃進球與積分）。AI 預測 2:0，勝負未中。
  - #22 英格蘭 **4:2** 克羅地亞（主勝）——卡尼梅開二度，貝靈漢、拉舒福特鍎勝。AI 預測 1:0，勝負命中、大幅低估進球。
- **球員統計更新**：卡尼 +2 球；若昂·尼維斯、韋薩、貝靈漢、拉舒福特、巴圖里納、穆薩各 +1 球；伯納多·施華、姆貝姆巴、塞梅多、阿勞需各 +1 黃。射手榜／紀律榜同步重算。Semedo、Araujo、Baturina、Musa 為名單外自動建檔。

### 變更（Changed）

- 重算 `accuracy.json`（已評 18 場，勝負 8/18）、`calibration.json`（AI Brier 0.2684，ECE 0.2089）、`benchmark_scores.json`。結果增至 22 場。
- Notion 追蹤庫新增 2 筆預測頁（批次 `2026-06-18T0055Z`）。

---

## [資料更新] 2026-06-17 16:55 UTC（HKT 06-18 00:55）第 13 次定時批次

### 新增（Added）

- **4 場新預測**（Sonnet 4.6，批次 `2026-06-17T1655Z`，均 ≥100 源/場）：
  - #25 捷克 **2:0** 南非（主勝，信心 0.62，153 源）
  - #26 瑞士 **2:1** 波黑（主勝，信心 0.60，161 源）
  - #27 加拿大 **2:0** 卡塔爾（主勝，信心 0.73，145 源）
  - #28 墨西哥 **2:1** 南韓（主勝，信心 0.46，156 源）
  - 每場均附第三方多模型（Gemini 3.1 Pro／Grok 4.20／GLM-4.7 等）對照基準與共識（#25 2:0、#26 2:1、#27 2:0、#28 2:1，均主勝）。

### 變更（Changed）

- 重算 `accuracy.json`（已評 16 場，勝負 7/16）、`calibration.json`（Brier 0.2567）、`benchmark_scores.json`。本次無新完賽比賽，結果維持 20 場。
- Notion 追蹤庫新增 4 筆預測頁（批次 `2026-06-17T1655Z`）。

---

## [資料更新] 2026-06-17 09:12 UTC（HKT 17:12）第 12 次定時批次

### 新增（Added）

- **4 場新預測**（Sonnet 4.6，批次 `2026-06-17T0912Z`）：
  - #21 葡萄牙 **2:0** 剛果民主共和國（主勝，信心 0.75，198 源）
  - #22 英格蘭 **1:0** 克羅地亞（主勝，信心 0.58，154 源）
  - #23 迦納 **1:0** 巴拿馬（主勝，信心 0.40，189 源）
  - #24 烏茲別克 **0:2** 哥倫比亞（客勝，信心 0.71，478 源）
  - 每場均附第三方多模型（MiniMax M3／Qwen3.7 Max／DeepSeek V4 Pro）對照基準與共識。
- **2 場新結果 + 賽後覆盤**：
  - #19 阿根廷 **3:0** 阿爾及利亞 — 美斯帽子戲法（17′／60′／76′），平克洛澤 16 球世界盃進球紀錄。
  - #20 奧地利 **3:1** 約旦 — Schmid 21′、Ali Olwan 50′（約旦世界盃史上首球）、Yazan Al-Arab 76′ 烏龍球、Arnautovic 90+12′ 十二碼。Sabitzer 一黃。
- **球員統計更新**：美斯 +3 球、Schmid／Ali Olwan／Arnautovic 各 +1 球、Sabitzer +1 黃；射手榜／紀律榜同步重算（烏龍球不計入任何球員）。Schmid 為名單外自動建檔。

### 變更（Changed）

- 重算 `accuracy.json`（已評 16 場，勝負 7/16）、`calibration.json`（Brier 0.2567）、`benchmark_scores.json`（13 來源）。
- Notion 追蹤庫新增 4 筆預測頁（批次 `2026-06-17T0912Z`）。

---

## [新功能] 2026-06-17 新增「球員介紹」功能 + 定時更新球員統計

### 新增（Added）

- 網站新增**「球員」分頁**：展示重點球員基本資料與繁中簡介、本屆統計（進球／黃牌／紅牌），並提供**射手榜**與**紀律榜**。
- 新增資料檔 `players.json`（48 隊重點球員，目前共 346 人）與 `leaderboards.json`（自動計算榜單），以及 `data/PLAYERS_SCHEMA.md` 結構文檔。
- 後端新增 `/api/players`、`/api/leaderboards` 路由；前端新增 `PlayersTab.tsx`（搜尋＋球隊篩選＋分組卡片）。
- 新增 `update_players.py` 合併引擎：`--merge-stdin` 依 `id` 與 `matches_with_events` **冪等累加**單場進球／紅黃牌，名單外球員自動建檔，並重算榜單。
- 定時任務 `c53acfd7` 新增**步驟 (3.5)**：每場賽後用 Sonnet 4.6 研究入球者與紅黃牌球員（烏龍球不計），合併更新球員統計。排程維持每 8 小時不變。

### 變更（Changed）

- `sync_to_site.py`、`push_to_github.py` 同步清單加入 `players.json`／`leaderboards.json`；`CRON_RUNBOOK.md` 與技能 `wc2026-prediction-automation`（SKILL.md + runbook.md，已重新驗證存庫）同步新增球員統計步驟。
- 詳見 [`RELEASE_NOTES_2026-06-17-players-feature.md`](RELEASE_NOTES_2026-06-17-players-feature.md)。

---

## [網站文字] 2026-06-17 前端主模型標示更新為 Sonnet 4.6

### 變更（Changed）

- 首頁副標題、預測卡「多模型對決」標題、`Consensus` 型別註解中的「Opus 4.8」描述更新為 **Sonnet 4.6**，與現行主預測模型一致。
- 純為前端静態文字調整；預測資料、指標與歷史批次不受影響。

---

## [設定變更] 2026-06-17 主預測模型切換 Opus 4.8 → Sonnet 4.6（僅未來）

### 變更（Changed）

- 依使用者指示，定時任務 AI 預測主模型由 **Claude Opus 4.8** 切換為 **Claude Sonnet 4.6（最新型號）**：研究子代理 `model="claude_sonnet_4_6"`、預測檔 `model:"claude-sonnet-4.6"`、賽後覆盤生成模型同步更新。
- 同步更新 cron `c53acfd7` 任務定義、技能 `wc2026-prediction-automation`（SKILL.md + runbook.md，已重新驗證存庫）、`CRON_RUNBOOK.md`。
- 網站基準計分主預測標籤改為模型中立的「AI（本站主預測）」；`multimodel_predict.py` 共識說明改為依預測檔 `model` 欄動態顯示實際模型。
- **僅影響未來預測批次**；所有歷史預測檔、賽後覆盤與舊版發行紀錄保留不動。
- 詳見 [`RELEASE_NOTES_2026-06-17-model-switch-sonnet46.md`](RELEASE_NOTES_2026-06-17-model-switch-sonnet46.md)。

---

## [資料更新] 2026-06-17T0107Z 新增 #28 預測 + 補記 #17/#18 賽果（HKT 6/17 上午）

### 新增（Added）

- 新增 1 場小組賽預測（Claude Opus 4.8 主預測 + 7 家第三方模型對照與共識 `models_used=8`）：**#28 墨西哥 2:1 南韓**（A 組，HKT 06/19 09:00，主勝，信心 0.55，來源 102 處）。七家第三方 AI（MiniMax M3／Qwen3.7 Max／DeepSeek V4 Pro／GPT-5.1 Thinking／Gemini 3.1 Pro／Grok 4.20／GLM-4.7）**全數**預測墨西哥 2:1 小勝，與主預測完全一致。
- 補記 2 場已確認賽果並產生 Opus 4.8 繁中賽後覆盤：**#17 法國 3:1 塞內加爾**（姆巴佩梅開二度破紀錄；賽前預測 2:1 主勝，勝負命中）、**#18 伊拉克 1:4 挪威**（哈蘭德世界盃首秀梅開二度；賽前預測 0:3 客勝，勝負命中、比分接近）。

### 變更（Changed）

- #20–#27 已於前一輪 Run #10（`2026-06-17T0055Z`）完整預測，本輪不重複；本輪為 00:55Z 槽次（真實觸發 01:07Z）。
- **防偽驗證成功**：前一輪因 YouTube 流出「法國 2-0／伊拉克 1-2」未經權威確認而延後記錄；本輪經 ESPN、Sky Sports、衛報、Washington Post、FOX Sports 等 8+ 權威來源交叉確認真實比分為 **3:1** 與 **1:4**，證實前一輪延後決策正確。
- 指標提升：**勝負命中率 5/14（35.7%）**（前一輪 3/12=25.0%）、比分完全命中 0/14、Brier **0.281**、ECE **0.2857**。
- 同步至網站（96 個預測批次檔）、Notion（新增 #28 頁）與 GitHub。仍處小組賽，排程維持每 8 小時。
- 詳見 [`RELEASE_NOTES_2026-06-17T0107Z.md`](RELEASE_NOTES_2026-06-17T0107Z.md)。

---

## [資料更新] 2026-06-17T0055Z 8 場新預測 #20–#27（含 3 場新場次）（HKT 6/17 凌晨）

### 新增（Added）

- 新增 8 場小組賽預測（Claude Opus 4.8 主預測，每場附 7 家第三方模型對照與共識 `models_used=8`）：#20 奧地利 2:0 主（共識 2:0）·#21 葡萄牙 2:0 主（共識 2:0）·#22 英格蘭 1:0 主（信心 .55，AI 共識側偏 2:1）·#23 迦納 2:1 主（信心 .46，Opta 模型反看好巴拿馬）·#24 烏茲別克 0:2 客（共識 0:2）·#25 捷克 2:0 主·#26 瑞士 2:0 主·#27 加拿大 2:0 主。其中 **#25 捷克 vs 南非、#26 瑞士 vs 波黑、#27 加拿大 vs 卡塔爾為首次納入的新場次**（#27 為主辦國加拿大主場戰）。
- 來源數：#20 (105)、#21 (102)、#22 (103)、#23 (100)、#24 (102)、#25 (66)、#26 (62)、#27 (58)。近 36 小時內開賽者（#20–#24）≥100 處／場，其餘 48 小時窗口（#25–#27）≥50 處／場。

### 變更（Changed）

- 本輪無新增已確認賽果：#17 法國 vs 塞內加爾、#18 伊拉克 vs 挪威剛結束，權威即時比分服務尚未刊出可信最終比分，依防偽鐵則延至下一輪確認後再記錄。整體指標維持 **勝負命中率 3/12（25.0%）**、比分完全命中 0/12、Brier 0.3126、ECE 0.3875。
- 同步至網站（95 個預測批次檔）、Notion（資料庫新增 8 頁）與 GitHub。仍處小組賽，排程維持每 8 小時。
- 詳見 [`RELEASE_NOTES_2026-06-17T0055Z.md`](RELEASE_NOTES_2026-06-17T0055Z.md)。

---

## [資料更新] 2026-06-16T0855Z 1 場冷門和局賽果 #16 + 8 場新預測 #17–#24（HKT 6/16 下午）

### 新增（Added）

- 新增 1 場賽果（**又一冷門和局，AI 落空**）：#16 伊朗 2:2 紐西蘭（紐西蘭 Elijah Just 梅開二度，伊朗兩度落後兩度追平）。賽前預測 2:0 主勝（信心 .56）→ 落空；賽後覆盤 verdict=`miss`。
- 新增 8 場小組賽預測（Claude Opus 4.8 主預測，每場附 7 家第三方模型對照與共識 `models_used=8`）：#17 法國 2:1 主（共識 2:0）·#18 伊拉克 0:3 客（共識 0:2）·#19 阿根廷 2:0 主·#20 奧地利 2:0 主·#21 葡萄牙 2:0 主·#22 英格蘭 2:1 主·#23 迦納 1:1 和（信心 .42，AI 共識側偏迦納 2:1）·#24 烏茲別克 0:2 客（共識 0:2）。其中 **#24 烏茲別克 vs 哥倫比亞 為首次納入的新場次**（烏茲別克隊史首場世界盃）。
- 來源數：#17 (107)、#18 (112)、#19 (115)、#20 (106)、#21 (102)、#22 (101)、#23 (73)、#24 (69)。近 36 小時內開賽者（#17–#22）≥100 處／場，其餘 48 小時窗口 ≥50 處／場。

### 變更（Changed）

- 指標重算（`accuracy.json`／`calibration.json`／`benchmark_scores.json`）：因新增 #16 冷門和局，整體**勝負命中率降至 3/12（25.0%）**、比分完全命中 0/12、Brier 0.3126、ECE 0.3875（仍偏過度自信）。
- 同步至網站、Notion（資料庫新增 8 頁）與 GitHub。仍處小組賽，排程維持每 8 小時。
- 詳見 [`RELEASE_NOTES_2026-06-16T0855Z.md`](RELEASE_NOTES_2026-06-16T0855Z.md)。

---

## [資料更新] 2026-06-16T0055Z 3 場冷門和局賽果 #13–#15 + 7 場新預測 #17–#23（HKT 6/16 上午）

### 新增（Added）

- 新增 3 場賽果（**均為冷門和局，AI 三場全數落空**）：#13 西班牙 0:0 佛得角（40 歲門將神撲）、#14 比利時 1:1 埃及（烏龍球扳平）、#15 沙烏地 1:1 烏拉圭（門將神勇）。三場賽後覆盤（postmortem）已生成，verdict 皆為 `miss`。
- 新增 7 場小組賽預測（Claude Opus 4.8 主預測，每場附 7 家第三方模型對照與共識 `models_used=8`）：#17 法國 2:1 主（共識 2:0）·#18 伊拉克 0:3 客（共識 0:2）·#19 阿根廷 2:0 主·#20 奧地利 2:0 主·#21 葡萄牙 2:0 主·#22 英格蘭 2:1 主·#23 迦納 2:1 主（信心 .46）。其中 #22、#23 為首次納入的新場次。
- 來源數：#17 (109)、#18 (104)、#19 (105)、#20 (110)、#21 (74)、#22 (71)、#23 (67)。近 36 小時內開賽者（#17–#20）≥100 處／場，其餘 48 小時窗口 ≥50 處／場。

### 變更（Changed）

- 指標重算（`accuracy.json`／`calibration.json`／`benchmark_scores.json`）：因新增三場失準結果，整體**勝負命中率降至 3/11（27.3%）**、比分完全命中 0/11、Brier 0.3135、ECE 0.3718（仍偏過度自信）。
- 同步至網站、Notion（資料庫新增 7 頁）與 GitHub。仍處小組賽，排程維持每 8 小時。
- 詳見 [`RELEASE_NOTES_2026-06-16T0055Z.md`](RELEASE_NOTES_2026-06-16T0055Z.md)。

---

## [資料更新] 2026-06-15T1710Z 新增 8 場小組賽預測 #14–#21（HKT 6/16 清晨）

### 新增（Added）

- 新增 8 場小組賽預測（Claude Opus 4.8 主預測，每場附 7 家第三方模型對照與共識 `models_used=8`）：#14 比利時 2:1 主·#15 沙烏地 0:2 客·#16 伊朗 2:0 主·#17 法國 2:1 主（共識 2:0）·#18 伊拉克 0:3 客（共識 0:2）·#19 阿根廷 2:0 主·#20 奧地利 2:0 主·#21 葡萄牙 2:0 主。
- 來源數：#14 (180)、#15 (166)、#16 (229)、#17 (109)、#18 (104)、#19 (105)、#20 (153)、#21 (63)。近 36 小時內開賽者 ≥100 處／場。
- 每場含 `top_scorelines`、`scenarios`、`prediction.benchmarks`（公開博彩／模型基準線）與繁中 `reasoning`。

### 變更（Changed）

- 指標重算（`accuracy.json`／`calibration.json`／`benchmark_scores.json`）：本批次比賽尚無結果，整體指標維持不變。
- 同步至網站、Notion（資料庫新增 8 頁）與 GitHub。仍處小組賽，排程維持每 8 小時。
- 詳見 [`RELEASE_NOTES_2026-06-15T1710Z.md`](RELEASE_NOTES_2026-06-15T1710Z.md)。

---

## [變更] 2026-06-16 第三方多模型對照擴充至 7 家（HKT 6/16 清晨）

### 新增（Added）

- 第三方對照新增 4 家最新模型（經 Vercel AI Gateway）：OpenAI GPT-5.1 Thinking、Google Gemini 3.1 Pro、xAI Grok 4.20 Reasoning、Z.ai GLM-4.7。連同原有 MiniMax M3／千問 Qwen3.7 Max／DeepSeek V4 Pro，第三方對照共 7 家；加上本站 Opus 4.8 主預測，綜合共識 `models_used` 最多達 8。

### 變更（Changed）

- `multimodel_predict.py`：`MODELS` 擴充為 7 家；`max_tokens` 600 → 3000（reasoning 模型 Gemini／GLM 需較大上限才能在推理後輸出 JSON）；新增退化防護（比分須符合 `^\d+:\d+$`，否則視同失敗）。
- 回填 #13–#20：對 8 場既有預測各跑一次七模型對照，重算頂層 `benchmarks`（kind=ai）與 `consensus`。主 Opus 預測維持不變。回填後共識：#13 西班牙 3:0 · #14 比利時 2:0 · #15 沙烏地 0:2 客 · #16 伊朗 2:0 · #17 法國 2:0 · #18 伊拉克 0:2 客 · #19 阿根廷 2:0 · #20 奧地利 2:0。
- 文檔同步更新：`PREDICTION_METHODOLOGY.md`、`README.md`（§預測方法）、`data/predictions/SCHEMA.md`、`CRON_RUNBOOK.md` 全部改為 7 家模型、`max_tokens 3000`；前端 `PredictionCard` 對照說明列出 7 家來源。
- 指標重算（`accuracy.json`／`calibration.json`／`benchmark_scores.json`）。新增 4 家模型僅出現在尚無結果的 #13–#20，待相關比賽結束後才納入對照排行榜。
- 詳見 [`RELEASE_NOTES_2026-06-16-multimodel-7.md`](RELEASE_NOTES_2026-06-16-multimodel-7.md)。

---

## [文件] 2026-06-15 新增預測方法說明（HKT 6/15 晚間）

### 新增（Added）

- 新增 [`PREDICTION_METHODOLOGY.md`](PREDICTION_METHODOLOGY.md)：完整預測方法說明，涵蓋主預測引擎（Claude Opus 4.8、來源數分級、關鍵因素、輸出欄位）、第三方多模型對照與共識算法、賽後覆盤、評分與校準機制、設計原則。

### 變更（Changed）

- `README.md` 新增「預測方法（Prediction Methodology）」章節，摘要整條預測與評分邏輯並連結至完整文件；檔案索引表加入 `PREDICTION_METHODOLOGY.md`。

---

## [資料更新] 2026-06-15T0904Z 預測批次（HKT 6/15 下午）

### 新增（Added）— 第 13–20 場小組賽預測（8 場，主模型 Claude Opus 4.8）

- 對即將開賽的 8 場小組賽（#13–#20）產生全新預測批次 `2026-06-15T0904Z`，獨立寫入 `site/data/predictions/match_{13..20}__2026-06-15T0904Z.json`，不覆蓋舊批次。
  - #13 西班牙 3:0 佛得角（信心 0.81，122 源）· #14 比利時 2:1 埃及（0.58，180）· #15 沙烏地阿拉伯 0:2 烏拉圭（0.63，166）· #16 伊朗 2:0 紐西蘭（0.60，229）
  - #17 法國 2:1 塞內加爾（0.60，134）· #18 伊拉克 0:2 挪威（0.78，89）· #19 阿根廷 2:0 阿爾及利亞（0.73，97）· #20 奧地利 2:0 約旦（0.60，55）
  - 來源數分級：近 36h 內開賽者每場 ≥100 源；其餘 48h 窗口每場 ≥50 源。
- 每場預測檔均附**第三方多模型對照**（MiniMax M3／Qwen3.7 Max／DeepSeek V4 Pro）與**頂層共識**。

### 新增（Added）— 1 場比賽結果與 Opus 賽後覆盤

- #12 瑞典 **5:1** 突尼西亞（Ayari 7'&90+6'、Isak 30'、Gyökeres 59'、Svanberg 84'；突尼西亞 Rekik 43'）。原預測 1:0 主勝 → 方向正確、比分大幅偏保守。
- 附 Claude Opus 4.8 繁中賽後覆盤，合併寫入 `postmortems.json`。

### 變更（Changed）— 指標重算

- `accuracy.json`：已評估 8 場，勝負方向 **3/8（37.5%）**、正確比分 **0/8**。
- `calibration.json`：**Brier 0.2436、ECE 0.29、過度自信 0.2625**。
- `benchmark_scores.json`：9 條基準線、涵蓋 8 場（本站 Opus 3/8、Brier 0.2436；MiniMax 3/4；DeepSeek 3/4；Qwen 2/4；Football Meister AI 1/1；博彩 1/4；Opta 1/4；Polymarket 0/1；Kalshi 0/1）。

---

## [資料更新] 2026-06-15T0855Z 預測批次（HKT 6/15 下午）

### 新增（Added）— 第 12–19 場小組賽預測（8 場，主模型 Claude Opus 4.8）

- 對即將開賽的 8 場小組賽（#12–#19）產生全新預測批次 `2026-06-15T0855Z`，獨立寫入 `site/data/predictions/match_{12..19}__2026-06-15T0855Z.json`，不覆蓋舊批次。
  - #12 瑞典 1:0 突尼西亞（信心 0.57，155 源）· #13 西班牙 3:0 佛得角（0.80，106）· #14 比利時 2:1 埃及（0.58，180）· #15 沙烏地阿拉伯 0:2 烏拉圭（0.63，155）
  - #16 伊朗 1:0 紐西蘭（0.60，216）· #17 法國 2:1 塞內加爾（0.60，57）· #18 伊拉克 0:2 挪威（0.78，92）· #19 阿根廷 2:0 阿爾及利亞（0.74，92）
  - 來源數分級：#12–#16 在 36h 內開賽（≥100 源）；#17–#19 在 48h 窗口（≥50 源）。
- 每場預測檔均附**第三方多模型對照**（MiniMax M3／Qwen3.7 Max／DeepSeek V4 Pro）與**頂層共識**。

### 新增（Added）— 3 場比賽結果與 Opus 賽後覆盤

- #9 德國 **7:1** 庫拉索（方向正確、比分偏保守）· #10 荷蘭 **2:2** 日本（逼和 dissent 兌現）· #11 象牙海岸 **1:0** 厄瓜多爾（90' 絕殺，原 1:1 和局落空）。
- 三場各附 Claude Opus 4.8 繁中賽後覆盤，合併寫入 `postmortems.json`。

### 變更（Changed）— 指標重算

- `accuracy.json`：已評估 7 場，勝負方向 **2/7（28.6%）**、正確比分 **0/7**。
- `calibration.json`：**Brier 0.2455、ECE 0.3929、過度自信 0.3614**。
- `benchmark_scores.json`：9 條基準線、涵蓋 7 場（本站 Opus 2/7；MiniMax 2/3；DeepSeek 2/3；Qwen 1/3；Football Meister AI 1/1；博彩 1/4；Opta 1/4）。

---

## [資料更新] 2026-06-14T1655Z 預測批次（HKT 6/15 凌晨）

### 新增（Added）— 第 9–16 場小組賽預測刷新（全部 36h 內開賽，皆 ≥100 源）

- 以 **Claude Opus 4.8** 為本站主預測，對即將開賽的 8 場小組賽（#9–#16）產生全新預測批次 `2026-06-14T1655Z`，獨立寫入 `site/data/predictions/match_{9..16}__2026-06-14T1655Z.json`，不覆蓋舊批次。
  - #9 德國 4:0 庫拉索（信心 0.89，144 源）· #10 荷蘭 2:1 日本（0.56，133）· #11 象牙海岸 1:1 厄瓜多爾（0.42，148）· #12 瑞典 1:0 突尼西亞（0.57，135）
  - #13 西班牙 3:0 佛得角（0.86，140）· #14 比利時 2:1 埃及（0.58，164）· #15 沙烏地阿拉伯 0:2 烏拉圭（0.63，135）· #16 伊朗 1:0 紐西蘭（0.60，189）
  - 8 場皆落在觸發後 36 小時內開賽，故每場來源數 ≥100。
- 每場預測檔均附**第三方多模型對照**（MiniMax M3／Qwen3.7 Max／DeepSeek V4 Pro）與**頂層共識**；#15 DeepSeek 回傳格式異常已自動略過（以 2 個 AI 完成對照）。
- 重算 `accuracy.json`、`calibration.json`（Brier 0.3386、ECE 0.415）、`benchmark_scores.json`（6 基準線、4 場）。
- 本批次無新完成比賽：#9 觸發時剛開賽進行中，餘場未開賽；已嚴格排除網路上 AI 捏造的「賽後比分」偽結果。

### 移除（Removed）

- 清除誤入 `data/predictions/` 與 `site/data/predictions/` 的子代理建置腳本（`build_*.py`／`gen_*.py`／`_*.py`），保持資料目錄純淨。

---

## [資料更新] 2026-06-14T0855Z 預測批次（HKT 6/14 下午）

### 新增（Added）— 第 9–16 場小組賽預測刷新

- 以 **Claude Opus 4.8** 為本站主預測，對即將開賽的 8 場小組賽（#9–#16）產生全新預測批次 `2026-06-14T0855Z`，獨立寫入 `site/data/predictions/match_{9..16}__2026-06-14T0855Z.json`，不覆蓋舊批次。
  - #9 德國 4:0 庫拉索（信心 0.89，137 源）· #10 荷蘭 2:1 日本（0.55，116）· #11 象牙海岸 1:1 厄瓜多爾（0.43，139）· #12 瑞典 1:0 突尼西亞（0.56，111）
  - #13 西班牙 3:0 佛得角（0.85，128）· #14 比利時 2:1 埃及（0.61，121）· #15 沙烏地阿拉伯 0:2 烏拉圭（0.63，70）· #16 伊朗 1:0 紐西蘭（0.50，67）
  - 36 小時內開賽場次（#9–#14）來源數 ≥100；其餘 48 小時窗口場次（#15–#16）≥50。
- 每場預測檔均附**第三方多模型對照**（MiniMax M3／Qwen3.7 Max／DeepSeek V4 Pro，僅比分＋三向勝率＋一句話 take）與**頂層共識**，第三方僅作對照，主預測仍為 Opus 4.8。
- 重算 `accuracy.json`、`calibration.json`、`benchmark_scores.json`（已評估 4 場，維持不變）。

### 移除（Removed）

- 清除誤入 `site/data/predictions/` 的子代理建置腳本（`_*.py`），保持資料目錄純淨。

---

## [1.5.0] — 2026-06-14

### 變更（Changed）— 全站即時讀取按鈕移至頭部條

1. **後端新端點 `/api/live-all`**（`site/server/routes.ts`）
   - 一次並行抓取 GitHub raw 上**所有資料集**：`results`、`accuracy`、`calibration`、`postmortems`、`benchmark_scores`、`fixtures`，以及全部 `predictions`（先讀 `predictions/manifest.json` 取得檔案清單再並行抓取）。
   - predictions 依場次分組、依 `run_timestamp` 由新到舊排序，與 `/api/predictions` 一致。
   - 沿用 **60 秒快取**（`liveAllCache` / `LIVE_TTL_MS`）與 6 秒逾時保護（AbortController）；任一抓取失敗即整體回退本機打包資料並標明 `source`（`github` ／ `local-fallback`）。

2. **頭部條全站即時讀取按鈕**（`site/client/src/components/Header.tsx`）
   - 「即時讀取最新」按鈕移至頁面**頭部條**，**每一個分頁皆可見**（不再只限結果分頁）。
   - 來源／時間徽章：GitHub 即時 ／ 讀取失敗·本機；載入時 `RefreshCw` 圖示旋轉。

3. **點擊一鍵更新全站**（`site/client/src/pages/dashboard.tsx`）
   - 點擊後查詢 `/api/live-all`，並以結果回填（seed）所有相關 query 快取：`/api/fixtures`、`/api/predictions`、`/api/results`、`/api/accuracy`、`/api/calibration`、`/api/postmortems`、`/api/benchmark-scores`，再使 `/api/status` 失效。
   - **每一個分頁同步顯示 GitHub 最新內容**，不必等待下一次重新發布。
   - 移除結果分頁專屬的舊「即時讀取」控制卡（功能整併至頭部）。

4. **預測檔清單 `manifest.json`**（`sync_to_site.py`）
   - `sync_to_site.py` 同步時自動產生 `site/data/predictions/manifest.json`（列出全部 `match_*.json` 檔名），供前端／`/api/live-all` 在 GitHub raw 上枚舉預測檔（raw 無目錄列舉能力）。
   - `/api/predictions` 與 `/api/status` 掃描預測目錄時忽略 `manifest.json`。

---

## [1.4.0] — 2026-06-14（run 2026-06-14T0551Z）

### 新增（Added）— 即時讀取 GitHub 最新結果

1. **後端新端點 `/api/live-results`**（`site/server/routes.ts`）
   - 即時抓取 GitHub raw（`https://raw.githubusercontent.com/tonylnng/tonic-fifa-wc2026/master/site/data/results.json`）的最新比賽結果，不需等待網站重新發布。
   - 內建 **60 秒快取**（`liveCache` / `LIVE_TTL_MS`），避免每次請求都打 GitHub；6 秒逾時保護（AbortController）。
   - 回傳完整結果物件 ＋ `source`（`github` ／ `local-fallback`）＋ `cached` 旗標；GitHub 讀取失敗時自動回退本機打包資料並標明來源。

2. **前端「即時讀取」控制卡**（`site/client/src/pages/dashboard.tsx`）
   - 結果頁新增手動「即時讀取 GitHub 最新結果」按鈕（`RefreshCw` 圖示），點擊後查詢 `/api/live-results`。
   - 狀態徽章：GitHub 即時 ／ 快取 ／ 回退本機 ／ 本機打包，並以**香港時間**顯示資料更新時間（`hktTimestamp()` 輔助函式）。
   - 有即時資料時優先顯示 GitHub 最新結果（`active = live ?? results`），否則使用本機打包資料。

### 新增（Added）— 賽後覆盤改用 Opus 4.8

- 賽後覆盤（postmortems）生成模型由先前流程改為 **Claude Opus 4.8**（與本站主預測一致），確保覆盤分析品質一致。

### 資料更新（Data）

- 新增第 7、8 場最終比分：第 7 場 海地 0:1 蘇格蘭（蘇格蘭勝）、第 8 場 澳洲 2:0 土耳其（澳洲勝，爆冷）。`results.json` 現含 8 場結果。
- 第 7、8 場 Opus 4.8 賽後覆盤（run 2026-06-14T0057Z）：第 7 場勝負命中、比分失準；第 8 場爆冷失準。`postmortems.json` 現含第 5、6、7、8 場共 4 份覆盤。
- 第 9–16 場全新 Opus 4.8 預測（run 2026-06-14T0551Z），含 top_scorelines／scenarios／頂層 benchmarks（含第三方 AI MiniMax／千問／DeepSeek）／consensus，並已同步至 Notion。
- 重算 accuracy／calibration／benchmark_scores（已評估 4 場，勝負 1/4、比分 0/4、Brier 0.3386、ECE 0.415）。

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
