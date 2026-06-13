# Prediction JSON Schema

Each prediction run writes ONE file per match per run:
`data/predictions/match_{NUM}__{RUN_TIMESTAMP}.json`

Every run is preserved independently (never overwritten) so accuracy can be
re-evaluated against the latest pre-match prediction and the whole reasoning
trail is auditable.

```json
{
  "match": 6,
  "stage": "Group C",
  "home": "Brazil",
  "away": "Morocco",
  "kickoff": "2026-06-13T22:00 ET",
  "run_id": "2026-06-13T0800Z",
  "run_timestamp": "2026-06-13T08:00:00Z",
  "model": "research-pplx",
  "prediction": {
    "score": { "home": 2, "away": 1 },
    "scoreline": "2:1",
    "outcome": "home",            // home | draw | away
    "win_prob": { "home": 0.58, "draw": 0.24, "away": 0.18 },
    "confidence": 0.62             // 0..1 self-assessed
  },
  "reasoning": {
    "summary": "Short 2-3 sentence rationale in Traditional Chinese.",
    "key_factors": [
      "球員狀態：...",
      "傷停名單：...",
      "近期狀態/戰績：...",
      "戰術對位：...",
      "主客場/場地：...",
      "輿論共識：..."
    ],
    "consensus_lean": "home",     // what the aggregate of sources leans toward
    "dissent": "Notable contrarian view, if any."
  },
  "sources": [
    { "type": "official", "name": "FIFA.com", "url": "..." },
    { "type": "forum", "name": "r/worldcup", "url": "..." },
    { "type": "kol", "name": "...", "url": "..." },
    { "type": "youtube", "name": "...", "url": "..." },
    { "type": "media", "name": "ESPN", "url": "..." }
  ],
  "source_count": 52
}
```

## Source mix target (>= 50 per match)
- Official: FIFA, federations, club/national team sites
- Media: ESPN, BBC, Goal, Sky, Athletic, AS, Marca, etc.
- Betting/model: Opta, FiveThirtyEight-style, odds aggregators
- Forums/Community: Reddit, sports forums
- KOL / Pundits: named analysts, ex-players
- YouTube: preview/analysis videos

## Source type taxonomy
`official | media | model | betting | forum | kol | youtube | social`
