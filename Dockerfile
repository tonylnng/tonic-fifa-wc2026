# 世界盃 2026 AI 預測中心 — 自架 Docker 映像
# Express + Vite + React 全端應用，前後端同一個 port 提供服務

FROM node:20-bookworm-slim AS build
WORKDIR /app/site

# 先安裝相依套件（利用 Docker layer 快取）
COPY site/package.json site/package-lock.json ./
RUN npm ci

# 複製其餘原始碼並建置（產出 dist/public 與 dist/index.cjs）
COPY site/ ./
RUN npm run build


# ---- 執行階段：精簡映像 ----
FROM node:20-bookworm-slim AS runtime
WORKDIR /app/site
ENV NODE_ENV=production

# 只安裝正式環境相依套件
COPY site/package.json site/package-lock.json ./
RUN npm ci --omit=dev && npm cache clean --force

# 複製建置產物與資料目錄
COPY --from=build /app/site/dist ./dist
COPY site/data ./data

# 登入密碼預設為程式內建值 TN$$$$$$$$（8 個錢字號）
# 強烈建議部署時用環境變數覆寫，例如：docker run -e SITE_PASSWORD='你的密碼'
ENV PORT=5000

EXPOSE 5000
CMD ["node", "dist/index.cjs"]
