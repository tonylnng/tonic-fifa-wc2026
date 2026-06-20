import { Fragment, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  CalibrationData,
  BenchmarkScoresData,
  BenchmarkScoreRow,
} from "@/lib/types";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import {
  Gauge,
  Scale,
  TriangleAlert,
  Trophy,
  ChevronDown,
  ChevronRight,
  Check,
  X,
  Target,
} from "lucide-react";
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";

function pct(v: number | null | undefined) {
  if (v === null || v === undefined) return "—";
  return `${Math.round(v * 100)}%`;
}

function Metric({
  icon: Icon,
  label,
  value,
  sub,
  tone,
}: {
  icon: any;
  label: string;
  value: string;
  sub?: string;
  tone?: "good" | "bad" | "neutral";
}) {
  const color =
    tone === "good"
      ? "text-primary"
      : tone === "bad"
      ? "text-destructive"
      : "";
  return (
    <div className="bg-card border border-card-border rounded-xl p-4">
      <div className="flex items-center gap-2 text-muted-foreground text-xs mb-2">
        <Icon className="w-4 h-4" /> {label}
      </div>
      <div className={`text-xl font-extrabold tabular-nums ${color}`}>{value}</div>
      {sub && <div className="text-xs text-muted-foreground mt-1">{sub}</div>}
    </div>
  );
}

/** 自訂 tooltip：只顯示散點（信心分桶）本身的數值，避免與對角線錄位。 */
function ReliabilityTooltip({ active, payload }: any) {
  if (!active || !payload || payload.length === 0) return null;
  // 只取含 bucket 欄位的散點 payload（排除對角線 ideal 系列）
  const pt = payload.find((p: any) => p?.payload && p.payload.bucket !== undefined)?.payload;
  if (!pt) return null;
  return (
    <div
      style={{
        background: "hsl(var(--card))",
        border: "1px solid hsl(var(--border))",
        borderRadius: 8,
        fontSize: 12,
        padding: "8px 10px",
      }}
    >
      <div style={{ fontWeight: 600, marginBottom: 4 }}>{pt.bucket} 信心區間</div>
      <div>宣稱信心：{pt.x}%</div>
      <div>實際命中率：{pt.y}%</div>
      <div style={{ color: "hsl(var(--muted-foreground))" }}>樣本數：{pt.count} 場</div>
    </div>
  );
}

/** 可靠度圖：x = 宣稱信心，y = 實際命中率；對角線為完美校準。 */
function ReliabilityChart({ cal }: { cal: CalibrationData }) {
  const points = cal.buckets
    .filter((b) => b.count > 0 && b.avg_confidence !== null && b.hit_rate !== null)
    .map((b) => ({
      x: Math.round((b.avg_confidence as number) * 100),
      y: Math.round((b.hit_rate as number) * 100),
      count: b.count,
      bucket: b.bucket,
    }));


  return (
    <div className="bg-card border border-card-border rounded-xl p-4">
      <h3 className="text-sm font-semibold mb-1 flex items-center gap-1.5">
        <Gauge className="w-4 h-4 text-chart-2" />
        可靠度圖（信心 vs 實際命中率）
      </h3>
      <p className="text-xs text-muted-foreground mb-3">
        點越貼近對角線代表校準越好；落在對角線下方代表 AI 過度自信。
      </p>
      {points.length === 0 ? (
        <div className="h-64 flex items-center justify-center text-sm text-muted-foreground text-center px-4">
          尚無足夠已完成且具賽前預測的比賽。校準曲線會在累積比賽後自動繪製。
        </div>
      ) : (
        <ResponsiveContainer width="100%" height={300}>
          <ScatterChart margin={{ top: 10, right: 16, bottom: 24, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
            <XAxis
              type="number"
              dataKey="x"
              domain={[0, 100]}
              ticks={[0, 25, 50, 75, 100]}
              tick={{ fontSize: 11 }}
              label={{ value: "宣稱信心 %", position: "bottom", fontSize: 11 }}
            />
            <YAxis
              type="number"
              dataKey="y"
              domain={[0, 100]}
              ticks={[0, 25, 50, 75, 100]}
              tick={{ fontSize: 11 }}
              label={{ value: "命中率 %", angle: -90, position: "insideLeft", fontSize: 11 }}
            />
            {/* 完美校準對角線（參考線，不參與 tooltip） */}
            <ReferenceLine
              segment={[
                { x: 0, y: 0 },
                { x: 100, y: 100 },
              ]}
              stroke="hsl(var(--muted-foreground))"
              strokeDasharray="5 5"
              ifOverflow="extendDomain"
            />
            <Tooltip
              cursor={{ strokeDasharray: "3 3" }}
              content={<ReliabilityTooltip />}
            />
            <Scatter
              data={points}
              fill="hsl(var(--chart-2))"
              isAnimationActive={false}
            />
          </ScatterChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}

/** 某 AI 模型展開後的逐場明細表：每場預測 vs 實際 + 勝負/比分命中圖示。 */
function MatchDetailTable({ row }: { row: BenchmarkScoreRow }) {
  const matches = (row.matches ?? []).slice().sort((a, b) => a.match - b.match);
  if (matches.length === 0) {
    return (
      <div className="px-4 py-3 text-xs text-muted-foreground">
        尚無逐場明細資料。
      </div>
    );
  }
  return (
    <div className="bg-muted/30 px-3 py-3 border-t border-border/60">
      <div className="flex flex-wrap items-center gap-x-4 gap-y-1 mb-2 text-[11px] text-muted-foreground">
        <span className="flex items-center gap-1">
          <Check className="w-3.5 h-3.5 text-primary" /> 勝負命中
        </span>
        <span className="flex items-center gap-1">
          <Target className="w-3.5 h-3.5 text-chart-2" /> 比分命中
        </span>
        <span className="flex items-center gap-1">
          <X className="w-3.5 h-3.5 text-destructive" /> 未中
        </span>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-xs">
          <thead>
            <tr className="text-muted-foreground border-b border-border/60">
              <th className="text-left font-medium px-2 py-1.5 whitespace-nowrap">場次</th>
              <th className="text-left font-medium px-2 py-1.5">對戰</th>
              <th className="text-center font-medium px-2 py-1.5 whitespace-nowrap">預測</th>
              <th className="text-center font-medium px-2 py-1.5 whitespace-nowrap">信心</th>
              <th className="text-center font-medium px-2 py-1.5 whitespace-nowrap">實際</th>
              <th className="text-center font-medium px-2 py-1.5 whitespace-nowrap">勝負</th>
              <th className="text-center font-medium px-2 py-1.5 whitespace-nowrap">比分</th>
            </tr>
          </thead>
          <tbody>
            {matches.map((m) => (
              <tr
                key={m.match}
                className={`border-b border-border/40 last:border-0 ${
                  m.exact_hit ? "bg-chart-2/10" : ""
                }`}
              >
                <td className="px-2 py-1.5 tabular-nums text-muted-foreground whitespace-nowrap">
                  #{m.match}
                </td>
                <td className="px-2 py-1.5 whitespace-nowrap">
                  {m.home_zh} <span className="text-muted-foreground">vs</span>{" "}
                  {m.away_zh}
                </td>
                <td className="px-2 py-1.5 text-center tabular-nums whitespace-nowrap">
                  {m.pred_scoreline ?? "—"}
                </td>
                <td className="px-2 py-1.5 text-center tabular-nums whitespace-nowrap text-muted-foreground">
                  {pct(m.confidence)}
                </td>
                <td className="px-2 py-1.5 text-center tabular-nums font-semibold whitespace-nowrap">
                  {m.final_scoreline}
                </td>
                <td className="px-2 py-1.5 text-center">
                  {m.outcome_hit ? (
                    <Check className="w-4 h-4 text-primary inline" />
                  ) : (
                    <X className="w-4 h-4 text-destructive inline" />
                  )}
                </td>
                <td className="px-2 py-1.5 text-center">
                  {m.exact_hit ? (
                    <Target className="w-4 h-4 text-chart-2 inline" />
                  ) : (
                    <span className="text-muted-foreground">–</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function Leaderboard({ data }: { data: BenchmarkScoresData }) {
  const lb = data.leaderboard;
  const [expanded, setExpanded] = useState<Record<number, boolean>>({});
  const toggle = (i: number) => setExpanded((s) => ({ ...s, [i]: !s[i] }));

  return (
    <div className="bg-card border border-card-border rounded-xl overflow-hidden">
      <div className="p-4 pb-2">
        <h3 className="text-sm font-semibold flex items-center gap-1.5">
          <Trophy className="w-4 h-4 text-chart-2" />
          AI vs 市場 vs 超級電腦 — 準確率排行
        </h3>
        <p className="text-xs text-muted-foreground mt-1">
          在 {data.total_matches_scored} 場已完成比賽上的對照計分（僅納入該來源有提供預測的場次）。點擊 AI 模型列可展開逐場命中明細。
        </p>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border text-muted-foreground text-xs">
              <th className="text-left font-medium px-3 py-2.5">來源</th>
              <th className="text-center font-medium px-3 py-2.5 whitespace-nowrap">勝負命中</th>
              <th className="text-center font-medium px-3 py-2.5 whitespace-nowrap">比分命中</th>
              <th className="text-center font-medium px-3 py-2.5 whitespace-nowrap">Brier↓</th>
            </tr>
          </thead>
          <tbody>
            {lb.map((r, i) => {
              const isAI = r.kind === "ai";
              const open = !!expanded[i];
              return (
                <Fragment key={i}>
                  <tr
                    onClick={isAI ? () => toggle(i) : undefined}
                    className={`border-b border-border/60 last:border-0 ${
                      isAI ? "bg-primary/5 cursor-pointer hover:bg-primary/10" : ""
                    } ${open ? "border-b-0" : ""}`}
                    data-testid={`leaderboard-row-${i}`}
                  >
                    <td className="px-3 py-2.5 font-medium whitespace-nowrap">
                      <span className="flex items-center gap-1.5">
                        {isAI ? (
                          open ? (
                            <ChevronDown className="w-3.5 h-3.5 text-muted-foreground shrink-0" />
                          ) : (
                            <ChevronRight className="w-3.5 h-3.5 text-muted-foreground shrink-0" />
                          )
                        ) : (
                          <span className="w-3.5 shrink-0" />
                        )}
                        {isAI ? (
                          <Badge className="bg-primary text-primary-foreground text-[10px] px-1 py-0">
                            AI
                          </Badge>
                        ) : (
                          <Badge variant="outline" className="text-[10px] px-1 py-0">
                            {r.kind === "betting" ? "博彩" : r.kind === "market" ? "市場" : "模型"}
                          </Badge>
                        )}
                        {r.source}
                        {r.stale && (
                          <Badge
                            variant="outline"
                            className="text-[10px] px-1 py-0 text-amber-500 border-amber-500/50 whitespace-nowrap"
                          >
                            已停更·止於 #{r.latest_match}
                          </Badge>
                        )}
                      </span>
                    </td>
                    <td className="px-3 py-2.5 text-center tabular-nums">
                      {pct(r.outcome_accuracy)}
                      <span className="text-muted-foreground text-xs ml-1">
                        ({r.outcome_correct}/{r.evaluated})
                      </span>
                    </td>
                    <td className="px-3 py-2.5 text-center tabular-nums">
                      {pct(r.exact_accuracy)}
                      <span className="text-muted-foreground text-xs ml-1">
                        ({r.exact_correct}/{r.evaluated})
                      </span>
                    </td>
                    <td className="px-3 py-2.5 text-center tabular-nums text-muted-foreground">
                      {r.brier_score === null ? "—" : r.brier_score.toFixed(3)}
                    </td>
                  </tr>
                  {isAI && open && (
                    <tr>
                      <td colSpan={4} className="p-0">
                        <MatchDetailTable row={r} />
                      </td>
                    </tr>
                  )}
                </Fragment>
              );
            })}
          </tbody>
        </table>
      </div>
      <p className="text-[11px] text-muted-foreground p-3 pt-2">
        Brier 分數越低代表機率校準越好（0 = 完美，1 = 最差）。標「已停更」者為早期手動寫入的公開市場/超級電腦基準線，後續批次未再供應資料，樣本有限僅供參考。
      </p>
    </div>
  );
}

export function CalibrationTab() {
  const calQ = useQuery<CalibrationData>({ queryKey: ["/api/calibration"] });
  const benchQ = useQuery<BenchmarkScoresData>({
    queryKey: ["/api/benchmark-scores"],
  });

  if (calQ.isLoading || benchQ.isLoading) {
    return <Skeleton className="h-96 rounded-xl" />;
  }

  const cal = calQ.data;
  const bench = benchQ.data;

  return (
    <div className="space-y-4">
      {cal && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          <Metric
            icon={Gauge}
            label="已評估場數"
            value={`${cal.total_evaluated}`}
            sub="納入校準的比賽"
          />
          <Metric
            icon={TriangleAlert}
            label="過度自信"
            value={
              cal.overconfidence === null
                ? "—"
                : `${cal.overconfidence > 0 ? "+" : ""}${Math.round(cal.overconfidence * 100)}pp`
            }
            sub="信心 − 命中率（正=過度自信）"
            tone={
              cal.overconfidence === null
                ? "neutral"
                : cal.overconfidence > 0.1
                ? "bad"
                : "good"
            }
          />
          <Metric
            icon={Scale}
            label="ECE"
            value={cal.ece === null ? "—" : cal.ece.toFixed(3)}
            sub="期望校準誤差（越低越好）"
          />
          <Metric
            icon={Scale}
            label="Brier 分數"
            value={cal.brier_score === null ? "—" : cal.brier_score.toFixed(3)}
            sub="機率準確度（越低越好）"
          />
        </div>
      )}

      {cal?.notes && (
        <div className="bg-chart-2/10 border border-chart-2/30 rounded-lg px-3 py-2 text-sm">
          {cal.notes}
        </div>
      )}

      {cal && <ReliabilityChart cal={cal} />}

      {bench && bench.leaderboard.length > 0 ? (
        <Leaderboard data={bench} />
      ) : (
        <div className="bg-card border border-card-border rounded-xl p-4 text-sm text-muted-foreground">
          對比基準線排行將在已完成比賽具備 AI 預測與基準線資料後自動生成。
        </div>
      )}
    </div>
  );
}
