import { useAuth } from "@/lib/auth";
import { Button } from "@/components/ui/button";
import { LogOut } from "lucide-react";

function relativeTime(iso: string): string {
  const diffMin = Math.floor((Date.now() - new Date(iso).getTime()) / 60000);
  if (diffMin < 1) return "剛剛";
  if (diffMin < 60) return `${diffMin} 分鐘前`;
  const h = Math.floor(diffMin / 60);
  if (h < 24) return `${h} 小時前`;
  return `${Math.floor(h / 24)} 天前`;
}

export function Header({ lastUpdated }: { lastUpdated?: string }) {
  const { logout } = useAuth();
  return (
    <header className="sticky top-0 z-30 border-b border-border bg-background/80 backdrop-blur-md">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
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
          <div className="leading-tight">
            <div className="font-extrabold tracking-tight text-base">世界盃 2026</div>
            <div className="text-xs text-muted-foreground hidden sm:block">
              AI 預測與準確率追蹤
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          {lastUpdated && (
            <span
              className="text-xs text-muted-foreground hidden md:inline"
              title={new Date(lastUpdated).toLocaleString("zh-HK", { timeZone: "Asia/Hong_Kong" })}
              data-testid="text-last-updated"
            >
              資料更新：{new Date(lastUpdated).toLocaleString("zh-HK", { timeZone: "Asia/Hong_Kong" })}
              <span className="ml-1 text-primary">（{relativeTime(lastUpdated)}）</span>
            </span>
          )}
          <Button variant="ghost" size="sm" onClick={logout} data-testid="button-logout">
            <LogOut className="w-4 h-4 mr-1" /> 登出
          </Button>
        </div>
      </div>
    </header>
  );
}
