# 世界盃 2026 AI 預測中心

一個全自動的 FIFA 世界盃 2026 賽事預測系統。雲端工作區每隔數小時研究最新情報、產生 X:X 比分預測與分析理由，把資料推送到 GitHub；你的 Docker 伺服器自動拉取並展示；同時同步到 Notion 追蹤。所有使用者介面皆為**繁體中文**。

- 🌐 雲端版：<https://tonic-fifa-wc2026.pplx.app>
- 🏠 自架版：<https://wc2026.toniclab.ai>（你的伺服器）

---

## 系統架構

整套系統分四個角色，預測運算全部在雲端，你的伺服器零運算負擔、不需任何 API 金鑰。

![系統架構圖](docs/architecture.svg)

> 上圖為 animated SVG overview（在瀏覽器 / GitHub 開啟時資料流會動）。完整技術圖表（應用架構、工作流程、狀態、循序、ER 圖、資料字典）見 [`docs/技術圖表.md`](docs/技術圖表.md)。資料流向：

```
雲端工作區（每 8 小時 · 16 強起每 4 小時）
   │  研究 ≥50 來源 → X:X 預測 + 理由 → 算準確率
   ├──→ push data/ ─────────────→ GitHub（資料中轉站）
   │                                   │
   │                                   │ 你的伺服器偵測新 commit
   │                                   ▼
   │                          你的 Docker 伺服器（git pull + 重啟容器）
   │                          Nginx + Certbot → wc2026.toniclab.ai
   │
   └──→ 同步預測 ────────────────→ Notion（預測追蹤資料庫）
```

**雙方都有定時任務：**

| 角色 | 定時任務 | 頻率 |
|------|----------|------|
| 雲端工作區 | 產生預測 → push GitHub → 同步 Notion → 重新發布 pplx.app | 每 8 小時（16 強起每 4 小時） |
| 你的伺服器 | 偵測 GitHub 新 commit → `git pull` → 重啟容器 | webhook 即時 ／ systemd timer 每 5 分鐘輪詢 |

---

## 這個項目包含什麼

| 路徑 | 用途 |
|------|------|
| `site/` | 全端網站（Express + Vite + React + Tailwind）：賽程 Master List、AI 預測卡（附 50+ 來源連結 + 賽前倒數 + 多模型對決 + 模型共識）、結果與準確率儀表板、校準與基準、賽後覆盤（無密碼，公開）。頭部條提供**全站即時讀取 GitHub 最新內容**按鈕（`/api/live-all`），點擊即同步更新所有分頁 |
| `site/data/fixtures.json` | 104 場賽程 Master List（48 隊分 A–L 組 + 淘汰賽路徑），含權威 `kickoff_utc`（前端統一轉香港時間） |
| `site/data/results.json` | 已完成比賽的最終比分 |
| `site/data/accuracy.json` | 勝負命中率、比分命中率統計 |
| `site/data/calibration.json` | 信心校準：信心分桶 vs 實際命中率、Brier、ECE、過度自信 |
| `site/data/benchmark_scores.json` | AI vs 博彩／Opta／預測市場 的並列計分排行榜 |
| `site/data/postmortems.json` | 賽後覆盤：每場「為何命中／失準」短評（可搜尋知識庫） |
| `site/data/predictions/` | 每場每批次獨立保存的預測 JSON（永不覆蓋，檔名含 run_id），含 top_scorelines／scenarios／頂層 benchmarks（含第三方 AI）／consensus |
| `Dockerfile` / `docker-compose.yml` | 自架部署用的容器設定 |
| `deploy/` | 伺服器自動拉取與重啟工具（webhook + systemd timer + Nginx 設定） |
| `multimodel_predict.py` | 經 Vercel AI Gateway 呼叫第三方 AI（MiniMax／千問／DeepSeek），寫入頂層 benchmarks（kind=ai）與 consensus |
| `update_accuracy.py` `compute_calibration.py` `compute_benchmark_scores.py` `build_postmortems.py` `sync_to_site.py` `push_to_github.py` | 雲端排程每輪呼叫的資料處理腳本 |
| `fix_fixture_times.py` | 一次性開賽時間校正腳本（以權威 UTC 賽程修正 fixtures） |
| `CRON_RUNBOOK.md` | 雲端排程每輪執行的完整手冊 |
| `PREDICTION_METHODOLOGY.md` | 預測方法完整說明：主預測引擎、第三方對照、評分與校準機制 |
| `automation/排程自動化總覽.md` | 整套自動化邏輯與檔案說明 |
| `docs/architecture.svg` | 上方的動態架構圖（overview） |
| `docs/技術圖表.md` | Mermaid 技術圖：應用架構 / 工作流程 / 狀態 / 循序 / ER 圖 / 資料字典 |

---

## 安裝步驟（在你的伺服器上）

> 適合用 OpenClaw 或任何能執行 shell 的環境照著跑。前置：已安裝 **Docker** 與 **Docker Compose**，且 `wc2026.toniclab.ai` 的 DNS A/AAAA 紀錄已指向這台伺服器。

### 步驟 0 — 校準系統時鐘（NTP，必做）

伺服器時鐘要準，否則 webhook 簽章驗證、timer 觸發、資料「距今多久」計算都可能出錯。

```bash
# 開啟 NTP 自動授時並確認狀態
sudo timedatectl set-ntp true
timedatectl                 # 確認 "System clock synchronized: yes" 且時區正確
# 若無 systemd-timesyncd，可裝 chrony：sudo apt install -y chrony && sudo systemctl enable --now chrony
```

### 步驟 1 — 取得程式碼並啟動容器

```bash
# clone 到 /opt（路徑可自訂，後續 deploy 工具預設用這個）
sudo git clone https://github.com/tonylnng/tonic-fifa-wc2026.git /opt/tonic-fifa-wc2026
cd /opt/tonic-fifa-wc2026

# 本站預設無密碼、公開存取。若要自架時加上登入密碼：
#   取消 docker-compose.yml 內 SITE_PASSWORD 那行的註解並填入你自己的密碼。
#   注意：YAML 會把 $$ 解析成一個 $，密碼若含 $ 字元請自行加倍跳脫。

# 因為前面會放 Nginx，建議容器只綁本機（避免被繞過直接存取）：
#   把 docker-compose.yml 的 ports 改成  "127.0.0.1:5000:5000"

docker compose up -d
chmod +x deploy/update.sh deploy/webhook.py
```

此時 `http://127.0.0.1:5000` 已可在本機存取。

### 步驟 2 — 設定網域 + HTTPS（Nginx + Certbot）

```bash
# 安裝 Nginx 並啟用 server block
sudo apt install -y nginx
sudo cp deploy/nginx/wc2026.toniclab.ai.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/wc2026.toniclab.ai.conf /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# 申請 HTTPS 憑證（Certbot 會自動補上 443 區塊並設定自動續期）
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d wc2026.toniclab.ai
```

完成後開 <https://wc2026.toniclab.ai> 輸入密碼即可登入。

### 步驟 3 — 設定自動更新（webhook 或 timer，擇一）

讓伺服器在雲端排程 push 後自動拉取最新資料。完整說明見 [`deploy/自動部署說明.md`](deploy/自動部署說明.md)。

**方案 A — Webhook 即時觸發（推薦，秒級更新）**

```bash
# 產生密鑰（GitHub 那邊要填一樣的）
openssl rand -hex 20

sudo cp deploy/wc2026-webhook.service /etc/systemd/system/
sudo nano /etc/systemd/system/wc2026-webhook.service   # 填入上面的 WEBHOOK_SECRET
sudo systemctl daemon-reload
sudo systemctl enable --now wc2026-webhook.service
```

再把 `deploy/nginx/wc2026.toniclab.ai.conf` 裡的 `/gh-webhook` 區塊取消註解、`reload nginx`，
然後到 GitHub repo → Settings → Webhooks 新增：
- Payload URL：`https://wc2026.toniclab.ai/gh-webhook`
- Content type：`application/json`、Secret：上面的密鑰、事件選 push

**方案 B — systemd timer 定時輪詢（不需對外開埠）**

```bash
sudo cp deploy/wc2026-deploy.service /etc/systemd/system/
sudo cp deploy/wc2026-deploy.timer   /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now wc2026-deploy.timer
systemctl list-timers wc2026-deploy.timer   # 確認下次執行時間
```

> 輪詢間隔預設 **每 15 分鐘**（`wc2026-deploy.timer` 的 `OnUnitActiveSec=15min`）。因為雲端每 8 小時（16 強起 4 小時）才更新一次，15 分鐘已綣綣有餘；要更即時可改用方案 A webhook。

---

## 更新步驟

### 平常更新（全自動，無需動手）

雲端排程每輪 push 後，伺服器會透過 webhook（秒級）或 timer（5 分鐘內）自動：
`git reset --hard` 拉最新 → 只動到 `site/data/` 就 `docker compose restart`、動到程式碼就 `docker compose up -d --build`。

### 手動更新（如要立即拉一次）

```bash
cd /opt/tonic-fifa-wc2026
REPO_DIR=/opt/tonic-fifa-wc2026 ./deploy/update.sh
```

### 更新邏輯設定（`deploy/update.sh` 環境變數）

| 變數 | 說明 | 預設 |
|------|------|------|
| `REPO_DIR` | repo 在伺服器路徑 | `/opt/tonic-fifa-wc2026` |
| `BRANCH` | 追蹤分支 | `master` |
| `COMPOSE` | compose 指令 | `docker compose`（舊版改 `docker-compose`） |
| `FORCE_REBUILD` | 設 `1` 則每次強制重新 build | `0` |
| `LOG` | 日誌路徑 | `/var/log/wc2026-deploy.log` |

---

## 驗證與排錯

```bash
docker compose ps                                  # 容器是否在跑
tail -f /var/log/wc2026-deploy.log                 # 自動更新日誌
sudo journalctl -u wc2026-webhook.service -f       # webhook 服務（方案 A）
sudo journalctl -u wc2026-deploy.service -f        # timer 執行紀錄（方案 B）
sudo nginx -t                                       # Nginx 設定檢查
sudo systemctl status certbot.timer                 # 憑證自動續期
```

---

## 雲端端（預測引擎）說明

預測產生、Notion 同步、pplx.app 重新發布由 Perplexity 雲端排程負責，**不需要在你的伺服器上跑**。
你的伺服器只讀取 GitHub 上的 `data/` 並展示。若日後想把預測引擎搬到自己環境，需自備來源蒐集與 LLM 推理管線；
本 repo 的資料處理腳本與 JSON 結構（`update_accuracy.py` / `sync_to_site.py` / `push_to_github.py`）可直接沿用。

完整每輪步驟見 [`CRON_RUNBOOK.md`](CRON_RUNBOOK.md) 與 [`automation/排程自動化總覽.md`](automation/排程自動化總覽.md)。

---

## 預測方法（Prediction Methodology）

> 這一節說明「如何產生一場比賽的 AI 預測」以及「如何評分與對照」的完整邏輯。完整版另見 [`PREDICTION_METHODOLOGY.md`](PREDICTION_METHODOLOGY.md)。

### 一次排程做了什麼

定時任務每 8 小時觸發（小組賽；16 強起每 4 小時），走一條完整管線：

```
判斷階段 → 找未來 48h 內、尚無結果的即將開賽比賽
  → 對每場：①Opus 4.8 深度研究預測  ②第三方多模型對照+共識
    → 收錄新完成比賽結果 + Opus 賽後覆盤
      → 重算 準確率 / 校準 / 基準線排行
        → 同步：網站 → Notion → GitHub → 重新發布 pplx.app → 發繁中通知
```

### ① 主預測引擎：Claude Opus 4.8

本站主預測固定為 **Anthropic Claude Opus 4.8**。每場由獨立研究子代理負責，**證據驅動而非記憶驅動**：

- **來源數分級**（依開賽急迫度）：
  - 近 36 小時內開賽 → **≥100 處來源**
  - 其餘 48 小時窗口內 → **≥50 處來源**
- **來源涵蓋多視角**：官方（FIFA／足協／球隊）、媒體（ESPN／BBC／Goal／The Athletic…）、博彩／模型（盤口、Opta 超級電腦、Elo）、論壇社群（Reddit）、KOL／名嘴、YouTube 賽前分析。
- **關鍵判斷因素**：球員狀態、傷停名單、近期戰績、戰術對位、主客場／場地、輿論共識。
- **輸出非單一比分**，而是機率分佈與多角度：主預測比分＋三向勝率（總和=1）＋信心（0–1）、`top_scorelines`（3–5 個最可能比分）、`scenarios`（2–4 個情境）、`benchmarks`（博彩／Opta／市場等公開基準線）、繁中 `reasoning`。
- **每批次獨立保存**：寫入 `data/predictions/match_{場次}__{run_id}.json`，**永不覆蓋**舊批次，可回溯賽前最後判斷並稽核推理鏈。

> ⚠️ 宣稱「尚未開賽比賽最終比分」的 YouTube／網路「賽後 review」多為 AI 捏造，一律不採信。

### ② 第三方多模型對照 + 綜合共識

主預測寫好後，經 **Vercel AI Gateway** 呼叫三家第三方 AI（`minimax/minimax-m3`、`alibaba/qwen3.7-max`、`deepseek/deepseek-v4-pro`）作對照。第三方**只回傳比分＋三向勝率＋一句話 take**，僅作基準（`kind:"ai"`），本站結論永遠是 Opus 4.8。

- 三家 AI 追加到預測檔頂層 `benchmarks[]`；整數機率會 sum-normalize 為總和 1。
- **綜合共識（consensus）**：勝率採加權平均（**主預測權重 2、每家第三方權重 1**），比分採多數決（平手靠近主預測）。

### 賽後覆盤

比賽完成後寫入 `results.json`，並用 Opus 4.8 生成繁中覆盤（`postmortems.json`）：`verdict` 分 exact（比分全中）／outcome（方向中）／miss（落空），含 headline／review／lessons／vs_benchmarks。

### 評分機制（衡量準不準）

每輪以「該場最新一筆賽前預測」對比實際比分，重算三組指標：

| 指標檔 | 內容 |
|---|---|
| `accuracy.json` | 勝負命中率（1X2）、比分命中率（完全相同），並按階段分組 |
| `calibration.json` | **Brier**（機率均方差，越低越好）、**ECE**（期望校準誤差）、**過度自信**（平均信心 − 平均命中率） |
| `benchmark_scores.json` | 本站 AI 與所有基準線（博彩／Opta／市場／三家第三方 AI）在相同已完成比賽上的並列排行 |

### 設計原則

1. **權威主預測單一化** — 結論永遠是 Opus 4.8，第三方只作對照。
2. **證據驅動** — 每場強制蒐集 50–100+ 處即時來源。
3. **表達不確定性** — 機率分佈、多情境、多基準線，而非單點猜測。
4. **可稽核、不可竄改歷史** — 每批次獨立保存。
5. **持續自我評估** — 準確率／校準／基準排行三管齊下 + Opus 賽後覆盤。
6. **全繁中、香港時間** — 所有使用者面向內容一致。

---

## 安全注意事項

- 登入密碼由容器的 `SITE_PASSWORD` 環境變數控制，請務必改成你自己的強密碼。
- 建議容器只綁 `127.0.0.1`，對外一律走 Nginx + HTTPS。
- Webhook 使用 HMAC-SHA256 驗證 GitHub 簽章，密鑰請妥善保管。
