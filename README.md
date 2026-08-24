# ml-sandbox

## Python 環境（uv）

このリポジトリは **ディレクトリ単位で uv プロジェクトを分ける**。ルートに共通の `.venv` は置かない。

| パス | uv プロジェクト | Python |
|------|----------------|--------|
| `develop/api/` | API サーバー | 3.14（`.python-version` 参照） |
| `research/<YYYYMMDD-...>/` | 調査・実験ごと | 調査ディレクトリの `.python-version` 参照 |

### venv の activate / deactivate

`uv run` は activate 不要。シェルでそのプロジェクトの Python を使いたいときだけ、**作業中のディレクトリの `.venv`** を有効化する。

```bash
source .venv/bin/activate   # 有効化（プロンプトにプロジェクト名が出る）
deactivate                  # 解除
```

例（API）:

```bash
cd develop/api
source .venv/bin/activate
# ...
deactivate
```

別プロジェクトの venv を入れたまま `uv add` / `uv sync` すると、`VIRTUAL_ENV` がプロジェクトの `.venv` と一致せず warning が出る。プロジェクトを切り替える前に `deactivate` する。

### develop/api

```bash
cd develop/api
uv sync
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

詳細: [develop/api/README.md](./develop/api/README.md)

### research

調査ディレクトリ（例: `research/20260526-Search-Tree/`）ごとに独立した `pyproject.toml` / `.venv` を持つ。

```bash
cd research/20260526-Search-Tree
uv sync
uv run jupyter lab notebooks/
```

詳細: [research/README.md](./research/README.md)

### Cursor / VS Code

`.vscode/settings.json` の `python.venvFolders` に uv プロジェクトのパスを列挙している。  
notebook や Python ファイルでは、カーネル / インタープリタ選択で該当ディレクトリの `.venv` を選ぶ。

新しい `research/` 配下プロジェクトを追加したら、`python.venvFolders` への追記を忘れないこと。

## 前提
gcloud CLIをインストールすること
https://docs.cloud.google.com/sdk/docs/install-sdk?hl=ja#linux

```
gcloud --version

gcloud auth login

gcloud auth application-default login
```


ディレクトリ構成
```.ini
ml-sandbox/
├── develop/api/          ← uv プロジェクト（API 専用）
│   ├── pyproject.toml
│   ├── .python-version   # 3.14
│   └── .venv/
└── research/
    └── 20260526-Search-Tree/  ← uv プロジェクト（調査専用）
        ├── pyproject.toml
        ├── .python-version   # 調査ごとに変更可
        └── .venv/
```