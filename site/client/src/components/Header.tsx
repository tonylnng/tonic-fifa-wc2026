import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { RefreshCw, Github } from "lucide-react";

function relativeTime(iso: string): string {
  const diffMin = Math.floor((Date.now() - new Date(iso).getTime()) / 60000);
  if (diffMin < 1) return "剛剛";
  if (diffMin < 60) return `${diffMin} 分鐘前`;
  const h = Math.floor(diffMin / 60);
  if (h < 24) return `${h} 小時前`;
  return `${Math.floor(h / 24)} 天前`;
}

export function Header({
  lastUpdated,
  onLiveRefresh,
  liveLoading,
  liveSource,
}: {
  lastUpdated?: string;
  onLiveRefresh?: () => void;
  liveLoading?: boolean;
  liveSource?: "github" | "local-fallback" | null;
}) {
  return (
    <header className="sticky top-0 z-30 border-b border-border bg-background/80 backdrop-blur-md">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-3">
        <div className="flex items-center gap-3 min-w-0">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none" className="shrink-0">
            <rect width="32" height="32" rx="7" fill="hsl(var(--primary))" />
            <path d="M16 6 L24 11 L21 21 L11 21 L8 11 Z" className="fill-background" />
            <path
              d="M16 6 L24 11 L21 21 L11 21 L8 11 Z"
              stroke="hsl(var(--chart-2))"
              strokeWidth="1.4"
              strokeLinejoin="round"
            />
            <circle cx="16" cy="15" r="2.2" fill="hsl(var(--chart-2))" />
          </svg>
          <div className="leading-tight min-w-0">
            <div className="font-extrabold tracking-tight text-base truncate">世界盃 2026</div>
            <div className="text-xs text-muted-foreground hidden sm:block">
              AI 預測與準確率追蹤
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2 sm:gap-3 shrink-0">
          {lastUpdated && (
            <span
              className="text-xs text-muted-foreground hidden lg:inline"
              title={new Date(lastUpdated).toLocaleString("zh-HK", { timeZone: "Asia/Hong_Kong" })}
              data-testid="text-last-updated"
            >
              資料更新：{new Date(lastUpdated).toLocaleString("zh-HK", { timeZone: "Asia/Hong_Kong" })}
              <span className="ml-1 text-primary">（{relativeTime(lastUpdated)}）</span>
            </span>
          )}

          {/* 全站即時讀取 GitHub 最新資料：所有分頁共用。 */}
          {onLiveRefresh && (
            <>
              {liveSource === "github" && (
                <Badge className="bg-primary text-primary-foreground text-[11px] hidden sm:inline-flex">
                  GitHub 即時
                </Badge>
              )}
              {liveSource === "local-fallback" && (
                <Badge variant="outline" className="text-[11px] text-destructive hidden sm:inline-flex">
                  讀取失敗·本機
                </Badge>
              )}
              <Button
                size="sm"
                variant="outline"
                onClick={onLiveRefresh}
                disabled={liveLoading}
                data-testid="button-live-refresh"
                className="shrink-0"
                title="從 GitHub 即時讀取全站最新資料（預測、結果、準確率、校準、覆盤）"
              >
                <RefreshCw
                  className={`w-4 h-4 sm:mr-1.5 ${liveLoading ? "animate-spin" : ""}`}
                />
                <Github className="w-4 h-4 mr-1.5 hidden sm:inline" />
                <span className="hidden sm:inline">
                  {liveLoading ? "讀取中…" : "即時讀取最新"}
                </span>
              </Button>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
