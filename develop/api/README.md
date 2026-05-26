# api

FastAPI サーバー（uv / Python 3.14）

このディレクトリは `develop/api/` 配下の **独立した uv プロジェクト**。  
リポジトリ全体の Python 方針: [ルート README](../../README.md#python-環境uv)

## ローカル起動

```bash
cd develop/api
uv sync
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Docker 起動

```bash
cd develop/api
cp .env.sample .env   # 初回のみ
docker compose up -d --build
```

## 動作確認

```bash
curl http://localhost:8000/health
# {"status":"ok"}
```

## API仕様
```
http://localhost:8000/docs
```


## 環境変数

`.env.sample` を `.env` にコピーして設定する。
