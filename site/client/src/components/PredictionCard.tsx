import { Prediction, ResultItem } from "@/lib/types";
import { flag, zh } from "@/lib/flags";
import { stageZh, outcomeZh } from "@/lib/stage";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { Check, X, TrendingUp, History, ChevronDown, ArrowRight } from "lucide-react";
import { useState } from "react";

function runTimeZh(ts: string) {
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

function DeltaChip({
  label,
  oldV,
  newV,
}: {
  label: string;
  oldV: number;
  newV: number;
}) {
  const diff = Math.round((newV - oldV) * 100);
  const up = diff > 0;
  const flat = diff === 0;
  return (
    <span className="text-[11px] text-muted-foreground">
      {label} {Math.round(oldV * 100)}%
      <ArrowRight className="inline w-3 h-3 mx-0.5" />
      {Math.round(newV * 100)}%
      {!flat && (
        <span className={up ? "text-primary ml-0.5" : "text-destructive ml-0.5"}>
          {up ? "↑" : "↓"}
          {Math.abs(diff)}
        </span>
      )}
    </span>
  );
}

function HistorySection({ history }: { history: Prediction[] }) {
  const [open, setOpen] = useState(false);
  if (!history || history.length <= 1) return null;
  const latest = history[0];
  const older = history.slice(1);
  return (
    <Collapsible open={open} onOpenChange={setOpen}>
      <CollapsibleTrigger asChild>
        <button
          className="flex items-center gap-2 text-sm font-semibold w-full text-left"
          data-testid={`btn-history-${latest.match}`}
        >
          <History className="w-4 h-4 text-chart-2" />
          歷史預測版本（{history.length} 個批次）
          <ChevronDown
            className={`w-4 h-4 ml-auto transition-transform ${open ? "rotate-180" : ""}`}
          />
        </button>
      </CollapsibleTrigger>
      <CollapsibleContent>
        <div className="mt-2 space-y-2">
          <div className="flex items-center gap-2 rounded-lg border border-primary/40 bg-primary/5 px-3 py-2">
            <Badge className="bg-primary text-primary-foreground text-[10px]">最新</Badge>
            <span className="font-mono font-bold">{latest.prediction.scoreline}</span>
            <span className="text-xs text-muted-foreground">
              {outcomeZh(latest.prediction.outcome)} · 信心{" "}
              {Math.round(latest.prediction.confidence * 100)}%
            </span>
            <span className="text-[11px] text-muted-foreground ml-auto">
              {runTimeZh(latest.run_timestamp)}
            </span>
          </div>
          {older.map((h, i) => {
            const scoreChanged =
              h.prediction.scoreline !== latest.prediction.scoreline;
            const outcomeChanged =
              h.prediction.outcome !== latest.prediction.outcome;
            return (
              <div
                key={i}
                className="rounded-lg border border-border px-3 py-2"
                data-testid={`history-row-${latest.match}-${i}`}
              >
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="font-mono font-bold text-muted-foreground">
                    {h.prediction.scoreline}
                  </span>
                  {scoreChanged && (
                    <Badge variant="outline" className="text-[10px] text-chart-2">
                      比分變動
                    </Badge>
                  )}
                  <span className="text-xs text-muted-foreground">
                    {outcomeZh(h.prediction.outcome)}
                  </span>
                  {outcomeChanged && (
                    <Badge variant="outline" className="text-[10px] text-destructive">
                      勝負反轉
                    </Badge>
                  )}
                  <span className="text-[11px] text-muted-foreground ml-auto">
                    {runTimeZh(h.run_timestamp)}
                  </span>
                </div>
                <div className="flex items-center gap-3 mt-1.5 flex-wrap">
                  <DeltaChip
                    label="信心"
                    oldV={h.prediction.confidence}
                    newV={latest.prediction.confidence}
                  />
                  <DeltaChip
                    label="主勝"
                    oldV={h.prediction.win_prob.home}
                    newV={latest.prediction.win_prob.home}
                  />
                  <DeltaChip
                    label="客勝"
                    oldV={h.prediction.win_prob.away}
                    newV={latest.prediction.win_prob.away}
                  />
                </div>
              </div>
            );
          })}
          <p className="text-[11px] text-muted-foreground">
            箭頭左側為舊批次數值，右側為最新批次；↑/↓ 表示 AI 隨情報更新後的調整幅度。
          </p>
        </div>
      </CollapsibleContent>
    </Collapsible>
  );
}

function ProbBar({ p }: { p: { home: number; draw: number; away: number } }) {
  const seg = (v: number, cls: string) => (
    <div className={cls} style={{ width: `${Math.round(v * 100)}%` }} />
  );
  return (
    <div className="flex h-2 w-full rounded-full overflow-hidden bg-muted">
      {seg(p.home, "bg-chart-1")}
      {seg(p.draw, "bg-muted-foreground/40")}
      {seg(p.away, "bg-chart-3")}
    </div>
  );
}

export function PredictionCard({
  pred,
  result,
  history,
}: {
  pred: Prediction;
  result?: ResultItem;
  history?: Prediction[];
}) {
  const correctOutcome = result && result.outcome === pred.prediction.outcome;
  const exactScore =
    result &&
    result.score.home === pred.prediction.score.home &&
    result.score.away === pred.prediction.score.away;

  return (
    <Dialog>
      <DialogTrigger asChild>
        <button
          className="text-left w-full bg-card border border-card-border rounded-xl p-4 hover-elevate active-elevate-2 transition"
          data-testid={`card-prediction-${pred.match}`}
        >
          <div className="flex items-center justify-between mb-3">
            <Badge variant="secondary" className="text-xs">
              #{pred.match} · {stageZh(pred.stage)}
            </Badge>
            {history && history.length > 1 && (
              <span
                className="flex items-center gap-1 text-[10px] text-chart-2 mr-auto ml-2"
                data-testid={`badge-history-${pred.match}`}
              >
                <History className="w-3 h-3" />
                {history.length} 批次
              </span>
            )}
            {result ? (
              correctOutcome ? (
                <span className="flex items-center gap-1 text-xs text-primary font-medium">
                  <Check className="w-3.5 h-3.5" />
                  {exactScore ? "命中比分" : "命中勝負"}
                </span>
              ) : (
                <span className="flex items-center gap-1 text-xs text-destructive font-medium">
                  <X className="w-3.5 h-3.5" /> 未命中
                </span>
              )
            ) : (
              <span className="text-xs text-muted-foreground">待賽</span>
            )}
          </div>

          <div className="flex items-center justify-between gap-2">
            <div className="flex-1 min-w-0">
              <div className="text-sm font-semibold truncate">
                {flag(pred.home)} {zh(pred.home)}
              </div>
              <div className="text-sm font-semibold truncate mt-1">
                {flag(pred.away)} {zh(pred.away)}
              </div>
            </div>
            <div className="text-center px-3">
              <div className="font-mono text-2xl font-bold tabular-nums">
                {pred.prediction.score.home}
                <span className="text-muted-foreground mx-1">:</span>
                {pred.prediction.score.away}
              </div>
              <div className="text-xs text-muted-foreground mt-0.5">
                {outcomeZh(pred.prediction.outcome)}
              </div>
            </div>
            {result && (
              <div className="text-center px-2 border-l border-border">
                <div className="text-xs text-muted-foreground mb-0.5">實際</div>
                <div className="font-mono text-lg font-bold tabular-nums">
                  {result.score.home}:{result.score.away}
                </div>
              </div>
            )}
          </div>

          <div className="mt-3">
            <ProbBar p={pred.prediction.win_prob} />
            <div className="flex justify-between text-xs text-muted-foreground mt-1.5">
              <span>主 {Math.round(pred.prediction.win_prob.home * 100)}%</span>
              <span>和 {Math.round(pred.prediction.win_prob.draw * 100)}%</span>
              <span>客 {Math.round(pred.prediction.win_prob.away * 100)}%</span>
            </div>
          </div>

          <div className="flex items-center justify-between mt-3 text-xs text-muted-foreground">
            <span className="flex items-center gap-1">
              <TrendingUp className="w-3 h-3" /> 信心 {Math.round(pred.prediction.confidence * 100)}%
            </span>
            <span>{pred.source_count} 處來源</span>
          </div>
        </button>
      </DialogTrigger>

      <DialogContent className="max-w-2xl max-h-[85vh]">
        <DialogHeader>
          <DialogTitle className="text-base">
            #{pred.match} · {stageZh(pred.stage)} ·{" "}
            {flag(pred.home)} {zh(pred.home)} vs {zh(pred.away)} {flag(pred.away)}
          </DialogTitle>
        </DialogHeader>
        <ScrollArea className="max-h-[68vh] pr-3">
          <div className="space-y-5">
            <div className="flex items-center gap-4">
              <div className="bg-muted rounded-lg px-4 py-2 text-center">
                <div className="text-xs text-muted-foreground">AI 預測</div>
                <div className="font-mono text-2xl font-bold">
                  {pred.prediction.scoreline}
                </div>
              </div>
              {result && (
                <div className="bg-muted rounded-lg px-4 py-2 text-center">
                  <div className="text-xs text-muted-foreground">實際結果</div>
                  <div className="font-mono text-2xl font-bold">
                    {result.score.home}:{result.score.away}
                  </div>
                </div>
              )}
              <div className="text-sm text-muted-foreground">
                信心 {Math.round(pred.prediction.confidence * 100)}% · 共識傾向{" "}
                {pred.reasoning.consensus_lean
                  ? outcomeZh(pred.reasoning.consensus_lean)
                  : "—"}
              </div>
            </div>

            <div>
              <h4 className="text-sm font-semibold mb-1.5">分析摘要</h4>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {pred.reasoning.summary}
              </p>
            </div>

            <div>
              <h4 className="text-sm font-semibold mb-1.5">關鍵因素</h4>
              <ul className="space-y-1.5">
                {pred.reasoning.key_factors.map((f, i) => (
                  <li key={i} className="text-sm text-muted-foreground flex gap-2">
                    <span className="text-primary mt-0.5">▪</span>
                    <span>{f}</span>
                  </li>
                ))}
              </ul>
            </div>

            {pred.reasoning.dissent && (
              <div>
                <h4 className="text-sm font-semibold mb-1.5">反方觀點</h4>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {pred.reasoning.dissent}
                </p>
              </div>
            )}

            {history && history.length > 1 && (
              <div className="border-t border-border pt-4">
                <HistorySection history={history} />
              </div>
            )}

            <div>
              <h4 className="text-sm font-semibold mb-2">
                資料來源（{pred.source_count} 處）
              </h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5">
                {pred.sources.map((s, i) => (
                  <a
                    key={i}
                    href={s.url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-xs text-muted-foreground hover:text-primary truncate flex items-center gap-1.5 py-0.5"
                    data-testid={`link-source-${pred.match}-${i}`}
                  >
                    <Badge variant="outline" className="text-[10px] px-1 py-0 shrink-0">
                      {s.type}
                    </Badge>
                    <span className="truncate">{s.name}</span>
                  </a>
                ))}
              </div>
            </div>

            <p className="text-xs text-muted-foreground border-t border-border pt-3">
              執行批次 {pred.run_id} · {pred.model} ·{" "}
              {new Date(pred.run_timestamp).toLocaleString("zh-HK", {
                timeZone: "Asia/Hong_Kong",
              })}
            </p>
          </div>
        </ScrollArea>
      </DialogContent>
    </Dialog>
  );
}
