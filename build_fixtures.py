#!/usr/bin/env python3
"""Build the World Cup 2026 fixtures Master List as JSON.
Times are local kickoff strings as published (HKT context noted separately).
Played results are seeded from authoritative sources (Al Jazeera, ESPN, FOX, wc2026fixtures)."""
import json, datetime

# Group draw
groups = {
    "A": ["Mexico", "South Africa", "South Korea", "Czech Republic"],
    "B": ["Canada", "Bosnia & Herzegovina", "Qatar", "Switzerland"],
    "C": ["Brazil", "Morocco", "Haiti", "Scotland"],
    "D": ["USA", "Paraguay", "Australia", "Turkey"],
    "E": ["Germany", "Curacao", "Ivory Coast", "Ecuador"],
    "F": ["Netherlands", "Japan", "Sweden", "Tunisia"],
    "G": ["Belgium", "Egypt", "Iran", "New Zealand"],
    "H": ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],
    "I": ["France", "Senegal", "Iraq", "Norway"],
    "J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "K": ["Portugal", "DR Congo", "Uzbekistan", "Colombia"],
    "L": ["England", "Croatia", "Ghana", "Panama"],
}

# Each match: (num, stage, date, kickoff_local, home, away, venue, city)
# Group stage matches #1-#72
M = [
 (1,"Group A","2026-06-11","16:00","Mexico","South Africa","Estadio Azteca","Mexico City, Mexico"),
 (2,"Group A","2026-06-12","20:00","South Korea","Czech Republic","Estadio Akron","Zapopan, Mexico"),
 (3,"Group B","2026-06-12","15:00","Canada","Bosnia & Herzegovina","BMO Field","Toronto, Canada"),
 (4,"Group D","2026-06-13","18:00","USA","Paraguay","SoFi Stadium","Inglewood, USA"),
 (5,"Group B","2026-06-13","19:00","Qatar","Switzerland","Levi's Stadium","Santa Clara, USA"),
 (6,"Group C","2026-06-13","22:00","Brazil","Morocco","MetLife Stadium","East Rutherford, USA"),
 (7,"Group C","2026-06-14","01:00","Haiti","Scotland","Gillette Stadium","Foxborough, USA"),
 (8,"Group D","2026-06-14","04:00","Australia","Turkey","BC Place","Vancouver, Canada"),
 (9,"Group E","2026-06-14","17:00","Germany","Curacao","NRG Stadium","Houston, USA"),
 (10,"Group F","2026-06-14","20:00","Netherlands","Japan","AT&T Stadium","Arlington, USA"),
 (11,"Group E","2026-06-14","23:00","Ivory Coast","Ecuador","Lincoln Financial Field","Philadelphia, USA"),
 (12,"Group F","2026-06-15","02:00","Sweden","Tunisia","Estadio BBVA","Guadalupe, Mexico"),
 (13,"Group H","2026-06-15","16:00","Spain","Cape Verde","Mercedes-Benz Stadium","Atlanta, USA"),
 (14,"Group G","2026-06-15","19:00","Belgium","Egypt","Lumen Field","Seattle, USA"),
 (15,"Group H","2026-06-15","22:00","Saudi Arabia","Uruguay","Hard Rock Stadium","Miami Gardens, USA"),
 (16,"Group G","2026-06-16","01:00","Iran","New Zealand","SoFi Stadium","Inglewood, USA"),
 (17,"Group I","2026-06-16","19:00","France","Senegal","MetLife Stadium","East Rutherford, USA"),
 (18,"Group I","2026-06-16","22:00","Iraq","Norway","Gillette Stadium","Foxborough, USA"),
 (19,"Group J","2026-06-17","01:00","Argentina","Algeria","Arrowhead Stadium","Kansas City, USA"),
 (20,"Group J","2026-06-17","04:00","Austria","Jordan","Levi's Stadium","Santa Clara, USA"),
 (21,"Group K","2026-06-17","17:00","Portugal","DR Congo","NRG Stadium","Houston, USA"),
 (22,"Group L","2026-06-17","20:00","England","Croatia","AT&T Stadium","Arlington, USA"),
 (23,"Group L","2026-06-17","23:00","Ghana","Panama","BMO Field","Toronto, Canada"),
 (24,"Group K","2026-06-18","02:00","Uzbekistan","Colombia","Estadio Azteca","Mexico City, Mexico"),
 (25,"Group A","2026-06-18","16:00","Czech Republic","South Africa","Mercedes-Benz Stadium","Atlanta, USA"),
 (26,"Group B","2026-06-18","19:00","Switzerland","Bosnia & Herzegovina","SoFi Stadium","Inglewood, USA"),
 (27,"Group B","2026-06-18","22:00","Canada","Qatar","BC Place","Vancouver, Canada"),
 (28,"Group A","2026-06-19","01:00","Mexico","South Korea","Estadio Akron","Zapopan, Mexico"),
 (29,"Group D","2026-06-19","19:00","USA","Australia","Lumen Field","Seattle, USA"),
 (30,"Group C","2026-06-19","22:00","Scotland","Morocco","Gillette Stadium","Foxborough, USA"),
 (31,"Group C","2026-06-20","00:30","Brazil","Haiti","Lincoln Financial Field","Philadelphia, USA"),
 (32,"Group D","2026-06-20","03:00","Turkey","Paraguay","Levi's Stadium","Santa Clara, USA"),
 (33,"Group F","2026-06-20","17:00","Netherlands","Sweden","NRG Stadium","Houston, USA"),
 (34,"Group E","2026-06-20","20:00","Germany","Ivory Coast","BMO Field","Toronto, Canada"),
 (35,"Group E","2026-06-21","00:00","Ecuador","Curacao","Arrowhead Stadium","Kansas City, USA"),
 (36,"Group F","2026-06-21","04:00","Tunisia","Japan","Estadio BBVA","Guadalupe, Mexico"),
 (37,"Group H","2026-06-21","16:00","Spain","Saudi Arabia","Mercedes-Benz Stadium","Atlanta, USA"),
 (38,"Group G","2026-06-21","19:00","Belgium","Iran","SoFi Stadium","Inglewood, USA"),
 (39,"Group H","2026-06-21","22:00","Uruguay","Cape Verde","Hard Rock Stadium","Miami Gardens, USA"),
 (40,"Group G","2026-06-22","01:00","New Zealand","Egypt","BC Place","Vancouver, Canada"),
 (41,"Group J","2026-06-22","17:00","Argentina","Austria","AT&T Stadium","Arlington, USA"),
 (42,"Group I","2026-06-22","21:00","France","Iraq","Lincoln Financial Field","Philadelphia, USA"),
 (43,"Group I","2026-06-23","00:00","Norway","Senegal","MetLife Stadium","East Rutherford, USA"),
 (44,"Group J","2026-06-23","03:00","Jordan","Algeria","Levi's Stadium","Santa Clara, USA"),
 (45,"Group K","2026-06-23","17:00","Portugal","Uzbekistan","NRG Stadium","Houston, USA"),
 (46,"Group L","2026-06-23","20:00","England","Ghana","Gillette Stadium","Foxborough, USA"),
 (47,"Group L","2026-06-23","23:00","Panama","Croatia","BMO Field","Toronto, Canada"),
 (48,"Group K","2026-06-24","02:00","Colombia","DR Congo","Estadio Akron","Zapopan, Mexico"),
 (49,"Group B","2026-06-24","19:00","Bosnia & Herzegovina","Qatar","Lumen Field","Seattle, USA"),
 (50,"Group B","2026-06-24","19:00","Switzerland","Canada","BC Place","Vancouver, Canada"),
 (51,"Group C","2026-06-24","22:00","Scotland","Brazil","Hard Rock Stadium","Miami Gardens, USA"),
 (52,"Group C","2026-06-24","22:00","Morocco","Haiti","Mercedes-Benz Stadium","Atlanta, USA"),
 (53,"Group A","2026-06-25","01:00","Czech Republic","Mexico","Estadio Azteca","Mexico City, Mexico"),
 (54,"Group A","2026-06-25","01:00","South Africa","South Korea","Estadio BBVA","Guadalupe, Mexico"),
 (55,"Group E","2026-06-25","20:00","Ecuador","Germany","MetLife Stadium","East Rutherford, USA"),
 (56,"Group E","2026-06-25","20:00","Curacao","Ivory Coast","Lincoln Financial Field","Philadelphia, USA"),
 (57,"Group F","2026-06-25","23:00","Tunisia","Netherlands","Arrowhead Stadium","Kansas City, USA"),
 (58,"Group F","2026-06-25","23:00","Japan","Sweden","AT&T Stadium","Arlington, USA"),
 (59,"Group D","2026-06-26","02:00","Paraguay","Australia","Levi's Stadium","Santa Clara, USA"),
 (60,"Group D","2026-06-26","02:00","Turkey","USA","SoFi Stadium","Inglewood, USA"),
 (61,"Group I","2026-06-26","19:00","Senegal","Iraq","BMO Field","Toronto, Canada"),
 (62,"Group I","2026-06-26","19:00","Norway","France","Gillette Stadium","Foxborough, USA"),
 (63,"Group H","2026-06-27","00:00","Cape Verde","Saudi Arabia","NRG Stadium","Houston, USA"),
 (64,"Group H","2026-06-27","00:00","Uruguay","Spain","Estadio Akron","Zapopan, Mexico"),
 (65,"Group G","2026-06-27","03:00","New Zealand","Belgium","BC Place","Vancouver, Canada"),
 (66,"Group G","2026-06-27","03:00","Egypt","Iran","Lumen Field","Seattle, USA"),
 (67,"Group L","2026-06-27","21:00","Croatia","Ghana","Lincoln Financial Field","Philadelphia, USA"),
 (68,"Group L","2026-06-27","21:00","Panama","England","MetLife Stadium","East Rutherford, USA"),
 (69,"Group K","2026-06-27","23:30","Colombia","Portugal","Hard Rock Stadium","Miami Gardens, USA"),
 (70,"Group K","2026-06-27","23:30","DR Congo","Uzbekistan","Mercedes-Benz Stadium","Atlanta, USA"),
 (71,"Group J","2026-06-28","02:00","Jordan","Argentina","AT&T Stadium","Arlington, USA"),
 (72,"Group J","2026-06-28","02:00","Algeria","Austria","Arrowhead Stadium","Kansas City, USA"),
]

# Knockout placeholders #73-#104
KO = [
 (73,"Round of 32","2026-07-01","20:00","MetLife Stadium","East Rutherford, USA"),
 (74,"Round of 32","2026-07-01","23:00","AT&T Stadium","Arlington, USA"),
 (75,"Round of 32","2026-07-02","20:00","SoFi Stadium","Los Angeles, USA"),
 (76,"Round of 32","2026-07-02","23:00","NRG Stadium","Houston, USA"),
 (77,"Round of 32","2026-07-03","02:00","Estadio Azteca","Mexico City, Mexico"),
 (78,"Round of 32","2026-07-03","20:00","Hard Rock Stadium","Miami, USA"),
 (79,"Round of 32","2026-07-03","22:00","BC Place","Vancouver, Canada"),
 (80,"Round of 32","2026-07-03","23:00","Levi's Stadium","San Francisco, USA"),
 (81,"Round of 32","2026-07-04","18:00","Lincoln Financial Field","Philadelphia, USA"),
 (82,"Round of 32","2026-07-04","21:00","Arrowhead Stadium","Kansas City, USA"),
 (83,"Round of 32","2026-07-05","00:00","Lumen Field","Seattle, USA"),
 (84,"Round of 32","2026-07-05","02:00","Estadio BBVA","Monterrey, Mexico"),
 (85,"Round of 32","2026-07-05","22:00","BMO Field","Toronto, Canada"),
 (86,"Round of 32","2026-07-06","00:00","Mercedes-Benz Stadium","Atlanta, USA"),
 (87,"Round of 32","2026-07-06","02:00","Estadio Akron","Guadalajara, Mexico"),
 (88,"Round of 32","2026-07-06","22:00","Gillette Stadium","Foxborough, USA"),
 (89,"Round of 16","2026-07-07","23:00","MetLife Stadium","East Rutherford, USA"),
 (90,"Round of 16","2026-07-08","02:00","AT&T Stadium","Arlington, USA"),
 (91,"Round of 16","2026-07-08","23:00","SoFi Stadium","Los Angeles, USA"),
 (92,"Round of 16","2026-07-09","02:00","Hard Rock Stadium","Miami, USA"),
 (93,"Round of 16","2026-07-09","23:00","NRG Stadium","Houston, USA"),
 (94,"Round of 16","2026-07-10","02:00","Levi's Stadium","San Francisco, USA"),
 (95,"Round of 16","2026-07-10","23:00","BC Place","Vancouver, Canada"),
 (96,"Round of 16","2026-07-11","02:00","Estadio Azteca","Mexico City, Mexico"),
 (97,"Quarter-final","2026-07-11","22:00","MetLife Stadium","East Rutherford, USA"),
 (98,"Quarter-final","2026-07-12","01:00","AT&T Stadium","Arlington, USA"),
 (99,"Quarter-final","2026-07-12","22:00","SoFi Stadium","Los Angeles, USA"),
 (100,"Quarter-final","2026-07-13","01:00","Hard Rock Stadium","Miami, USA"),
 (101,"Semi-final","2026-07-14","23:00","AT&T Stadium","Arlington, USA"),
 (102,"Semi-final","2026-07-15","23:00","MetLife Stadium","East Rutherford, USA"),
 (103,"Third Place","2026-07-18","22:00","Hard Rock Stadium","Miami, USA"),
 (104,"Final","2026-07-19","20:00","MetLife Stadium","East Rutherford, USA"),
]

# Played results (home_score, away_score) keyed by match number
RESULTS = {
 1: (2, 0),   # Mexico 2-0 South Africa
 2: (2, 1),   # South Korea 2-1 Czech Republic
 3: (1, 1),   # Canada 1-1 Bosnia & Herzegovina
 4: (4, 1),   # USA 4-1 Paraguay
}

fixtures = []
for num, stage, date, ko, home, away, venue, city in M:
    grp = stage.replace("Group ", "")
    res = RESULTS.get(num)
    fixtures.append({
        "match": num, "stage": stage, "group": grp,
        "date": date, "kickoff_local": ko,
        "home": home, "away": away,
        "venue": venue, "city": city,
        "status": "FT" if res else "scheduled",
        "result": {"home": res[0], "away": res[1]} if res else None,
    })

for num, stage, date, ko, venue, city in KO:
    fixtures.append({
        "match": num, "stage": stage, "group": None,
        "date": date, "kickoff_local": ko,
        "home": "TBD", "away": "TBD",
        "venue": venue, "city": city,
        "status": "scheduled", "result": None,
    })

out = {
    "tournament": "FIFA World Cup 2026",
    "hosts": ["USA", "Canada", "Mexico"],
    "total_matches": 104,
    "teams": 48,
    "groups": groups,
    "last_updated": datetime.datetime.utcnow().isoformat() + "Z",
    "fixtures": fixtures,
}

with open("/home/user/workspace/wc2026/data/fixtures.json", "w") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"Wrote {len(fixtures)} fixtures. Played: {len(RESULTS)}")
print("Stages:", {s: sum(1 for x in fixtures if x['stage']==s) for s in sorted(set(x['stage'] for x in fixtures))})
