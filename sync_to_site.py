#!/usr/bin/env python3
"""Copy all data files (fixtures, results, accuracy, predictions/*) from
the canonical data/ dir into site/data/ so a redeploy serves the latest."""
import shutil, glob, os

BASE = "/home/user/workspace/wc2026/data"
SITE = "/home/user/workspace/wc2026/site/data"

os.makedirs(os.path.join(SITE, "predictions"), exist_ok=True)
for f in ["fixtures.json", "results.json", "accuracy.json",
          "calibration.json", "postmortems.json", "benchmark_scores.json",
          "players.json", "leaderboards.json"]:
    src = os.path.join(BASE, f)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(SITE, f))

for f in glob.glob(os.path.join(BASE, "predictions", "*")):
    shutil.copy2(f, os.path.join(SITE, "predictions", os.path.basename(f)))

# Write a manifest of prediction JSON filenames so the live (GitHub) endpoint
# can discover which prediction files exist on the repo in a single request.
import json
pred_files = sorted(
    os.path.basename(p)
    for p in glob.glob(os.path.join(SITE, "predictions", "match_*.json"))
)
with open(os.path.join(SITE, "predictions", "manifest.json"), "w", encoding="utf-8") as fh:
    json.dump({"files": pred_files, "count": len(pred_files)}, fh, ensure_ascii=False, indent=2)

n = len(pred_files)
print(f"Synced to site/data: {n} prediction files (+manifest) + fixtures/results/accuracy")
