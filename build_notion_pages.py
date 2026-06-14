#!/usr/bin/env python3
"""Build Notion page objects from prediction JSONs + fixtures + results.
Outputs a JSON array of page property dicts ready for notion-create-pages.
"""
import json, glob, os, sys

BASE = "/home/user/workspace/wc2026/data"
ZH = {
    "Qatar":"卡塔爾","Switzerland":"瑞士","Brazil":"巴西","Morocco":"摩洛哥",
    "Haiti":"海地","Scotland":"蘇格蘭","Australia":"澳洲","Turkey":"土耳其",
    "Germany":"德國","Curacao":"庫拉索","Netherlands":"荷蘭","Japan":"日本",
    "Ivory Coast":"象牙海岸","Ecuador":"厄瓜多爾","Mexico":"墨西哥","South Africa":"南非",
    "South Korea":"南韓","Czech Republic":"捷克","Canada":"加拿大","Bosnia":"波黑",
    "United States":"美國","USA":"美國","Paraguay":"巴拉圭",
    "Sweden":"瑞典","Tunisia":"突尼西亞","Spain":"西班牙","Cape Verde":"佛得角",
    "Belgium":"比利時","Egypt":"埃及","Saudi Arabia":"沙烏地阿拉伯","Uruguay":"烏拉圭",
    "Iran":"伊朗","New Zealand":"紐西蘭","Bosnia & Herzegovina":"波黑",
}
STAGE = {"Group":"小組賽","Round of 32":"32強","Round of 16":"16強",
         "Quarter":"八強","Semi":"四強","Third":"季軍戰","Final":"決賽"}
OUTCOME = {"home":"主勝","draw":"和局","away":"客勝"}

def zh(t): return ZH.get(t, t)
def stage_zh(s):
    for k,v in STAGE.items():
        if s and s.startswith(k): return v
    return "小組賽"

# load results to backfill final scores
results = {}
rj = json.load(open(os.path.join(BASE,"results.json")))
for r in (rj.get("results") or rj if isinstance(rj,dict) else rj):
    if isinstance(r,dict) and "match" in r:
        results[r["match"]] = r

pages = []
files = sorted(glob.glob(os.path.join(BASE,"predictions","match_*.json")),
               key=lambda p: int(os.path.basename(p).split("__")[0].split("_")[1]))
for f in files:
    d = json.load(open(f))
    m = d["match"]
    pred = d["prediction"]
    rsn = d.get("reasoning",{})
    summary = rsn.get("summary","") if isinstance(rsn,dict) else str(rsn)
    home, away = d["home"], d["away"]
    res = results.get(m)
    props = {
        "比賽": f"#{m} {zh(home)} vs {zh(away)}",
        "場次": m,
        "階段": stage_zh(d.get("stage","")),
        "主隊": zh(home),
        "客隊": zh(away),
        "AI預測比分": pred.get("scoreline",""),
        "預測結果": OUTCOME.get(pred.get("outcome"),"和局"),
        "信心度": pred.get("confidence",0),
        "來源數": d.get("source_count",0),
        "預測批次": d.get("run_id",""),
        "分析摘要": summary[:1900],
        "date:更新時間:start": d.get("run_timestamp","2026-06-13T08:00:00Z").replace("Z","+00:00"),
        "date:更新時間:is_datetime": 1,
    }
    if res:
        props["最終比分"] = res.get("scoreline","")
    pages.append({"properties": props})

print(json.dumps(pages, ensure_ascii=False))
