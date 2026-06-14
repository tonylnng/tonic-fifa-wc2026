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

/** 對比基準線：博彩隱含機率、Opta 超級電腦、ESPN Elo 等公開模型。
 *  win_prob 三向機率總和應近 1（博彩隱含機率可能含抽水，供顯示）。 */
export interface Benchmark {
  source: string; // 來源名稱，例：博彩隱含機率 / Opta 超級電腦 / MiniMax M3 / 千問 / DeepSeek
  kind: "betting" | "model" | "market" | "ai"; // 類型（ai = 第三方大模型預測）
  win_prob: { home: number; draw: number; away: number };
  outcome?: "home" | "draw" | "away"; // 最高機率的向
  scoreline?: string; // 可選：最可能比分
  model_id?: string; // 第三方模型 Gateway ID（kind=ai）
  url?: string;
  note?: string; // 繁中一句說明 / take
}

/** 綜合共識（ensemble）：本站 Opus 4.8 主預測 + 三家第三方 AI 的加權平均。 */
export interface Consensus {
  scoreline: string;
  outcome: "home" | "draw" | "away";
  win_prob: { home: number; draw: number; away: number };
  models_used: number; // 參與模型數（含主預測）
  logic: string; // 綜合邏輯一句（繁中）
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
  benchmarks?: Benchmark[];
  consensus?: Consensus; // 多模型綜合共識
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

/** 校準（可靠度）資料：信心分桶 vs 實際命中率。 */
export interface CalibrationBucket {
  bucket: string; // 例："50-60%"
  lower: number; // 0.5
  upper: number; // 0.6
  mid: number; // 代表信心（桶中點或平均）
  count: number; // 該桶內預測場數
  hit_rate: number | null; // 實際勝負命中率 0..1（count=0 時為 null）
  avg_confidence: number | null; // 該桶平均宣稱信心
}

export interface CalibrationData {
  tournament: string;
  last_updated: string;
  total_evaluated: number;
  buckets: CalibrationBucket[];
  brier_score: number | null; // 整體 Brier 分數（越低越好）
  ece: number | null; // Expected Calibration Error（越低越好）
  overconfidence: number | null; // 平均信心 - 平均命中率（正=過度自信）
  notes?: string;
}

/** 對比基準線排行榜。 */
export interface BenchmarkScoreRow {
  source: string;
  kind: "ai" | "betting" | "model" | "market";
  evaluated: number;
  outcome_correct: number;
  outcome_accuracy: number;
  exact_correct: number;
  exact_accuracy: number;
  brier_score: number | null;
}

export interface BenchmarkScoresData {
  tournament: string;
  last_updated: string;
  total_matches_scored: number;
  leaderboard: BenchmarkScoreRow[];
  notes?: string;
}

/** 賽後覆盤：為何命中 / 失準的短評。 */
export interface Postmortem {
  match: number;
  home: string;
  away: string;
  stage: string;
  predicted: string; // AI 預測比分
  predicted_outcome: "home" | "draw" | "away";
  final: string; // 實際比分
  actual_outcome: "home" | "draw" | "away";
  outcome_correct: boolean;
  exact_correct: boolean;
  verdict: "exact" | "outcome" | "miss"; // 命中比分 / 命中勝負 / 未中
  run_id: string;
  headline: string; // 一句標題（繁中）
  review: string; // 數句覆盤分析（繁中）
  lessons?: string[]; // 可沉澱的教訓/規律（繁中）
  vs_benchmarks?: string; // 與博彩/Opta 基準線相比誰更準（繁中）
  generated_at: string;
  model?: string;
}

export interface PostmortemsData {
  tournament: string;
  last_updated: string;
  postmortems: Postmortem[];
}

export interface StatusData {
  last_updated: string;
  total_matches: number;
  prediction_files: number;
  total_runs: number;
  runs: string[];
  accuracy: AccuracyData["metrics"];
}
