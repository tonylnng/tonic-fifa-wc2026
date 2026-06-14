export interface Fixture {
  match: number;
  stage: string;
  group: string | null;
  date: string;
  kickoff_local: string;
  kickoff_utc?: string;
  timezone?: string;
  home: string;
  away: string;
  venue: string;
  city: string;
  status: "FT" | "scheduled";
  result: { home: number; away: number } | null;
}

export interface FixturesData {
  tournament: string;
  hosts: string[];
  total_matches: number;
  teams: number;
  groups: Record<string, string[]>;
  last_updated: string;
  fixtures: Fixture[];
}

export interface PredictionSource {
  type: string;
  name: string;
  url: string;
}

export interface ScorelineProb {
  scoreline: string;
  prob: number;
}

export interface PredictionScenario {
  name: string;
  scoreline: string;
  outcome: "home" | "draw" | "away";
  confidence: number;
  basis?: string;
}

export interface Prediction {
  match: number;
  stage: string;
  home: string;
  away: string;
  kickoff?: string;
  kickoff_utc?: string;
  run_id: string;
  run_timestamp: string;
  model: string;
  prediction: {
    score: { home: number; away: number };
    scoreline: string;
    outcome: "home" | "draw" | "away";
    win_prob: { home: number; draw: number; away: number };
    confidence: number;
    top_scorelines?: ScorelineProb[];
    scenarios?: PredictionScenario[];
  };
  reasoning: {
    summary: string;
    key_factors: string[];
    consensus_lean?: string;
    dissent?: string;
  };
  sources: PredictionSource[];
  source_count: number;
}

export type PredictionsData = Record<string, Prediction[]>;

export interface ResultItem {
  match: number;
  stage: string;
  home: string;
  away: string;
  score: { home: number; away: number };
  outcome: "home" | "draw" | "away";
  recorded_at: string;
  source: string;
}

export interface ResultsData {
  tournament: string;
  last_updated: string;
  results: ResultItem[];
}

export interface AccuracyData {
  tournament: string;
  last_updated: string;
  metrics: {
    total_evaluated: number;
    outcome_correct: number;
    outcome_accuracy: number;
    exact_score_correct: number;
    exact_score_accuracy: number;
  };
  by_stage: Record<string, any>;
  evaluations: any[];
}

export interface StatusData {
  last_updated: string;
  total_matches: number;
  prediction_files: number;
  total_runs: number;
  runs: string[];
  accuracy: AccuracyData["metrics"];
}
