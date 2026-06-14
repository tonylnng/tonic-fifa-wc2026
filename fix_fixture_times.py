#!/usr/bin/env python3
"""一次性修正 fixtures.json 的開賽時間。
背景：原始 fixtures 的 date/kickoff_local 來源時間系統性錯誤（偏移數小時），
導致 kickoff_utc 全部錯誤。本腳本以 fixturedownload.com 權威 UTC 賽程為準，
依「隊伍對」對應小組賽，依「本站賽號」對應淘汰賽（TBD），重算正確 kickoff_utc，
並由 kickoff_utc + timezone 反推正確的 date 與 kickoff_local（純顯示）。
保留所有其他欄位（venue/city/result/status/group/stage/隊名）不變。
"""
import json
from datetime import datetime
from zoneinfo import ZoneInfo

FX = "/home/user/workspace/wc2026/data/fixtures.json"

def norm(s):
    return (s or "").lower().replace(".", "").replace("'", "").replace("-", " ").replace("&", "and").strip()

# 小組賽：以隊伍對 -> 權威 UTC
GROUP = """Mexico|South Africa|2026-06-11T19:00:00Z
Korea Republic|Czechia|2026-06-12T02:00:00Z
Canada|Bosnia and Herzegovina|2026-06-12T19:00:00Z
USA|Paraguay|2026-06-13T01:00:00Z
Qatar|Switzerland|2026-06-13T19:00:00Z
Brazil|Morocco|2026-06-13T22:00:00Z
Haiti|Scotland|2026-06-14T01:00:00Z
Australia|Turkiye|2026-06-14T04:00:00Z
Germany|Curacao|2026-06-14T17:00:00Z
Netherlands|Japan|2026-06-14T20:00:00Z
Cote dIvoire|Ecuador|2026-06-14T23:00:00Z
Sweden|Tunisia|2026-06-15T02:00:00Z
Spain|Cabo Verde|2026-06-15T16:00:00Z
Belgium|Egypt|2026-06-15T19:00:00Z
Saudi Arabia|Uruguay|2026-06-15T22:00:00Z
Iran|New Zealand|2026-06-16T01:00:00Z
France|Senegal|2026-06-16T19:00:00Z
Iraq|Norway|2026-06-16T22:00:00Z
Argentina|Algeria|2026-06-17T01:00:00Z
Austria|Jordan|2026-06-17T04:00:00Z
Portugal|Congo DR|2026-06-17T17:00:00Z
England|Croatia|2026-06-17T20:00:00Z
Ghana|Panama|2026-06-17T23:00:00Z
Uzbekistan|Colombia|2026-06-18T02:00:00Z
Czechia|South Africa|2026-06-18T16:00:00Z
Switzerland|Bosnia and Herzegovina|2026-06-18T19:00:00Z
Canada|Qatar|2026-06-18T22:00:00Z
Mexico|Korea Republic|2026-06-19T01:00:00Z
USA|Australia|2026-06-19T19:00:00Z
Scotland|Morocco|2026-06-19T22:00:00Z
Brazil|Haiti|2026-06-20T01:00:00Z
Turkiye|Paraguay|2026-06-20T04:00:00Z
Netherlands|Sweden|2026-06-20T17:00:00Z
Germany|Cote dIvoire|2026-06-20T20:00:00Z
Ecuador|Curacao|2026-06-21T00:00:00Z
Tunisia|Japan|2026-06-21T04:00:00Z
Spain|Saudi Arabia|2026-06-21T16:00:00Z
Belgium|Iran|2026-06-21T19:00:00Z
Uruguay|Cabo Verde|2026-06-21T22:00:00Z
New Zealand|Egypt|2026-06-22T01:00:00Z
Argentina|Austria|2026-06-22T17:00:00Z
France|Iraq|2026-06-22T21:00:00Z
Norway|Senegal|2026-06-23T00:00:00Z
Jordan|Algeria|2026-06-23T03:00:00Z
Portugal|Uzbekistan|2026-06-23T17:00:00Z
England|Ghana|2026-06-23T20:00:00Z
Panama|Croatia|2026-06-23T23:00:00Z
Colombia|Congo DR|2026-06-24T02:00:00Z
Switzerland|Canada|2026-06-24T19:00:00Z
Bosnia and Herzegovina|Qatar|2026-06-24T19:00:00Z
Scotland|Brazil|2026-06-24T22:00:00Z
Morocco|Haiti|2026-06-24T22:00:00Z
Czechia|Mexico|2026-06-25T01:00:00Z
South Africa|Korea Republic|2026-06-25T01:00:00Z
Curacao|Cote dIvoire|2026-06-25T20:00:00Z
Ecuador|Germany|2026-06-25T20:00:00Z
Japan|Sweden|2026-06-25T23:00:00Z
Tunisia|Netherlands|2026-06-25T23:00:00Z
Turkiye|USA|2026-06-26T02:00:00Z
Paraguay|Australia|2026-06-26T02:00:00Z
Norway|France|2026-06-26T19:00:00Z
Senegal|Iraq|2026-06-26T19:00:00Z
Cabo Verde|Saudi Arabia|2026-06-27T00:00:00Z
Uruguay|Spain|2026-06-27T00:00:00Z
Egypt|Iran|2026-06-27T03:00:00Z
New Zealand|Belgium|2026-06-27T03:00:00Z
Panama|England|2026-06-27T21:00:00Z
Croatia|Ghana|2026-06-27T21:00:00Z
Colombia|Portugal|2026-06-27T23:30:00Z
Congo DR|Uzbekistan|2026-06-27T23:30:00Z
Algeria|Austria|2026-06-28T02:00:00Z
Jordan|Argentina|2026-06-28T02:00:00Z"""

# 淘汰賽：以本站賽號 -> 權威 UTC（feed 賽號 73-104 與本站一致順序，TBD）
KO = {
    73: "2026-06-28T19:00:00Z", 74: "2026-06-29T20:30:00Z", 75: "2026-06-30T01:00:00Z",
    76: "2026-06-29T17:00:00Z", 77: "2026-06-30T21:00:00Z", 78: "2026-06-30T17:00:00Z",
    79: "2026-07-01T01:00:00Z", 80: "2026-07-01T16:00:00Z", 81: "2026-07-02T00:00:00Z",
    82: "2026-07-01T20:00:00Z", 83: "2026-07-02T23:00:00Z", 84: "2026-07-02T19:00:00Z",
    85: "2026-07-03T03:00:00Z", 86: "2026-07-03T22:00:00Z", 87: "2026-07-04T01:30:00Z",
    88: "2026-07-03T18:00:00Z", 89: "2026-07-04T21:00:00Z", 90: "2026-07-04T17:00:00Z",
    91: "2026-07-05T20:00:00Z", 92: "2026-07-06T00:00:00Z", 93: "2026-07-06T19:00:00Z",
    94: "2026-07-07T00:00:00Z", 95: "2026-07-07T16:00:00Z", 96: "2026-07-07T20:00:00Z",
    97: "2026-07-09T20:00:00Z", 98: "2026-07-10T19:00:00Z", 99: "2026-07-11T21:00:00Z",
    100: "2026-07-12T01:00:00Z", 101: "2026-07-14T19:00:00Z", 102: "2026-07-15T19:00:00Z",
    103: "2026-07-18T21:00:00Z", 104: "2026-07-19T19:00:00Z",
}

gmap = {}
for line in GROUP.strip().split("\n"):
    h, a, utc = line.split("|")
    gmap[(norm(h), norm(a))] = utc

# 隊名別名（本站隊名 -> feed 隊名規範化）
ALIAS = {
    "turkey": "turkiye",
    "ivory coast": "cote divoire",
    "south korea": "korea republic",
    "czech republic": "czechia",
    "dr congo": "congo dr",
    "curaçao": "curacao",
    "côte d'ivoire": "cote divoire",
    "ir iran": "iran",
    "cape verde": "cabo verde",
}
def canon(s):
    n = norm(s)
    return ALIAS.get(n, n)

data = json.load(open(FX))
fixtures = data["fixtures"]
fixed, unmatched = 0, []
for f in fixtures:
    num = f["match"]
    new_utc = None
    if num in KO:
        new_utc = KO[num]
    else:
        key = (canon(f["home"]), canon(f["away"]))
        new_utc = gmap.get(key)
    if not new_utc:
        unmatched.append((num, f["home"], f["away"]))
        continue
    # recompute local date/time from UTC + timezone (display only)
    tz = ZoneInfo(f["timezone"])
    dt_utc = datetime.fromisoformat(new_utc.replace("Z", "+00:00"))
    local = dt_utc.astimezone(tz)
    f["kickoff_utc"] = new_utc
    f["date"] = local.strftime("%Y-%m-%d")
    f["kickoff_local"] = local.strftime("%H:%M")
    fixed += 1

data["last_updated"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:00Z")
json.dump(data, open(FX, "w"), ensure_ascii=False, indent=2)
print(f"FIXED {fixed} / {len(fixtures)} fixtures")
if unmatched:
    print("UNMATCHED:")
    for u in unmatched:
        print("  ", u)
else:
    print("All fixtures matched.")
