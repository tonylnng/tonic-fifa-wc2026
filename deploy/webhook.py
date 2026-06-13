#!/usr/bin/env python3
"""世界盃 2026 — GitHub Webhook 監聽器（方案 A）
收到 GitHub push 事件、驗證 HMAC 簽章後，背景執行 deploy/update.sh。
無外部相依，只用 Python 標準庫。

環境變數：
  WEBHOOK_SECRET  必填，與 GitHub webhook 設定的 Secret 相同
  WEBHOOK_PORT    監聽埠（預設 9000）
  UPDATE_SCRIPT   更新腳本路徑（預設 /opt/tonic-fifa-wc2026/deploy/update.sh）
  BRANCH          只在這個分支的 push 觸發（預設 master）
"""
import hmac, hashlib, json, os, subprocess, sys
from http.server import BaseHTTPRequestHandler, HTTPServer

SECRET = os.environ.get("WEBHOOK_SECRET", "").encode()
PORT = int(os.environ.get("WEBHOOK_PORT", "9000"))
UPDATE_SCRIPT = os.environ.get("UPDATE_SCRIPT", "/opt/tonic-fifa-wc2026/deploy/update.sh")
BRANCH = os.environ.get("BRANCH", "master")

if not SECRET:
    print("錯誤：請設定 WEBHOOK_SECRET 環境變數", file=sys.stderr)
    sys.exit(1)


def verify(body: bytes, sig: str) -> bool:
    if not sig or not sig.startswith("sha256="):
        return False
    mac = hmac.new(SECRET, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest("sha256=" + mac, sig)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # 安靜
        pass

    def do_POST(self):
        if self.path != "/webhook":
            self.send_response(404); self.end_headers(); return
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        sig = self.headers.get("X-Hub-Signature-256", "")
        if not verify(body, sig):
            self.send_response(403); self.end_headers()
            self.wfile.write(b"bad signature"); return

        event = self.headers.get("X-GitHub-Event", "")
        if event == "ping":
            self.send_response(200); self.end_headers()
            self.wfile.write(b"pong"); return
        if event != "push":
            self.send_response(204); self.end_headers(); return

        try:
            payload = json.loads(body)
            ref = payload.get("ref", "")
        except Exception:
            ref = ""
        if ref and ref != f"refs/heads/{BRANCH}":
            self.send_response(200); self.end_headers()
            self.wfile.write(b"ignored branch"); return

        # 背景執行更新，立刻回 GitHub 200，避免 webhook timeout
        subprocess.Popen(["/usr/bin/env", "bash", UPDATE_SCRIPT])
        self.send_response(202); self.end_headers()
        self.wfile.write(b"deploy triggered")


if __name__ == "__main__":
    print(f"Webhook 監聽 0.0.0.0:{PORT}  分支={BRANCH}")
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
