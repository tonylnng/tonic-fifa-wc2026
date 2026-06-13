import type { Express, Request, Response, NextFunction } from "express";
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

const PASSWORD = process.env.SITE_PASSWORD || "TN$$$$$$$$";

function readJSON(file: string): any {
  const p = join(dataDir(), file);
  if (!existsSync(p)) return null;
  return JSON.parse(readFileSync(p, "utf-8"));
}

function requireAuth(req: Request, res: Response, next: NextFunction) {
  const token = req.headers["x-site-auth"];
  if (token === PASSWORD) return next();
  return res.status(401).json({ error: "Unauthorized" });
}

export async function registerRoutes(
  httpServer: Server,
  app: Express
): Promise<Server> {
  // Login — verifies password, returns the token (the password itself) for header use
  app.post("/api/login", (req, res) => {
    const { password } = req.body || {};
    if (password === PASSWORD) {
      return res.json({ ok: true, token: PASSWORD });
    }
    return res.status(401).json({ ok: false, error: "密碼錯誤" });
  });

  app.get("/api/fixtures", requireAuth, (_req, res) => {
    res.json(readJSON("fixtures.json"));
  });

  app.get("/api/results", requireAuth, (_req, res) => {
    res.json(readJSON("results.json"));
  });

  app.get("/api/accuracy", requireAuth, (_req, res) => {
    res.json(readJSON("accuracy.json"));
  });

  // All predictions, grouped by match, sorted by run timestamp (latest first)
  app.get("/api/predictions", requireAuth, (_req, res) => {
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

  // Lightweight status/health for the dashboard header
  app.get("/api/status", requireAuth, (_req, res) => {
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
      last_updated: fixtures?.last_updated,
      total_matches: fixtures?.total_matches,
      prediction_files: predFiles,
      total_runs: runs.size,
      runs: Array.from(runs).sort().reverse(),
      accuracy: accuracy?.metrics,
    });
  });

  return httpServer;
}
