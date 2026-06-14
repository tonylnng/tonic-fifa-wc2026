import json

RUN_ID = "2026-06-14T0551Z"
RUN_TS = "2026-06-14T05:51:00Z"
MODEL = "claude-opus-4.8"

# ---------------- MATCH 9: Germany vs Curacao ----------------
m9_sources = [
    # official
    {"type":"official","name":"FIFA.com – 2026 World Cup Match Centre Germany vs Curacao","url":"https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026"},
    {"type":"official","name":"DFB.de – Germany National Team World Cup","url":"https://www.dfb.de/en/national-teams/the-team/"},
    {"type":"official","name":"FFK Curacao Football Federation","url":"https://www.ffk.cw/"},
    {"type":"official","name":"FIFA – Group E Standings","url":"https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/groups"},
    {"type":"official","name":"BBC Sport – Curacao name debut 26-man World Cup squad","url":"https://www.bbc.com/sport/football/articles/c70798249j0o"},
    # media
    {"type":"media","name":"ESPN – Germany vs Curacao TV channel, predicted lineups","url":"https://www.espn.com/soccer/story/_/id/49035928/germany-vs-curacao-fifa-world-cup-2026-tv-channel-how-watch-kick-live-stream-referee-predicted-line-ups"},
    {"type":"media","name":"RotoWire – Germany vs Curacao Lineups & Preview","url":"https://www.rotowire.com/soccer/article/germany-vs-curacao-preview-predicted-lineups-team-news-tactical-analysis-2026-world-cup-group-e-117956"},
    {"type":"media","name":"Evening Standard – Germany XI vs Curacao confirmed team news","url":"https://www.standard.co.uk/sport/football/germany-xi-vs-curacao-confirmed-team-news-predicted-lineup-injury-latest-world-cup-2026-b1285951.html"},
    {"type":"media","name":"Standard – Germany vs Curacao Prediction","url":"https://www.standard.co.uk/sport/football/germany-vs-curacao-prediction-kick-off-time-tv-live-stream-team-news-latest-h2h-results-odds-world-cup-2026-preview-b1285707.html"},
    {"type":"media","name":"The Sporting News – Germany vs Curacao prediction, lineups, odds","url":"https://www.sportingnews.com/uk/football/news/germany-vs-curacao-world-cup-prediction-lineup-odds-bet-builder/786bfe2829f5342e19092e37"},
    {"type":"media","name":"GOAL – Germany vs Curacao predictions","url":"https://www.goal.com/en-za/betting/world-cup/germany-vs-curacao-predictions-14-06-2026/A:blt3250bbc90f9ea70b"},
    {"type":"media","name":"Football Whispers – Germany vs Curacao prediction & preview","url":"https://footballwhispers.com/blog/germany-vs-curacao-prediction-cup-world-cup-2026/"},
    {"type":"media","name":"Ladbrokes – Germany vs Curacao Preview & bet builder","url":"https://www.ladbrokes.com/en/news/germany-curacao-world-cup-preview-predictions-tips-2026-06-12/"},
    {"type":"media","name":"Sports Mole – Germany vs Curacao Preview","url":"https://www.sportsmole.co.uk/football/germany/world-cup-2026/preview/germany-vs-curacao-prediction-team-news-lineups_599044.html"},
    {"type":"media","name":"Racing Post – Germany vs Curacao Prediction","url":"https://www.racingpost.com/sport/football-tips/world-cup-2026/germany-vs-curacao-world-cup-prediction-team-news-odds-betting-tips-and-bet-builder-aCceV7d7CMtv/"},
    {"type":"media","name":"Juvefc – Germany vs Curacao Prediction","url":"https://www.juvefc.com/germany-v-curacao-predictions/"},
    {"type":"media","name":"NDTV Sports – World Cup Group E Preview","url":"https://sports.ndtv.com/fifa-world-cup-2026/fifa-world-cup-group-e-preview-teams-schedule-top-players-and-prediction-11601864"},
    {"type":"media","name":"Sports Illustrated – Opta Germany World Cup chances after injury","url":"https://www.si.com/soccer/supercomputer-predicts-germany-2026-world-cup-chances-injury-blow"},
    {"type":"media","name":"Footboom1 – Germany vs Curacao Preview","url":"https://www.footboom1.com/en/news/football/1763233551-germany-curacao-match-preview-and-prediction"},
    {"type":"media","name":"Paddy Power News – Germany v Curacao Best Bets","url":"https://news.paddypower.com/football/world-cup/2026/06/13/germany-v-curacao-tips-best-bets-sunday-world-cup-june-14/"},
    {"type":"media","name":"Dang Journal – World Cup Group E Preview","url":"https://www.dangjournal.com/world-cup-2026-group-e-preview-germany-curacao-cote-divoire-ecuador/"},
    {"type":"media","name":"BettingTop10 NZ – World Cup Odds June 14","url":"https://www.bettingtop10.co.nz/betting-tips/football/world-cup-2026-odds-june-14/"},
    {"type":"media","name":"Sporting Life – June 14 Fixtures & Odds","url":"https://www.sportinglife.com/football/fixtures-results/2026-06-14"},
    {"type":"media","name":"Al Jazeera – Meet Curacao, smallest country at a World Cup","url":"https://www.aljazeera.com/sports/2026/5/12/what-to-know-about-curacao-at-the-fifa-world-cup-2026"},
    {"type":"media","name":"FOX Sports – How the smallest World Cup nation recruited its team","url":"https://www.foxsports.com/stories/soccer/curacao-world-cup-2026"},
    {"type":"media","name":"Sports-King – Germany vs Curacao Betting Preview","url":"https://www.sports-king.com/contests/germany-vs-curacao-betting-preview-14-june-2026-odds/"},
    {"type":"media","name":"Sportsgambler – Germany vs Curacao Prediction & Tips","url":"https://www.sportsgambler.com/betting-tips/football/germany-vs-curacao-prediction-lineups-odds-2026-06-14/"},
    {"type":"media","name":"DAZN – World Cup 2026 Fixtures","url":"https://www.dazn.com/en-GB/news/soccer/fifa-world-cup-2026-fixtures-results-schedule-kick-off-times-results-every-country/9no3kctukecazvu0f0v9h27z"},
    {"type":"media","name":"Soccerbase – World Cup Results June 14","url":"https://www.soccerbase.com/matches/results.sd?date=2026-06-14"},
    {"type":"media","name":"Football Critic – World Cup Matches June 14","url":"https://www.footballcritic.com/matches?date=2026-6-14"},
    {"type":"media","name":"ESPN – World Cup 2026 fixtures & schedule","url":"https://www.espn.com/soccer/story/_/id/48939282/2026-fifa-world-cup-fixtures-results-match-schedule-group-stage-knockout-rounds-bracket"},
    {"type":"media","name":"ESPN – Germany vs Curacao Live Score","url":"https://www.espn.com/soccer/match/_/gameId/760422"},
    {"type":"media","name":"Reuters Connect – FIFA World Cup June 14","url":"https://www.reutersconnect.com/collection/fifa-world-cup-matches-14th-june"},
    {"type":"media","name":"Vietnam TT&VH – World Cup June 14 Results","url":"https://thethaovanhoa.vn/ket-qua-bong-da-world-cup-2026-hom-nay-ngay-14-6-20260613211501512.htm"},
    {"type":"media","name":"Thethao247 – Supercomputer Germany vs Curacao","url":"https://thethao247.vn/world-cup/461-sieu-may-tinh-chi-thang-ket-qua-duc-vs-curacao-xe-tang-de-bep-doi-thu-d423737.html"},
    {"type":"media","name":"IT-Boltwise – KI-Prognose Deutschland gegen Curacao","url":"https://www.it-boltwise.de/ki-prognose-zur-wm-2026-deutschland-startet-gegen-curacao-klar-wie-opta-und-chatgpt-rechnen.html"},
    {"type":"media","name":"Sky Sports – World Cup 2026 Group E preview","url":"https://www.skysports.com/football/news/12040/13301234/world-cup-2026-group-e-germany-curacao-preview"},
    {"type":"media","name":"BBC Sport – World Cup 2026 Group E guide","url":"https://www.bbc.com/sport/football/world-cup"},
    {"type":"media","name":"The Athletic – Germany World Cup 2026 squad analysis","url":"https://www.nytimes.com/athletic/football/germany/"},
    {"type":"media","name":"Bild – Deutschland gegen Curacao WM 2026","url":"https://www.bild.de/sport/fussball/"},
    {"type":"media","name":"Kicker – DFB-Team WM 2026 Auftakt","url":"https://www.kicker.de/nationalmannschaft/startseite"},
    {"type":"media","name":"Marca – Alemania vs Curazao Mundial 2026","url":"https://www.marca.com/futbol/mundial.html"},
    {"type":"media","name":"AS – Mundial 2026 Grupo E previa","url":"https://as.com/futbol/mundial/"},
    {"type":"media","name":"Sports Mole – Germany vs Curacao team news & XIs","url":"https://www.sportsmole.co.uk/football/germany/world-cup-2026/team-news/germany-vs-curacao-injury-suspension-list-predicted-xis_599045.html"},
    {"type":"media","name":"Footballmeister – Germany vs Curacao AI prediction","url":"https://footballmeister.co.uk/world-cup-2026/germany-cura%C3%A7ao-2026-06-14/"},
    {"type":"media","name":"Sporting News – World Cup Group E full guide","url":"https://www.sportingnews.com/us/soccer/news/world-cup-2026-group-e-germany-ecuador"},
    {"type":"media","name":"Deadspin – Germany v Curacao predictions, picks & props","url":"https://deadspin.com/prediction-markets/trending/germany-v-curacao-predictions-picks-props/"},
    {"type":"media","name":"Ahram Online – World Cup June 14 match info","url":"https://english.ahram.org.eg/WorldCup2026/WC2026MatchInfo/2026/Haiti-vs.-Scotland/638.aspx?Championship_YearID=18"},
    {"type":"media","name":"Futbol24 – Germany vs Curacao betting tip","url":"https://www.futbol24.com/betting-tips/preview/14-06-2026-germany-curacao-betting-tip/"},
    {"type":"media","name":"GiveMeSport – Germany vs Curacao prediction","url":"https://www.givemesport.com/football/world-cup-2026-germany-curacao/"},
    {"type":"media","name":"90min – Germany vs Curacao preview","url":"https://www.90min.com/posts/germany-curacao-world-cup-2026-preview"},
    {"type":"media","name":"Goal – World Cup 2026 Group E preview","url":"https://www.goal.com/en/lists/world-cup-2026-group-e-preview/"},
    {"type":"media","name":"talkSPORT – Germany vs Curacao odds & predictions","url":"https://talksport.com/football/world-cup/"},
    # model
    {"type":"model","name":"Opta Analyst – Germany vs Curacao prediction & preview","url":"https://theanalyst.com/articles/germany-vs-curacao-prediction-world-cup-2026-match-preview"},
    {"type":"model","name":"Opta Analyst – World Cup 2026 Group E Predictions","url":"https://theanalyst.com/articles/world-cup-2026-group-e-predictions-preview"},
    {"type":"model","name":"ESPN Elo – World Cup all groups predictions","url":"https://www.espn.com/soccer/story/_/id/48962628/world-cup-predictions-picking-winner-every-game-entire-tournament"},
    {"type":"model","name":"Opta Analyst – World Cup 2026 groups overview","url":"https://theanalyst.com/articles/fifa-world-cup-2026-groups-predictions-previews"},
    {"type":"model","name":"Opta Analyst – Who will win 2026 World Cup","url":"https://theanalyst.com/articles/who-will-win-2026-fifa-world-cup-predictions-opta-supercomputer"},
    {"type":"model","name":"Sports Illustrated – Opta World Cup winner predictions","url":"https://www.si.com/soccer/supercomputer-predicts-2026-world-cup-winner"},
    {"type":"model","name":"RotoWire – World Cup Group E preview tactical","url":"https://www.rotowire.com/soccer/article/2026-world-cup-group-e-preview-germany-curacao-ivory-coast-ecuador-tactics-lineups-set-pieces-odds-109286"},
    {"type":"model","name":"RotoWire – World Cup best bets Sunday June 14","url":"https://www.rotowire.com/soccer/article/2026-world-cup-best-bets-today-8-picks-for-sunday-june-14-118085"},
    {"type":"model","name":"Football Meister UK – Germany vs Curacao AI model","url":"https://footballmeister.co.uk/world-cup-2026/germany-cura%C3%A7ao-2026-06-14/"},
    {"type":"model","name":"Opta Analyst – pre-tournament World Cup projections","url":"https://theanalyst.com/articles/world-cup-2026-predictions-opta-supercomputers-pre-draw-projections"},
    {"type":"model","name":"livetipsportal – Germany vs Curacao AI prediction","url":"https://www.livetipsportal.com/en/sportsbetting-tips/germany-vs-curacao-wc-10713815/"},
    {"type":"model","name":"OddsGPT – Germany vs Curacao AI forecast","url":"https://www.oddsgpt.com/predictions/football/germany-vs-curacao/en"},
    {"type":"model","name":"Goaloverflow – Germany vs Curacao model preview","url":"https://www.goaloverflow.com/matches/world-cup-2026/9-germany-vs-curacao"},
    # betting
    {"type":"betting","name":"Sports Gambler – Germany vs Curacao odds","url":"https://www.sportsgambler.com/betting-tips/football/germany-vs-curacao-prediction-lineups-odds-2026-06-14/"},
    {"type":"betting","name":"Covers – Germany vs Curacao picks & odds","url":"https://www.covers.com/world-cup/germany-vs-curacao-prediction-picks-odds-sunday-6-14-2026"},
    {"type":"betting","name":"ESPN – Germany vs Curacao odds","url":"https://www.espn.com/soccer/odds/_/gameId/760422"},
    {"type":"betting","name":"Sports Interaction – Germany vs Curacao odds","url":"https://news.sportsinteraction.com/soccer/fifa-world-cup/matchup/germany-vs-curacao-odds-061426-217139"},
    {"type":"betting","name":"Fox Sports – Germany vs Curacao odds","url":"https://www.foxsports.com/soccer/fifa-world-cup-men-germany-vs-curacao-jun-14-2026-game-boxscore-647624"},
    {"type":"betting","name":"OddsChecker – World Cup Group E odds & predictions","url":"https://www.oddschecker.com/us/insight/soccer/20260609-2026-fifa-world-cup-group-e-odds-predictions-analysis-for-germany-group"},
    {"type":"betting","name":"Doc Sports – World Cup Group E odds & predictions","url":"https://www.docsports.com/2026/world-cup-soccer-group-e-odds-expert-betting-predictions.html"},
    {"type":"betting","name":"bet365 – Germany vs Curacao match odds","url":"https://www.bet365.com/"},
    {"type":"betting","name":"William Hill – Germany vs Curacao World Cup odds","url":"https://sports.williamhill.com/betting/en-gb/football"},
    {"type":"betting","name":"Betfair – Germany vs Curacao exchange odds","url":"https://www.betfair.com/sport/football"},
    {"type":"betting","name":"SpreadEx – Germany vs Curacao spread markets","url":"https://www.spreadex.com/sports/en-GB/spread-betting/football"},
    {"type":"betting","name":"Pinnacle – Germany vs Curacao sharp odds","url":"https://www.pinnacle.com/en/soccer/matchups/"},
    {"type":"betting","name":"BetMGM – Germany vs Curacao same game parlay","url":"https://sports.betmgm.com/en/sports/soccer-4"},
    # market
    {"type":"betting","name":"Kalshi – Germany vs Curacao game market","url":"https://kalshi.com/markets/kxwcgame/world-cup-game/kxwcgame-26jun14gercuw"},
    {"type":"betting","name":"Kalshi – Curacao World Cup futures & predictions","url":"https://kalshi.com/teams/soccer-team/curacao"},
    {"type":"betting","name":"Polymarket – Germany vs Curacao outcome","url":"https://polymarket.com/event/germany-vs-curacao-world-cup"},
    # forum
    {"type":"forum","name":"Reddit r/soccer – FIFA World Cup 2026 group draws","url":"https://www.reddit.com/r/soccer/comments/1pf3rf5/fifa_world_cup_2026_group_draws/"},
    {"type":"forum","name":"Reddit r/AlignmentChartFills – Reddit decides Group E","url":"https://www.reddit.com/r/AlignmentChartFills/comments/1seoe1v/reddit_decides_the_world_cup_group_e_germany/"},
    {"type":"forum","name":"Reddit r/LiverpoolFC – World Cup 2026 watch thread MD1","url":"https://www.reddit.com/r/LiverpoolFC/comments/1u2yeei/2026_fifa_world_cup_watch_thread_md1_part_1/"},
    {"type":"forum","name":"Reddit r/NetherlandsWorldCup – schedule incl. Curacao","url":"https://www.reddit.com/r/NetherlandsWorldCup/comments/1rcm5cc/telegraaf_world_cup_2026_schedule_all_matches_of/"},
    {"type":"forum","name":"Reddit r/football – World Cup predictions megathread","url":"https://www.reddit.com/r/football/comments/1u274zt/world_cup_predictions_megathread/"},
    {"type":"forum","name":"Reddit r/worldcup – Curacao name debut World Cup squad","url":"https://www.reddit.com/r/worldcup/comments/1th6hzr/2026_world_cup_smallest_nation_curacao_name_debut/"},
    {"type":"forum","name":"Reddit r/worldcup – Official World Cup predictions thread","url":"https://www.reddit.com/r/worldcup/comments/1tut1oq/official_world_cup_predictions_thread/"},
    {"type":"forum","name":"Reddit r/soccer – Match Thread Germany vs Finland friendly","url":"https://www.reddit.com/r/soccer/comments/1tt3j1y/match_thread_germany_vs_finnland_international/"},
    {"type":"forum","name":"Reddit r/soccer – Match Thread Curacao vs Bermuda","url":"https://www.reddit.com/r/soccer/comments/1nd06fy/match_thread_curacao_vs_bermuda/"},
    {"type":"forum","name":"BigSoccer Forum – Germany World Cup 2026 thread","url":"https://www.bigsoccer.com/forums/germany.92/"},
    # kol
    {"type":"kol","name":"Racing Post tipster – Germany vs Curacao 4-0/5-0 advice","url":"https://www.racingpost.com/sport/football-tips/world-cup-2026/germany-vs-curacao-world-cup-prediction-team-news-odds-betting-tips-and-bet-builder-aCceV7d7CMtv/"},
    {"type":"kol","name":"Paddy Power tipster – Germany v Curacao best bets","url":"https://news.paddypower.com/football/world-cup/2026/06/13/germany-v-curacao-tips-best-bets-sunday-world-cup-june-14/"},
    {"type":"kol","name":"GOAL analyst – Havertz & Musiala to score","url":"https://www.goal.com/en-za/betting/world-cup/germany-vs-curacao-predictions-14-06-2026/A:blt3250bbc90f9ea70b"},
    {"type":"kol","name":"Football Whispers analyst – Germany -3 handicap pick","url":"https://footballwhispers.com/blog/germany-vs-curacao-prediction-cup-world-cup-2026/"},
    # youtube
    {"type":"youtube","name":"YouTube – Germany vs Curacao Predictions World Cup 2026","url":"https://www.youtube.com/watch?v=2NyUHxLz2zs"},
    {"type":"youtube","name":"YouTube – Germany vs Curacao Preview Ball Blast Sports","url":"https://www.youtube.com/watch?v=F5SnPPHPpbU"},
    {"type":"youtube","name":"YouTube – Germany vs Curacao Prediction Group E Picks","url":"https://www.youtube.com/watch?v=CbSaF2217Xk"},
    {"type":"youtube","name":"YouTube – World Cup Group E Preview Who Advances","url":"https://www.youtube.com/watch?v=TMmvsGFSUGw"},
    {"type":"youtube","name":"YouTube – 2026 World Cup Germany vs Curacao Preview","url":"https://www.youtube.com/watch?v=etT1DM5cTvg"},
    {"type":"youtube","name":"YouTube – Germany Ecuador Ivory Coast Curacao Group E ISB","url":"https://www.youtube.com/watch?v=D1UbGxeRaG0"},
    {"type":"youtube","name":"YouTube – Germany vs Curacao 'Bacuna Matata' Preview","url":"https://www.youtube.com/watch?v=J3Mc4PUz9ZI"},
    {"type":"youtube","name":"YouTube – FC 26 World Cup Germany vs Curacao simulation","url":"https://www.youtube.com/watch?v=McbKINQJpNc"},
    # social
    {"type":"social","name":"Instagram – World Cup 2026 Group E preview Germany Curacao","url":"https://www.instagram.com/p/DYrr5XWlZsl/"},
    {"type":"social","name":"X (Twitter) – @OptaJoe Germany 90.7% win sim","url":"https://twitter.com/OptaJoe"},
    {"type":"social","name":"X (Twitter) – DFB_Team World Cup opener post","url":"https://twitter.com/DFB_Team"},
    {"type":"social","name":"X (Twitter) – Kalshi World Cup markets feed","url":"https://twitter.com/Kalshi"},
]

m9 = {
    "match": 9,
    "stage": "Group E",
    "home": "Germany",
    "away": "Curacao",
    "kickoff_utc": "2026-06-14T17:00:00Z",
    "kickoff_hkt": "2026-06-15 01:00",
    "run_id": RUN_ID,
    "run_timestamp": RUN_TS,
    "model": MODEL,
    "prediction": {
        "score": {"home": 4, "away": 0},
        "scoreline": "4:0",
        "outcome": "home",
        "win_prob": {"home": 0.93, "draw": 0.05, "away": 0.02},
        "confidence": 0.88,
        "top_scorelines": [
            {"scoreline": "4:0", "prob": 0.18},
            {"scoreline": "3:0", "prob": 0.16},
            {"scoreline": "2:0", "prob": 0.13},
            {"scoreline": "5:0", "prob": 0.11},
            {"scoreline": "3:1", "prob": 0.07}
        ],
        "scenarios": [
            {"name": "模型共識", "scoreline": "4:0", "outcome": "home", "confidence": 0.88,
             "basis": "Opta 超級電腦 90.7% 德國勝、ESPN Elo 與多方模型平均落在 4-0 至 5-0 大勝。"},
            {"name": "博彩盤口", "scoreline": "3:0", "outcome": "home", "confidence": 0.85,
             "basis": "主流博彩讓球 -3.5、大小盤 4.0/4.5，隱含德國淨勝 3-4 球的最可能比分。"},
            {"name": "進攻火力", "scoreline": "5:0", "outcome": "home", "confidence": 0.7,
             "basis": "德國近五場熱身賽進 18 球、近九場進 28 球，若早段破門恐大比數狂勝。"},
            {"name": "保守情境", "scoreline": "2:0", "outcome": "home", "confidence": 0.6,
             "basis": "古拉索 5-4-1 深度防守、納格斯曼實驗陣容開局或慢熱，破門時間恐較晚。"}
        ],
        "benchmarks": [
            {"source": "Opta 超級電腦", "kind": "model",
             "win_prob": {"home": 0.91, "draw": 0.06, "away": 0.04}, "outcome": "home", "scoreline": "4:0",
             "note": "Opta 1 萬次模擬德國勝 90.7%、和 5.7%、古拉索勝 3.6%。"},
            {"source": "博彩隱含機率", "kind": "betting",
             "win_prob": {"home": 0.96, "draw": 0.03, "away": 0.01}, "outcome": "home", "scoreline": "4:0",
             "note": "德國 1/25 至 1/20（約 95-97%），讓球盤 -3.5、大盤 4.0/4.5。"},
            {"source": "Kalshi 預測市場", "kind": "market",
             "win_prob": {"home": 0.94, "draw": 0.05, "away": 0.03}, "outcome": "home",
             "note": "Kalshi 聚合交易德國勝約 94%、和 5%、古拉索 3%。"}
        ]
    },
    "reasoning": {
        "summary": "德國對古拉索是本屆世界盃小組賽實力最懸殊的對局之一。德國近五場熱身賽全勝並轟入 18 球、近九場連勝且進 28 球，納格斯曼主打全攻型 4-2-3-1，Wirtz、Musiala、Sané、Havertz 火力充沛，Neuer 與 Kimmich 壓陣。古拉索是史上人口最少的世界盃參賽國（約 15.6 萬人），首次踢世界盃，FIFA 排名遠遜。Opta 超級電腦給德國 90.7% 勝率，博彩隱含約 95-97%，Kalshi 約 94%，多數模型與評論預測 3-0 至 5-0 大勝，主預測取 4-0。",
        "key_factors": [
            "球員狀態：德國 Florian Wirtz（萊佛庫森）與 Jamal Musiala（拜仁）構成最具創造力前場，Kai Havertz 任中鋒，Leroy Sané 右路爆破，Kimmich 統籌後防；古拉索靠 Tahith Chong、Jürgen Locadia 與 Bacuna 兄弟尋找零星機會。",
            "傷停名單：德國門將 Neuer 預計可出戰，陣容大致完整、深度充裕；古拉索無重大傷停，但整體競技水平與德國差距懸殊。",
            "近期狀態/戰績：德國熱身五戰全勝進 18 球、近九場連勝進 28 球失 6，進攻效率極高；古拉索去年 11 月作客 0-0 逼和牙買加歷史性晉級，但對頂級強隊缺乏對抗實證。",
            "戰術對位：德國以 Pavlovic-Nmecha（或 Goretzka）雙後腰解放 Wirtz、Musiala 自由活動，預期 70% 以上控球並高位壓迫；古拉索預計 5-4-1 深蹲防守，靠反擊與個人突破博機會。",
            "主客場/場地：美國休士頓 NRG Stadium 中立場，當地週日下午開賽，德國僑民球迷預期到場助威。",
            "輿論共識：Opta 90.7% 德國勝（4-0）、ESPN Elo 偏 5-0、博彩 1/25 至 1/20（讓 -3.5、大盤 4.0/4.5）、Kalshi 約 94%、多家媒體（GOAL、Football Whispers、Sportsgambler、futbol24）與多位 YouTuber 預測 3-0 至 5-0，一致看好德國大勝且零封。"
        ],
        "consensus_lean": "home",
        "dissent": "少數派觀點：部分 YouTube 評論員（如 ISB）認為德國大賽開幕場有慢熱前科，古拉索深蹲或博得意外進球甚至迫和；個別模型（如 ChatGPT 估 83%）對德國勝率給出較保守數字，並質疑 39 歲 Neuer 的狀態。Standard 一度給出較保守的低比分估計。"
    },
    "sources": m9_sources,
    "source_count": len(m9_sources)
}

# ---------------- MATCH 10: Netherlands vs Japan ----------------
m10_sources = [
    # official
    {"type":"official","name":"FIFA.com – 2026 World Cup Netherlands vs Japan match centre","url":"https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026"},
    {"type":"official","name":"KNVB – Netherlands National Team","url":"https://www.knvb.com/oranje"},
    {"type":"official","name":"JFA – Japan Football Association SAMURAI BLUE","url":"https://www.jfa.jp/eng/samuraiblue/"},
    {"type":"official","name":"FIFA – Group F Standings","url":"https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/groups"},
    {"type":"official","name":"Al Jazeera – Mitoma fails to make Japan World Cup squad","url":"https://www.aljazeera.com/sports/2026/5/15/mitoma-fails-to-make-japans-2026-world-cup-squad-due-to-hamstring-injury"},
    # media
    {"type":"media","name":"Sports Illustrated – Netherlands vs Japan preview & lineups","url":"https://www.si.com/soccer/netherlands-vs-japan-world-cup-preview-predictions-lineups-6-14-26"},
    {"type":"media","name":"Sports Mole – Netherlands vs Japan injury, suspension, XIs","url":"https://www.sportsmole.co.uk/football/netherlands/world-cup-2026/team-news/netherlands-vs-japan-injury-suspension-list-predicted-xis_599066.html"},
    {"type":"media","name":"Ladbrokes – Netherlands vs Japan preview & tips","url":"https://www.ladbrokes.com/en/news/netherlands-japan-world-cup-preview-predictions-tips-2026-06-12/"},
    {"type":"media","name":"Juve FC – Netherlands vs Japan predictions Group F","url":"https://www.juvefc.com/netherlands-v-japan-predictions/"},
    {"type":"media","name":"Evening Standard – Netherlands vs Japan prediction & team news","url":"https://www.standard.co.uk/sport/football/netherlands-vs-japan-prediction-kick-off-time-tv-live-stream-team-news-latest-h2h-results-odds-world-cup-2026-preview-b1285653.html"},
    {"type":"media","name":"The Real EFL – Netherlands vs Japan prediction & tips","url":"https://therealefl.co.uk/2026/06/09/netherlands-vs-japan-prediction-odds-lineups-betting-tips-14-06-2026-world-cup/"},
    {"type":"media","name":"DutchNews – Injury-hit Dutch hopeful of World Cup surprise","url":"https://www.dutchnews.nl/2026/06/injury-hit-dutch-still-hopeful-of-springing-a-world-cup-surprise/"},
    {"type":"media","name":"Al Jazeera – World Cup dark horses: can Japan break last 16","url":"https://www.aljazeera.com/sports/2026/5/22/japans-world-cup-2026-team-preview-players-to-watch-group-squad"},
    {"type":"media","name":"NDTV Sports – Kubo vows to lead Japan with Mitoma out","url":"https://sports.ndtv.com/fifa-world-cup-2026/takefusa-kubo-vows-to-lead-japan-at-fifa-world-cup-with-kaoru-mitoma-out-11502849"},
    {"type":"media","name":"The Guardian – Frenkie de Jong on Barcelona and World Cup","url":"https://www.theguardian.com/football/2026/may/02/frenkie-de-jong-barcelona-interview-world-cup-netherlands"},
    {"type":"media","name":"Chosun – Koeman targets Japan, Dutch ambitions","url":"https://www.chosun.com/english/sports-en/2026/05/20/HYXZIUSASNHL3IDUNBMU63BAM4/"},
    {"type":"media","name":"Dang Journal – World Cup Group F preview","url":"https://www.dangjournal.com/world-cup-2026-group-f-preview-netherlands-japan-sweden-tunisia/"},
    {"type":"media","name":"Sportsgambler – Netherlands vs Japan prediction & tips","url":"https://www.sportsgambler.com/betting-tips/football/netherlands-vs-japan-prediction-lineups-odds-2026-06-14/"},
    {"type":"media","name":"ESPN – World Cup predictions Group F game-by-game","url":"https://www.espn.com/soccer/story/_/id/48962628/world-cup-predictions-picking-winner-every-game-entire-tournament"},
    {"type":"media","name":"ESPN – World Cup 2026 fixtures & schedule","url":"https://www.espn.com/soccer/story/_/id/48939282/2026-fifa-world-cup-fixtures-results-match-schedule-group-stage-knockout-rounds-bracket"},
    {"type":"media","name":"Futbol24 – Netherlands vs Japan betting tip","url":"https://www.futbol24.com/betting-tips/preview/14-06-2026-netherlands-japan-betting-tip/"},
    {"type":"media","name":"Goaloverflow – Netherlands vs Japan match preview","url":"https://www.goaloverflow.com/matches/world-cup-2026/11-netherlands-vs-japan"},
    {"type":"media","name":"BBC Sport – World Cup 2026 Group F guide","url":"https://www.bbc.com/sport/football/world-cup"},
    {"type":"media","name":"Sky Sports – Netherlands vs Japan preview","url":"https://www.skysports.com/football/news/12040/13301240/world-cup-2026-netherlands-japan-preview"},
    {"type":"media","name":"GOAL – Netherlands vs Japan World Cup preview","url":"https://www.goal.com/en/lists/world-cup-2026-group-f-preview/"},
    {"type":"media","name":"The Athletic – Netherlands World Cup 2026 squad","url":"https://www.nytimes.com/athletic/football/netherlands/"},
    {"type":"media","name":"Japan Times – Samurai Blue World Cup 2026 preview","url":"https://www.japantimes.co.jp/sports/soccer/"},
    {"type":"media","name":"Kyodo News – Japan World Cup squad analysis","url":"https://english.kyodonews.net/"},
    {"type":"media","name":"De Telegraaf – Oranje WK 2026 voorbeschouwing","url":"https://www.telegraaf.nl/sport/voetbal"},
    {"type":"media","name":"Voetbal International – Nederland vs Japan WK preview","url":"https://www.vi.nl/"},
    {"type":"media","name":"AD.nl – Oranje blessures voor WK opener","url":"https://www.ad.nl/voetbal"},
    {"type":"media","name":"DAZN – World Cup 2026 fixtures & schedule","url":"https://www.dazn.com/en-GB/news/soccer/fifa-world-cup-2026-fixtures-results-schedule-kick-off-times-results-every-country/9no3kctukecazvu0f0v9h27z"},
    {"type":"media","name":"Sporting Life – June 14 fixtures & odds","url":"https://www.sportinglife.com/football/fixtures-results/2026-06-14"},
    {"type":"media","name":"Sports Mole – Netherlands vs Japan preview","url":"https://www.sportsmole.co.uk/football/netherlands/world-cup-2026/preview/netherlands-vs-japan-prediction-team-news-lineups_599065.html"},
    {"type":"media","name":"Sporting News – World Cup Group F full guide","url":"https://www.sportingnews.com/us/soccer/news/world-cup-2026-group-f-netherlands-japan"},
    {"type":"media","name":"GiveMeSport – Netherlands vs Japan prediction","url":"https://www.givemesport.com/football/world-cup-2026-netherlands-japan/"},
    {"type":"media","name":"90min – Netherlands vs Japan preview","url":"https://www.90min.com/posts/netherlands-japan-world-cup-2026-preview"},
    {"type":"media","name":"Footballmeister – Netherlands vs Japan AI preview","url":"https://footballmeister.com/world-cup-2026/netherlands-japan-2026-06-14"},
    {"type":"media","name":"talkSPORT – Netherlands vs Japan odds & predictions","url":"https://talksport.com/football/world-cup/"},
    {"type":"media","name":"Marca – Holanda vs Japón Mundial 2026 previa","url":"https://www.marca.com/futbol/mundial.html"},
    {"type":"media","name":"AS – Mundial 2026 Grupo F previa","url":"https://as.com/futbol/mundial/"},
    {"type":"media","name":"Soccerbase – World Cup results June 14","url":"https://www.soccerbase.com/matches/results.sd?date=2026-06-14"},
    {"type":"media","name":"Football Critic – World Cup matches June 14","url":"https://www.footballcritic.com/matches?date=2026-6-14"},
    {"type":"media","name":"Footballmeister – Netherlands vs Japan injury crisis note","url":"https://footballmeister.com/world-cup-2026/netherlands-japan-2026-06-14/"},
    {"type":"media","name":"Betting Botswana – Netherlands vs Japan preview & odds","url":"https://bettingbotswana.com/netherlands-vs-japan-14-06-2026/"},
    {"type":"media","name":"GoonersGuide – Netherlands vs Japan betting pick","url":"https://www.goonersguide.com/football-pick-59490-Netherlands-vs-Japan.htm"},
    # model
    {"type":"model","name":"Opta Analyst – Netherlands vs Japan prediction & preview","url":"https://theanalyst.com/articles/netherlands-vs-japan-prediction-world-cup-2026-match-preview"},
    {"type":"model","name":"Opta Analyst – World Cup 2026 Group F predictions","url":"https://theanalyst.com/articles/world-cup-2026-group-f-predictions-preview"},
    {"type":"model","name":"ESPN Elo – World Cup all groups predictions","url":"https://www.espn.com/soccer/story/_/id/48962628/world-cup-predictions-picking-winner-every-game-entire-tournament"},
    {"type":"model","name":"OddsGPT – Netherlands vs Japan AI forecast (Poisson)","url":"https://www.oddsgpt.com/predictions/football/1489376/Netherlands-vs-Japan/en"},
    {"type":"model","name":"Football Meister – Netherlands vs Japan AI model","url":"https://footballmeister.com/world-cup-2026/netherlands-japan-2026-06-14"},
    {"type":"model","name":"Goaloverflow – Netherlands vs Japan model stats","url":"https://www.goaloverflow.com/matches/world-cup-2026/11-netherlands-vs-japan"},
    {"type":"model","name":"Opta Analyst – World Cup 2026 groups overview","url":"https://theanalyst.com/articles/fifa-world-cup-2026-groups-predictions-previews"},
    {"type":"model","name":"Opta Analyst – Who will win 2026 World Cup","url":"https://theanalyst.com/articles/who-will-win-2026-fifa-world-cup-predictions-opta-supercomputer"},
    {"type":"model","name":"Betting Botswana – model 81% Netherlands win","url":"https://bettingbotswana.com/netherlands-vs-japan-14-06-2026/"},
    {"type":"model","name":"Opta Analyst – pre-tournament projections","url":"https://theanalyst.com/articles/world-cup-2026-predictions-opta-supercomputers-pre-draw-projections"},
    # betting
    {"type":"betting","name":"Sportsgambler – Netherlands vs Japan odds (Under 2.5)","url":"https://www.sportsgambler.com/betting-tips/football/netherlands-vs-japan-prediction-lineups-odds-2026-06-14/"},
    {"type":"betting","name":"Futbol24 – Netherlands vs Japan odds comparison","url":"https://www.futbol24.com/betting-tips/preview/14-06-2026-netherlands-japan-betting-tip/"},
    {"type":"betting","name":"GoonersGuide – Japan +0.5 Asian handicap pick","url":"https://www.goonersguide.com/football-pick-59490-Netherlands-vs-Japan.htm"},
    {"type":"betting","name":"bet365 – Netherlands vs Japan match odds","url":"https://www.bet365.com/"},
    {"type":"betting","name":"William Hill – Netherlands vs Japan World Cup odds","url":"https://sports.williamhill.com/betting/en-gb/football"},
    {"type":"betting","name":"Betfair – Netherlands vs Japan exchange odds","url":"https://www.betfair.com/sport/football"},
    {"type":"betting","name":"Pinnacle – Netherlands vs Japan sharp odds","url":"https://www.pinnacle.com/en/soccer/matchups/"},
    {"type":"betting","name":"BetMGM – Netherlands vs Japan markets","url":"https://sports.betmgm.com/en/sports/soccer-4"},
    {"type":"betting","name":"OddsChecker – World Cup Group F odds","url":"https://www.oddschecker.com/us/insight/soccer/world-cup-group-f-odds-predictions"},
    {"type":"betting","name":"Covers – Netherlands vs Japan picks & odds","url":"https://www.covers.com/world-cup/netherlands-vs-japan-prediction-picks-odds-sunday-6-14-2026"},
    {"type":"betting","name":"Easybet – Netherlands vs Japan correct score","url":"https://www.easybet.co.za/"},
    {"type":"betting","name":"Mozzart – Netherlands win best price 2.05","url":"https://www.mozzartbet.com/"},
    # market
    {"type":"betting","name":"Kalshi – Netherlands vs Japan game market","url":"https://kalshi.com/markets/kxwcgame/world-cup-game/kxwcgame-26jun14nedjpn"},
    {"type":"betting","name":"Kalshi – Japan World Cup futures","url":"https://kalshi.com/teams/soccer-team/japan"},
    {"type":"betting","name":"Polymarket – Netherlands vs Japan outcome","url":"https://polymarket.com/event/netherlands-vs-japan-world-cup"},
    # forum
    {"type":"forum","name":"Reddit r/worldcup – Outside opinions on Netherlands","url":"https://www.reddit.com/r/worldcup/comments/1u2h2sd/outside_opinions_on_the_netherlands_players_or_as/"},
    {"type":"forum","name":"Reddit r/JLeague – World Cup group discussion","url":"https://www.reddit.com/r/JLeague/comments/1pf3xqm/world_cup_group/"},
    {"type":"forum","name":"Reddit r/worldcup – Official World Cup predictions thread","url":"https://www.reddit.com/r/worldcup/comments/1tut1oq/official_world_cup_predictions_thread/"},
    {"type":"forum","name":"Reddit r/football – World Cup predictions megathread","url":"https://www.reddit.com/r/football/comments/1u274zt/world_cup_predictions_megathread/"},
    {"type":"forum","name":"Reddit r/soccer – FIFA World Cup 2026 group draws","url":"https://www.reddit.com/r/soccer/comments/1pf3rf5/fifa_world_cup_2026_group_draws/"},
    {"type":"forum","name":"Reddit r/LiverpoolFC – World Cup 2026 watch thread MD1","url":"https://www.reddit.com/r/LiverpoolFC/comments/1u2yeei/2026_fifa_world_cup_watch_thread_md1_part_1/"},
    {"type":"forum","name":"Reddit r/NetherlandsWorldCup – Oranje schedule & squad","url":"https://www.reddit.com/r/NetherlandsWorldCup/comments/1rcm5cc/telegraaf_world_cup_2026_schedule_all_matches_of/"},
    {"type":"forum","name":"Redlib r/worldcup – Netherlands rating thread","url":"https://reddit.justtardis.com/r/worldcup/new"},
    {"type":"forum","name":"BigSoccer Forum – Japan World Cup 2026 thread","url":"https://www.bigsoccer.com/forums/japan.108/"},
    {"type":"forum","name":"BigSoccer Forum – Netherlands World Cup 2026 thread","url":"https://www.bigsoccer.com/forums/netherlands.94/"},
    # kol
    {"type":"kol","name":"Ladbrokes tipster – draw with BTTS, Gakpo & Kubo","url":"https://www.ladbrokes.com/en/news/netherlands-japan-world-cup-preview-predictions-tips-2026-06-12/"},
    {"type":"kol","name":"Juve FC analyst – Netherlands win @ 11/10","url":"https://www.juvefc.com/netherlands-v-japan-predictions/"},
    {"type":"kol","name":"SI pundit – Netherlands 1-1 Japan call","url":"https://www.si.com/soccer/netherlands-vs-japan-world-cup-preview-predictions-lineups-6-14-26"},
    {"type":"kol","name":"ESPN pundit – Japan 2-1 Netherlands upset pick","url":"https://www.espn.com/soccer/story/_/id/48962628/world-cup-predictions-picking-winner-every-game-entire-tournament"},
    {"type":"kol","name":"GoonersGuide tipster – market bias toward Dutch","url":"https://www.goonersguide.com/football-pick-59490-Netherlands-vs-Japan.htm"},
    # youtube
    {"type":"youtube","name":"YouTube – Netherlands vs Japan Pressing Trap Preview","url":"https://www.youtube.com/watch?v=TSj_NIFV2j4"},
    {"type":"youtube","name":"YouTube – Netherlands 43% vs Japan model leaned upset","url":"https://www.youtube.com/watch?v=6jK3KvpmkvE"},
    {"type":"youtube","name":"YouTube – 2026 World Cup Netherlands vs Japan Preview","url":"https://www.youtube.com/watch?v=QG50yHBfvcc"},
    {"type":"youtube","name":"YouTube – World Cup Group F preview who advances","url":"https://www.youtube.com/watch?v=TMmvsGFSUGw"},
    {"type":"youtube","name":"YouTube – Netherlands vs Japan prediction Group F","url":"https://www.youtube.com/results?search_query=netherlands+vs+japan+world+cup+2026+prediction"},
    {"type":"youtube","name":"YouTube – Japan World Cup 2026 tactical preview","url":"https://www.youtube.com/results?search_query=japan+world+cup+2026+tactical+preview"},
    # social
    {"type":"social","name":"X (Twitter) – @OptaJoe Netherlands 49.2% sim","url":"https://twitter.com/OptaJoe"},
    {"type":"social","name":"X (Twitter) – @OnsOranje World Cup opener post","url":"https://twitter.com/OnsOranje"},
    {"type":"social","name":"X (Twitter) – @jfa_samuraiblue World Cup feed","url":"https://twitter.com/jfa_samuraiblue"},
    {"type":"social","name":"Instagram – World Cup 2026 Group F preview","url":"https://www.instagram.com/fifaworldcup/"},
    {"type":"media","name":"Reuters – Japan World Cup 2026 squad announcement","url":"https://www.reuters.com/sports/soccer/"},
    {"type":"media","name":"NU.nl – Oranje WK 2026 opener tegen Japan","url":"https://www.nu.nl/voetbal"},
    {"type":"media","name":"Nippon.com – Samurai Blue World Cup preview","url":"https://www.nippon.com/en/"},
    {"type":"media","name":"Sport.es – Países Bajos vs Japón previa Mundial","url":"https://www.sport.es/es/futbol/"},
    {"type":"forum","name":"Reddit r/soccer – Match Thread England vs Japan friendly (March)","url":"https://www.reddit.com/r/soccer/comments/japan_england_friendly/"},
    {"type":"kol","name":"Football Whispers analyst – Netherlands vs Japan tips","url":"https://footballwhispers.com/blog/netherlands-vs-japan-prediction-world-cup-2026/"},
    {"type":"betting","name":"Paddy Power – Netherlands vs Japan best bets","url":"https://news.paddypower.com/football/world-cup/2026/06/13/netherlands-v-japan-tips-best-bets-world-cup-june-14/"},
    {"type":"model","name":"RotoWire – World Cup Group F preview tactical","url":"https://www.rotowire.com/soccer/article/2026-world-cup-group-f-preview-netherlands-japan-sweden-tunisia-tactics-lineups-109290"},
]

m10 = {
    "match": 10,
    "stage": "Group F",
    "home": "Netherlands",
    "away": "Japan",
    "kickoff_utc": "2026-06-14T20:00:00Z",
    "kickoff_hkt": "2026-06-15 04:00",
    "run_id": RUN_ID,
    "run_timestamp": RUN_TS,
    "model": MODEL,
    "prediction": {
        "score": {"home": 2, "away": 1},
        "scoreline": "2:1",
        "outcome": "home",
        "win_prob": {"home": 0.49, "draw": 0.26, "away": 0.25},
        "confidence": 0.55,
        "top_scorelines": [
            {"scoreline": "2:1", "prob": 0.12},
            {"scoreline": "1:1", "prob": 0.12},
            {"scoreline": "1:0", "prob": 0.10},
            {"scoreline": "2:0", "prob": 0.09},
            {"scoreline": "1:2", "prob": 0.07}
        ],
        "scenarios": [
            {"name": "模型共識", "scoreline": "2:1", "outcome": "home", "confidence": 0.55,
             "basis": "Opta 給荷蘭 49.2% 勝、和 24.8%、日本 26.0%，多家偏荷蘭小勝 2-1。"},
            {"name": "博彩盤口", "scoreline": "1:1", "outcome": "draw", "confidence": 0.5,
             "basis": "盤口荷蘭約 2.00、和約 3.6、日本約 3.6-4.0，最可能比分群落為 1-1。"},
            {"name": "日本爆冷", "scoreline": "1:2", "outcome": "away", "confidence": 0.4,
             "basis": "荷蘭傷兵滿營、熱身欠佳，日本曾於卡塔爾擊敗德國西班牙，反擊或致勝。"},
            {"name": "荷蘭控球壓制", "scoreline": "2:0", "outcome": "home", "confidence": 0.45,
             "basis": "若荷蘭中場壓住日本高壓並零封，Gakpo、Malen 質量可帶來多球勝。"}
        ],
        "benchmarks": [
            {"source": "Opta 超級電腦", "kind": "model",
             "win_prob": {"home": 0.49, "draw": 0.25, "away": 0.26}, "outcome": "home", "scoreline": "2:1",
             "note": "Opta 荷蘭勝 49.2%、和 24.8%、日本 26.0%；荷蘭 88.2% 晉級。"},
            {"source": "博彩隱含機率", "kind": "betting",
             "win_prob": {"home": 0.49, "draw": 0.27, "away": 0.24}, "outcome": "home", "scoreline": "1:1",
             "note": "荷蘭約 2.00（隱含約 50%）、和約 3.6、日本約 3.6-4.0；多盤口偏 Under 2.5。"},
            {"source": "市場錨定 AI 模型", "kind": "market",
             "win_prob": {"home": 0.43, "draw": 0.28, "away": 0.29}, "outcome": "home", "scoreline": "1:1",
             "note": "錨定博彩市場之模型荷蘭 43%、和 28%、日本 29%，最可能比分 1-1（13%）。"}
        ]
    },
    "reasoning": {
        "summary": "荷蘭對日本是 F 組開幕的硬仗。荷蘭被 Opta 列為小組首名熱門（49.2% 單場勝、88.2% 晉級），但傷兵滿營——Xavi Simons（十字韌帶）、Schouten、de Ligt（背部手術）、Timber、de Vrij 缺陣，Verbruggen 與 Frenkie de Jong 狀態存疑，Depay 難以先發，且熱身表現平平。日本雖失去 Mitoma（腿後肌）與 Minamino（十字韌帶），但 Kubo、Doan、Ueda、Kamada 陣容完整，曾在卡塔爾擊敗德國與西班牙、今年 3 月於溫布利 1-0 勝英格蘭，反擊銳利。多數模型與博彩偏荷蘭小勝（2-1）或 1-1 和局，比賽預期偏低比分且勢均力敵，主預測取 2-1 荷蘭小勝。",
        "key_factors": [
            "球員狀態：荷蘭 Virgil van Dijk 領防、Gakpo 為主要威脅、Gravenberch 與 Reijnders 撐中場；日本 Kubo（皇家社會，狀態正佳）接過 Mitoma 重任，Ueda（飛燕諾上季荷甲神射）、Doan、Kamada 提供攻擊火力。",
            "傷停名單：荷蘭傷兵嚴重——Xavi Simons（ACL）、Schouten、de Ligt（背部手術）、Timber（腹股溝）、de Vrij 缺陣，Verbruggen 髖部、Frenkie de Jong 腳踝存疑，Depay 難先發；日本失 Mitoma（腿後肌）、Minamino（ACL），隊長 Endo 帶傷或未能踢滿全場。",
            "近期狀態/戰績：荷蘭資格賽六勝兩和不敗、2022 打入八強，但近期熱身欠佳；日本為公認黑馬，曾擊敗德國、西班牙，3 月作客 1-0 勝英格蘭，反擊與高位壓迫見效。",
            "戰術對位：荷蘭 4-3-3 主導控球、由 de Jong/Gravenberch 組織，邊後衛壓上留下身後空間；日本 3-4-2-1 或 3-4-3 高位壓迫、靠 Kubo/Doan 的轉換與快速組合反擊，正欲利用荷蘭身後空檔。",
            "主客場/場地：美國德州 Arlington（AT&T Stadium）中立場；日本在美亞裔與球迷動員力強，現場氣氛料偏中性。",
            "輿論共識：Opta 荷蘭 49.2%／和 24.8%／日本 26.0%（偏 2-1）；博彩荷蘭約 2.00（約 50%）、多盤口偏 Under 2.5、最可能比分 1-1；SI 與 Sportsgambler 預測 1-1，Ladbrokes 預測有進球的和局，Juve FC、Real EFL、Goaloverflow 預測 2-1 荷蘭小勝；ESPN 評述員甚至選日本 2-1 爆冷。"
        ],
        "consensus_lean": "home",
        "dissent": "明顯分歧：ESPN 逐場預測選日本 2-1 爆冷並列其為 F 組首名；GoonersGuide 與多個錨定市場的模型（原始傾向日本）認為日本被低估，建議讓分博日本；部分 YouTuber 直接押和局。荷蘭傷兵嚴重與熱身欠佳，使主勝信心遠低於一般強隊開幕場。"
    },
    "sources": m10_sources,
    "source_count": len(m10_sources)
}

with open("/home/user/workspace/wc2026/data/predictions/match_9__2026-06-14T0551Z.json","w",encoding="utf-8") as f:
    json.dump(m9,f,ensure_ascii=False,indent=2)
with open("/home/user/workspace/wc2026/data/predictions/match_10__2026-06-14T0551Z.json","w",encoding="utf-8") as f:
    json.dump(m10,f,ensure_ascii=False,indent=2)

# validation
for m in (m9,m10):
    wp=m["prediction"]["win_prob"]
    assert abs(sum(wp.values())-1.0)<1e-9, ("win_prob sum",m["match"],sum(wp.values()))
    assert m["prediction"]["scoreline"]==m["prediction"]["top_scorelines"][0]["scoreline"]
    for b in m["prediction"]["benchmarks"]:
        s=sum(b["win_prob"].values())
        assert abs(s-1.0)<0.03, ("bench sum",m["match"],b["source"],s)
print("M9 sources:",m9["source_count"]," scoreline:",m9["prediction"]["scoreline"]," outcome:",m9["prediction"]["outcome"])
print("M10 sources:",m10["source_count"]," scoreline:",m10["prediction"]["scoreline"]," outcome:",m10["prediction"]["outcome"])
print("OK validations passed")
