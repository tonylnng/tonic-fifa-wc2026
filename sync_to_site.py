#!/usr/bin/env python3
"""Copy all data files (fixtures, results, accuracy, predictions/*) from
the canonical data/ dir into site/data/ so a redeploy serves the latest."""
import shutil, glob, os

BASE = "/home/user/workspace/wc2026/data"
SITE = "/home/user/workspace/wc2026/site/data"

os.makedirs(os.path.join(SITE, "predictions"), exist_ok=True)
for f in ["fixtures.json", "results.json", "accuracy.json"]:
    src = os.path.join(BASE, f)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(SITE, f))

for f in glob.glob(os.path.join(BASE, "predictions", "*")):
    shutil.copy2(f, os.path.join(SITE, "predictions", os.path.basename(f)))

n = len(glob.glob(os.path.join(SITE, "predictions", "match_*.json")))
print(f"Synced to site/data: {n} prediction files + fixtures/results/accuracy")
