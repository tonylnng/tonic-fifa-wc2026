#!/usr/bin/env bash
# 世界盃 2026 — 自動更新腳本
# 從 GitHub 拉最新 data/，若有變更則重啟（或重建）Docker 容器。
# 方案 A（webhook）與方案 B（timer）都呼叫這支腳本。
set -euo pipefail

# ===== 設定（請依你的環境修改）=====
REPO_DIR="${REPO_DIR:-/opt/tonic-fifa-wc2026}"   # repo 在伺服器上的路徑
BRANCH="${BRANCH:-master}"
COMPOSE="${COMPOSE:-docker compose}"             # 舊版請改成 "docker-compose"
LOG="${LOG:-/var/log/wc2026-deploy.log}"
# 若資料是用 volume 掛載（docker-compose.yml 預設掛 ./site/data），
# 改資料後通常 restart 即可；設成 1 則每次強制重新 build。
FORCE_REBUILD="${FORCE_REBUILD:-0}"
# ===================================

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"; }

# 讀資料新鮮度：accuracy.json 的 last_updated（UTC）
freshness() {
  local f="$REPO_DIR/site/data/accuracy.json"
  [ -f "$f" ] || { echo "無資料檔"; return; }
  local lu
  lu=$(grep -oE '"last_updated"[^,]*' "$f" | head -1 | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:Z+-]+' || true)
  [ -n "$lu" ] || { echo "未知"; return; }
  local age=""
  if epoch=$(date -u -d "$lu" +%s 2>/dev/null); then
    age=" （距今 $(( ( $(date -u +%s) - epoch ) / 60 )) 分鐘）"
  fi
  echo "${lu}${age}"
}

cd "$REPO_DIR"

log "抓取遠端更新…"
git fetch --quiet origin "$BRANCH"

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse "origin/$BRANCH")

if [ "$LOCAL" = "$REMOTE" ]; then
  log "已是最新（$LOCAL），無需更新。"
  exit 0
fi

log "偵測到新版本：$LOCAL -> $REMOTE，開始更新…"
git reset --hard "origin/$BRANCH" >>"$LOG" 2>&1

# 判斷這次更新是否動到 data/ 以外的程式碼（程式碼變更需重新 build）
CHANGED=$(git diff --name-only "$LOCAL" "$REMOTE")
CODE_CHANGED=$(echo "$CHANGED" | grep -vE '^site/data/' || true)

if [ "$FORCE_REBUILD" = "1" ] || [ -n "$CODE_CHANGED" ]; then
  log "偵測到程式碼變更或強制重建，執行 build + up…"
  $COMPOSE up -d --build >>"$LOG" 2>&1
else
  log "僅資料變更，重啟容器即可…"
  $COMPOSE restart >>"$LOG" 2>&1
fi

log "更新完成：$REMOTE"
log "資料新鮮度（accuracy.json last_updated）：$(freshness)"
