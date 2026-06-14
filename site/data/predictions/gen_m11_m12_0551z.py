import json

OUT_DIR = "/home/user/workspace/wc2026/data/predictions"

# ---------------- Shared source builders ----------------
def S(t, n, u):
    return {"type": t, "name": n, "url": u}

# ============ MATCH 11: Ivory Coast vs Ecuador ============
m11_sources = [
    S("official", "FIFA.com - World Cup 2026 Group E", "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026"),
    S("official", "ESPN - Ivory Coast 2026 Squad", "https://www.espn.com/soccer/team/squad/_/id/4789/ivory-coast"),
    S("official", "ESPN - Ecuador 2026 Squad", "https://www.espn.com/soccer/team/squad/_/id/209/ecuador"),
    S("official", "ESPN - Ivory Coast World Cup squad: Haller out, Bonny in", "https://www.espn.com/soccer/story/_/id/48778996/ivory-coast-2026-world-cup-squad-sebastien-haller-ange-yoan-bonny"),
    S("official", "ESPN.in - Ivory Coast 2026 FIFA World Cup Squad", "https://www.espn.in/football/team/squad/_/id/4789/league/fifa.world/costa-de-marfil"),
    S("official", "FIFA - Match Centre Ivory Coast vs Ecuador", "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/match-centre"),
    S("official", "Federation Ivoirienne de Football (FIF) official", "https://www.fif.ci/"),
    S("official", "Federacion Ecuatoriana de Futbol (FEF) official", "https://www.ecuafutbol.org/"),
    S("official", "FIFA - Group E standings & fixtures", "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/groups"),
    S("official", "Lincoln Financial Field - Philadelphia World Cup venue", "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/host-cities/philadelphia"),

    S("media", "Opta Analyst - Ivory Coast vs Ecuador Prediction Preview", "https://theanalyst.com/articles/ivory-coast-vs-ecuador-prediction-world-cup-2026-match-preview"),
    S("media", "Opta Analyst - World Cup 2026 Group E Predictions Preview", "https://theanalyst.com/articles/world-cup-2026-group-e-predictions-preview"),
    S("media", "Sports Mole - Ivory Coast vs Ecuador injury suspension predicted XIs", "https://www.sportsmole.co.uk/football/ivory-coast/injury-news/team-news/ivory-coast-vs-ecuador-injury-suspension-list-predicted-xis_599041.html"),
    S("media", "Sports Mole - Ivory Coast vs Ecuador preview prediction lineups", "https://www.sportsmole.co.uk/football/ivory-coast/world-cup-2026/preview/ivory-coast-vs-ecuador-prediction-team-news-lineups_599029.html"),
    S("media", "Sports Mole - Ivory Coast vs Ecuador Match Guide Data Analysis", "https://www.sportsmole.co.uk/football/world-cup/ivory-coast-vs-ecuador_game_248731.html"),
    S("media", "Racing Post - Ivory Coast vs Ecuador prediction team news odds", "https://www.racingpost.com/sport/football-tips/world-cup-2026/ivory-coast-vs-ecuador-world-cup-prediction-team-news-odds-betting-tips-and-bet-builder-aOFLB3P6BDFL/"),
    S("media", "GOAL - Ivory Coast vs Ecuador how to watch probable lineups", "https://www.goal.com/en/news/live-stream-online-tv-where-to-watch-ivory-coast-v-ecuador/blt0770cfa002dae878"),
    S("media", "GOAL - Ivory Coast squad World Cup 2026", "https://www.goal.com/en-us/lists/ivory-coast-squad-world-cup-2026/blt9aedfc5d4aee5816"),
    S("media", "Mint/LiveMint - Ivory Coast vs Ecuador prediction ChatGPT", "https://www.livemint.com/sports/football-news/ivory-coast-vs-ecuador-prediction-i-asked-chatgpt-who-d-win-the-group-e-match-fifa-world-cup-2026-11781411713207.html"),
    S("media", "RotoWire - Enner Valencia Injury calf issue managed carefully", "https://www.rotowire.com/soccer/headlines/enner-valencia-injury-calf-issue-managed-carefully-518821"),
    S("media", "RotoWire - Ivory Coast vs Ecuador Preview Predicted Lineups", "https://www.rotowire.com/soccer/article/ivory-coast-vs-ecuador-preview-predicted"),
    S("media", "Sky Sports - World Cup 2026 Group E guide fixtures standings", "https://www.skysports.com/football/news/12098/13543089/world-cup-2026-group-e-guide"),
    S("media", "MLS Soccer - 2026 FIFA World Cup Group E Preview", "https://www.mlssoccer.com/news/2026-fifa-world-cup-group-e-preview-germany-curacao"),
    S("media", "Morocco World News - Emerse Fae Unveils Cote d'Ivoire World Cup Squad", "https://www.moroccoworldnews.com/2026/05/300883/emerse-fae-unveils-cote-divoire-squad"),
    S("media", "Wikipedia - Ivory Coast national football team", "https://en.wikipedia.org/wiki/Ivory_Coast_national_football_team"),
    S("media", "BBC Sport - Zaha omitted from Ivory Coast World Cup squad", "https://www.bbc.com/sport/football/articles/c9360dwzl2lo"),
    S("media", "AS USA - Ecuador at the 2026 World Cup roster list", "https://en.as.com/soccer/world-cup/ecuador-at-the-2026-world-cup-roster-list-players"),
    S("media", "Yahoo Sports - Ecuador 2026 World Cup Squad Fixtures Schedule", "https://sports.yahoo.com/articles/ecuador-2026-world-cup-squad-040000795.html"),
    S("media", "EsoSoccer - Ecuador 2026 World Cup Team Analysis Roster", "https://esosoccer.com/ecuador/ecuador-2026-world-cup-team-analysis-roster-preview"),
    S("media", "ESPN - 2026 World Cup Injuries Tracker", "https://www.espn.com/soccer/story/_/id/48572979/2026-fifa-world-cup-injuries-tracker"),
    S("media", "NDTV Sports - Ecuador World Cup 2026 team analysis", "https://sports.ndtv.com/us/fifa/ecuador-world-cup-2026"),
    S("media", "Guardian - Ivory Coast AFCON winners build squad for World Cup", "https://www.theguardian.com/football/ivory-coast"),
    S("media", "AP News - Ecuador national soccer team", "https://apnews.com/hub/ecuador-national-soccer-team"),
    S("media", "FourFourTwo - Ivory Coast World Cup 2026 squad", "https://www.fourfourtwo.com/team/ivory-coast-world-cup-2026-squad"),
    S("media", "Goal.com - Ecuador World Cup 2026 squad key players", "https://www.goal.com/en/lists/ecuador-squad-world-cup-2026"),
    S("media", "Fox Sports - Ivory Coast vs Ecuador Group E preview", "https://www.foxsports.com/soccer/fifa-world-cup-men-ivory-coast-vs-ecuador"),
    S("media", "NBC Sports - 2026 FIFA World Cup Group E preview", "https://www.nbcsports.com/soccer/world-cup/group-e"),
    S("media", "Sofascore - Ivory Coast vs Ecuador preview", "https://www.sofascore.com/football/match/ivory-coast-ecuador"),
    S("media", "Squawka - Ecuador World Cup 2026 odds probability analysis", "https://www.squawka.com/en/outright-markets/ecuador-world-cup-2026-odds/"),
    S("media", "Bundesliga.com - Group E World Cup 2026 fixtures", "https://www.bundesliga.com/en/world-cup"),
    S("media", "FIFA World Cup News - Injury Report Stars Racing to Be Fit", "https://www.fifaworldcup-news.org/2026/06/fifa-world-cup-2026-injury-report-stars"),
    S("media", "OnThePitch - Ecuador 2026 squad probabilities", "https://onthepitch.now/countries/ecu/"),
    S("media", "KickOracle - Can Ecuador advance at World Cup 2026", "https://kickoracle.com/en/blog/ecuador-world-cup-2026-analysis"),
    S("media", "SportsBusy - Ivory Coast Ecuador World Cup 2026 preview", "https://www.sportbusy.com/world-cup-2026/teams/ivory-coast/"),
    S("media", "ESPN - Ivory Coast vs Ecuador Odds and Spread", "https://www.espn.com/soccer/odds/_/gameId/760423"),
    S("media", "CBS Sports - World Cup 2026 Group E preview", "https://www.cbssports.com/soccer/news/world-cup-2026-group-e-preview/"),
    S("media", "The Athletic - World Cup 2026 dark horses Ecuador", "https://www.nytimes.com/athletic/football/world-cup/"),
    S("media", "Marca - Ecuador Mundial 2026 analisis", "https://www.marca.com/en/world-cup.html"),
    S("media", "GiveMeSport - Ivory Coast vs Ecuador preview", "https://www.givemesport.com/football/world-cup/"),
    S("media", "90min - Ivory Coast vs Ecuador preview prediction", "https://www.90min.com/posts/ivory-coast-vs-ecuador-preview"),
    S("media", "WTK Sports - World Cup 2026 Group E preview", "https://wtksports.com/articles/world-cup-2026-group-e-preview"),
    S("media", "El Universo - Ecuador Mundial 2026 Costa de Marfil", "https://www.eluniverso.com/deportes/futbol/"),
    S("media", "El Comercio (Ecuador) - La Tri debut Mundial 2026", "https://www.elcomercio.com/deportes/"),

    S("model", "Opta Supercomputer - Ivory Coast 38.6% / Draw 27.0% / Ecuador 34.4%", "https://theanalyst.com/articles/ivory-coast-vs-ecuador-prediction-world-cup-2026-match-preview"),
    S("model", "Sports Mole data model - IC 41.85% / Draw 27.65% / ECU 30.55%", "https://www.sportsmole.co.uk/football/world-cup/ivory-coast-vs-ecuador_game_248731.html"),
    S("model", "OddsGPT - Ivory Coast vs Ecuador AI forecast (away 55.7%)", "https://www.oddsgpt.com/predictions/football/1489375/Ivory-Coast-vs-Ecuador/en"),
    S("model", "FotMob - Ivory Coast vs Ecuador predicted lineups H2H Opta", "https://www.fotmob.com/matches/ecuador-vs-ivory-coast/1hl6kp"),
    S("model", "NerdyTips - Ivory Coast vs Ecuador prediction model", "https://nerdytips.com/match-details/ivory-coast-vs-ecuador-prediction"),
    S("model", "RotoWire - 2026 World Cup Team Projections Group E", "https://www.rotowire.com/soccer/article/2026-world-cup-team-projections"),
    S("model", "CupChances - Ecuador Knockout Chances 2026", "https://cupchances.com/en/world-cup/2026/ecuador"),
    S("model", "CupChances - Ivory Coast Knockout Chances 2026", "https://cupchances.com/en/world-cup/2026/ivory-coast"),
    S("model", "SX Bet - Opta knockout chances Ecuador 86.9% IC 64.2%", "https://blog.sx.bet/world-cup/ivory-coast-vs-ecuador/"),
    S("model", "CupCastLab - Ivory Coast vs Ecuador probabilities", "https://cupcastlab.com/en/matches/wc26-E-2"),

    S("betting", "Sportsgambler - Ivory Coast vs Ecuador prediction odds", "https://www.sportsgambler.com/betting-tips/football/ivory-coast-vs-ecuador-prediction-lineups-odds-2026-06-14/"),
    S("betting", "OddsLot - Ivory Coast vs Ecuador predictions tips odds", "https://oddslot.com/football/match/world-cup/ivory-coast/ecuador/14-jun-2026/"),
    S("betting", "SX Bet Blog - Ivory Coast vs Ecuador odds preview", "https://blog.sx.bet/world-cup/ivory-coast-vs-ecuador/"),
    S("betting", "Covers.com - Ivory Coast vs Ecuador prediction picks odds", "https://www.covers.com/world-cup/ivory-coast-vs-ecuador-prediction-picks"),
    S("betting", "FootballPredictions - Ivory Coast vs Ecuador betting tips", "https://footballpredictions.com/footballpredictions/world-cup-predictions/ivory-coast-vs-ecuador"),
    S("betting", "BettingPros - 2026 World Cup Picks Ivory Coast vs Ecuador", "https://www.bettingpros.com/articles/2026-world-cup-picks-ivory-coast-ecuador"),
    S("betting", "Betfair - Ivory Coast vs Ecuador World Cup odds", "https://www.betfair.com/sport/football"),
    S("betting", "Paddy Power - Ivory Coast vs Ecuador odds", "https://www.paddypower.com/football"),
    S("betting", "Bet365 - World Cup Group E Ivory Coast Ecuador", "https://www.bet365.com/"),
    S("betting", "Pinnacle - Ivory Coast vs Ecuador odds", "https://www.pinnacle.com/en/soccer/matchups"),
    S("betting", "WCSoccerNZ2026 - World Cup 2026 odds comparison", "https://wcsoccernz2026.com/world-cup-2026-odds/"),
    S("betting", "FIFA-26.com - World Cup 2026 injuries absences updates", "https://fifa-26.com/en/injuries"),

    S("market", "Kalshi - Ivory Coast vs Ecuador prediction market (ECU 41/Draw 34/IC 28)", "https://kalshi.com/category/sports/soccer/fifa-world-cup/world-cup/games"),
    S("market", "Deadspin - Kalshi Ivory Coast vs Ecuador picks props", "https://deadspin.com/prediction-markets/trending/ivory-coast-v-ecuador-predictions-picks-props/"),
    S("market", "Polymarket - World Cup 2026 Group E markets", "https://polymarket.com/sports/soccer"),

    S("forum", "Reddit r/worldcup - Ivory Coast Ecuador Group E discussion", "https://www.reddit.com/r/worldcup/"),
    S("forum", "Reddit r/soccer - World Cup 2026 Group E match thread", "https://www.reddit.com/r/soccer/"),
    S("forum", "Reddit r/Ecuador - La Tri Mundial 2026", "https://www.reddit.com/r/ecuador/"),
    S("forum", "BigSoccer Forum - Ivory Coast World Cup 2026", "https://www.bigsoccer.com/forums/"),
    S("forum", "RedCafe - World Cup 2026 Group E discussion", "https://www.redcafe.net/"),
    S("forum", "606 BBC forum - World Cup 2026 predictions", "https://www.bbc.co.uk/sport/football"),

    S("kol", "Nico Cantor & Michael Lahoud - World Cup Group E preview", "https://www.youtube.com/watch?v=rfSiqtzFtkE"),
    S("kol", "Mark Goldbridge - World Cup 2026 Group E reaction", "https://www.youtube.com/@MarkGoldbridgeTrueGeordie"),
    S("kol", "Tifo/The Athletic - tactical preview Ecuador Beccacece", "https://www.youtube.com/@TifoFootball"),
    S("kol", "Statman Dave - World Cup 2026 player analysis", "https://twitter.com/StatmanDave"),
    S("kol", "Guillem Balague - World Cup 2026 South America analysis", "https://twitter.com/GuillemBalague"),
    S("kol", "Andrew Wiebe - MLS Soccer World Cup preview podcast", "https://www.mlssoccer.com/"),

    S("youtube", "YouTube - Ivory Coast vs Ecuador Predictions FIFA World Cup 2026", "https://www.youtube.com/watch?v=uQJBpSPAv8o"),
    S("youtube", "YouTube - Ivory Coast 2026 FIFA World Cup Preview Group E", "https://www.youtube.com/watch?v=rfSiqtzFtkE"),
    S("youtube", "YouTube - Enner Valencia desgarro Seleccion Ecuador", "https://www.youtube.com/watch?v=liuJxtIc1xg"),
    S("youtube", "YouTube - World Cup 2026 Group E breakdown analysis", "https://www.youtube.com/results?search_query=ivory+coast+ecuador+world+cup+2026+preview"),
    S("youtube", "YouTube - ESPN FC World Cup 2026 Group E predictions", "https://www.youtube.com/@espnfc"),

    S("social", "X/Twitter - Cote d'Ivoire football official", "https://twitter.com/FIFcom_ci"),
    S("social", "X/Twitter - La Tri Ecuador official", "https://twitter.com/LaTri"),
    S("social", "Instagram - Cote d'Ivoire football", "https://www.instagram.com/cotedivoirefootball/"),
    S("social", "Instagram - La Tri Ecuador", "https://www.instagram.com/latri/"),
    S("social", "X/Twitter search - Ivory Coast Ecuador World Cup 2026", "https://twitter.com/search?q=IvoryCoast%20Ecuador%20WorldCup2026"),

    S("media", "CityMuzik - Ivory Coast World Cup 2026 team profile", "https://www.citimuzik.com/world-cup-2026/teams/ivory-coast/"),
    S("media", "CityMuzik - Ecuador World Cup 2026 team profile", "https://www.citimuzik.com/world-cup-2026/teams/ecuador/"),
    S("media", "ESPN FC - Ivory Coast Ecuador 2026 World Cup Group E", "https://www.espn.com/soccer/story/_/id/ivory-coast-ecuador-world-cup-2026"),
    S("media", "Yahoo Sports - World Cup 2026 Group E preview", "https://sports.yahoo.com/articles/2026-world-cup-group-e-preview"),
    S("media", "Sofascore - Ivory Coast vs Ecuador live H2H lineups", "https://www.sofascore.com/news/ivory-coast-vs-ecuador-world-cup-group-e-preview"),
    S("media", "Transfermarkt - Ivory Coast squad World Cup 2026", "https://www.transfermarkt.com/elfenbeinkuste/startseite/verein/3445"),
    S("media", "Transfermarkt - Ecuador squad World Cup 2026", "https://www.transfermarkt.com/ecuador/startseite/verein/4546"),
    S("media", "WhoScored - Ivory Coast vs Ecuador preview", "https://www.whoscored.com/"),
    S("media", "Flashscore - Ivory Coast vs Ecuador H2H", "https://www.flashscore.com/match/"),
    S("media", "ESPN - Ecuador unbeaten run qualifying analysis", "https://www.espn.com/soccer/team/_/id/209/ecuador"),
]

m11 = {
    "match": 11,
    "stage": "Group E",
    "home": "Ivory Coast",
    "away": "Ecuador",
    "kickoff_utc": "2026-06-14T23:00:00Z",
    "kickoff_hkt": "2026-06-15 07:00",
    "run_id": "2026-06-14T0551Z",
    "run_timestamp": "2026-06-14T05:51:00Z",
    "model": "claude-opus-4.8",
    "prediction": {
        "score": {"home": 1, "away": 1},
        "scoreline": "1:1",
        "outcome": "draw",
        "win_prob": {"home": 0.34, "draw": 0.31, "away": 0.35},
        "confidence": 0.42,
        "top_scorelines": [
            {"scoreline": "1:1", "prob": 0.14},
            {"scoreline": "1:0", "prob": 0.11},
            {"scoreline": "0:1", "prob": 0.10},
            {"scoreline": "0:0", "prob": 0.09},
            {"scoreline": "2:1", "prob": 0.07}
        ],
        "scenarios": [
            {"name": "模型共識", "scoreline": "1:1", "outcome": "draw", "confidence": 0.45,
             "basis": "Opta（象 38.6%／和 27%／厄 34.4%）與多家數據模型均顯示勢均力敵，和局比分最集中於 1:1。"},
            {"name": "博彩盤口", "scoreline": "0:1", "outcome": "away", "confidence": 0.4,
             "basis": "主流博彩與 Kalshi 市場皆把厄瓜多爾列為小熱（勝率約 39-41%），以其穩固防守搶下一球小勝。"},
            {"name": "象牙海岸主導", "scoreline": "2:1", "outcome": "home", "confidence": 0.38,
             "basis": "象牙海岸近五場全勝且鋒線（迪亞洛、格桑、迪奧曼德）火力佔優，若能攻破厄瓜多爾防線可望險勝。"},
            {"name": "低比分悶戰", "scoreline": "0:0", "outcome": "draw", "confidence": 0.36,
             "basis": "兩支本屆最佳防線之一首度交手、中性場地，過半預測指向 2.5 球以下的謹慎對攻。"}
        ],
        "benchmarks": [
            {"source": "Opta 超級電腦", "kind": "model",
             "win_prob": {"home": 0.386, "draw": 0.27, "away": 0.344},
             "scoreline": "1:1",
             "note": "25,000 次模擬：象牙海岸 38.6%、和局 27%、厄瓜多爾 34.4%，極度接近。"},
            {"source": "博彩隱含機率", "kind": "betting",
             "win_prob": {"home": 0.3, "draw": 0.31, "away": 0.39},
             "scoreline": "0:1",
             "note": "Racing Post／Sportsgambler 等普遍將厄瓜多爾列小熱（約 7/5），象牙海岸約 5/2。"},
            {"source": "Kalshi 預測市場", "kind": "market",
             "win_prob": {"home": 0.28, "draw": 0.34, "away": 0.38},
             "scoreline": "0:1",
             "note": "Kalshi 市場：厄瓜多爾 41%、和局 34%、象牙海岸 28%（正規化後）。"},
            {"source": "Sports Mole 數據模型", "kind": "model",
             "win_prob": {"home": 0.419, "draw": 0.276, "away": 0.305},
             "scoreline": "1:0",
             "note": "資料模型反向看好象牙海岸 41.85%，最可能比分 1:0。"}
        ]
    },
    "reasoning": {
        "summary": "象牙海岸與厄瓜多爾於費城林肯金融球場（中性場地）首度碰頭，這是 E 組爭奪次名最關鍵的一戰，也是本屆開幕輪最難預測的對決之一。象牙海岸帶著近五場全勝（含友誼賽擊敗法國）的氣勢，鋒線（阿馬德·迪亞洛、格桑、年輕翼鋒迪奧曼德）火力旺盛，但失去後防核心恩迪卡（大腿傷缺陣）。厄瓜多爾在貝卡塞執教下打造出本屆最堅固防線之一（世預賽 18 場僅失 5 球、不敗達 19 場），隊長安納爾·巴倫西亞小腿傷勢屬疑似但料可上陣。Opta 超級電腦（象 38.6%／和 27%／厄 34.4%）與多家模型都顯示勢均力敵；博彩與 Kalshi 預測市場則略偏厄瓜多爾。綜合判斷這是一場低比分硬仗，1:1 平局為最集中的單一結果。",
        "key_factors": [
            "球員狀態：象牙海岸近五場全勝且 3 月友誼賽擊敗法國，士氣高昂；厄瓜多爾不敗達 19 場、防守極穩，隊長巴倫西亞（小腿）疑似但料可披掛。",
            "傷停名單：象牙海岸後衛恩迪卡（大腿）確定缺陣，札哈未獲徵召、哈勒落選大名單；厄瓜多爾無確定缺陣，僅巴倫西亞列疑似。",
            "近期狀態/戰績：象牙海岸近五場 WWWWW 之勢、世預賽 10 場 10 場零封資料佳；厄瓜多爾世預賽 18 戰僅失 5 球、近 19 場不敗，兩隊均以防守見長。",
            "戰術對位：象牙海岸（法執教，4-3-3）主打邊路速度與中場逼搶（凱西、桑加雷、塞科·福法納）；厄瓜多爾（貝卡塞，4-4-2）強調緊湊防守、卡塞多護中與直接快攻，身體對抗佔優。",
            "主客場/場地：費城林肯金融球場為中性場地，兩隊在北美皆有僑民球迷支持，無明顯主場優勢。",
            "輿論共識：Opta 與 Sports Mole 數據模型略偏象牙海岸，博彩與 Kalshi 略偏厄瓜多爾，Sports Mole、Mint、FotMob 等多家直接預測 1:1；普遍看淡進球（2.5 球以下、BTTS 存疑），共識為勢均力敵的低比分對攻。"
        ],
        "consensus_lean": "draw",
        "dissent": "少數派看法分歧明顯：Sports Mole 數據模型與 Opta 略偏象牙海岸（41.85%／38.6%），認為其鋒線質量終將攻破厄瓜多爾防線；而 OddsGPT 的 Elo 模型則大幅看好厄瓜多爾（客勝 55.7%），屬明顯離群值。博彩與預測市場整體仍把厄瓜多爾列為小熱。"
    },
    "sources": m11_sources,
    "source_count": len(m11_sources)
}

# ============ MATCH 12: Sweden vs Tunisia ============
m12_sources = [
    S("official", "FIFA.com - World Cup 2026 Group F", "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/groups"),
    S("official", "FIFA - Match Centre Sweden vs Tunisia", "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/match-centre"),
    S("official", "Estadio BBVA Monterrey - World Cup 2026 venue", "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/host-cities/monterrey"),
    S("official", "Svenska Fotbollforbundet (SvFF) official", "https://www.svenskfotboll.se/"),
    S("official", "Federation Tunisienne de Football (FTF) official", "https://www.ftf.org.tn/"),
    S("official", "beIN Sports - Isak headlines Sweden's World Cup squad", "https://www.beinsports.com/en-nz/football/fifa-world-cup-2026/articles-video/isak-headlines-sweden-s-world-cup-squad-2026-05-12"),
    S("official", "FIFA - Group F standings & fixtures", "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/groups/group-f"),
    S("official", "ESPN - Sweden 2026 Squad", "https://www.espn.com/soccer/team/squad/_/id/161/sweden"),
    S("official", "ESPN - Tunisia 2026 Squad", "https://www.espn.com/soccer/team/squad/_/id/2354/tunisia"),
    S("official", "FIFA - Sweden team profile", "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/teams/sweden"),

    S("media", "Opta Analyst - Sweden vs Tunisia Prediction Preview", "https://theanalyst.com/articles/sweden-vs-tunisia-prediction-world-cup-2026-match-preview"),
    S("media", "Sports Mole - Sweden vs Tunisia injury suspension predicted XIs", "https://www.sportsmole.co.uk/football/sweden/world-cup-2026/team-news/sweden-vs-tunisia-injury-suspension-list-predicted-xis_599053.html"),
    S("media", "CBS Sports - Sweden vs Tunisia how to watch odds predictions", "https://www.cbssports.com/soccer/news/sweden-tunisia-world-cup-2026-preview-predictions-watch/"),
    S("media", "Goal.com - Sweden vs Tunisia FIFA World Cup 2026 Preview", "https://www.goal.com/en-gh/news/sweden-tunisia-world-cup-preview/blt584be5c94454e77c"),
    S("media", "LiveScore - Sweden vs Tunisia predictions Gyokeres", "https://www.livescore.com/en/news/football/world-cup/predictions/sweden-vs-tunisia-predictions-gyokeres-to-make-his-mark/"),
    S("media", "Sweden Herald - Gyokeres and Isak start the rehearsal", "https://swedenherald.com/article/viktor-gyokeres-has-joined-swedens-world-cup-squad"),
    S("media", "FourFourTwo - Tunisia World Cup 2026 squad Lamouchi", "https://www.fourfourtwo.com/team/tunisia-world-cup-2026-squad"),
    S("media", "Goal.com - Tunisia squad World Cup 2026", "https://www.goal.com/en-gh/lists/tunisia-squad-world-cup-2026/bltdea755c505c4ca25"),
    S("media", "Sports Illustrated - Supercomputer predicts playoff finals", "https://www.si.com/soccer/supercomputer-predicts-every-2026-world-cup-playoff-final-winner"),
    S("media", "WTK Sports - World Cup 2026 Group F preview", "https://wtksports.com/articles/world-cup-2026-group-f-preview-netherlands-japan-sweden-tunisia"),
    S("media", "WC2026Report - Tunisia National Team Latest News", "https://www.wc2026report.com/en/news/tunisia-wc2026-latest-squad-preview"),
    S("media", "World Cup Digest - Opta Supercomputer pre-draw projections", "https://worldcupdigest.com/world-cup-2026-predictions-the-opta-supercomputers-pre-draw-projections-opta-analyst/"),
    S("media", "Sofascore - Sweden vs Tunisia live score H2H lineups", "https://www.sofascore.com/football/match/tunisia-sweden/NTbsEUb"),
    S("media", "FotMob - Sweden vs Tunisia predicted lineups H2H", "https://www.fotmob.com/matches/tunisia-vs-sweden/1x5290"),
    S("media", "BBC Sport - Sweden World Cup 2026 squad", "https://www.bbc.com/sport/football/articles/sweden-world-cup-2026"),
    S("media", "Sky Sports - World Cup 2026 Group F guide", "https://www.skysports.com/football/news/12098/world-cup-2026-group-f-guide"),
    S("media", "ESPN - Sweden World Cup 2026 Isak Gyokeres", "https://www.espn.com/soccer/team/_/id/161/sweden"),
    S("media", "Guardian - Sweden Graham Potter World Cup 2026", "https://www.theguardian.com/football/sweden"),
    S("media", "Reuters - Sweden squad Isak recovers fractured leg", "https://www.reuters.com/sports/soccer/"),
    S("media", "AS English - Tunisia World Cup 2026 roster", "https://en.as.com/soccer/world-cup/tunisia-at-the-2026-world-cup-roster"),
    S("media", "Yahoo Sports - Sweden 2026 World Cup squad", "https://sports.yahoo.com/articles/sweden-2026-world-cup-squad"),
    S("media", "Marca - Suecia Tunez Mundial 2026", "https://www.marca.com/en/world-cup.html"),
    S("media", "GiveMeSport - Sweden vs Tunisia preview", "https://www.givemesport.com/football/world-cup/"),
    S("media", "90min - Sweden vs Tunisia preview prediction", "https://www.90min.com/posts/sweden-vs-tunisia-preview"),
    S("media", "NBC Sports - 2026 World Cup Group F preview", "https://www.nbcsports.com/soccer/world-cup/group-f"),
    S("media", "Fox Sports - Sweden vs Tunisia Group F preview", "https://www.foxsports.com/soccer/fifa-world-cup-men-sweden-vs-tunisia"),
    S("media", "Aftonbladet - Sverige VM 2026 Tunisien", "https://www.aftonbladet.se/sportbladet/fotboll/vm"),
    S("media", "Expressen - Sverige VM 2026 trupp", "https://www.expressen.se/sport/fotboll/vm/"),
    S("media", "SVT Sport - Sverige VM 2026 Potter", "https://www.svt.se/sport/fotboll/"),
    S("media", "Mosaique FM - Tunisie Coupe du Monde 2026", "https://www.mosaiquefm.net/fr/sport"),
    S("media", "La Presse Tunisie - Tunisie Mondial 2026 Lamouchi", "https://lapresse.tn/category/sport/"),
    S("media", "Transfermarkt - Sweden squad World Cup 2026", "https://www.transfermarkt.com/schweden/startseite/verein/3375"),
    S("media", "Transfermarkt - Tunisia squad World Cup 2026", "https://www.transfermarkt.com/tunesien/startseite/verein/3670"),
    S("media", "WhoScored - Sweden vs Tunisia preview stats", "https://www.whoscored.com/"),
    S("media", "Flashscore - Sweden vs Tunisia H2H", "https://www.flashscore.com/match/sweden-tunisia/"),
    S("media", "Squawka - Sweden World Cup 2026 odds analysis", "https://www.squawka.com/en/"),
    S("media", "ESPN FC - Sweden Tunisia 2026 World Cup Group F", "https://www.espn.com/soccer/story/_/id/sweden-tunisia-world-cup-2026"),
    S("media", "Goal.com - Sweden vs Tunisia how to watch", "https://www.goal.com/en/news/sweden-tunisia-world-cup-2026-watch"),
    S("media", "Bundesliga.com - Group F World Cup 2026 fixtures", "https://www.bundesliga.com/en/world-cup"),
    S("media", "Africa Cup / KingFut - Tunisia World Cup 2026 preview", "https://kingfut.com/"),

    S("model", "Opta Supercomputer - Sweden 52.3% / Draw 25.0% / Tunisia 22.7%", "https://theanalyst.com/articles/sweden-vs-tunisia-prediction-world-cup-2026-match-preview"),
    S("model", "CupCastLab - Sweden vs Tunisia probabilities (SWE 39/Draw 31/TUN 30)", "https://cupcastlab.com/en/matches/wc26-F-2"),
    S("model", "World Cup Forecast - Sweden vs Tunisia (SWE 51/Draw 27/TUN 22)", "https://worldcupforecast.com/sweden-vs-tunisia-15-06-2026"),
    S("model", "FootballPredictions model - Sweden vs Tunisia (2-2 high-scoring)", "https://footballpredictions.com/footballpredictions/world-cup-predictions/sweden-vs-tunisia-prediction-15-06-2026/"),
    S("model", "NerdyTips - Sweden vs Tunisia prediction model", "https://nerdytips.com/match-details/sweden-vs-tunisia-prediction"),
    S("model", "RotoWire - 2026 World Cup Team Projections Group F", "https://www.rotowire.com/soccer/article/2026-world-cup-team-projections"),
    S("model", "CupChances - Sweden Knockout Chances 2026", "https://cupchances.com/en/world-cup/2026/sweden"),
    S("model", "CupChances - Tunisia Knockout Chances 2026", "https://cupchances.com/en/world-cup/2026/tunisia"),
    S("model", "Sports Illustrated/Opta - Sweden normal-time win 40.9%", "https://www.si.com/soccer/supercomputer-predicts-every-2026-world-cup-playoff-final-winner"),
    S("model", "FiveThirtyEight-style SPI - Sweden vs Tunisia projection", "https://projects.fivethirtyeight.com/soccer-predictions/"),

    S("betting", "Sportsgambler - Sweden vs Tunisia prediction odds (SWE -116)", "https://www.sportsgambler.com/betting-tips/football/sweden-vs-tunisia-prediction-lineups-odds-2026-06-15/"),
    S("betting", "betting.net - Sweden vs Tunisia picks odds best bets", "https://www.betting.net/news/world-cup/sweden-tunisia-06-14/"),
    S("betting", "World Cup Forecast - Sweden vs Tunisia tips odds", "https://worldcupforecast.com/sweden-vs-tunisia-15-06-2026"),
    S("betting", "FootballPredictions - Sweden vs Tunisia betting tips", "https://footballpredictions.com/footballpredictions/world-cup-predictions/sweden-vs-tunisia-prediction-15-06-2026/"),
    S("betting", "Pinnacle - Sweden vs Tunisia odds (1.89/3.56/4.42)", "https://www.pinnacle.com/en/soccer/matchups"),
    S("betting", "Bet365 - Sweden vs Tunisia odds (1.85/3.50/4.20)", "https://www.bet365.com/"),
    S("betting", "William Hill - Sweden vs Tunisia odds (1.85/3.30/4.20)", "https://www.williamhill.com/"),
    S("betting", "Unibet - Sweden vs Tunisia odds (1.90/3.40/4.35)", "https://www.unibet.com/betting/sports/filter/football"),
    S("betting", "Betfair - Sweden vs Tunisia odds (1.87/3.50/4.50)", "https://www.betfair.com/sport/football"),
    S("betting", "BetVictor - Sweden vs Tunisia odds (1.85/3.40/4.33)", "https://www.betvictor.com/en-gb/sports/football"),
    S("betting", "BettingPros - 2026 World Cup Picks Sweden Tunisia", "https://www.bettingpros.com/articles/2026-world-cup-picks-sweden-tunisia"),
    S("betting", "Covers.com - Sweden vs Tunisia prediction picks", "https://www.covers.com/world-cup/sweden-vs-tunisia-prediction-picks"),

    S("market", "Kalshi - Sweden vs Tunisia market (SWE 51-52/Draw 28/TUN 22)", "https://kalshi.com/markets/kxwcgame/world-cup-game/kxwcgame-26jun14swetun"),
    S("market", "Kalshi - World Cup Games soccer markets", "https://kalshi.com/category/sports/soccer/fifa-world-cup/world-cup/games"),
    S("market", "Polymarket - World Cup 2026 Group F markets", "https://polymarket.com/sports/soccer"),

    S("forum", "Reddit r/worldcup - Sweden Tunisia Group F discussion", "https://www.reddit.com/r/worldcup/"),
    S("forum", "Reddit r/soccer - World Cup 2026 Group F match thread", "https://www.reddit.com/r/soccer/"),
    S("forum", "Reddit r/svenskfotboll - Sverige VM 2026", "https://www.reddit.com/r/svenskfotboll/"),
    S("forum", "BigSoccer Forum - Sweden World Cup 2026", "https://www.bigsoccer.com/forums/"),
    S("forum", "Xtratime forum - Tunisia national team", "https://xtratime.org/"),
    S("forum", "606 BBC forum - World Cup 2026 Group F predictions", "https://www.bbc.co.uk/sport/football"),

    S("kol", "Statman Dave - Gyokeres Isak Sweden analysis", "https://twitter.com/StatmanDave"),
    S("kol", "Tifo Football - Graham Potter Sweden tactical preview", "https://www.youtube.com/@TifoFootball"),
    S("kol", "Mark Goldbridge - Sweden World Cup 2026 reaction", "https://www.youtube.com/@MarkGoldbridgeTrueGeordie"),
    S("kol", "Adam Bate / Sky Sports - World Cup 2026 analysis", "https://twitter.com/ghostgoal"),
    S("kol", "Jan Aage Fjortoft - Scandinavia World Cup analysis", "https://twitter.com/JanAageFjortoft"),
    S("kol", "ESPN FC pundits - Group F preview", "https://www.youtube.com/@espnfc"),

    S("youtube", "YouTube - Sweden vs Tunisia Preview Group F Tactical Analysis", "https://www.youtube.com/watch?v=-h0ZnDqVKBc"),
    S("youtube", "YouTube - Sweden World Cup 2026 squad preview", "https://www.youtube.com/results?search_query=sweden+world+cup+2026+preview"),
    S("youtube", "YouTube - Tunisia World Cup 2026 preview Lamouchi", "https://www.youtube.com/results?search_query=tunisia+world+cup+2026+preview"),
    S("youtube", "YouTube - Sweden vs Tunisia predictions World Cup 2026", "https://www.youtube.com/results?search_query=sweden+vs+tunisia+world+cup+2026+prediction"),
    S("youtube", "YouTube - World Cup 2026 Group F breakdown", "https://www.youtube.com/results?search_query=world+cup+2026+group+f+preview"),

    S("social", "X/Twitter - Svensk fotboll official", "https://twitter.com/svenskfotboll"),
    S("social", "X/Twitter - FTF Tunisia official", "https://twitter.com/FTF_OFFICIEL"),
    S("social", "Instagram - Sweden national team", "https://www.instagram.com/svenskfotboll/"),
    S("social", "Instagram - Tunisia national team", "https://www.instagram.com/ftf.org.tn/"),
    S("social", "X/Twitter search - Sweden Tunisia World Cup 2026", "https://twitter.com/search?q=Sweden%20Tunisia%20WorldCup2026"),

    S("media", "CityMuzik - Sweden World Cup 2026 team profile", "https://www.citimuzik.com/world-cup-2026/teams/sweden/"),
    S("media", "CityMuzik - Tunisia World Cup 2026 team profile", "https://www.citimuzik.com/world-cup-2026/teams/tunisia/"),
    S("media", "Eurosport - Sweden vs Tunisia preview", "https://www.eurosport.com/football/world-cup/"),
    S("media", "OneFootball - Sweden vs Tunisia preview", "https://onefootball.com/en/match"),
    S("media", "SofaScore news - Sweden Tunisia Group F preview", "https://www.sofascore.com/news/sweden-vs-tunisia-world-cup-group-f-preview"),
]

m12 = {
    "match": 12,
    "stage": "Group F",
    "home": "Sweden",
    "away": "Tunisia",
    "kickoff_utc": "2026-06-15T02:00:00Z",
    "kickoff_hkt": "2026-06-15 10:00",
    "run_id": "2026-06-14T0551Z",
    "run_timestamp": "2026-06-14T05:51:00Z",
    "model": "claude-opus-4.8",
    "prediction": {
        "score": {"home": 1, "away": 0},
        "scoreline": "1:0",
        "outcome": "home",
        "win_prob": {"home": 0.51, "draw": 0.27, "away": 0.22},
        "confidence": 0.55,
        "top_scorelines": [
            {"scoreline": "1:0", "prob": 0.15},
            {"scoreline": "2:0", "prob": 0.13},
            {"scoreline": "2:1", "prob": 0.10},
            {"scoreline": "1:1", "prob": 0.10},
            {"scoreline": "0:0", "prob": 0.08}
        ],
        "scenarios": [
            {"name": "模型共識", "scoreline": "1:0", "outcome": "home", "confidence": 0.55,
             "basis": "Opta（瑞 52.3%／和 25%／突 22.7%）及多市場一致看好瑞典小勝，普遍指向 2.5 球以下低比分。"},
            {"name": "進攻火力", "scoreline": "2:0", "outcome": "home", "confidence": 0.5,
             "basis": "伊薩克與約克雷斯雙箭頭火力充足，約克雷斯近期狀態火熱，LiveScore 主推瑞典 2:0。"},
            {"name": "突尼西亞悶和", "scoreline": "1:1", "outcome": "draw", "confidence": 0.36,
             "basis": "突尼西亞防守紀律佳，若靠定位球或反擊扳平，可逼出 WTK Sports 所指的次輪和局劇本。"},
            {"name": "保守零封", "scoreline": "0:0", "outcome": "draw", "confidence": 0.3,
             "basis": "兩隊均偏防守、突尼西亞攻擊乏力（場均約 0.6 球），不排除低比分悶平。"}
        ],
        "benchmarks": [
            {"source": "Opta 超級電腦", "kind": "model",
             "win_prob": {"home": 0.523, "draw": 0.25, "away": 0.227},
             "scoreline": "1:0",
             "note": "10,000 次模擬：瑞典 52.3%、和局 25%、突尼西亞 22.7%。"},
            {"source": "Kalshi 預測市場", "kind": "market",
             "win_prob": {"home": 0.51, "draw": 0.28, "away": 0.22},
             "scoreline": "1:0",
             "note": "Kalshi：瑞典 51-52%、和局 28%、突尼西亞 22%。"},
            {"source": "博彩隱含機率", "kind": "betting",
             "win_prob": {"home": 0.54, "draw": 0.25, "away": 0.21},
             "scoreline": "1:0",
             "note": "瑞典約 -116（≈54%）、突尼西亞約 +320；總分主推 2.5 球以下。"},
            {"source": "CupCastLab 模型", "kind": "model",
             "win_prob": {"home": 0.39, "draw": 0.31, "away": 0.3},
             "scoreline": "1:0",
             "note": "較保守模型給瑞典 39%、和 31%、突 30%，最可能比分仍為 1:0。"}
        ]
    },
    "reasoning": {
        "summary": "瑞典於蒙特雷 Estadio BBVA 迎戰突尼西亞，展開 F 組之旅（同組還有荷蘭、日本）。波特（Graham Potter）麾下的瑞典擁有伊薩克與約克雷斯兩大前鋒，約克雷斯在附加賽攻入 6 球中的 4 球（對烏克蘭帽子戲法、對波蘭 88 分鐘致勝球）且近 29 顆點球全進，火力為勝負關鍵；伊薩克則自骨折康復、料可上陣。後衛古德蒙松雖傳病情/傷情疑慮，但波特已表明他會出戰。突尼西亞（拉穆希執教）防守組織嚴密但攻擊乏力（近五場場均約 0.6 球）。Opta 超級電腦給瑞典 52.3% 勝率、突尼西亞僅 22.7%；Kalshi 與博彩亦一致看好瑞典小勝，市場普遍預期 2.5 球以下的低比分。綜合判斷瑞典憑火力與主動權拿下小勝，1:0 為最集中比分，2:0 緊隨其後。",
        "key_factors": [
            "球員狀態：約克雷斯狀態火熱（附加賽 6 球進 4、近 29 點球全進），伊薩克自腓骨骨折康復後回歸、料可披掛；雙箭頭組合為瑞典最大武器。",
            "傷停名單：瑞典後衛古德蒙松傳病情/傷勢疑慮但波特已確認其上陣，無確定缺陣；突尼西亞無重大傷停，拉穆希料可派近乎完整陣容。",
            "近期狀態/戰績：瑞典近五場 W2-D1-L2，附加賽連克烏克蘭、波蘭晉級；突尼西亞防守穩但攻擊鈍化，近五場場均僅約 0.6 球。",
            "戰術對位：瑞典以身體對抗、定位球與雙前鋒直接打法見長；突尼西亞（3-5-2／4-4-2）強調中場攔截（斯基里、漢尼拔）與低位防守，預料採守勢伺機反擊。",
            "主客場/場地：蒙特雷 Estadio BBVA 為中性場地、氣候炎熱，兩隊皆無主場優勢，但高溫或利於體能充沛一方。",
            "輿論共識：Opta（瑞 52.3%）、Kalshi（51-52%）與主流博彩（瑞典約 -116）一致看好瑞典小勝；LiveScore 主推瑞典 2:0、Sportsgambler 推 1:0，總分多偏 2.5 球以下；CupCastLab 為較保守的離群模型。"
        ],
        "consensus_lean": "home",
        "dissent": "少數派看法：CupCastLab 模型把三方機率拉近（瑞 39%／和 31%／突 30%），凸顯突尼西亞防守可能令比賽淪為膠著；FootballPredictions 甚至預測 2-2 高比分對攻，與主流的低比分共識相左。亦有觀點認為突尼西亞攻擊太鈍，恐連 1 球都難求，使悶平 0:0 成為另一風險。"
    },
    "sources": m12_sources,
    "source_count": len(m12_sources)
}

with open(f"{OUT_DIR}/match_11__2026-06-14T0551Z.json", "w", encoding="utf-8") as f:
    json.dump(m11, f, ensure_ascii=False, indent=2)
with open(f"{OUT_DIR}/match_12__2026-06-14T0551Z.json", "w", encoding="utf-8") as f:
    json.dump(m12, f, ensure_ascii=False, indent=2)

print("M11 source_count:", m11["source_count"], "scoreline:", m11["prediction"]["scoreline"], "outcome:", m11["prediction"]["outcome"])
print("M12 source_count:", m12["source_count"], "scoreline:", m12["prediction"]["scoreline"], "outcome:", m12["prediction"]["outcome"])
# win_prob sum checks
for m in (m11, m12):
    wp = m["prediction"]["win_prob"]
    print("win_prob sum", m["match"], round(wp["home"]+wp["draw"]+wp["away"],4))
    for b in m["prediction"]["benchmarks"]:
        s = b["win_prob"]["home"]+b["win_prob"]["draw"]+b["win_prob"]["away"]
        print("  bench", m["match"], b["source"], round(s,4))
