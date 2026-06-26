#!/usr/bin/env python3
"""多模型第三方預測（A + C 方案）。

對單一場比賽，透過 Vercel AI Gateway 呼叫多家第三方 AI
（MiniMax / 千問 Qwen / DeepSeek / Google Gemini），
各自產生「比分 + 三向勝率 + 一句話 take（繁中）」，併入該場最新預測檔頂層的
benchmarks[]（kind="ai"），並計算「綜合共識」寫入頂層 consensus。

2026-06-26 成本優化：模型由 7 家精簡至 4 家。
移除 OpenAI GPT-5.1-thinking、xAI Grok-4.20-reasoning（reasoning 模型 max_tokens=3000，
token 消耗最高）、Z.ai GLM-4.7（與 DeepSeek 高度重疊）。
max_tokens 設為 1500：DeepSeek V4 Pro 為 hybrid reasoning 模型，
<think> 區塊可達 500-800 token，需保留足夠空間讓 JSON 不被截斷。
其餘三家（MiniMax/Qwen/Gemini）輸出直接，1500 仍比原 3000 省大量 token。

本站主預測（Sonnet 4.6 / research-pplx）維持不變。

用法：
  python3 multimodel_predict.py --match 9
  python3 multimodel_predict.py --file data/predictions/match_9__2026-06-14T0057Z.json

需在 bash 以 api_credentials=["custom-cred:ai-gateway.vercel.sh"] 執行。
金鑰由代理自動注入，本腳本不接觸明文金鑰。

排程整合：每輪對每場「即將開賽」比賽，在主預測（Sonnet 4.6）寫檔後呼叫本腳本。
"""
import argparse, glob, json, os, re, sys, datetime, subprocess

GATEWAY = "https://ai-gateway.vercel.sh/v1/chat/completions"
# 代理憑證：curl 對 proxy CONNECT 的憑證鏈處理較寬鬆，requests 在此代理環境會
# 卡在 proxy 驗證，故統一以 curl 發送（已驗證 HTTP 200）。
CA = os.environ.get("SSL_CERT_FILE", "/etc/ssl/certs/agent-proxy-ca-2.pem")

# 「全部用最新 model」：依 Gateway 最新可用檔
# 2026-06-26 成本優化：由 7 家精簡至 4 家
# 移除：OpenAI GPT-5.1-thinking, xAI Grok-4.20-reasoning（reasoning 模型最燒）, Z.ai GLM-4.7（與 DeepSeek 重疊）
MODELS = [
    {"id": "minimax/minimax-m3",            "label": "MiniMax M3"},
    {"id": "alibaba/qwen3.7-max",           "label": "千問 Qwen3.7 Max"},
    {"id": "deepseek/deepseek-v4-pro",      "label": "DeepSeek V4 Pro"},
    {"id": "google/gemini-3.1-pro-preview", "label": "Google Gemini 3.1 Pro"},
]

SYSTEM = (
    "你是足球賽事預測分析師。只輸出一個 JSON 物件，不要任何額外文字或 markdown。"
    "所有文字一律使用繁體中文。"
)

PROMPT_TMPL = """請為以下世界盃 2026 比賽做預測。

賽事：{stage}
對戰：{home}（主）vs {away}（客）
開賽（UTC）：{kickoff}

只輸出一個 JSON 物件，欄位如下（不要解釋、不要 markdown、不要程式碼框）：
{{
  "scoreline": "X:Y",                         // 你最可能的比分，主隊在前
  "outcome": "home|draw|away",
  "win_prob": {{ "home": 0.00, "draw": 0.00, "away": 0.00 }},  // 三向機率，總和=1
  "take": "一句話精簡分析（繁體中文，30字內）"
}}
注意：win_prob 三個數字相加必須等於 1.0；scoreline 與 outcome 必須一致。"""


def call_model(model_id, payload_msg):
    body = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": payload_msg},
        ],
        "max_tokens": 1500,  # DeepSeek V4 Pro 有 hybrid reasoning，<think> 區塊可達 500-800 token；1500 確保 JSON 不被截斷
        "temperature": 0.4,
    }
    proc = subprocess.run(
        [
            "curl", "-s", "--max-time", "120", "--cacert", CA,
            GATEWAY, "-H", "Content-Type: application/json",
            "-d", json.dumps(body),
        ],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"curl rc={proc.returncode}: {proc.stderr[:160]}")
    j = json.loads(proc.stdout)
    if "choices" not in j:
        raise RuntimeError(f"gateway error: {proc.stdout[:200]}")
    msg = j["choices"][0]["message"]
    content = msg.get("content", "") or ""
    # 有些 reasoning 模型把答案放在 content；若空則嘗試 reasoning
    if not content.strip():
        content = msg.get("reasoning", "") or ""
    return content


def extract_json(text):
    """從模型輸出中抽出第一個 JSON 物件。
    
    支援：
    - DeepSeek V4 Pro 的 <think>...</think> hybrid reasoning 前置
    - ```json ... ``` markdown 包裝
    - 一般純 JSON 輸出
    """
    text = text.strip()
    # 剝離 <think>...</think> 區塊（DeepSeek V4 Pro hybrid reasoning）
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    # 去除 ```json ... ``` 包裝
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1)
    # 抓第一個平衡的大括號區段
    start = text.find("{")
    if start == -1:
        raise ValueError("no JSON object found")
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start:i + 1])
    raise ValueError("unbalanced JSON")


def normalize_probs(wp):
    h = float(wp.get("home", 0)); d = float(wp.get("draw", 0)); a = float(wp.get("away", 0))
    s = h + d + a
    if s <= 0:
        return {"home": 0.34, "draw": 0.33, "away": 0.33}
    return {"home": round(h / s, 3), "draw": round(d / s, 3), "away": round(a / s, 3)}


def outcome_from_probs(wp):
    return max(wp, key=wp.get)


def predict_one_model(m, ctx, retries=1):
    """回傳一個 benchmarks[] 項目（kind=ai），失敗回 None。失敗會重試一次。"""
    msg = PROMPT_TMPL.format(**ctx)
    last_err = None
    for attempt in range(retries + 1):
        try:
            raw = call_model(m["id"], msg)
            obj = extract_json(raw)
            wp = normalize_probs(obj.get("win_prob", {}))
            scoreline = str(obj.get("scoreline", "")).replace("-", ":").strip()
            outcome = obj.get("outcome") or outcome_from_probs(wp)
            take = str(obj.get("take", "")).strip()[:60]
            # 防退化：模型未給出可用比分（空 scoreline）代表無效回應，視同失敗。
            if not re.match(r"^\d+:\d+$", scoreline):
                raise ValueError(f"invalid/empty scoreline: {scoreline!r}")
            return {
                "source": m["label"],
                "kind": "ai",
                "model_id": m["id"],
                "win_prob": wp,
                "scoreline": scoreline,
                "note": take,
            }
        except Exception as e:
            last_err = e
    sys.stderr.write(f"[WARN] {m['label']} ({m['id']}) 失敗: {last_err}\n")
    return None


def majority_scoreline(items, main_scoreline):
    """共識比分：多數決；平手時靠近主預測。"""
    from collections import Counter
    sl = [it["scoreline"] for it in items if it.get("scoreline")]
    if main_scoreline:
        sl.append(main_scoreline)  # 讓主預測也有一票
    if not sl:
        return main_scoreline or ""
    cnt = Counter(sl)
    top = cnt.most_common()
    best = top[0][1]
    tied = [s for s, c in top if c == best]
    if main_scoreline in tied:
        return main_scoreline
    return tied[0]


def avg_probs(prob_list):
    n = len(prob_list)
    if n == 0:
        return {"home": 0.34, "draw": 0.33, "away": 0.33}
    agg = {"home": 0.0, "draw": 0.0, "away": 0.0}
    for wp in prob_list:
        for k in agg:
            agg[k] += float(wp.get(k, 0))
    return normalize_probs({k: agg[k] / n for k in agg})


def friendly_main_label(model_id):
    """由預測檔 model 欄位推導繁中友善標籤（使歷史與未來批次都正確顯示實際模型）。"""
    mid = (model_id or "").lower()
    if "sonnet" in mid:
        return "本站 Sonnet 4.6"
    if "opus" in mid:
        return "本站 Opus 4.8"
    return "本站主預測"


def build_consensus(ai_items, main_pred, main_model=None):
    """C：綜合共識。含主預測 + 三家 AI 的加權平均勝率與多數比分。"""
    main_wp = main_pred.get("win_prob", {})
    main_sl = main_pred.get("scoreline", "")
    # 加權：主預測權重 2，每家第三方權重 1
    weighted = [main_wp, main_wp] + [it["win_prob"] for it in ai_items]
    cons_wp = avg_probs(weighted)
    cons_sl = majority_scoreline(ai_items, main_sl)
    cons_out = outcome_from_probs(cons_wp)
    n_models = 1 + len(ai_items)
    main_label = friendly_main_label(main_model)
    logic = (
        f"綜合 {n_models} 個模型（{main_label} + {len(ai_items)} 家第三方 AI）：" 
        f"勝率採主預測加權平均、比分採多數決"
        + ("（平手靠近主預測）" if ai_items else "") + "。"
    )
    return {
        "scoreline": cons_sl,
        "outcome": cons_out,
        "win_prob": cons_wp,
        "models_used": n_models,
        "logic": logic,
    }


def find_latest_file(match_num):
    files = sorted(glob.glob(f"data/predictions/match_{match_num}__*.json"))
    if not files:
        raise SystemExit(f"找不到 match {match_num} 的預測檔")
    return files[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--match", type=int)
    ap.add_argument("--file")
    ap.add_argument("--dry-run", action="store_true", help="只印結果不寫檔")
    args = ap.parse_args()

    path = args.file or find_latest_file(args.match)
    d = json.load(open(path))
    ctx = {
        "stage": d.get("stage", ""),
        "home": d.get("home", ""),
        "away": d.get("away", ""),
        "kickoff": d.get("kickoff_utc", ""),
    }
    # 主預測（本站 Sonnet 4.6）位於 d["prediction"]；共識計算用。
    main_pred = d.get("prediction", {})
    main_model = d.get("model", "")

    print(f"# {ctx['home']} vs {ctx['away']} ({ctx['stage']}) — 主預測 {main_pred.get('scoreline')}")

    ai_items = []
    for m in MODELS:
        it = predict_one_model(m, ctx)
        if it:
            ai_items.append(it)
            print(f"  {it['source']:18s} {it['scoreline']:6s} "
                  f"H{it['win_prob']['home']} D{it['win_prob']['draw']} A{it['win_prob']['away']} — {it['note']}")

    if not ai_items:
        sys.stderr.write("[ERROR] 三家模型全部失敗，未寫檔\n")
        sys.exit(2)

    consensus = build_consensus(ai_items, main_pred, main_model=main_model)
    print(f"  {'綜合共識':18s} {consensus['scoreline']:6s} "
          f"H{consensus['win_prob']['home']} D{consensus['win_prob']['draw']} A{consensus['win_prob']['away']}")

    if args.dry_run:
        print("\n[dry-run] 不寫檔")
        return

    # 併入頂層 benchmarks（前端讀 pred.benchmarks）：移除舊的同名 ai 項目避免重複，
    # 保留 betting/model/market 等原有基準線，再接上三家 AI。
    bms = d.get("benchmarks", [])
    existing_labels = {m["label"] for m in MODELS}
    bms = [b for b in bms if not (b.get("kind") == "ai" and b.get("source") in existing_labels)]
    bms.extend(ai_items)
    d["benchmarks"] = bms
    # 共識寫在頂層（前端讀 pred.consensus）
    d["consensus"] = consensus
    d["multimodel_updated_at"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    # 清除舊版寫錄（曾誤寫入 prediction 內層）
    if "benchmarks" in main_pred and any(
        b.get("kind") == "ai" for b in main_pred.get("benchmarks", [])
    ):
        main_pred["benchmarks"] = [
            b for b in main_pred["benchmarks"] if b.get("kind") != "ai"
        ]
        if not main_pred["benchmarks"]:
            main_pred.pop("benchmarks", None)
    main_pred.pop("consensus", None)
    main_pred.pop("multimodel_updated_at", None)
    d["prediction"] = main_pred

    with open(path, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"\n已寫入 {path}（頂層 benchmarks +{len(ai_items)} AI、consensus）")


if __name__ == "__main__":
    main()
