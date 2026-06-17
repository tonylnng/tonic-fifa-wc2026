import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { PlayersData, LeaderboardsData, Player, LeaderRow } from "@/lib/types";
import { flag, zh } from "@/lib/flags";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Users, Search, Goal, RectangleVertical, Trophy } from "lucide-react";

const POS_ZH: Record<string, string> = {
  GK: "門將",
  DF: "後衛",
  MF: "中場",
  FW: "前鋒",
};

const POS_TONE: Record<string, string> = {
  GK: "bg-amber-500/15 text-amber-600 dark:text-amber-400 border-amber-500/30",
  DF: "bg-sky-500/15 text-sky-600 dark:text-sky-400 border-sky-500/30",
  MF: "bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border-emerald-500/30",
  FW: "bg-rose-500/15 text-rose-600 dark:text-rose-400 border-rose-500/30",
};

function StatPill({
  icon,
  value,
  label,
  tone,
}: {
  icon: React.ReactNode;
  value: number;
  label: string;
  tone: string;
}) {
  return (
    <div className="flex items-center gap-1.5" title={label}>
      <span className={tone}>{icon}</span>
      <span className="font-mono font-semibold text-sm tabular-nums">{value}</span>
    </div>
  );
}

function PlayerCard({ p }: { p: Player }) {
  const s = p.stats;
  return (
    <div
      className="rounded-xl border bg-card p-4 flex flex-col gap-3"
      data-testid={`player-${p.id}`}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <span className="text-lg leading-none">{flag(p.team)}</span>
            <h4 className="font-semibold truncate">{p.name_zh}</h4>
          </div>
          <p className="text-xs text-muted-foreground truncate mt-0.5">
            {p.name_en}
          </p>
        </div>
        <div className="flex flex-col items-end gap-1 shrink-0">
          {p.shirt_no != null && (
            <span className="font-mono text-lg font-bold text-muted-foreground leading-none">
              #{p.shirt_no}
            </span>
          )}
          <Badge
            variant="outline"
            className={`text-[10px] px-1.5 py-0 ${POS_TONE[p.position] || ""}`}
          >
            {POS_ZH[p.position] || p.position}
          </Badge>
        </div>
      </div>

      <div className="flex flex-wrap gap-x-3 gap-y-1 text-xs text-muted-foreground">
        <span>{zh(p.team)}</span>
        {p.club && <span>· {p.club}</span>}
        {p.age != null && <span>· {p.age} 歲</span>}
      </div>

      {p.bio_zh && (
        <p className="text-sm leading-relaxed text-foreground/90">{p.bio_zh}</p>
      )}

      <div className="flex items-center gap-4 pt-2 mt-auto border-t">
        <StatPill
          icon={<Goal className="w-4 h-4" />}
          value={s.goals}
          label="本屆進球"
          tone="text-primary"
        />
        <StatPill
          icon={<RectangleVertical className="w-4 h-4 fill-yellow-400 text-yellow-500" />}
          value={s.yellow_cards}
          label="本屆黃牌"
          tone="text-yellow-500"
        />
        <StatPill
          icon={<RectangleVertical className="w-4 h-4 fill-red-500 text-red-600" />}
          value={s.red_cards}
          label="本屆紅牌"
          tone="text-red-600"
        />
      </div>
    </div>
  );
}

function LeaderTable({
  title,
  icon: Icon,
  rows,
  kind,
}: {
  title: string;
  icon: any;
  rows: LeaderRow[];
  kind: "scorers" | "discipline";
}) {
  return (
    <div className="rounded-xl border bg-card overflow-hidden">
      <div className="flex items-center gap-2 px-4 py-3 border-b bg-muted/40">
        <Icon className="w-4 h-4 text-chart-2" />
        <h3 className="font-semibold text-sm">{title}</h3>
      </div>
      {rows.length === 0 ? (
        <p className="text-sm text-muted-foreground text-center py-8">
          尚未有紀錄。每場賽後自動更新。
        </p>
      ) : (
        <div className="divide-y">
          {rows.slice(0, 15).map((r, i) => (
            <div
              key={r.id}
              className="flex items-center gap-3 px-4 py-2.5 text-sm"
              data-testid={`leader-${kind}-${r.id}`}
            >
              <span className="font-mono text-xs text-muted-foreground w-5 text-right">
                {i + 1}
              </span>
              <span className="text-base leading-none">{flag(r.team)}</span>
              <div className="min-w-0 flex-1">
                <span className="font-medium">{r.name_zh}</span>
                <span className="text-xs text-muted-foreground ml-2">
                  {r.team_zh}
                </span>
              </div>
              {kind === "scorers" ? (
                <span className="flex items-center gap-1.5 font-mono font-semibold tabular-nums text-primary">
                  <Goal className="w-3.5 h-3.5" />
                  {r.goals}
                </span>
              ) : (
                <span className="flex items-center gap-2 font-mono tabular-nums">
                  {r.yellow_cards > 0 && (
                    <span className="flex items-center gap-0.5 text-yellow-500">
                      <RectangleVertical className="w-3.5 h-3.5 fill-yellow-400 text-yellow-500" />
                      {r.yellow_cards}
                    </span>
                  )}
                  {r.red_cards > 0 && (
                    <span className="flex items-center gap-0.5 text-red-600">
                      <RectangleVertical className="w-3.5 h-3.5 fill-red-500 text-red-600" />
                      {r.red_cards}
                    </span>
                  )}
                </span>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export function PlayersTab() {
  const playersQ = useQuery<PlayersData>({ queryKey: ["/api/players"] });
  const lbQ = useQuery<LeaderboardsData>({ queryKey: ["/api/leaderboards"] });
  const [q, setQ] = useState("");
  const [team, setTeam] = useState("all");

  const players = playersQ.data?.players ?? [];
  const lb = lbQ.data;

  const teams = useMemo(() => {
    const set = Array.from(new Set(players.map((p) => p.team)));
    set.sort((a, b) => zh(a).localeCompare(zh(b), "zh-Hant"));
    return set;
  }, [players]);

  const filtered = useMemo(() => {
    const needle = q.trim().toLowerCase();
    return players.filter((p) => {
      if (team !== "all" && p.team !== team) return false;
      if (!needle) return true;
      return (
        p.name_zh.toLowerCase().includes(needle) ||
        p.name_en.toLowerCase().includes(needle) ||
        zh(p.team).includes(needle) ||
        (p.club || "").toLowerCase().includes(needle)
      );
    });
  }, [players, q, team]);

  // 依隊伍分組
  const grouped = useMemo(() => {
    const map = new Map<string, Player[]>();
    for (const p of filtered) {
      const arr = map.get(p.team) || [];
      arr.push(p);
      map.set(p.team, arr);
    }
    return Array.from(map.entries()).sort((a, b) =>
      zh(a[0]).localeCompare(zh(b[0]), "zh-Hant")
    );
  }, [filtered]);

  if (playersQ.isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        {[...Array(6)].map((_, i) => (
          <Skeleton key={i} className="h-44 rounded-xl" />
        ))}
      </div>
    );
  }

  if (players.length === 0) {
    return (
      <div className="text-center py-16 text-muted-foreground">
        <Users className="w-10 h-10 mx-auto mb-3 opacity-40" />
        <p>球員名單建置中。每隊重點球員的資料與本屆統計即將上線。</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* 排行榜 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <LeaderTable
          title="射手榜"
          icon={Trophy}
          rows={lb?.scorers ?? []}
          kind="scorers"
        />
        <LeaderTable
          title="紀律榜（紅黃牌）"
          icon={RectangleVertical}
          rows={lb?.discipline ?? []}
          kind="discipline"
        />
      </div>

      {/* 篩選 */}
      <div className="flex flex-col sm:flex-row gap-2">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
          <Input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="搜尋球員、球隊或俱樂部…"
            className="pl-9 h-9"
            data-testid="input-player-search"
          />
        </div>
        <Select value={team} onValueChange={setTeam}>
          <SelectTrigger className="w-full sm:w-[180px] h-9 text-sm" data-testid="select-player-team">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">全部球隊</SelectItem>
            {teams.map((t) => (
              <SelectItem key={t} value={t}>
                {flag(t)} {zh(t)}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <p className="text-sm text-muted-foreground">
        共 {players.length} 名重點球員（每隊約 6 人）· 顯示 {filtered.length} 名 ·
        統計為本屆累計，每場賽後由 AI 研究權威來源自動更新。
      </p>

      {/* 依隊分組顯示 */}
      {grouped.length === 0 ? (
        <div className="text-center py-12 text-muted-foreground">
          <Search className="w-8 h-8 mx-auto mb-2 opacity-40" />
          <p>找不到符合的球員。</p>
        </div>
      ) : (
        grouped.map(([t, list]) => (
          <div key={t} className="space-y-3">
            <div className="flex items-center gap-2 sticky top-0 bg-background/80 backdrop-blur py-1 z-10">
              <span className="text-xl leading-none">{flag(t)}</span>
              <h3 className="font-semibold">{zh(t)}</h3>
              <Badge variant="secondary" className="text-[10px]">
                {list.length} 人
              </Badge>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {list.map((p) => (
                <PlayerCard key={p.id} p={p} />
              ))}
            </div>
          </div>
        ))
      )}
    </div>
  );
}
