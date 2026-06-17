import type { Express } from "express";
import { createServer } from "node:http";
import type { Server } from "node:http";
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

// In CJS build, import.meta.url is empty -> fileURLToPath throws; guard it.
let __dirname_resolved = process.cwd();
try {
  if (import.meta && import.meta.url) {
    __dirname_resolved = dirname(fileURLToPath(import.meta.url));
  }
} catch {
  __dirname_resolved = process.cwd();
}
const __dirname = __dirname_resolved;

// Data dir resolves whether running from source (server/) or built (dist/)
function dataDir(): string {
  const candidates = [
    join(process.cwd(), "data"),
    join(__dirname, "..", "data"),
    join(__dirname, "..", "..", "data"),
    join(process.cwd(), "..", "data"),
  ];
  for (const c of candidates) {
    if (existsSync(join(c, "fixtures.json"))) return c;
  }
  return candidates[0];
}

function readJSON(file: string): any {
  const p = join(dataDir(), file);
  if (!existsSync(p)) return null;
  return JSON.parse(readFileSync(p, "utf-8"));
}

export async function registerRoutes(
  httpServer: Server,
  app: Express
): Promise<Server> {
  app.get("/api/fixtures", (_req, res) => {
    res.json(readJSON("fixtures.json"));
  });

  app.get("/api/results", (_req, res) => {
    res.json(readJSON("results.json"));
  });

  // 即時讀取 GitHub 上的最新比賽結果（raw.githubusercontent）。
  // GitHub 是這套自動化的權威資料來源：排程每輪把最新 results.json 推送到 repo，
  // 此端點讓網站不必等下一次重新發布，就能直接顯示 repo 上的最新結果。
  // 失敗時回退到本機打包的 results.json，並標明 source。
  const GH_RESULTS_URL =
    "https://raw.githubusercontent.com/tonylnng/tonic-fifa-wc2026/master/site/data/results.json";
  let liveCache: { at: number; data: any } | null = null;
  const LIVE_TTL_MS = 60_000; // 1 分鐘快取，避免每次請求都打 GitHub

  app.get("/api/live-results", async (_req, res) => {
    const local = readJSON("results.json");
    // 命中快取
    if (liveCache && Date.now() - liveCache.at < LIVE_TTL_MS) {
      res.json({ ...liveCache.data, source: "github", cached: true });
      return;
    }
    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 6000);
      const r = await fetch(GH_RESULTS_URL, {
        signal: controller.signal,
        headers: { "Cache-Control": "no-cache" },
      });
      clearTimeout(timer);
      if (!r.ok) throw new Error(`GitHub HTTP ${r.status}`);
      const data = await r.json();
      liveCache = { at: Date.now(), data };
      res.json({ ...data, source: "github", cached: false });
    } catch (e: any) {
      // 回退到本機資料
      res.json({
        ...(local || { results: [] }),
        source: "local-fallback",
        error: String(e?.message || e),
      });
    }
  });

  // ----- 全站即時讀取 GitHub 最新資料 -----
  // 一次抓取 repo 上所有資料檔（results/accuracy/calibration/postmortems/
  // benchmark_scores/fixtures + 全部 predictions），讓整個網站每個分頁都能
  // 同步顯示 GitHub 最新內容，不必等下一次重新發布。
  const GH_RAW =
    "https://raw.githubusercontent.com/tonylnng/tonic-fifa-wc2026/master/site/data";
  let liveAllCache: { at: number; data: any } | null = null;

  async function ghFetchJSON(url: string, timeoutMs = 6000): Promise<any> {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const r = await fetch(url, {
        signal: controller.signal,
        headers: { "Cache-Control": "no-cache" },
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return await r.json();
    } finally {
      clearTimeout(timer);
    }
  }

  app.get("/api/live-all", async (_req, res) => {
    if (liveAllCache && Date.now() - liveAllCache.at < LIVE_TTL_MS) {
      res.json({ ...liveAllCache.data, source: "github", cached: true });
      return;
    }
    try {
      // 單檔資料集並行抓取
      const singles = [
        "results",
        "accuracy",
        "calibration",
        "postmortems",
        "benchmark_scores",
        "fixtures",
      ] as const;
      const singleResults = await Promise.all(
        singles.map((name) => ghFetchJSON(`${GH_RAW}/${name}.json`))
      );
      const payload: Record<string, any> = {};
      singles.forEach((name, i) => (payload[name] = singleResults[i]));

      // predictions：先抓 manifest 取得檔案清單，再並行抓每個預測檔，
      // 然後依場次分組、依 run_timestamp 由新到舊排序（與 /api/predictions 一致）。
      const manifest = await ghFetchJSON(`${GH_RAW}/predictions/manifest.json`);
      const files: string[] = Array.isArray(manifest?.files)
        ? manifest.files
        : [];
      const preds = await Promise.all(
        files.map((f) =>
          ghFetchJSON(`${GH_RAW}/predictions/${f}`).catch(() => null)
        )
      );
      const grouped: Record<string, any[]> = {};
      for (const p of preds) {
        if (!p || p.match == null) continue;
        const key = String(p.match);
        (grouped[key] = grouped[key] || []).push(p);
      }
      for (const k of Object.keys(grouped)) {
        grouped[k].sort((a, b) =>
          (b.run_timestamp || "").localeCompare(a.run_timestamp || "")
        );
      }
      payload.predictions = grouped;

      liveAllCache = { at: Date.now(), data: payload };
      res.json({ ...payload, source: "github", cached: false });
    } catch (e: any) {
      // 全部回退到本機打包資料
      const dir = join(dataDir(), "predictions");
      const grouped: Record<string, any[]> = {};
      if (existsSync(dir)) {
        for (const f of readdirSync(dir)) {
          if (!f.endsWith(".json") || f === "manifest.json") continue;
          try {
            const pred = JSON.parse(readFileSync(join(dir, f), "utf-8"));
            const key = String(pred.match);
            (grouped[key] = grouped[key] || []).push(pred);
          } catch {
            /* skip */
          }
        }
        for (const k of Object.keys(grouped)) {
          grouped[k].sort((a, b) =>
            (b.run_timestamp || "").localeCompare(a.run_timestamp || "")
          );
        }
      }
      res.json({
        results: readJSON("results.json"),
        accuracy: readJSON("accuracy.json"),
        calibration: readJSON("calibration.json"),
        postmortems: readJSON("postmortems.json"),
        benchmark_scores: readJSON("benchmark_scores.json"),
        fixtures: readJSON("fixtures.json"),
        predictions: grouped,
        source: "local-fallback",
        error: String(e?.message || e),
      });
    }
  });

  app.get("/api/accuracy", (_req, res) => {
    res.json(readJSON("accuracy.json"));
  });

  app.get("/api/calibration", (_req, res) => {
    res.json(readJSON("calibration.json"));
  });

  app.get("/api/postmortems", (_req, res) => {
    res.json(readJSON("postmortems.json"));
  });

  app.get("/api/benchmark-scores", (_req, res) => {
    res.json(readJSON("benchmark_scores.json"));
  });

  // 球員介紹 + 本屆統計（進球/黃牌/紅牌）。
  app.get("/api/players", (_req, res) => {
    res.json(readJSON("players.json") ?? { players: [] });
  });

  // 射手榜 + 紀律榜（由 update_players.py 計算）。
  app.get("/api/leaderboards", (_req, res) => {
    res.json(
      readJSON("leaderboards.json") ?? {
        scorers: [],
        discipline: [],
        totals: { players: 0, goals: 0, yellow_cards: 0, red_cards: 0 },
      }
    );
  });

  // All predictions, grouped by match, sorted by run timestamp (latest first)
  app.get("/api/predictions", (_req, res) => {
    const dir = join(dataDir(), "predictions");
    const out: Record<string, any[]> = {};
    if (existsSync(dir)) {
      for (const f of readdirSync(dir)) {
        if (!f.endsWith(".json") || f === "manifest.json") continue;
        try {
          const pred = JSON.parse(readFileSync(join(dir, f), "utf-8"));
          const key = String(pred.match);
          (out[key] = out[key] || []).push(pred);
        } catch {
          /* skip malformed */
        }
      }
    }
    for (const k of Object.keys(out)) {
      out[k].sort((a, b) =>
        (b.run_timestamp || "").localeCompare(a.run_timestamp || "")
      );
    }
    res.json(out);
  });

  // Lightweight status/health for the dashboard header.
  // last_updated reflects the most recent automation run — accuracy.json is
  // refreshed on every cron run, so it is the authoritative freshness signal.
  app.get("/api/status", (_req, res) => {
    const dir = join(dataDir(), "predictions");
    let runs = new Set<string>();
    let predFiles = 0;
    if (existsSync(dir)) {
      for (const f of readdirSync(dir)) {
        if (!f.endsWith(".json") || f === "manifest.json") continue;
        predFiles++;
        const m = f.match(/__(.+)\.json$/);
        if (m) runs.add(m[1]);
      }
    }
    const fixtures = readJSON("fixtures.json");
    const accuracy = readJSON("accuracy.json");
    res.json({
      last_updated: accuracy?.last_updated || fixtures?.last_updated,
      total_matches: fixtures?.total_matches,
      prediction_files: predFiles,
      total_runs: runs.size,
      runs: Array.from(runs).sort().reverse(),
      accuracy: accuracy?.metrics,
    });
  });

  return httpServer;
}
