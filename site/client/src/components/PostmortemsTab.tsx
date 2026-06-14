import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { PostmortemsData, Postmortem } from "@/lib/types";
import { flag, zh } from "@/lib/flags";
import { stageZh } from "@/lib/stage";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Input } from "@/components/ui/input";
import { Search, BookOpen, Check, X, Target } from "lucide-react";

function VerdictBadge({ v }: { v: Postmortem["verdict"] }) {
  if (v === "exact")
    return (
      <Badge className="bg-primary text-primary-foreground text-[11px]">
        <Check className="w-3 h-3 mr-0.5" /> 命中比分
      </Badge>
    );
  if (v === "outcome")
    return (
      <Badge variant="secondary" className="text-[11px]">
        <Check className="w-3 h-3 mr-0.5" /> 命中勝負
      </Badge>
    );
  return (
    <Badge variant="outline" className="text-[11px] text-destructive">
      <X className="w-3 h-3 mr-0.5" /> 未命中
    </Badge>
  );
}

function Card({ pm }: { pm: Postmortem }) {
  return (
    <div
      className="bg-card border border-card-border rounded-xl p-4"
      data-testid={`postmortem-${pm.match}`}
    >
      <div className="flex items-center justify-between gap-2 mb-2 flex-wrap">
        <span className="flex items-center gap-2">
          <Badge variant="secondary" className="text-xs">
            #{pm.match} · {stageZh(pm.stage)}
          </Badge>
          <span className="text-sm font-semibold">
            {flag(pm.home)} {zh(pm.home)} vs {zh(pm.away)} {flag(pm.away)}
          </span>
        </span>
        <VerdictBadge v={pm.verdict} />
      </div>

      <div className="flex items-center gap-3 mb-2 text-sm">
        <span className="text-muted-foreground">
          AI <span className="font-mono font-bold text-foreground">{pm.predicted}</span>
        </span>
        <span className="text-muted-foreground">→</span>
        <span className="text-muted-foreground">
          實際 <span className="font-mono font-bold text-foreground">{pm.final}</span>
        </span>
      </div>

      <h4 className="text-sm font-semibold mb-1.5">{pm.headline}</h4>
      <p className="text-sm text-muted-foreground leading-relaxed">{pm.review}</p>

      {pm.lessons && pm.lessons.length > 0 && (
        <div className="mt-3">
          <div className="text-xs font-semibold mb-1 flex items-center gap-1">
            <Target className="w-3.5 h-3.5 text-chart-2" /> 可沉澱的規律
          </div>
          <ul className="space-y-1">
            {pm.lessons.map((l, i) => (
              <li key={i} className="text-xs text-muted-foreground flex gap-1.5">
                <span className="text-chart-2 mt-0.5">▪</span>
                <span>{l}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {pm.vs_benchmarks && (
        <p className="text-xs text-muted-foreground mt-3 border-t border-border pt-2">
          <span className="font-semibold text-foreground">vs 基準線：</span>{" "}
          {pm.vs_benchmarks}
        </p>
      )}
    </div>
  );
}

export function PostmortemsTab() {
  const pmQ = useQuery<PostmortemsData>({ queryKey: ["/api/postmortems"] });
  const [q, setQ] = useState("");
  const [filter, setFilter] = useState<"all" | "exact" | "outcome" | "miss">("all");

  const list = useMemo(() => {
    const all = pmQ.data?.postmortems || [];
    return [...all]
      .filter((p) => filter === "all" || p.verdict === filter)
      .filter((p) => {
        if (!q) return true;
        const hay = `${p.home} ${p.away} ${zh(p.home)} ${zh(p.away)} ${p.headline} ${p.review} ${(p.lessons || []).join(" ")}`.toLowerCase();
        return hay.includes(q.toLowerCase());
      })
      .sort((a, b) => b.match - a.match);
  }, [pmQ.data, q, filter]);

  if (pmQ.isLoading) return <Skeleton className="h-96 rounded-xl" />;

  const total = pmQ.data?.postmortems.length || 0;

  if (total === 0) {
    return (
      <div className="text-center py-16 text-muted-foreground">
        <BookOpen className="w-10 h-10 mx-auto mb-3 opacity-40" />
        <p>尚未有賽後覆盤。每場比賽結果出爐後，AI 會自動生成「為何命中 / 失準」短評。</p>
      </div>
    );
  }

  const filters: { k: typeof filter; label: string }[] = [
    { k: "all", label: "全部" },
    { k: "exact", label: "命中比分" },
    { k: "outcome", label: "命中勝負" },
    { k: "miss", label: "未命中" },
  ];

  return (
    <div>
      <div className="flex flex-col sm:flex-row gap-3 mb-4">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
          <Input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="搜尋球隊、關鍵字、教訓…"
            className="pl-9"
            data-testid="input-search-postmortems"
          />
        </div>
        <div className="flex gap-2 overflow-x-auto pb-1">
          {filters.map((f) => (
            <button
              key={f.k}
              onClick={() => setFilter(f.k)}
              className={`text-xs px-3 py-1.5 rounded-full border whitespace-nowrap hover-elevate ${
                filter === f.k
                  ? "bg-primary text-primary-foreground border-primary"
                  : "border-border"
              }`}
              data-testid={`pm-filter-${f.k}`}
            >
              {f.label}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
        {list.map((pm) => (
          <Card key={`${pm.match}-${pm.run_id}`} pm={pm} />
        ))}
      </div>
      <p className="text-xs text-muted-foreground mt-3">
        共 {list.length} 篇覆盤 · 可搜尋的賽後知識庫，記錄 AI 的命中與失準原因
      </p>
    </div>
  );
}
