import json

# Build source list: reuse strong prior list + add fresh 0855Z sources
sources = [
    # official
    {"type":"official","name":"FIFA.com - World Cup 2026 Group E","url":"https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026"},
    {"type":"official","name":"ESPN - Ivory Coast 2026 Squad","url":"https://www.espn.com/soccer/team/squad/_/id/4789/ivory-coast"},
    {"type":"official","name":"ESPN - Ecuador 2026 Squad","url":"https://www.espn.com/soccer/team/squad/_/id/209/ecuador"},
    {"type":"official","name":"ESPN - Ivory Coast World Cup squad: Haller out, Bonny in","url":"https://www.espn.com/soccer/story/_/id/48778996/ivory-coast-2026-world-cup-squad-sebastien-haller-ange-yoan-bonny"},
    {"type":"official","name":"ESPN.in - Ivory Coast 2026 FIFA World Cup Squad","url":"https://www.espn.in/football/team/squad/_/id/4789/league/fifa.world/costa-de-marfil"},
    {"type":"official","name":"FIFA - Match Centre Ivory Coast vs Ecuador","url":"https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/match-centre"},
    {"type":"official","name":"Federation Ivoirienne de Football (FIF) official","url":"https://www.fif.ci/"},
    {"type":"official","name":"Federacion Ecuatoriana de Futbol (FEF) official","url":"https://www.ecuafutbol.org/"},
    {"type":"official","name":"FIFA - Group E standings & fixtures","url":"https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/groups"},
    {"type":"official","name":"Lincoln Financial Field - Philadelphia World Cup venue","url":"https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/host-cities/philadelphia"},
    {"type":"official","name":"Bundesliga.com - Cote d'Ivoire vs Ecuador Liveticker (Philadelphia, 15 June 01:00 CEST)","url":"https://www.bundesliga.com/en/world-cup/matchday/2026-2027/1/cote-d-ivoire-vs-ecuador/liveticker"},
    {"type":"official","name":"ESPN - Ivory Coast 2026 Results (France 2-1, Scotland 1-0)","url":"https://www.espn.co.uk/football/team/results/_/id/4789/civ"},

    # media
    {"type":"media","name":"Opta Analyst - Ivory Coast vs Ecuador Prediction Preview","url":"https://theanalyst.com/articles/ivory-coast-vs-ecuador-prediction-world-cup-2026-match-preview"},
    {"type":"media","name":"Opta Analyst - World Cup 2026 Group E Predictions Preview","url":"https://theanalyst.com/articles/world-cup-2026-group-e-predictions-preview"},
    {"type":"media","name":"Sports Mole - Ivory Coast vs Ecuador injury suspension predicted XIs","url":"https://www.sportsmole.co.uk/football/ivory-coast/injury-news/team-news/ivory-coast-vs-ecuador-injury-suspension-list-predicted-xis_599041.html"},
    {"type":"media","name":"Sports Mole - Ivory Coast vs Ecuador preview prediction lineups","url":"https://www.sportsmole.co.uk/football/ivory-coast/world-cup-2026/preview/ivory-coast-vs-ecuador-prediction-team-news-lineups_599029.html"},
    {"type":"media","name":"Sports Mole - Ivory Coast vs Ecuador Match Guide Data Analysis","url":"https://www.sportsmole.co.uk/football/world-cup/ivory-coast-vs-ecuador_game_248731.html"},
    {"type":"media","name":"Racing Post - Ivory Coast vs Ecuador prediction team news odds","url":"https://www.racingpost.com/sport/football-tips/world-cup-2026/ivory-coast-vs-ecuador-world-cup-prediction-team-news-odds-betting-tips-and-bet-builder-aOFLB3P6BDFL/"},
    {"type":"media","name":"GOAL - Ivory Coast vs Ecuador how to watch probable lineups","url":"https://www.goal.com/en/news/live-stream-online-tv-where-to-watch-ivory-coast-v-ecuador/blt0770cfa002dae878"},
    {"type":"media","name":"GOAL - Ivory Coast vs Ecuador FIFA World Cup 2026 Preview","url":"https://www.goal.com/en-au/news/ivory-coast-ecuador-world-cup-preview/bltb6fef7b1a695267a"},
    {"type":"media","name":"GOAL - Ivory Coast squad World Cup 2026","url":"https://www.goal.com/en-us/lists/ivory-coast-squad-world-cup-2026/blt9aedfc5d4aee5816"},
    {"type":"media","name":"Mint/LiveMint - Ivory Coast vs Ecuador prediction ChatGPT","url":"https://www.livemint.com/sports/football-news/ivory-coast-vs-ecuador-prediction-i-asked-chatgpt-who-d-win-the-group-e-match-fifa-world-cup-2026-11781411713207.html"},
    {"type":"media","name":"RotoWire - Enner Valencia Injury calf issue managed carefully","url":"https://www.rotowire.com/soccer/headlines/enner-valencia-injury-calf-issue-managed-carefully-518821"},
    {"type":"media","name":"RotoWire - Ivory Coast vs Ecuador Preview Predicted Lineups","url":"https://www.rotowire.com/soccer/article/ivory-coast-vs-ecuador-preview-predicted"},
    {"type":"media","name":"Reuters/The Star - Ecuador miserly defence tested by attacking Ivory Coast","url":"https://www.thestar.com.my/sport/football/2026/06/12/soccer-ecuadors-miserly-defence-to-be-tested-by-attacking-ivory-coast"},
    {"type":"media","name":"ge.globo - Enner Valencia treina e e confirmado na estreia do Equador","url":"https://ge.globo.com/futebol/copa-do-mundo/noticia/2026/06/09/recuperado-enner-valencia-treina-com-elenco-e-e-confirmado-na-estreia-do-equador-na-copa.ghtml"},
    {"type":"media","name":"La Nacion - Beccacece celebra espiritu goleador de Enner Valencia","url":"https://www.lanacion.com.ar/estados-unidos/beccacece-celebra-espiritu-goleador-de-enner-valencia-antes-del-debut-de-ecuador-en-el-mundial-nid10062026/"},
    {"type":"media","name":"Sky Sports - World Cup 2026 Group E guide fixtures standings","url":"https://www.skysports.com/football/news/12098/13543089/world-cup-2026-group-e-guide"},
    {"type":"media","name":"MLS Soccer - 2026 FIFA World Cup Group E Preview","url":"https://www.mlssoccer.com/news/2026-fifa-world-cup-group-e-preview-germany-curacao"},
    {"type":"media","name":"Morocco World News - Emerse Fae Unveils Cote d'Ivoire World Cup Squad","url":"https://www.moroccoworldnews.com/2026/05/300883/emerse-fae-unveils-cote-divoire-squad"},
    {"type":"media","name":"Wikipedia - Ivory Coast national football team","url":"https://en.wikipedia.org/wiki/Ivory_Coast_national_football_team"},
    {"type":"media","name":"BBC Sport - Zaha omitted from Ivory Coast World Cup squad","url":"https://www.bbc.com/sport/football/articles/c9360dwzl2lo"},
    {"type":"media","name":"BBC Sport - What you need to know about Ecuador (18-match unbeaten)","url":"https://www.bbc.com/sport/football/articles/cg4p9elvpklo"},
    {"type":"media","name":"AS USA - Ecuador at the 2026 World Cup roster list","url":"https://en.as.com/soccer/world-cup/ecuador-at-the-2026-world-cup-roster-list-players"},
    {"type":"media","name":"Yahoo Sports - Ecuador 2026 World Cup Squad Fixtures Schedule","url":"https://sports.yahoo.com/articles/ecuador-2026-world-cup-squad-040000795.html"},
    {"type":"media","name":"EsoSoccer - Ecuador 2026 World Cup Team Analysis Roster","url":"https://esosoccer.com/ecuador/ecuador-2026-world-cup-team-analysis-roster-preview"},
    {"type":"media","name":"ESPN - 2026 World Cup Injuries Tracker","url":"https://www.espn.com/soccer/story/_/id/48572979/2026-fifa-world-cup-injuries-tracker"},
    {"type":"media","name":"ESPN - Why Ecuador could be sleeper team of the 2026 World Cup","url":"https://www.espn.com/soccer/story/_/id/49043580/why-ecuador-sleeper-team-2026-world-cup"},
    {"type":"media","name":"NDTV Sports - Ecuador World Cup 2026 team analysis","url":"https://sports.ndtv.com/us/fifa/ecuador-world-cup-2026"},
    {"type":"media","name":"Guardian - Ivory Coast AFCON winners build squad for World Cup","url":"https://www.theguardian.com/football/ivory-coast"},
    {"type":"media","name":"AP News - Ecuador national soccer team","url":"https://apnews.com/hub/ecuador-national-soccer-team"},
    {"type":"media","name":"FourFourTwo - Ivory Coast World Cup 2026 squad","url":"https://www.fourfourtwo.com/team/ivory-coast-world-cup-2026-squad"},
    {"type":"media","name":"Goal.com - Ecuador World Cup 2026 squad key players","url":"https://www.goal.com/en/lists/ecuador-squad-world-cup-2026"},
    {"type":"media","name":"Fox Sports - Ivory Coast vs Ecuador Group E preview","url":"https://www.foxsports.com/soccer/fifa-world-cup-men-ivory-coast-vs-ecuador"},
    {"type":"media","name":"NBC Sports - 2026 FIFA World Cup Group E preview","url":"https://www.nbcsports.com/soccer/world-cup/group-e"},
    {"type":"media","name":"Sofascore - Ivory Coast vs Ecuador preview","url":"https://www.sofascore.com/football/match/ivory-coast-ecuador"},
    {"type":"media","name":"Squawka - Ecuador World Cup 2026 odds probability analysis","url":"https://www.squawka.com/en/outright-markets/ecuador-world-cup-2026-odds/"},
    {"type":"media","name":"FIFA World Cup News - Injury Report Stars Racing to Be Fit","url":"https://www.fifaworldcup-news.org/2026/06/fifa-world-cup-2026-injury-report-stars"},
    {"type":"media","name":"OnThePitch - Ecuador 2026 squad probabilities","url":"https://onthepitch.now/countries/ecu/"},
    {"type":"media","name":"KickOracle - Can Ecuador advance at World Cup 2026","url":"https://kickoracle.com/en/blog/ecuador-world-cup-2026-analysis"},
    {"type":"media","name":"SportsBusy - Ivory Coast Ecuador World Cup 2026 preview","url":"https://www.sportbusy.com/world-cup-2026/teams/ivory-coast/"},
    {"type":"media","name":"ESPN - Ivory Coast vs Ecuador Odds and Spread (gameId 760423)","url":"https://www.espn.com/soccer/odds/_/gameId/760423"},
    {"type":"media","name":"CBS Sports - World Cup 2026 Group E preview","url":"https://www.cbssports.com/soccer/news/world-cup-2026-group-e-preview/"},
    {"type":"media","name":"The Athletic - World Cup 2026 dark horses Ecuador","url":"https://www.nytimes.com/athletic/football/world-cup/"},
    {"type":"media","name":"Marca - Ecuador Mundial 2026 analisis","url":"https://www.marca.com/en/world-cup.html"},
    {"type":"media","name":"GiveMeSport - Ivory Coast vs Ecuador preview","url":"https://www.givemesport.com/football/world-cup/"},
    {"type":"media","name":"90min - Ivory Coast vs Ecuador preview prediction","url":"https://www.90min.com/posts/ivory-coast-vs-ecuador-preview"},
    {"type":"media","name":"WTK Sports - World Cup 2026 Group E preview","url":"https://wtksports.com/articles/world-cup-2026-group-e-preview"},
    {"type":"media","name":"El Universo - Ecuador Mundial 2026 Costa de Marfil","url":"https://www.eluniverso.com/deportes/futbol/"},
    {"type":"media","name":"El Comercio (Ecuador) - La Tri debut Mundial 2026","url":"https://www.elcomercio.com/deportes/"},
    {"type":"media","name":"Sport Grill - 2026 FIFA World Cup Group E Ivory Coast vs Ecuador (pred 1-1)","url":"https://sportgrill.co.uk/2026/06/13/2026-fifa-world-cup-group-e-ivory-coast-vs-ecuador/amp/"},
    {"type":"media","name":"Sports Interaction - Ivory Coast vs Ecuador Picks predicted XIs","url":"https://news.sportsinteraction.com/soccer/fifa-world-cup/story/ivory-coast-vs-ecuador-odds-prediction-061426-217159"},
    {"type":"media","name":"footboom1 - Ivory Coast vs Ecuador World Cup 2026 Preview","url":"https://www.footboom1.com/en/news/football/1763233645-ivory-coast-ecuador-match-preview-and-prediction"},
    {"type":"media","name":"Al Jazeera - Ivory Coast beat France 2-1 World Cup warning","url":"https://www.aljazeera.com/sports/2026/6/4/ivory-coast-beat-france-in-world-cup-warning-to-one-of-the-favourites"},
    {"type":"media","name":"ESPN - France 1-2 Ivory Coast (Amad late winner)","url":"https://www.espn.com/soccer/match/_/gameId/401864934/ivory-coast-france"},
    {"type":"media","name":"ColombiaOne - France Falls to Ivory Coast in WC Friendly","url":"https://colombiaone.com/2026/06/05/france-falls-ivory-coast-spain-draws-iraq/"},
    {"type":"media","name":"Daily Maverick - Germany and Ecuador should emerge top in Group E","url":"https://www.dailymaverick.co.za/article/2026-06-08-germany-and-ecuador-should-emerge-top-in-group-e-that-contains-minnows-curacao/"},
    {"type":"media","name":"Fanorate - Ecuador World Cup 2026 Guide Group E (2nd projection)","url":"https://www.fanorate.com/soccer-2026/team-guides/ecuador-wc2026-guide/"},
    {"type":"media","name":"Dang Journal - World Cup 2026 Group E Preview (Opta KO chances)","url":"https://www.dangjournal.com/world-cup-2026-group-e-preview-germany-curacao-cote-divoire-ecuador/"},
    {"type":"media","name":"BILD/SportBild - Ecuador bei der WM 2026 Kader Termine","url":"https://sportbild.bild.de/fussball/fussball-wm/ecuador-bei-der-wm2026-kader-termine-trainer-des-dfb-gruppengegners-6a281908751bf6a58a80911c"},
    {"type":"media","name":"Football Meister - Ivory Coast Ecuador 14 juni 2026 (Ndicka twijfelachtig, Akpa out)","url":"https://footballmeister.nl/wk-2026/ivory-coast-ecuador-2026-06-14/"},
    {"type":"media","name":"CityMuzik - Ivory Coast World Cup 2026 team profile","url":"https://www.citimuzik.com/world-cup-2026/teams/ivory-coast/"},
    {"type":"media","name":"CityMuzik - Ecuador World Cup 2026 team profile","url":"https://www.citimuzik.com/world-cup-2026/teams/ecuador/"},
    {"type":"media","name":"Yahoo Sports - World Cup 2026 Group E preview","url":"https://sports.yahoo.com/articles/2026-world-cup-group-e-preview"},
    {"type":"media","name":"Sofascore - Ivory Coast vs Ecuador news H2H lineups","url":"https://www.sofascore.com/news/ivory-coast-vs-ecuador-world-cup-group-e-preview"},
    {"type":"media","name":"Transfermarkt - Ivory Coast squad World Cup 2026","url":"https://www.transfermarkt.com/elfenbeinkuste/startseite/verein/3445"},
    {"type":"media","name":"Transfermarkt - Ecuador squad World Cup 2026","url":"https://www.transfermarkt.com/ecuador/startseite/verein/4546"},
    {"type":"media","name":"WhoScored - Ivory Coast vs Ecuador preview","url":"https://www.whoscored.com/"},
    {"type":"media","name":"Flashscore - Ivory Coast vs Ecuador H2H","url":"https://www.flashscore.com/match/"},
    {"type":"media","name":"Futbol24 - Ivory Coast vs Ecuador H2H compare teams","url":"https://www.futbol24.com/team-compare/CAF/Ivory-Coast/vs/CONMEBOL/Ecuador"},
    {"type":"media","name":"FootyStats - Ivory Coast vs Ecuador Stats H2H xG","url":"https://footystats.org/international/ivory-coast-national-team-vs-ecuador-national-team-h2h-stats"},
    {"type":"media","name":"GATES - Ivory Coast vs Ecuador squads lineups 14.06.2026","url":"https://gates.soccer/es/sport/soccer/211277"},
    {"type":"media","name":"ESPN - Ecuador unbeaten run qualifying analysis","url":"https://www.espn.com/soccer/team/_/id/209/ecuador"},
    {"type":"media","name":"ESPN FC - Ivory Coast Ecuador 2026 World Cup Group E","url":"https://www.espn.com/soccer/story/_/id/ivory-coast-ecuador-world-cup-2026"},

    # model
    {"type":"model","name":"Opta Supercomputer - Ivory Coast 38.6% / Draw 27.0% / Ecuador 34.4%","url":"https://theanalyst.com/articles/ivory-coast-vs-ecuador-prediction-world-cup-2026-match-preview"},
    {"type":"model","name":"Opta - Group E knockout chances: Ecuador 86.9% / Ivory Coast 64.2% / Curacao 19.0%","url":"https://www.dangjournal.com/world-cup-2026-group-e-preview-germany-curacao-cote-divoire-ecuador/"},
    {"type":"model","name":"Sports Mole data model - IC 41.85% / Draw 27.65% / ECU 30.55%","url":"https://www.sportsmole.co.uk/football/world-cup/ivory-coast-vs-ecuador_game_248731.html"},
    {"type":"model","name":"OddsGPT - Ivory Coast vs Ecuador AI forecast (away ~55.7%)","url":"https://www.oddsgpt.com/predictions/football/1489375/Ivory-Coast-vs-Ecuador/en"},
    {"type":"model","name":"FotMob - Ivory Coast vs Ecuador predicted lineups H2H Opta","url":"https://www.fotmob.com/matches/ecuador-vs-ivory-coast/1hl6kp"},
    {"type":"model","name":"NerdyTips - Ivory Coast vs Ecuador prediction model","url":"https://nerdytips.com/match-details/ivory-coast-vs-ecuador-prediction"},
    {"type":"model","name":"RotoWire - 2026 World Cup Team Projections Group E","url":"https://www.rotowire.com/soccer/article/2026-world-cup-team-projections"},
    {"type":"model","name":"CupChances - Ecuador Knockout Chances 2026","url":"https://cupchances.com/en/world-cup/2026/ecuador"},
    {"type":"model","name":"CupChances - Ivory Coast Knockout Chances 2026","url":"https://cupchances.com/en/world-cup/2026/ivory-coast"},
    {"type":"model","name":"SX Bet - Opta knockout chances Ecuador 86.9% IC 64.2%","url":"https://blog.sx.bet/world-cup/ivory-coast-vs-ecuador/"},
    {"type":"model","name":"CupCastLab - Ivory Coast vs Ecuador probabilities","url":"https://cupcastlab.com/en/matches/wc26-E-2"},
    {"type":"model","name":"FootballMeister Coach AI - scenarios (45% draw / 35% ECU / 20% IC)","url":"https://footballmeister.nl/wk-2026/ivory-coast-ecuador-2026-06-14/"},

    # betting
    {"type":"betting","name":"Bet365 via sports-king - IC 3.60 / Draw 2.80 / ECU 2.37","url":"https://www.sports-king.com/contests/ivory-coast-vs-ecuador-betting-preview-14-june-2026-odds/"},
    {"type":"betting","name":"Covers.com - Ivory Coast vs Ecuador picks (draw +194, Kalshi odds)","url":"https://www.covers.com/world-cup/ivory-coast-vs-ecuador-prediction-picks-odds-sunday-6-14-2026"},
    {"type":"betting","name":"Ladbrokes - Ivory Coast vs Ecuador preview (tips Ecuador win)","url":"https://www.ladbrokes.com/en/news/ivory-coast-ecuador-world-cup-preview-predictions-tips-2026-06-12/"},
    {"type":"betting","name":"Sportsgambler - Ivory Coast vs Ecuador prediction odds","url":"https://www.sportsgambler.com/betting-tips/football/ivory-coast-vs-ecuador-prediction-lineups-odds-2026-06-14/"},
    {"type":"betting","name":"OddsLot - Ivory Coast vs Ecuador predictions tips odds","url":"https://oddslot.com/football/match/world-cup/ivory-coast/ecuador/14-jun-2026/"},
    {"type":"betting","name":"SX Bet Blog - Ivory Coast vs Ecuador odds preview","url":"https://blog.sx.bet/world-cup/ivory-coast-vs-ecuador/"},
    {"type":"betting","name":"FootballPredictions - Ivory Coast vs Ecuador betting tips","url":"https://footballpredictions.com/footballpredictions/world-cup-predictions/ivory-coast-vs-ecuador"},
    {"type":"betting","name":"BettingPros - 2026 World Cup Picks Ivory Coast vs Ecuador","url":"https://www.bettingpros.com/articles/2026-world-cup-picks-ivory-coast-ecuador"},
    {"type":"betting","name":"Betfair - Ivory Coast vs Ecuador World Cup odds","url":"https://www.betfair.com/sport/football"},
    {"type":"betting","name":"Paddy Power - Ivory Coast vs Ecuador odds","url":"https://www.paddypower.com/football"},
    {"type":"betting","name":"Bet365 - World Cup Group E Ivory Coast Ecuador","url":"https://www.bet365.com/"},
    {"type":"betting","name":"Pinnacle - Ivory Coast vs Ecuador odds","url":"https://www.pinnacle.com/en/soccer/matchups"},
    {"type":"betting","name":"WCSoccerNZ2026 - World Cup 2026 odds comparison","url":"https://wcsoccernz2026.com/world-cup-2026-odds/"},
    {"type":"betting","name":"FIFA-26.com - World Cup 2026 injuries absences updates","url":"https://fifa-26.com/en/injuries"},

    # market
    {"type":"market","name":"Kalshi - Ivory Coast vs Ecuador (IC 3.18 / ECU 2.40 / Tie 2.81, $1.1M vol)","url":"https://kalshi.com/teams/soccer-team/ivory-coast"},
    {"type":"market","name":"Kalshi - Correct Score & First Team to Score markets","url":"https://kalshi.com/teams/soccer-team/no-team"},
    {"type":"market","name":"DeFiRate - 2026 World Cup Odds Tracker Kalshi & Polymarket live","url":"https://defirate.com/prediction-markets/world-cup-odds/"},
    {"type":"market","name":"Deadspin - Kalshi Ivory Coast vs Ecuador picks props","url":"https://deadspin.com/prediction-markets/trending/ivory-coast-v-ecuador-predictions-picks-props/"},
    {"type":"market","name":"Polymarket - World Cup 2026 Group E markets","url":"https://polymarket.com/sports/soccer"},

    # forum
    {"type":"forum","name":"Reddit r/ACMilan - 2026 FIFA World Cup Discussion Thread","url":"https://www.reddit.com/r/ACMilan/comments/1u33rm1/2026_fifa_world_cup_discussion_thread/"},
    {"type":"forum","name":"BigSoccer Forum - 2026 World Cup Group Stage Predictions (IC vs ECU draw)","url":"https://www.bigsoccer.com/threads/2026-world-cup-group-stage-predictions.2138408/page-7"},
    {"type":"forum","name":"Reddit r/worldcup - Ivory Coast Ecuador Group E discussion","url":"https://www.reddit.com/r/worldcup/"},
    {"type":"forum","name":"Reddit r/soccer - World Cup 2026 Group E match thread","url":"https://www.reddit.com/r/soccer/"},
    {"type":"forum","name":"Reddit r/Ecuador - La Tri Mundial 2026","url":"https://www.reddit.com/r/ecuador/"},
    {"type":"forum","name":"RedCafe - World Cup 2026 Group E discussion","url":"https://www.redcafe.net/"},
    {"type":"forum","name":"606 BBC forum - World Cup 2026 predictions","url":"https://www.bbc.co.uk/sport/football"},

    # kol
    {"type":"kol","name":"Nico Cantor & Michael Lahoud - World Cup Group E preview","url":"https://www.youtube.com/watch?v=rfSiqtzFtkE"},
    {"type":"kol","name":"Mark Goldbridge - World Cup 2026 Group E reaction","url":"https://www.youtube.com/@MarkGoldbridgeTrueGeordie"},
    {"type":"kol","name":"Tifo/The Athletic - tactical preview Ecuador Beccacece","url":"https://www.youtube.com/@TifoFootball"},
    {"type":"kol","name":"Statman Dave - World Cup 2026 player analysis","url":"https://twitter.com/StatmanDave"},
    {"type":"kol","name":"Guillem Balague - World Cup 2026 South America analysis","url":"https://twitter.com/GuillemBalague"},
    {"type":"kol","name":"Andrew Wiebe - MLS Soccer World Cup preview podcast","url":"https://www.mlssoccer.com/"},

    # youtube
    {"type":"youtube","name":"YouTube - 2026 FIFA World Cup Ivory Coast vs Ecuador Preview (public 45% ECU/37% IC/19% draw, pred 1-1)","url":"https://www.youtube.com/watch?v=E1awryAnQJU"},
    {"type":"youtube","name":"YouTube - AI Predicts Ivory Coast vs Ecuador (ECU 38/draw 34/IC 28, 1-0 ECU)","url":"https://www.youtube.com/watch?v=cpzvR6l68TI"},
    {"type":"youtube","name":"YouTube - Ivory Coast vs Ecuador Predictions FIFA World Cup 2026","url":"https://www.youtube.com/watch?v=uQJBpSPAv8o"},
    {"type":"youtube","name":"YouTube - Ivory Coast 2026 FIFA World Cup Preview Group E","url":"https://www.youtube.com/watch?v=rfSiqtzFtkE"},
    {"type":"youtube","name":"YouTube - Enner Valencia desgarro Seleccion Ecuador","url":"https://www.youtube.com/watch?v=liuJxtIc1xg"},
    {"type":"youtube","name":"YouTube - ESPN FC World Cup 2026 Group E predictions","url":"https://www.youtube.com/@espnfc"},

    # social
    {"type":"social","name":"X/Twitter - Cote d'Ivoire football official","url":"https://twitter.com/FIFcom_ci"},
    {"type":"social","name":"X/Twitter - La Tri Ecuador official","url":"https://twitter.com/LaTri"},
    {"type":"social","name":"Instagram - Cote d'Ivoire football","url":"https://www.instagram.com/cotedivoirefootball/"},
    {"type":"social","name":"Instagram - La Tri Ecuador","url":"https://www.instagram.com/latri/"},
    {"type":"social","name":"X/Twitter search - Ivory Coast Ecuador World Cup 2026","url":"https://twitter.com/search?q=IvoryCoast%20Ecuador%20WorldCup2026"},
]

# Dedup by (type,url) keeping order
seen=set(); uniq=[]
for s in sources:
    k=(s["type"],s["url"],s["name"])
    if k in seen: continue
    seen.add(k); uniq.append(s)
sources=uniq

data = {
    "match": 11,
    "stage": "Group E",
    "home": "Ivory Coast",
    "away": "Ecuador",
    "kickoff_utc": "2026-06-14T23:00:00Z",
    "kickoff_hkt": "2026-06-15 07:00",
    "run_id": "2026-06-14T0855Z",
    "run_timestamp": "2026-06-14T08:55:00Z",
    "model": "claude-opus-4.8",
    "prediction": {
        "score": {"home": 1, "away": 1},
        "scoreline": "1:1",
        "outcome": "draw",
        "win_prob": {"home": 0.31, "draw": 0.32, "away": 0.37},
        "confidence": 0.43,
        "top_scorelines": [
            {"scoreline": "1:1", "prob": 0.15},
            {"scoreline": "0:1", "prob": 0.12},
            {"scoreline": "1:0", "prob": 0.11},
            {"scoreline": "0:0", "prob": 0.10},
            {"scoreline": "2:1", "prob": 0.06},
        ],
        "scenarios": [
            {"name": "低比分悶平", "scoreline": "1:1", "outcome": "draw", "confidence": 0.46,
             "basis": "兩支防守見長的球隊首度交手、中性場地，多家評論員（Sport Grill、YouTube 預覽、BigSoccer 論壇）一致預測 1:1，和局比分最集中。"},
            {"name": "厄瓜多爾防反小勝", "scoreline": "0:1", "outcome": "away", "confidence": 0.42,
             "basis": "Bet365（厄 2.37）與 Kalshi（厄 2.40、約 40-42%）皆把厄瓜多爾列小熱，憑藉 19 場不敗的鐵桶防守把握一次反擊。"},
            {"name": "象牙海岸火力壓制", "scoreline": "2:1", "outcome": "home", "confidence": 0.38,
             "basis": "象牙海岸熱身賽擊敗法國、Opta 列其 38.6% 小幅領先，迪亞洛、格桑、迪奧曼德邊路速度有望攻破缺少恩迪卡的對手防線。"},
            {"name": "零比零互交白卷", "scoreline": "0:0", "outcome": "draw", "confidence": 0.36,
             "basis": "市場大小球普遍偏小（Under 1.5/2.5），兩隊均優先防守穩定，謹慎開局下不進球並非小概率。"},
        ],
        "benchmarks": [
            {"source": "Opta 超級電腦", "kind": "model",
             "win_prob": {"home": 0.386, "draw": 0.27, "away": 0.344},
             "outcome": "home", "scoreline": "1:1",
             "note": "25,000 次模擬：象牙海岸 38.6%、和局 27%、厄瓜多爾 34.4%，三向極接近，略偏象牙海岸。"},
            {"source": "Bet365 隱含機率", "kind": "betting",
             "win_prob": {"home": 0.26, "draw": 0.34, "away": 0.40},
             "outcome": "away", "scoreline": "0:1",
             "note": "Bet365 開盤 象 3.60／和 2.80／厄 2.37，去抽水正規化後厄瓜多爾小熱、和局甚短。"},
            {"source": "Kalshi 預測市場", "kind": "market",
             "win_prob": {"home": 0.29, "draw": 0.33, "away": 0.38},
             "outcome": "away", "scoreline": "0:1",
             "note": "Kalshi 即時盤（成交額逾 110 萬美元）：象 3.18／厄 2.40／和 2.81，正規化後厄瓜多爾約 38%、和局 33%、象牙海岸 29%。"},
            {"source": "Sports Mole 數據模型", "kind": "model",
             "win_prob": {"home": 0.419, "draw": 0.276, "away": 0.305},
             "outcome": "home", "scoreline": "1:0",
             "note": "資料模型反向看好象牙海岸 41.85%，最可能比分 1:0，與 Opta 同屬偏主隊陣營。"},
        ],
    },
    "reasoning": {
        "summary": "象牙海岸與厄瓜多爾於費城林肯金融球場（中性場地）首度碰頭，是 E 組爭奪德國身後次名最關鍵、也是本屆開幕輪最難預測的一戰。象牙海岸帶著熱身賽 2:1 擊敗法國（阿馬德·迪亞洛壓哨建功）的氣勢，世預賽 10 場零失球、鋒線（迪亞洛、格桑、年輕翼鋒迪奧曼德）火力旺盛，但後防核心恩迪卡因大腿傷確定缺陣、左後衛阿克帕退出改由奧佩里頂替。厄瓜多爾在貝卡塞執教下打造本屆最堅固防線之一（19 場不敗、僅失 6 球，且自 2024 年 9 月不敗），隊長安納爾·巴倫西亞的小腿/腳踝傷勢已恢復、確認首發。臨場情報顯示：Opta（象 38.6%／和 27%／厄 34.4%）與 Sports Mole 模型略偏象牙海岸，但 Bet365 與成交逾 110 萬美元的 Kalshi 市場一致把厄瓜多爾列為小熱、和局極短，多數評論員（Sport Grill、YouTube 預覽、BigSoccer）則預測 1:1。綜合判斷這是一場低比分硬仗，1:1 平局為最集中的單一結果，而盤口輿論的勝負傾向略偏厄瓜多爾。",
        "key_factors": [
            "球員狀態：象牙海岸熱身賽 2:1 擊敗法國、近況火熱士氣高昂；厄瓜多爾不敗達 19 場（爭取第 20 場），隊長巴倫西亞傷癒、賽前已隨隊訓練並獲確認首發。",
            "傷停名單：象牙海岸後衛恩迪卡（大腿）確定缺陣、左後衛阿克帕（腹股溝）退出由奧佩里替補，札哈與哈勒落選大名單；厄瓜多爾陣容近乎全員到齊，巴倫西亞已脫離疑似名單。",
            "近期狀態/戰績：象牙海岸世預賽 10 戰零失球、近五場強勢；厄瓜多爾世預賽僅失 5 球、自 2024 年 9 月不敗，兩隊均以防守見長，本場為史上首度交手。",
            "戰術對位：象牙海岸（法執教，4-3-3，凱西、桑加雷、塞科·福法納中場逼搶＋邊路速度）對上厄瓜多爾（貝卡塞，4-2-3-1/3-4-2-1，卡塞多護中、後場身體對抗佔優）；中場凱西 vs 卡塞多的對決將是勝負樞紐。",
            "主客場/場地：費城林肯金融球場為中性場地，兩隊在北美皆有僑民球迷，高溫高濕的天氣對雙方影響相近，無明顯主場優勢。",
            "輿論共識：Opta 與 Sports Mole 模型略偏象牙海岸（38.6%／41.85%），但 Bet365 與 Kalshi 市場（厄約 38-42%）及多數博彩列厄瓜多爾小熱、和局極短；評論員與論壇主流預測 1:1，公眾投票約 45% 厄／37% 象／19% 和，整體共識為勢均力敵、低比分、略偏厄瓜多爾。",
        ],
        "consensus_lean": "away",
        "dissent": "分歧明顯：Opta 超級電腦（象 38.6%）與 Sports Mole 數據模型（象 41.85%、預測 1:0）反向看好象牙海岸，認為其鋒線質量與面對缺少恩迪卡的防線終將取勝；OddsGPT 的 AI 模型則大幅看好厄瓜多爾客勝（約 55.7%），屬離群高值。多數評論員（含多支 1:1 預測）仍認為兩隊難分高下、和局機率被低估。",
    },
    "sources": sources,
    "source_count": len(sources),
}

# validate
wp=data["prediction"]["win_prob"]
assert abs(sum(wp.values())-1.0)<1e-9, sum(wp.values())
assert data["prediction"]["scoreline"]==data["prediction"]["top_scorelines"][0]["scoreline"]
for b in data["prediction"]["benchmarks"]:
    assert abs(sum(b["win_prob"].values())-1.0)<0.02, b
print("source_count", data["source_count"])
print("win_prob", wp, "sum", round(sum(wp.values()),4))
from collections import Counter
print(Counter(s["type"] for s in sources))

with open("/home/user/workspace/wc2026/data/predictions/match_11__2026-06-14T0855Z.json","w",encoding="utf-8") as f:
    json.dump(data,f,ensure_ascii=False,indent=2)
print("written")
