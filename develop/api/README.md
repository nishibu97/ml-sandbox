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

curl http://localhost:8000/deps
```

## API仕様
```
http://localhost:8000/docs
```


## 環境変数

`.env.sample` を `.env` にコピーして設定する。

## ディレクトリ構成（機能別垂直スライス）

```text
app/
├── main.py
├── core/                    # アプリケーション全体の共通設定
│   ├── config.py
│   └── exceptions.py
├── clients/                 # 外部API通信（機能横断で共有）
└── features/                # 機能ごとに独立
    ├── health/
    │   └── router.py
    └── deps/                # ベンチマーク用（ネストした Depends）
        ├── router.py
        ├── schemas.py
        └── deps.py
```

将来の AI 機能（例: `chat` / `analyze`）は `features/<name>/` 配下に
`router.py` / `schemas.py` / `service.py` / `prompts.py` を揃えて追加する。
