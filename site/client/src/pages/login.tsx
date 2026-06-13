import { useState } from "react";
import { useAuth } from "@/lib/auth";
import { apiRequest } from "@/lib/queryClient";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2, Lock } from "lucide-react";

export default function Login() {
  const { login } = useAuth();
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await apiRequest("POST", "/api/login", { password });
      const data = await res.json();
      login(data.token);
    } catch {
      setError("密碼錯誤，請重試");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-background relative overflow-hidden px-4">
      {/* pitch texture backdrop */}
      <div
        className="absolute inset-0 opacity-[0.04] pointer-events-none"
        style={{
          backgroundImage:
            "repeating-linear-gradient(90deg, hsl(var(--primary)) 0 2px, transparent 2px 80px)",
        }}
      />
      <div className="absolute -top-24 -left-24 w-96 h-96 rounded-full bg-primary/10 blur-3xl pointer-events-none" />
      <div className="absolute -bottom-24 -right-24 w-96 h-96 rounded-full bg-chart-2/10 blur-3xl pointer-events-none" />

      <form
        onSubmit={submit}
        className="relative w-full max-w-sm bg-card border border-card-border rounded-xl p-8 shadow-lg"
        data-testid="form-login"
      >
        <div className="flex flex-col items-center text-center mb-8">
          <svg width="56" height="56" viewBox="0 0 32 32" fill="none" className="mb-4">
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
          <h1 className="text-xl font-extrabold tracking-tight">世界盃 2026</h1>
          <p className="text-sm text-muted-foreground mt-1">AI 預測與準確率追蹤中心</p>
        </div>

        <label className="text-sm font-medium flex items-center gap-2 mb-2">
          <Lock className="w-4 h-4" /> 登入密碼
        </label>
        <Input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="請輸入密碼"
          autoFocus
          data-testid="input-password"
          className="mb-3"
        />
        {error && (
          <p className="text-sm text-destructive mb-3" data-testid="text-error">
            {error}
          </p>
        )}
        <Button
          type="submit"
          className="w-full"
          disabled={loading || !password}
          data-testid="button-submit"
        >
          {loading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
          進入儀表板
        </Button>
        <p className="text-xs text-muted-foreground text-center mt-6">
          FIFA World Cup 2026 · USA · Canada · Mexico
        </p>
      </form>
    </div>
  );
}
