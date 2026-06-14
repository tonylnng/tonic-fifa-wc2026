#!/usr/bin/env python3
"""把工作區最新的 data/ 同步進 gitsync repo 並 push 到 GitHub。
排程每輪結束時呼叫。需在 bash 以 api_credentials=["github"] 執行 git push。
此腳本只負責複製 + commit；push 由呼叫端在同一個 bash（帶 github 憑證）執行。
"""
import shutil, subprocess, os, datetime, sys

# 路徑可用環境變數覆寫，預設為雲端排程的工作區路徑
SRC = os.environ.get("WC_SRC", "/home/user/workspace/wc2026/data")
REPO = os.environ.get("WC_REPO", "/home/user/workspace/wc2026/gitsync")
DST = os.environ.get("WC_DST", os.path.join(REPO, "site", "data"))
GIT_EMAIL = os.environ.get("WC_GIT_EMAIL", "tonylnng@gmail.com")
GIT_NAME = os.environ.get("WC_GIT_NAME", "Tony")

def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)

# 1. 同步 data/（predictions 為累加，不刪舊批次；fixtures/results/accuracy 覆蓋）
os.makedirs(os.path.join(DST, "predictions"), exist_ok=True)
for f in ["fixtures.json", "results.json", "accuracy.json",
          "calibration.json", "postmortems.json", "benchmark_scores.json"]:
    s = os.path.join(SRC, f)
    if os.path.exists(s):
        shutil.copy2(s, os.path.join(DST, f))
# predictions：複製全部（含 SCHEMA.md）
for f in os.listdir(os.path.join(SRC, "predictions")):
    shutil.copy2(os.path.join(SRC, "predictions", f),
                 os.path.join(DST, "predictions", f))

# 2. git add + 檢查是否有變更
run(["git", "add", "-A"], cwd=REPO)
status = run(["git", "status", "--porcelain"], cwd=REPO)
if not status.stdout.strip():
    print("NOCHANGE")
    sys.exit(0)

ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H%MZ")
run(["git", "-c", f"user.email={GIT_EMAIL}", "-c", f"user.name={GIT_NAME}",
     "commit", "-q", "-m", f"自動更新預測/結果 {ts}"], cwd=REPO)
print(f"COMMITTED {ts}")
