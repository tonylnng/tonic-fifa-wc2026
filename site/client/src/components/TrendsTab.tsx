import { useMemo, useState } from "react";
import { PredictionsData, Prediction } from "@/lib/types";
import { flag, zh } from "@/lib/flags";
import { stageZh } from "@/lib/stage";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { TrendingUp, GitCommitVertical } from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

function runLabel(ts: string) {
  try {
    return new Date(ts).toLocaleString("zh-HK", {
      timeZone: "Asia/Hong_Kong",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return ts;
  }
}

// Build chart rows from a match's batch list (oldest -> newest along x-axis).
function buildSeries(list: Prediction[]) {
  return [...list]
    .sort((a, b) => (a.run_timestamp || "").localeCompare(b.run_timestamp || ""))
    .map((p) => ({
      run: runLabel(p.run_timestamp),
      run_id: p.run_id,
      confidence: Math.round(p.prediction.confidence * 100),
      home: Math.round(p.prediction.win_prob.home * 100),
      draw: Math.round(p.prediction.win_prob.draw * 100),
      away: Math.round(p.prediction.win_prob.away * 100),
      scoreline: p.prediction.scoreline,
    }));
}

export function TrendsTab({ preds }: { preds: PredictionsData }) {
  // Only matches that have more than one batch are interesting for trends.
  const multiMatches = useMemo(() => {
    return Object.entries(preds)
      .filter(([, list]) => list.length > 1)
      .map(([, list]) => list[0])
      .sort((a, b) => a.match - b.match);
  }, [preds]);

  const [selected, setSelected] = useState<number | null>(null);
  const activeMatch = selected ?? multiMatches[0]?.match ?? null;
  const activeList =
    activeMatch != null ? preds[String(activeMatch)] || [] : [];
  const series = useMemo(() => buildSeries(activeList), [activeList]);
  const head = activeList[0];

  if (multiMatches.length === 0) {
    return (
      <div className="text-center py-16 text-muted-foreground">
        <TrendingUp className="w-10 h-10 mx-auto mb-3 opacity-40" />
        <p className="max-w-md mx-auto">
          目前尚無可比較的多批次比賽。預測演變只適用於「開賽前被預測超過一次」的比賽——
          需累積 2 個以上預測批次，才能以折線圖呈現 AI 信心度與勝率隨情報更新的變化。
        </p>
        <p className="max-w-md mx-auto mt-3 text-xs opacity-80">
          自 2026-06-23 起預測排程改為每日一次（成本優化），多數比賽只會在開賽前進入預測窗口一次、
          因而只有單一批次，不會出現在此頁；這屬正常情形，並非資料停止更新。
        </p>
      </div>
    );
  }

  return (
    <div>
      <p className="text-sm text-muted-foreground mb-1">
        選擇一場比賽，查看 AI 預測在每次執行批次間的演變（信心度與三向勝率，單位
        %）。
      </p>
      <p className="text-xs text-muted-foreground/80 mb-3">
        僅顯示開賽前被多次預測（≥2 批次）的比賽。每日一次模式下，多數比賽只有單一預測批次，
        不會出現在此清單——這屬正常，並非更新中斷。
      </p>

      {/* match selector chips */}
      <div className="flex gap-2 overflow-x-auto pb-2 mb-4">
        {multiMatches.map((p) => (
          <button
            key={p.match}
            onClick={() => setSelected(p.match)}
            className={`text-xs px-3 py-1.5 rounded-full border whitespace-nowrap hover-elevate ${
              activeMatch === p.match
                ? "bg-primary text-primary-foreground border-primary"
                : "border-border"
            }`}
            data-testid={`trend-match-${p.match}`}
          >
            #{p.match} {flag(p.home)} {zh(p.home)} vs {zh(p.away)} {flag(p.away)}
          </button>
        ))}
      </div>

      {head && (
        <div className="bg-card border border-card-border rounded-xl p-4">
          <div className="flex items-center justify-between flex-wrap gap-2 mb-4">
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="text-xs">
                #{head.match} · {stageZh(head.stage)}
              </Badge>
              <span className="text-sm font-semibold">
                {flag(head.home)} {zh(head.home)} vs {zh(head.away)}{" "}
                {flag(head.away)}
              </span>
            </div>
            <span className="flex items-center gap-1 text-xs text-muted-foreground">
              <GitCommitVertical className="w-3.5 h-3.5" />
              {activeList.length} 個批次
            </span>
          </div>

          {/* Confidence trend */}
          <h4 className="text-xs font-semibold text-muted-foreground mb-2">
            信心度演變
          </h4>
          <div className="h-48 w-full mb-6" data-testid="chart-confidence">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={series} margin={{ top: 5, right: 10, bottom: 0, left: -20 }}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-border" />
                <XAxis
                  dataKey="run"
                  tick={{ fontSize: 11 }}
                  className="text-muted-foreground"
                />
                <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} />
                <Tooltip
                  contentStyle={{
                    fontSize: 12,
                    borderRadius: 8,
                    background: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                  }}
                  formatter={(v: any) => [`${v}%`, "信心度"]}
                />
                <Line
                  type="monotone"
                  dataKey="confidence"
                  name="信心度"
                  stroke="hsl(var(--chart-2))"
                  strokeWidth={2.5}
                  dot={{ r: 4 }}
                  activeDot={{ r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Win-probability trend */}
          <h4 className="text-xs font-semibold text-muted-foreground mb-2">
            三向勝率演變
          </h4>
          <div className="h-56 w-full" data-testid="chart-winprob">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={series} margin={{ top: 5, right: 10, bottom: 0, left: -20 }}>
                <CartesianGrid strokeDasharray="3 3" className="stroke-border" />
                <XAxis
                  dataKey="run"
                  tick={{ fontSize: 11 }}
                  className="text-muted-foreground"
                />
                <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} />
                <Tooltip
                  contentStyle={{
                    fontSize: 12,
                    borderRadius: 8,
                    background: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                  }}
                  formatter={(v: any, n: any) => [`${v}%`, n]}
                />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Line
                  type="monotone"
                  dataKey="home"
                  name={`主勝（${zh(head.home)}）`}
                  stroke="hsl(var(--chart-1))"
                  strokeWidth={2}
                  dot={{ r: 3 }}
                />
                <Line
                  type="monotone"
                  dataKey="draw"
                  name="和局"
                  stroke="hsl(var(--muted-foreground))"
                  strokeWidth={2}
                  strokeDasharray="4 4"
                  dot={{ r: 3 }}
                />
                <Line
                  type="monotone"
                  dataKey="away"
                  name={`客勝（${zh(head.away)}）`}
                  stroke="hsl(var(--chart-3))"
                  strokeWidth={2}
                  dot={{ r: 3 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* per-batch scoreline strip */}
          <div className="flex items-center gap-2 flex-wrap mt-4 pt-4 border-t border-border">
            <span className="text-xs text-muted-foreground">各批次預測比分：</span>
            {series.map((s, i) => (
              <Badge
                key={i}
                variant={i === series.length - 1 ? "default" : "outline"}
                className="text-[11px] font-mono"
              >
                {s.scoreline}
              </Badge>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
