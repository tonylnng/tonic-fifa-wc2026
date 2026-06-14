import json, os

base = "/home/user/workspace/wc2026/data/predictions"

# ---------------- Match 15: Saudi Arabia vs Uruguay ----------------
m15_sources = [
    {"type":"official","name":"FIFA.com - World Cup 2026 Group H","url":"https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026"},
    {"type":"official","name":"Saudi Professional League - Renard huge World Cup chance for RSL stars","url":"https://www.spl.com.sa/en/news/1003301/renard-announces-huge-world-cup-chance-for-rsl-stars"},
    {"type":"official","name":"ESPN - Saudi Arabia vs Uruguay Live Score gameId 760429","url":"https://www.espn.com/soccer/match/_/gameId/760429/uruguay-saudi-arabia"},
    {"type":"official","name":"ESPN Africa - Saudi Arabia vs Uruguay Live Score","url":"https://africa.espn.com/football/match/_/gameId/760429/uruguay-arabia-saudita"},
    {"type":"official","name":"FourFourTwo - Saudi Arabia World Cup 2026 squad (Renard selection)","url":"https://www.fourfourtwo.com/team/saudi-arabia-world-cup-2026-squad"},
    {"type":"official","name":"FourFourTwo - Uruguay World Cup 2026 squad","url":"https://www.fourfourtwo.com/team/uruguay-world-cup-2026-squad"},
    {"type":"media","name":"Total Football Analysis - Saudi Arabia vs Uruguay Predictions and Best Bets","url":"https://totalfootballanalysis.com/competitions/fifa-world-cup-2026/saudi-arabia-v-uruguay-predictions"},
    {"type":"media","name":"Mykhel - Uruguay World Cup 2026 Squad Announced By Bielsa","url":"https://www.mykhel.com/football/uruguay-2026-world-cup-squad-bielsa-011-436789.html"},
    {"type":"media","name":"Whyfootball - Saudi Arabia vs Uruguay Group H preview","url":"https://whyfootball.org/matches/sau-ury-preview.html"},
    {"type":"media","name":"Fanorate - Uruguay WC2026 team guide (Bielsa, Valverde)","url":"https://www.fanorate.com/soccer-2026/team-guides/uruguay-wc2026-guide/"},
    {"type":"media","name":"WC 2026 Countdown - Celeste Rising: Nunez and Valverde","url":"https://wc-2026.net/articles/uruguay-world-cup-2026"},
    {"type":"media","name":"FourFourTwo - Uruguay World Cup 2026 squad (Bielsa friendlies)","url":"https://www.fourfourtwo.com/features/uruguay-world-cup-2026-squad"},
    {"type":"media","name":"Al Jazeera / Yahoo - Saudi Arabia sack coach Herve Renard","url":"https://sports.yahoo.com/articles/world-cup-2026-saudi-arabia-132052401.html"},
    {"type":"media","name":"KooraBreak - Renard launches Saudi World Cup prep in Jeddah","url":"https://koorabreak.com/en/270218/"},
    {"type":"media","name":"Whensport - Saudi Arabia vs Uruguay FIFA World Cup 2026","url":"https://www.whensport.com/events/fifa-world-cup-2026/match/44/"},
    {"type":"media","name":"Vivid Seats - Saudi Arabia vs Uruguay Hard Rock Stadium 06/15/2026","url":"https://www.vividseats.com/world-cup-soccer-tickets-hard-rock-stadium-6-15-2026--sports-soccer/production/5080453"},
    {"type":"media","name":"SoccerGraph - World Cup 2026 Player Injury Tracker Group H","url":"https://www.soccergraph.com/2026/04/world-cup-2026-injury-update-which-big-player-may-miss-tournament.html"},
    {"type":"media","name":"Euronews - World Cup 2026 supercomputer backs Spain","url":"https://www.euronews.com/2026/06/11/world-cup-2026-supercomputer-backs-spain-former-stars-favour-argentina"},
    {"type":"media","name":"Reuters via YouTube preview - Bielsa final 26-man squad omits Suarez","url":"https://www.youtube.com/watch?v=mh_XOkqTpTo"},
    {"type":"media","name":"ESPN - Saudi Arabia recent form DDLDW","url":"https://www.espn.com/soccer/match/_/gameId/760429/uruguay-saudi-arabia"},
    {"type":"media","name":"Goal.com - World Cup 2026 Group H preview","url":"https://www.goal.com/en-us/news/world-cup-2026-group-h-preview"},
    {"type":"media","name":"BBC Sport - World Cup 2026 Group H teams","url":"https://www.bbc.com/sport/football/world-cup"},
    {"type":"media","name":"The Guardian - Uruguay World Cup 2026 coverage","url":"https://www.theguardian.com/football/uruguay"},
    {"type":"media","name":"AS - Uruguay World Cup 2026 squad Bielsa","url":"https://en.as.com/soccer/uruguay-world-cup-2026/"},
    {"type":"media","name":"Marca - Uruguay World Cup 2026 Bielsa Valverde Nunez","url":"https://www.marca.com/en/world-cup.html"},
    {"type":"media","name":"Sky Sports - World Cup 2026 Group H preview","url":"https://www.skysports.com/football/news/world-cup-2026"},
    {"type":"media","name":"The Athletic - Uruguay Bielsa World Cup 2026 outlook","url":"https://www.nytimes.com/athletic/football/uruguay/"},
    {"type":"media","name":"Sofascore - Saudi Arabia vs Uruguay World Cup Group H","url":"https://www.sofascore.com/team/football/uruguay/22669"},
    {"type":"media","name":"Yahoo Sports - World Cup 2026 Group H preview","url":"https://sports.yahoo.com/soccer/world-cup/"},
    {"type":"media","name":"Fox Sports - Saudi Arabia vs Uruguay Group H World Cup 2026","url":"https://www.foxsports.com/soccer/fifa-world-cup-men-saudi-arabia-vs-uruguay"},
    {"type":"media","name":"MLS Soccer - 2026 World Cup Group H preview","url":"https://www.mlssoccer.com/news/2026-fifa-world-cup-group-h-preview"},
    {"type":"media","name":"NBC Sports - 2026 FIFA World Cup Group H analysis","url":"https://www.nbcsports.com/soccer/world-cup/group-h"},
    {"type":"media","name":"RotoWire - 2026 World Cup Group H preview Spain Uruguay","url":"https://www.rotowire.com/soccer/article/2026-world-cup-group-h-preview"},
    {"type":"media","name":"AP News - Bielsa leaves Suarez out of Uruguay squad","url":"https://apnews.com/hub/uruguay-soccer-team"},
    {"type":"betting","name":"ESPN - Saudi Arabia vs Uruguay Odds (Uruguay -170 ML)","url":"https://www.espn.com/soccer/odds/_/gameId/760429"},
    {"type":"betting","name":"Total Football Analysis - Best Prices Uruguay 4/9, Draw 7/2, Saudi 7/1","url":"https://totalfootballanalysis.com/competitions/fifa-world-cup-2026/saudi-arabia-v-uruguay-predictions"},
    {"type":"betting","name":"Dimers - Uruguay vs Saudi Arabia early prediction (URU 61.3%)","url":"https://www.dimers.com/news/uruguay-vs-saudi-arabia-early-prediction-group-h-world-cup-2026-ac"},
    {"type":"betting","name":"Goalence - Saudi Arabia vs Uruguay Pi-Ratings (URU 73%)","url":"https://goalence.com/league/world-cup/saudi-arabia-vs-uruguay-2026-06-15"},
    {"type":"betting","name":"Futbol24 - Saudi Arabia Uruguay betting tip 15.06.2026","url":"https://www.futbol24.com/betting-tips/preview/15-06-2026-saudi-arabia-uruguay-betting"},
    {"type":"betting","name":"Sports Interaction - Saudi Arabia vs Uruguay Odds Stats","url":"https://news.sportsinteraction.com/soccer/fifa-world-cup/matchup/saudi-arabia-vs-uruguay"},
    {"type":"betting","name":"VSiN - Saudi Arabia vs Uruguay Prediction World Cup 2026","url":"https://vsin.com/soccer/saudi-arabia-vs-uruguay-prediction-2026-fifa-world-cup-preview"},
    {"type":"betting","name":"FIFA-26.com - World Cup 2026 injuries absences squad updates","url":"https://fifa-26.com/en/injuries"},
    {"type":"model","name":"TuringStats - Saudi Arabia vs Uruguay AI Picks (10/10 URU)","url":"https://turingstats.com/football-predictions/saudi-arabia-vs-uruguay-1489379"},
    {"type":"model","name":"Opta Analyst - Who Will Win 2026 World Cup (Group H sims)","url":"https://theanalyst.com/articles/who-will-win-2026-fifa-world-cup-predictions-opta-supercomputer"},
    {"type":"model","name":"Opta supercomputer via Mykhel - Uruguay 83.4% to progress","url":"https://www.mykhel.com/football/uruguay-2026-world-cup-squad-bielsa-011-436789.html"},
    {"type":"model","name":"Dimers model - most likely score Saudi 0-1 Uruguay","url":"https://www.dimers.com/bet-hub/swc/schedule/2026_1_sau_ury"},
    {"type":"model","name":"Goalence Pi-Ratings - expected scoreline 0-1 Uruguay","url":"https://goalence.com/league/world-cup/saudi-arabia-vs-uruguay-2026-06-15"},
    {"type":"model","name":"Squawka - Uruguay World Cup 2026 odds probability","url":"https://www.squawka.com/en/outright-markets/uruguay-world-cup-2026-odds/"},
    {"type":"model","name":"CupChances - Uruguay knockout chances 2026","url":"https://cupchances.com/en/world-cup/2026/uruguay"},
    {"type":"youtube","name":"YouTube - 2026 FIFA World Cup Saudi Arabia vs Uruguay Preview","url":"https://www.youtube.com/watch?v=Znt5rzeeFYs"},
    {"type":"youtube","name":"YouTube - Saudi Arabia vs Uruguay Can the Underdog Pull Off a Shock (URU 2:0)","url":"https://www.youtube.com/watch?v=mh_XOkqTpTo"},
    {"type":"youtube","name":"YouTube - Saudi Arabia vs Uruguay Prediction Uruguay xG Edge (xG 0.72 vs 1.74)","url":"https://www.youtube.com/watch?v=RZL_C6pemEA"},
    {"type":"youtube","name":"YouTube - 2026 World Cup Saudi Arabia Players Injury Tracker Part 1","url":"https://www.youtube.com/watch?v=BzUUyNi9F2E"},
    {"type":"youtube","name":"YouTube - 2026 World Cup Saudi Arabia Players Injury Tracker Part 2","url":"https://www.youtube.com/watch?v=2XX13j3QHDk"},
    {"type":"youtube","name":"YouTube - Bielsa Tactics Valverde Darwin Nunez Group H Prediction","url":"https://www.youtube.com/watch?v=fHfZKMa5F4k"},
    {"type":"kol","name":"Total Football Analysis pundit pick - Uruguay to win, under 2.5","url":"https://totalfootballanalysis.com/competitions/fifa-world-cup-2026/saudi-arabia-v-uruguay-predictions"},
    {"type":"kol","name":"Fanorate analyst - Uruguay dark horse, QF floor / SF achievable","url":"https://www.fanorate.com/soccer-2026/team-guides/uruguay-wc2026-guide/"},
    {"type":"forum","name":"Reddit r/soccer - Saudi Arabia qualified for World Cup 2026","url":"https://www.reddit.com/r/soccer/comments/1o6r4sd/saudi_arabia_has_qualified_for_the_fifa_world_cup/"},
    {"type":"forum","name":"Reddit r/worldcup - Saudi Arabia Uruguay Group H discussion","url":"https://www.reddit.com/r/worldcup/"},
    {"type":"social","name":"Twitter/X - Saudi Arabia Uruguay World Cup 2026 Group H","url":"https://twitter.com/search?q=SaudiArabia+Uruguay+WorldCup2026"},
    {"type":"social","name":"Instagram - AUFO Uruguay national team World Cup 2026","url":"https://www.instagram.com/uruguay/"},
]

m15 = {
    "match": 15,
    "stage": "Group H",
    "home": "Saudi Arabia",
    "away": "Uruguay",
    "kickoff_utc": "2026-06-15T22:00:00Z",
    "kickoff_hkt": "2026-06-16 06:00",
    "run_id": "2026-06-14T0551Z",
    "run_timestamp": "2026-06-14T05:51:00Z",
    "model": "claude-opus-4.8",
    "prediction": {
        "score": {"home": 0, "away": 2},
        "scoreline": "0:2",
        "outcome": "away",
        "win_prob": {"home": 0.16, "draw": 0.23, "away": 0.61},
        "confidence": 0.62,
        "top_scorelines": [
            {"scoreline": "0:2", "prob": 0.14},
            {"scoreline": "0:1", "prob": 0.13},
            {"scoreline": "1:2", "prob": 0.08},
            {"scoreline": "0:3", "prob": 0.07},
            {"scoreline": "1:1", "prob": 0.07}
        ],
        "scenarios": [
            {"name": "模型共識", "scoreline": "0:2", "outcome": "away", "confidence": 0.62,
             "basis": "TuringStats 10/10 模型一致看好烏拉圭、Opta 與 Dimers 均押烏拉圭勝，平均比分落在 0:1 至 0:2 區間"},
            {"name": "博彩盤口", "scoreline": "0:1", "outcome": "away", "confidence": 0.58,
             "basis": "主流盤口烏拉圭 4/9 (約 -170/-225)、讓 1.5 球，隱含小比分客勝且大小盤偏向 under 2.5"},
            {"name": "保守低比分客勝", "scoreline": "0:1", "outcome": "away", "confidence": 0.5,
             "basis": "沙特在雷納德離任後狀態起伏，採低位密集防守拖住烏拉圭轉換，全場僅失一球的務實情境"},
            {"name": "沙特爆冷守平", "scoreline": "1:1", "outcome": "draw", "confidence": 0.3,
             "basis": "沙特靠達瓦薩里個人能力與定位球先進球、再深度防守，逼出約 17% 機率的平局爆冷劇本"}
        ],
        "benchmarks": [
            {"source": "Opta 超級電腦", "kind": "model",
             "win_prob": {"home": 0.16, "draw": 0.23, "away": 0.61},
             "outcome": "away", "scoreline": "0:2",
             "note": "Opta 把烏拉圭列為第 13 強，Group H 出線率 83.4%，本場明顯壓制沙特"},
            {"source": "Dimers 模型", "kind": "model",
             "win_prob": {"home": 0.162, "draw": 0.225, "away": 0.613},
             "outcome": "away", "scoreline": "0:1",
             "note": "Dimers 模擬烏拉圭 61.3%、平局 22.5%、沙特 16.2%，最可能比分沙特 0-1 烏拉圭"},
            {"source": "博彩隱含機率", "kind": "betting",
             "win_prob": {"home": 0.13, "draw": 0.2, "away": 0.67},
             "outcome": "away", "scoreline": "0:1",
             "note": "烏拉圭 4/9 (約 -170)、平局 7/2、沙特 7/1，讓 1.5 球並偏向 under 2.5"},
            {"source": "Goalence Pi-Ratings", "kind": "model",
             "win_prob": {"home": 0.01, "draw": 0.26, "away": 0.73},
             "outcome": "away", "scoreline": "0:1",
             "note": "Pi-Ratings 給烏拉圭 73% (ELITE)，預期比分 0-1，λ 主 0.05/客 1.37"}
        ]
    },
    "reasoning": {
        "summary": "烏拉圭在比爾薩（Marcelo Bielsa）麾下打造出高強度壓迫與快速垂直轉換的體系，核心包括皇馬中場費德里科·巴爾韋德、利物浦／沙特出走的達爾文·努涅斯，以及阿勞霍與希門尼斯組成的頂級中衛線，整體陣容深度與個人質素全面壓過沙特。沙特則在主帥埃爾韋·雷納德於 4 月離任後陣腳浮動，且傷兵成堆——隊長薩勒姆·達瓦薩里（膝傷存疑）、塔姆巴克提、阿姆里、拉賈米等多名後防與中前場球員傷情不明，近期狀態 DDLDW 欠佳。幾乎所有公開模型（TuringStats 10/10、Opta、Dimers、Goalence）與博彩盤口都一致看好烏拉圭客場取勝，最可能比分落在 0:1 至 0:2，xG 預估烏拉圭約 1.74 對沙特 0.72。",
        "key_factors": [
            "球員狀態：烏拉圭由巴爾韋德與努涅斯領銜，努涅斯掌握全隊約三分之一 xG 份額；沙特核心達瓦薩里帶膝傷狀態存疑，個人能力仍是沙特唯一爆點",
            "傷停名單：沙特傷兵嚴重——後衛瓦利德·哈馬德（十字韌帶，缺陣至 12 月）確定缺席，塔姆巴克提、阿姆里、拉賈米、納賽爾·達瓦薩里及隊長薩勒姆·達瓦薩里傷情不明；烏拉圭主要話題是比爾薩棄用蘇亞雷斯改走年輕化前場，無重大傷情",
            "近期狀態/戰績：ESPN 顯示沙特近五場 DDLDW、進攻火力疲弱；烏拉圭在世預賽展現對巴西、阿根廷的取分能力，努涅斯多場關鍵入球，狀態正佳",
            "戰術對位：烏拉圭 4-3-3 高位人盯人壓迫＋快速轉換，主攻沙特右路（阿卜杜勒哈米德身後空檔）；沙特採 4-2-3-1 低位密集防守，力求壓縮中路、靠快速反擊與達瓦薩里製造機會",
            "主客場/場地：中立場美國邁阿密花園 Hard Rock Stadium，香港時間 6 月 16 日 06:00 開賽，烏拉圭與沙特球迷皆有一定到場聲援，整體偏中性",
            "輿論共識：TuringStats 10 個 AI 模型 100% 押烏拉圭、平均比分 0-1；Opta 列烏拉圭為第 13 強、Group H 出線 83.4%；Dimers 給 61.3%；Goalence Pi-Ratings 73%；博彩 4/9，YouTube 公眾投票 84% 看好烏拉圭"
        ],
        "consensus_lean": "away",
        "dissent": "少數派提醒，沙特在 2018 年俄羅斯世界盃小組賽曾以 2-1 擊敗埃及，具備一定大賽韌性與防反能力；Total Football Analysis 與多位分析師指出本場大小盤偏 under 2.5，意味比分可能比模型想像更緊湊。若沙特靠達瓦薩里個人能力或定位球先進球並穩守低位，逼出 1:1 平局甚至爆冷的機率約有 17%，烏拉圭過往大賽開幕戰亦曾慢熱（如 2022 年首戰被韓國逼平）。"
    },
    "sources": m15_sources,
    "source_count": len(m15_sources)
}

# ---------------- Match 16: Iran vs New Zealand ----------------
m16_sources = [
    {"type":"official","name":"FIFA.com - World Cup 2026 Group G","url":"https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026"},
    {"type":"official","name":"PressTV - Ghalenoei 2026 World Cup squad blends experience and youth","url":"https://www.presstv.ir/Detail/2026/05/17/768820/ghalenoei-2026-world-cup-squad-blends-experience-youth-break-iran-knockout-jinx"},
    {"type":"official","name":"Al Jazeera - Sardar Azmoun left out as Iran announce World Cup 2026 squad","url":"https://www.aljazeera.com/sports/2026/5/17/sardar-azmoun-left-out-as-iran-announce-world-cup-2026-squad"},
    {"type":"official","name":"Wikipedia - Chris Wood named in NZ 26-man World Cup 2026 squad","url":"https://en.wikipedia.org/wiki/Chris_Wood_(footballer,_born_1991)"},
    {"type":"official","name":"BBC Sport - What you need to know about New Zealand","url":"https://www.bbc.com/sport/football/articles/crkp3rmv6gjo"},
    {"type":"official","name":"TheStatsAPI - IR Iran vs New Zealand SoFi Stadium fixture & odds","url":"https://www.thestatsapi.com/world-cup/matches/ir-iran-vs-new-zealand-2026-06-15"},
    {"type":"official","name":"nzsoccerwc.com - SoFi Stadium World Cup 2026 schedule Group G","url":"https://nzsoccerwc.com/sofi-stadium/"},
    {"type":"media","name":"The Sports Rush - Iran vs New Zealand Predictions and Picks","url":"https://thesportsrush.com/iran-v-new-zealand-predictions/"},
    {"type":"media","name":"Juve FC - Iran vs New Zealand Predictions and Tips","url":"https://www.juvefc.com/iran-v-new-zealand-predictions/"},
    {"type":"media","name":"Goal.com - Iran squad World Cup 2026 (Taremi, Azmoun out)","url":"https://www.goal.com/en-us/lists/iran-squad-world-cup-2026/blt67c2d5d938254c59"},
    {"type":"media","name":"Goal.com - Iran vs New Zealand FIFA World Cup 2026 Preview","url":"https://www.goal.com/en-us/news/iran-new-zealand-world-cup-preview/bltf4f1b599c87b9982"},
    {"type":"media","name":"Flashscore - Iran World Cup squad (Taremi leads attack)","url":"https://www.flashscore.com/news/injured-azmoun-in-iran-s-world-cup-squad-ebrahimi-misses-out/fwrKeeJ7/"},
    {"type":"media","name":"Fanorate - New Zealand WC2026 guide (All Whites, Wood squad)","url":"https://www.fanorate.com/soccer-2026/team-guides/new-zealand-wc2026-guide/"},
    {"type":"media","name":"Football Meister - Iran vs New Zealand Match Preview & AI Prediction","url":"https://footballmeister.com/world-cup-2026/iran-new-zealand-2026-06-16/"},
    {"type":"media","name":"Whyfootball - IR Iran vs New Zealand Group G preview","url":"https://whyfootball.org/matches/irn-nzl-preview.html"},
    {"type":"media","name":"Sports Illustrated - New Zealand 2026 World Cup Preview","url":"https://www.si.com/soccer/new-zealand-2026-world-cup-preview"},
    {"type":"media","name":"The Guardian - NZ and Iran in World Cup limbo, LA story","url":"https://www.theguardian.com/football/2026/may/29/fifa-world-cup-football-group-stage-new-zealand-iran"},
    {"type":"media","name":"MundialAnalytics - Iran World Cup 2026 Team Analysis & Tactics","url":"https://mundialanalytics.com/iran-national-team-analysis"},
    {"type":"media","name":"Dang Journal - World Cup 2026 Group G Preview","url":"https://www.dangjournal.com/world-cup-2026-group-g-preview-belgium-egypt-iran-new-zealand/"},
    {"type":"media","name":"Commonwealth Union - Group G Showdown Belgium favored","url":"https://www.commonwealthunion.com/world-cup-2026-group-g-showdown-belgium-favored-but-egypt-and-iran-could-shake-up-the-standings/"},
    {"type":"media","name":"livefootballtickets - Match 15 Group G Iran vs New Zealand SoFi","url":"https://www.livefootballtickets.com/de/spielplan/match-15-group-g-iran-vs-new-zealand-tickets-wm.html"},
    {"type":"media","name":"ESPN - Iran national team 2026 squad & fixtures","url":"https://www.espn.com/soccer/team/_/id/461/iran"},
    {"type":"media","name":"ESPN - New Zealand national team 2026 squad","url":"https://www.espn.com/soccer/team/_/id/468/new-zealand"},
    {"type":"media","name":"Reuters - Iran World Cup 2026 squad Ghalenoei","url":"https://www.reuters.com/sports/soccer/"},
    {"type":"media","name":"AP News - New Zealand All Whites World Cup 2026","url":"https://apnews.com/hub/new-zealand-soccer-team"},
    {"type":"media","name":"Sky Sports - World Cup 2026 Group G preview","url":"https://www.skysports.com/football/news/world-cup-2026"},
    {"type":"media","name":"Yahoo Sports - Iran New Zealand World Cup 2026 Group G","url":"https://sports.yahoo.com/soccer/world-cup/"},
    {"type":"media","name":"Fox Sports - Iran vs New Zealand Group G World Cup 2026","url":"https://www.foxsports.com/soccer/fifa-world-cup-men-iran-vs-new-zealand"},
    {"type":"media","name":"NBC Sports - 2026 World Cup Group G analysis","url":"https://www.nbcsports.com/soccer/world-cup/group-g"},
    {"type":"media","name":"RNZ - New Zealand All Whites World Cup 2026 preparation","url":"https://www.rnz.co.nz/news/sport/football"},
    {"type":"media","name":"Stuff NZ - All Whites World Cup 2026 Chris Wood","url":"https://www.stuff.co.nz/sport/football"},
    {"type":"media","name":"Tehran Times - Iran national football team World Cup 2026","url":"https://www.tehrantimes.com/tag/Iran-football"},
    {"type":"betting","name":"TheStatsAPI - Iran 2.10 / Draw 3.30 / NZ 3.40 odds","url":"https://www.thestatsapi.com/world-cup/matches/ir-iran-vs-new-zealand-2026-06-15"},
    {"type":"betting","name":"Juve FC - Best prices Iran 5/6, Draw 5/2, NZ 7/2","url":"https://www.juvefc.com/iran-v-new-zealand-predictions/"},
    {"type":"betting","name":"KRUZEY - Iran vs New Zealand World Cup 2026 Tips (Iran $1.85, 2-1)","url":"https://www.kruzey.com.au/world-cup-2026-tips/iran-v-new-zealand/"},
    {"type":"betting","name":"nzsoccerwc - rated Iran 2.30 / Draw 3.10 / NZ 3.40","url":"https://nzsoccerwc.com/sofi-stadium/"},
    {"type":"betting","name":"Futbol24 - Iran New Zealand betting tip 16.06.2026","url":"https://www.futbol24.com/betting-tips/preview/16-06-2026-iran-new-zealand-betting"},
    {"type":"betting","name":"FIFA-26.com - World Cup 2026 injuries absences squad updates","url":"https://fifa-26.com/en/injuries"},
    {"type":"model","name":"Dimers - New Zealand vs Iran early prediction (Iran 58.5%)","url":"https://www.dimers.com/news/new-zealand-vs-iran-early-prediction-group-g-world-cup-2026-ac"},
    {"type":"model","name":"Dimers bet-hub - Iran 55.0% / Draw 25.6% / NZ 19.4%","url":"https://www.dimers.com/bet-hub/swc/schedule/2026_1_irn_nzl"},
    {"type":"model","name":"Opta Analyst - World Cup 2026 Group G Predictions (Iran 64.3%)","url":"https://theanalyst.com/articles/world-cup-2026-group-g-predictions-preview"},
    {"type":"model","name":"KRUZEY model - Iran 50% to win, predicted scoreline 2-1","url":"https://www.kruzey.com.au/world-cup-2026-tips/iran-v-new-zealand/"},
    {"type":"model","name":"Squawka - Iran World Cup 2026 odds probability","url":"https://www.squawka.com/en/outright-markets/iran-world-cup-2026-odds/"},
    {"type":"model","name":"CupChances - Iran knockout chances 2026","url":"https://cupchances.com/en/world-cup/2026/iran"},
    {"type":"model","name":"CupChances - New Zealand knockout chances 2026","url":"https://cupchances.com/en/world-cup/2026/new-zealand"},
    {"type":"youtube","name":"YouTube - FIFA World Cup 2026 Group G Picks & Predictions (Iran -120)","url":"https://www.youtube.com/watch?v=nwy4lKxzx1s"},
    {"type":"youtube","name":"YouTube - Iran vs New Zealand 5 AI Results Predictions Debate","url":"https://www.youtube.com/watch?v=p6kj36JpHw4"},
    {"type":"youtube","name":"YouTube - New Zealand World Cup 2026 Preview Can Chris Wood Shock Group G","url":"https://www.youtube.com/watch?v=nzFi-F_3xPg"},
    {"type":"youtube","name":"YouTube - Chris Wood, Group G & The Real Goal","url":"https://www.youtube.com/watch?v=2KU6mKmnF14"},
    {"type":"kol","name":"Juve FC analyst - Iran favoured but domestic-league rust a concern","url":"https://www.juvefc.com/iran-v-new-zealand-predictions/"},
    {"type":"kol","name":"SI Brian Straus - NZ underdog, free hit with nothing to lose","url":"https://www.si.com/soccer/new-zealand-2026-world-cup-preview"},
    {"type":"kol","name":"Darren Bazeley (NZ assistant) - preparing as if playing Iran","url":"https://www.theguardian.com/football/2026/may/29/fifa-world-cup-football-group-stage-new-zealand-iran"},
    {"type":"forum","name":"Reddit r/newzealand - Iran Vs All Whites discussion","url":"https://www.reddit.com/r/newzealand/comments/1u3flhh/iran_vs_all_whites/"},
    {"type":"forum","name":"Reddit r/soccer - New Zealand's route to FIFA World Cup 2026","url":"https://www.reddit.com/r/soccer/comments/1jjgsnd/new_zealands_route_to_fifa_world_cup_2026/"},
    {"type":"forum","name":"Reddit r/worldcup - Iran New Zealand Group G discussion","url":"https://www.reddit.com/r/worldcup/"},
    {"type":"social","name":"Twitter/X - Iran New Zealand World Cup 2026 Group G","url":"https://twitter.com/search?q=Iran+NewZealand+WorldCup2026"},
    {"type":"social","name":"Instagram - NZ Football All Whites World Cup 2026","url":"https://www.instagram.com/nzfootball/"},
]

m16 = {
    "match": 16,
    "stage": "Group G",
    "home": "Iran",
    "away": "New Zealand",
    "kickoff_utc": "2026-06-16T01:00:00Z",
    "kickoff_hkt": "2026-06-16 09:00",
    "run_id": "2026-06-14T0551Z",
    "run_timestamp": "2026-06-14T05:51:00Z",
    "model": "claude-opus-4.8",
    "prediction": {
        "score": {"home": 1, "away": 0},
        "scoreline": "1:0",
        "outcome": "home",
        "win_prob": {"home": 0.54, "draw": 0.26, "away": 0.2},
        "confidence": 0.5,
        "top_scorelines": [
            {"scoreline": "1:0", "prob": 0.13},
            {"scoreline": "2:0", "prob": 0.11},
            {"scoreline": "1:1", "prob": 0.1},
            {"scoreline": "2:1", "prob": 0.08},
            {"scoreline": "0:0", "prob": 0.07}
        ],
        "scenarios": [
            {"name": "模型共識", "scoreline": "1:0", "outcome": "home", "confidence": 0.5,
             "basis": "Dimers 給伊朗 55-58.5%、Opta 出線率 64.3%，最可能比分伊朗 1-0，塔雷米一錘定音"},
            {"name": "博彩盤口", "scoreline": "2:1", "outcome": "home", "confidence": 0.5,
             "basis": "盤口伊朗約 5/6 至 2.10、讓 1 球、大小盤 2.5，KRUZEY 模型預測 2-1 伊朗勝"},
            {"name": "進攻火力", "scoreline": "2:0", "outcome": "home", "confidence": 0.45,
             "basis": "伊朗近五場進 10 球（含 5-0 大勝哥斯達黎加），若早進球可擴大比分壓制紐西蘭"},
            {"name": "紐西蘭守和爆冷", "scoreline": "1:1", "outcome": "draw", "confidence": 0.3,
             "basis": "紐西蘭以伍德為支點、定位球佔約三成 xG，加上伊朗本土聯賽停擺致狀態生疏，逼平甚至爆冷的劇本存在"}
        ],
        "benchmarks": [
            {"source": "Opta 超級電腦", "kind": "model",
             "win_prob": {"home": 0.5, "draw": 0.27, "away": 0.23},
             "outcome": "home", "scoreline": "1:0",
             "note": "Opta 給伊朗 Group G 出線率 64.3%、紐西蘭僅 47.8%，伊朗本場為較大熱門"},
            {"source": "Dimers 模型", "kind": "model",
             "win_prob": {"home": 0.55, "draw": 0.256, "away": 0.194},
             "outcome": "home", "scoreline": "1:0",
             "note": "Dimers 模擬伊朗 55.0%、平局 25.6%、紐西蘭 19.4%，最可能比分伊朗 1-0"},
            {"source": "博彩隱含機率", "kind": "betting",
             "win_prob": {"home": 0.5, "draw": 0.27, "away": 0.23},
             "outcome": "home", "scoreline": "1:0",
             "note": "伊朗約 5/6 至 2.10、平局 5/2 至 3.30、紐西蘭 7/2 至 3.40，讓 1 球"},
            {"source": "KRUZEY 模型", "kind": "model",
             "win_prob": {"home": 0.5, "draw": 0.27, "away": 0.23},
             "outcome": "home", "scoreline": "2:1",
             "note": "KRUZEY 給伊朗 50% 勝率，預測比分 2-1，大小盤偏 over 2.5"}
        ]
    },
    "reasoning": {
        "summary": "伊朗以 4-2-3-1 為主、可切換為更防守的 4-3-3，核心是奧林匹亞科斯前鋒梅赫迪·塔雷米，加上經驗豐富的門將貝蘭萬德與卡納尼扎德甘／哈利勒扎德赫中衛組合，整體實力與大賽經驗（第七次世界盃）優於首次重返世界盃 16 年的紐西蘭。但伊朗存在隱憂：頭號射手薩達爾·阿茲蒙因場外／政治爭議被排除於名單外，且本土聯賽自 2026 年 3 月停擺，多名國內球員缺乏比賽節奏。紐西蘭由諾丁漢森林前鋒、傷癒復出的隊長克里斯·伍德領銜，主打緊密 4-2-3-1 防守、卡卡切左路推進與定位球（約佔全隊三成 xG）。公開模型（Dimers 伊朗 55-58.5%、Opta 出線 64.3%）與博彩盤口（伊朗約 5/6）一致看好伊朗小勝，最可能比分 1-0 至 2-1。",
        "key_factors": [
            "球員狀態：伊朗倚靠塔雷米（近期狀態佳），但失去阿茲蒙後攻擊深度受損；紐西蘭隊長伍德膝傷手術後復出，承擔全隊約 43% xG，狀態與體能存在問號（34 歲）",
            "傷停名單：伊朗排除阿茲蒙（場外爭議，非傷停），埃扎托拉希已從足傷康復可上陣；紐西蘭主力辛格、加比特、卡卡切年內曾受傷，但無重大缺陣，伍德已恢復",
            "近期狀態/戰績：伊朗近五場三勝兩負，含 2-0 勝馬里、5-0 大勝哥斯達黎加、3-1 勝岡比亞，五場進 10 失 3；紐西蘭外圍賽 5 戰全勝進 29 失 1，但熱身賽近況起伏，曾 8 場 7 負",
            "戰術對位：伊朗中場塊狀防守＋右路低傳中找塔雷米；紐西蘭緊密 4-2-3-1、靠伍德高空支點與卡卡切左路反擊及定位球，雙方皆務實、比賽節奏偏慢",
            "主客場/場地：中立場美國洛杉磯 Inglewood 的 SoFi Stadium，香港時間 6 月 16 日 09:00 開賽，兩隊皆無真正主場優勢，洛杉磯波斯裔社群或為伊朗增添氣氛",
            "輿論共識：Dimers 給伊朗 55-58.5%、Opta 出線率 64.3% 對紐西蘭 47.8%、博彩伊朗約 5/6；KRUZEY 模型預測 2-1 伊朗勝；多數預覽視伊朗為熱門但承認本土球員生疏為變數"
        ],
        "consensus_lean": "home",
        "dissent": "少數派強烈看好紐西蘭：SI 指紐西蘭是「零壓力的免費一擊」，部分 YouTube 分析師認為紐西蘭借自全黑隊的拼搏 DNA、定位球精準與心理韌性，加上伊朗本土聯賽停擺致狀態生疏與阿茲蒙缺陣，足以製造爆冷（甚至預測紐西蘭 2-1）。nzsoccerwc 分析師更直接推介本場平局（賠率約 3.10）為最佳選擇，反映市場對伊朗能否如預期取勝並非全無疑慮。"
    },
    "sources": m16_sources,
    "source_count": len(m16_sources)
}

with open(os.path.join(base, "match_15__2026-06-14T0551Z.json"), "w", encoding="utf-8") as f:
    json.dump(m15, f, ensure_ascii=False, indent=2)
with open(os.path.join(base, "match_16__2026-06-14T0551Z.json"), "w", encoding="utf-8") as f:
    json.dump(m16, f, ensure_ascii=False, indent=2)

print("M15 sources:", len(m15_sources), "| scoreline:", m15["prediction"]["scoreline"], "| outcome:", m15["prediction"]["outcome"])
print("M16 sources:", len(m16_sources), "| scoreline:", m16["prediction"]["scoreline"], "| outcome:", m16["prediction"]["outcome"])
# validate win_prob sums
for tag, obj in [("M15", m15), ("M16", m16)]:
    wp = obj["prediction"]["win_prob"]
    print(tag, "win_prob sum:", round(sum(wp.values()), 4))
    for b in obj["prediction"]["benchmarks"]:
        print("  ", tag, b["source"], "sum:", round(sum(b["win_prob"].values()), 4))
