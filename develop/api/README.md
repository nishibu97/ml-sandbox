# api

FastAPI サーバー（uv / Python 3.14）

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
