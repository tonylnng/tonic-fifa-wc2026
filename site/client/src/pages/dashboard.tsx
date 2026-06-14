import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  FixturesData,
  PredictionsData,
  ResultsData,
  AccuracyData,
  StatusData,
  Fixture,
} from "@/lib/types";
import { flag, zh } from "@/lib/flags";
import { stageZh, outcomeZh } from "@/lib/stage";
import { kickoffHkt, countdown } from "@/lib/utils";
import { Header } from "@/components/Header";
import { PredictionCard } from "@/components/PredictionCard";
import { TrendsTab } from "@/components/TrendsTab";
import { CalibrationTab } from "@/components/CalibrationTab";
import { PostmortemsTab } from "@/components/PostmortemsTab";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Target,
  Crosshair,
  Database,
  CalendarClock,
  Search,
  Trophy,
  History,
} from "lucide-react";

function runLabelZh(runId: string) {
  const m = runId.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2})(\d{2})Z$/);
  if (!m) return runId;
  const utc = new Date(
    Date.UTC(+m[1], +m[2] - 1, +m[3], +m[4], +m[5])
  );
  return utc.toLocaleString("zh-HK", {
    timeZone: "Asia/Hong_Kong",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function Stat({
  icon: Icon,
  label,
  value,
  sub,
}: {
  icon: any;
  label: string;
  value: string;
  sub?: string;
}) {
  return (
    <div className="bg-card border border-card-border rounded-xl p-4">
      <div className="flex items-center gap-2 text-muted-foreground text-xs mb-2">
        <Icon className="w-4 h-4" /> {label}
      </div>
      <div className="text-xl font-extrabold tabular-nums">{value}</div>
      {sub && <div className="text-xs text-muted-foreground mt-1">{sub}</div>}
    </div>
  );
}

export default function Dashboard() {
  const fixturesQ = useQuery<FixturesData>({ queryKey: ["/api/fixtures"] });
  const predsQ = useQuery<PredictionsData>({ queryKey: ["/api/predictions"] });
  const resultsQ = useQuery<ResultsData>({ queryKey: ["/api/results"] });
  const accuracyQ = useQuery<AccuracyData>({ queryKey: ["/api/accuracy"] });
  const statusQ = useQuery<StatusData>({ queryKey: ["/api/status"] });

  const loading =
    fixturesQ.isLoading || predsQ.isLoading || resultsQ.isLoading;

  const fixtures = fixturesQ.data;
  const preds = predsQ.data || {};
  const results = resultsQ.data;
  const accuracy = accuracyQ.data;

  const resultByMatch = useMemo(() => {
    const m: Record<number, ResultsData["results"][0]> = {};
    results?.results.forEach((r) => (m[r.match] = r));
    return m;
  }, [results]);

  const fixtureByMatch = useMemo(() => {
    const m: Record<number, Fixture> = {};
    fixtures?.fixtures.forEach((f) => (m[f.match] = f));
    return m;
  }, [fixtures]);

  // ----- Feature C: batch snapshot selector -----
  const allRuns = statusQ.data?.runs || [];
  const [snapshot, setSnapshot] = useState<string>("latest");
  const isHistorical = snapshot !== "latest";

  // The prediction shown per match for the currently selected snapshot.
  // Feature A: upcoming / live matches are pinned to the top, sorted by
  // proximity to kickoff; completed and past matches fall to the bottom.
  const shownList = useMemo(() => {
    const out: any[] = [];
    for (const [, list] of Object.entries(preds)) {
      if (snapshot === "latest") {
        out.push(list[0]); // list already newest-first
      } else {
        const sorted = [...list].sort((a, b) =>
          (b.run_timestamp || "").localeCompare(a.run_timestamp || "")
        );
        const pick = sorted.find((p) => (p.run_id || "") <= snapshot);
        if (pick) out.push(pick);
      }
    }
    // Historical snapshots keep the simple match-number order.
    if (snapshot !== "latest") {
      return out.sort((a, b) => a.match - b.match);
    }
    const now = Date.now();
    // rank: 0 = live, 1 = upcoming (sooner first), 2 = completed, 3 = past-no-result
    const rankOf = (p: any) => {
      const f = fixtureByMatch[p.match];
      const done = !!resultByMatch[p.match];
      const c = f?.kickoff_utc ? countdown(f, now) : null;
      if (!done && c?.phase === "live") return 0;
      if (!done && c?.phase === "upcoming") return 1;
      if (done) return 2;
      return 3;
    };
    return out.sort((a, b) => {
      const ra = rankOf(a);
      const rb = rankOf(b);
      if (ra !== rb) return ra - rb;
      const fa = fixtureByMatch[a.match];
      const fb = fixtureByMatch[b.match];
      // Within upcoming/live: soonest kickoff first.
      if (ra <= 1) {
        const ta = fa?.kickoff_utc ? new Date(fa.kickoff_utc).getTime() : Infinity;
        const tb = fb?.kickoff_utc ? new Date(fb.kickoff_utc).getTime() : Infinity;
        if (ta !== tb) return ta - tb;
      }
      // Completed: most recent kickoff first; otherwise by match number.
      if (ra === 2) {
        const ta = fa?.kickoff_utc ? new Date(fa.kickoff_utc).getTime() : 0;
        const tb = fb?.kickoff_utc ? new Date(fb.kickoff_utc).getTime() : 0;
        if (ta !== tb) return tb - ta;
      }
      return a.match - b.match;
    });
  }, [preds, snapshot, fixtureByMatch, resultByMatch]);

  return (
    <div className="min-h-screen bg-background">
      <Header
        lastUpdated={
          statusQ.data?.last_updated ||
          accuracy?.last_updated ||
          fixtures?.last_updated
        }
      />
      <main className="max-w-6xl mx-auto px-4 sm:px-6 py-6">
        {/* Hero strip */}
        <div className="mb-6">
          <h1 className="text-xl font-extrabold tracking-tight flex items-center gap-2">
            <Trophy className="w-5 h-5 text-chart-2" />
            FIFA World Cup 2026
          </h1>
          <p className="text-sm text-muted-foreground mt-1">
            美國 · 加拿大 · 墨西哥 · 48 隊 · 104 場 · Opus 4.8 預測 · 近賽每場 100+ 來源
          </p>
        </div>

        {/* Stat row */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
          <Stat
            icon={Target}
            label="勝負準確率"
            value={
              accuracy && accuracy.metrics.total_evaluated > 0
                ? `${Math.round(accuracy.metrics.outcome_accuracy * 100)}%`
                : "—"
            }
            sub={
              accuracy
                ? `${accuracy.metrics.outcome_correct}/${accuracy.metrics.total_evaluated} 場`
                : ""
            }
          />
          <Stat
            icon={Crosshair}
            label="比分準確率"
            value={
              accuracy && accuracy.metrics.total_evaluated > 0
                ? `${Math.round(accuracy.metrics.exact_score_accuracy * 100)}%`
                : "—"
            }
            sub={
              accuracy
                ? `${accuracy.metrics.exact_score_correct}/${accuracy.metrics.total_evaluated} 場`
                : ""
            }
          />
          <Stat
            icon={CalendarClock}
            label="已完成比賽"
            value={`${results?.results.length ?? 0}`}
            sub={`/ ${fixtures?.total_matches ?? 104} 場`}
          />
          <Stat
            icon={Database}
            label="預測執行批次"
            value={`${statusQ.data?.total_runs ?? 0}`}
            sub={`${statusQ.data?.prediction_files ?? 0} 份預測檔`}
          />
        </div>

        <Tabs defaultValue="predictions">
          <TabsList className="mb-5">
            <TabsTrigger value="predictions" data-testid="tab-predictions">
              AI 預測
            </TabsTrigger>
            <TabsTrigger value="trends" data-testid="tab-trends">
              預測演變
            </TabsTrigger>
            <TabsTrigger value="fixtures" data-testid="tab-fixtures">
              賽程 Master List
            </TabsTrigger>
            <TabsTrigger value="results" data-testid="tab-results">
              結果與準確率
            </TabsTrigger>
            <TabsTrigger value="calibration" data-testid="tab-calibration">
              校準與基準
            </TabsTrigger>
            <TabsTrigger value="postmortems" data-testid="tab-postmortems">
              賽後覆盤
            </TabsTrigger>
          </TabsList>

          {/* PREDICTIONS */}
          <TabsContent value="predictions">
            {loading ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {[...Array(6)].map((_, i) => (
                  <Skeleton key={i} className="h-48 rounded-xl" />
                ))}
              </div>
            ) : shownList.length === 0 ? (
              <div className="text-center py-16 text-muted-foreground">
                <Database className="w-10 h-10 mx-auto mb-3 opacity-40" />
                <p>尚未有預測資料。自動流程每 8 小時會產生新的預測批次。</p>
              </div>
            ) : (
              <>
                <div className="flex flex-col sm:flex-row sm:items-center gap-2 mb-3">
                  <p className="text-sm text-muted-foreground flex-1">
                    {isHistorical
                      ? "正在檢視歷史批次快照（點擊卡片可看完整分析與歷史演變）"
                      : "即將開賽的比賽已自動置頂並顯示倒數；點擊卡片可看完整分析、來源與歷史版本。"}
                  </p>
                  <div className="flex items-center gap-2">
                    <History className="w-4 h-4 text-muted-foreground" />
                    <Select value={snapshot} onValueChange={setSnapshot}>
                      <SelectTrigger
                        className="w-[200px] h-9 text-xs"
                        data-testid="select-snapshot"
                      >
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="latest">最新批次</SelectItem>
                        {allRuns.map((r) => (
                          <SelectItem key={r} value={r}>
                            {runLabelZh(r)} 快照
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                {isHistorical && (
                  <div className="flex items-center gap-2 mb-3 text-xs bg-chart-2/10 border border-chart-2/30 rounded-lg px-3 py-2">
                    <History className="w-3.5 h-3.5 text-chart-2 shrink-0" />
                    <span>
                      正在顯示 <span className="font-mono font-semibold">{runLabelZh(snapshot)}</span>{" "}
                      的預測狀態快照。選「最新批次」可返回現時。
                    </span>
                  </div>
                )}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                  {shownList.map((p) => (
                    <PredictionCard
                      key={p.match}
                      pred={p}
                      result={resultByMatch[p.match]}
                      history={preds[String(p.match)]}
                      fixture={fixtureByMatch[p.match]}
                    />
                  ))}
                </div>
              </>
            )}
          </TabsContent>

          {/* TRENDS */}
          <TabsContent value="trends">
            {loading ? (
              <Skeleton className="h-96 rounded-xl" />
            ) : (
              <TrendsTab preds={preds} />
            )}
          </TabsContent>

          {/* FIXTURES */}
          <TabsContent value="fixtures">
            <FixturesTab fixtures={fixtures} preds={preds} />
          </TabsContent>

          {/* RESULTS */}
          <TabsContent value="results">
            <ResultsTab results={results} preds={preds} accuracy={accuracy} />
          </TabsContent>

          {/* CALIBRATION & BENCHMARKS */}
          <TabsContent value="calibration">
            <CalibrationTab />
          </TabsContent>

          {/* POSTMORTEMS */}
          <TabsContent value="postmortems">
            <PostmortemsTab />
          </TabsContent>
        </Tabs>

        <footer className="text-center text-xs text-muted-foreground mt-12 pb-8">
          自動更新 · 每 8 小時收集最新情況並重新預測（16 強起每 4 小時）· 所有預測批次獨立保存於 JSON
        </footer>
      </main>
    </div>
  );
}

/* ---------- Fixtures Master List ---------- */
function FixturesTab({
  fixtures,
  preds,
}: {
  fixtures?: FixturesData;
  preds: PredictionsData;
}) {
  const [q, setQ] = useState("");
  const [stageFilter, setStageFilter] = useState("all");

  const stages = useMemo(() => {
    if (!fixtures) return [];
    const order = [
      "Group A","Group B","Group C","Group D","Group E","Group F",
      "Group G","Group H","Group I","Group J","Group K","Group L",
      "Round of 32","Round of 16","Quarter-final","Semi-final","Third Place","Final",
    ];
    const present = new Set(fixtures.fixtures.map((f) => f.stage));
    return order.filter((s) => present.has(s));
  }, [fixtures]);

  const rows = useMemo(() => {
    if (!fixtures) return [];
    return fixtures.fixtures.filter((f) => {
      if (stageFilter !== "all" && f.stage !== stageFilter) return false;
      if (!q) return true;
      const hay = `${f.home} ${f.away} ${zh(f.home)} ${zh(f.away)} ${f.venue} ${f.city}`.toLowerCase();
      return hay.includes(q.toLowerCase());
    });
  }, [fixtures, q, stageFilter]);

  if (!fixtures) return <Skeleton className="h-96 rounded-xl" />;

  return (
    <div>
      <div className="flex flex-col sm:flex-row gap-3 mb-4">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
          <Input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="搜尋國家、球場、城市…"
            className="pl-9"
            data-testid="input-search-fixtures"
          />
        </div>
        <div className="flex gap-2 overflow-x-auto pb-1">
          <button
            onClick={() => setStageFilter("all")}
            className={`text-xs px-3 py-1.5 rounded-full border whitespace-nowrap hover-elevate ${
              stageFilter === "all"
                ? "bg-primary text-primary-foreground border-primary"
                : "border-border"
            }`}
            data-testid="filter-all"
          >
            全部
          </button>
          {stages.map((s) => (
            <button
              key={s}
              onClick={() => setStageFilter(s)}
              className={`text-xs px-3 py-1.5 rounded-full border whitespace-nowrap hover-elevate ${
                stageFilter === s
                  ? "bg-primary text-primary-foreground border-primary"
                  : "border-border"
              }`}
              data-testid={`filter-${s}`}
            >
              {stageZh(s)}
            </button>
          ))}
        </div>
      </div>

      <div className="bg-card border border-card-border rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border text-muted-foreground text-xs">
                <th className="text-left font-medium px-3 py-2.5 w-12">#</th>
                <th className="text-left font-medium px-3 py-2.5">階段</th>
                <th className="text-left font-medium px-3 py-2.5 whitespace-nowrap">開賽（香港時間）</th>
                <th className="text-right font-medium px-3 py-2.5">主隊</th>
                <th className="text-center font-medium px-3 py-2.5 w-24">比分 / 預測</th>
                <th className="text-left font-medium px-3 py-2.5">客隊</th>
                <th className="text-left font-medium px-3 py-2.5 hidden md:table-cell">場地</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((f: Fixture) => {
                const pred = preds[String(f.match)]?.[0];
                return (
                  <tr
                    key={f.match}
                    className="border-b border-border/60 last:border-0 hover-elevate"
                    data-testid={`row-fixture-${f.match}`}
                  >
                    <td className="px-3 py-2.5 text-muted-foreground tabular-nums">
                      {f.match}
                    </td>
                    <td className="px-3 py-2.5">
                      <Badge variant="secondary" className="text-[11px]">
                        {stageZh(f.stage)}
                      </Badge>
                    </td>
                    <td className="px-3 py-2.5 text-muted-foreground whitespace-nowrap text-xs">
                      {kickoffHkt(f, { withWeekday: true })}
                    </td>
                    <td className="px-3 py-2.5 text-right font-medium whitespace-nowrap">
                      {zh(f.home)} {flag(f.home)}
                    </td>
                    <td className="px-3 py-2.5 text-center">
                      {f.result ? (
                        <span className="font-mono font-bold tabular-nums">
                          {f.result.home}:{f.result.away}
                        </span>
                      ) : pred ? (
                        <span className="font-mono text-xs text-primary tabular-nums">
                          ◆ {pred.prediction.scoreline}
                        </span>
                      ) : (
                        <span className="text-muted-foreground text-xs">vs</span>
                      )}
                    </td>
                    <td className="px-3 py-2.5 font-medium whitespace-nowrap">
                      {flag(f.away)} {zh(f.away)}
                    </td>
                    <td className="px-3 py-2.5 text-muted-foreground text-xs hidden md:table-cell">
                      {f.city}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
      <p className="text-xs text-muted-foreground mt-2">
        共 {rows.length} 場 · ◆ 為 AI 預測比分 · 數字為已完成的最終比分
      </p>
    </div>
  );
}

/* ---------- Results & Accuracy ---------- */
function ResultsTab({
  results,
  preds,
  accuracy,
}: {
  results?: ResultsData;
  preds: PredictionsData;
  accuracy?: AccuracyData;
}) {
  if (!results) return <Skeleton className="h-96 rounded-xl" />;

  const rows = [...results.results].sort((a, b) => b.match - a.match);

  return (
    <div className="space-y-4">
      {accuracy && accuracy.metrics.total_evaluated > 0 ? (
        <div className="bg-card border border-card-border rounded-xl p-4">
          <h3 className="text-sm font-semibold mb-3">AI 預測準確率</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <div className="text-xs text-muted-foreground mb-1">勝負方向</div>
              <div className="text-2xl font-extrabold">
                {Math.round(accuracy.metrics.outcome_accuracy * 100)}%
              </div>
              <div className="text-xs text-muted-foreground">
                {accuracy.metrics.outcome_correct}/{accuracy.metrics.total_evaluated} 場命中
              </div>
            </div>
            <div>
              <div className="text-xs text-muted-foreground mb-1">精準比分</div>
              <div className="text-2xl font-extrabold">
                {Math.round(accuracy.metrics.exact_score_accuracy * 100)}%
              </div>
              <div className="text-xs text-muted-foreground">
                {accuracy.metrics.exact_score_correct}/{accuracy.metrics.total_evaluated} 場命中
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="bg-card border border-card-border rounded-xl p-4 text-sm text-muted-foreground">
          準確率將在已完成比賽有對應的賽前 AI 預測後自動計算。目前已記錄 {results.results.length} 場結果。
        </div>
      )}

      <div className="bg-card border border-card-border rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border text-muted-foreground text-xs">
                <th className="text-left font-medium px-3 py-2.5">#</th>
                <th className="text-left font-medium px-3 py-2.5">比賽</th>
                <th className="text-center font-medium px-3 py-2.5">最終</th>
                <th className="text-center font-medium px-3 py-2.5">AI 預測</th>
                <th className="text-center font-medium px-3 py-2.5">命中</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => {
                const pred = preds[String(r.match)]?.[0];
                const okOutcome = pred && pred.prediction.outcome === r.outcome;
                const okScore =
                  pred &&
                  pred.prediction.score.home === r.score.home &&
                  pred.prediction.score.away === r.score.away;
                return (
                  <tr
                    key={r.match}
                    className="border-b border-border/60 last:border-0"
                    data-testid={`row-result-${r.match}`}
                  >
                    <td className="px-3 py-2.5 text-muted-foreground tabular-nums">
                      {r.match}
                    </td>
                    <td className="px-3 py-2.5 font-medium whitespace-nowrap">
                      {flag(r.home)} {zh(r.home)} vs {zh(r.away)} {flag(r.away)}
                    </td>
                    <td className="px-3 py-2.5 text-center font-mono font-bold tabular-nums">
                      {r.score.home}:{r.score.away}
                    </td>
                    <td className="px-3 py-2.5 text-center font-mono tabular-nums text-muted-foreground">
                      {pred ? pred.prediction.scoreline : "—"}
                    </td>
                    <td className="px-3 py-2.5 text-center">
                      {!pred ? (
                        <span className="text-xs text-muted-foreground">無預測</span>
                      ) : okScore ? (
                        <Badge className="bg-primary text-primary-foreground text-[11px]">
                          比分
                        </Badge>
                      ) : okOutcome ? (
                        <Badge variant="secondary" className="text-[11px]">
                          勝負
                        </Badge>
                      ) : (
                        <Badge variant="outline" className="text-[11px] text-destructive">
                          未中
                        </Badge>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
