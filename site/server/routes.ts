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

  app.get("/api/accuracy", (_req, res) => {
    res.json(readJSON("accuracy.json"));
  });

  // All predictions, grouped by match, sorted by run timestamp (latest first)
  app.get("/api/predictions", (_req, res) => {
    const dir = join(dataDir(), "predictions");
    const out: Record<string, any[]> = {};
    if (existsSync(dir)) {
      for (const f of readdirSync(dir)) {
        if (!f.endsWith(".json")) continue;
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
        if (!f.endsWith(".json")) continue;
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
