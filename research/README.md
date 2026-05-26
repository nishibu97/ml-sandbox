# research

調査・実験用ディレクトリ。**プロジェクト（`YYYYMMDD-` 形式のディレクトリ）ごとに uv で Python 環境を分ける。**

## 方針

| 項目 | ルール |
|------|--------|
| ディレクトリ名 | `YYYYMMDD-トピック`（例: `20260526-Search-Tree`） |
| Python 管理 | 各ディレクトリ直下で **独立した uv プロジェクト** |
| 仮想環境 | `<調査ディレクトリ>/.venv/`（git 管理外） |
| Python バージョン | 調査ごとに `.python-version` で指定（他プロジェクトと共有しない） |
| 依存関係 | 各ディレクトリの `pyproject.toml` / `uv.lock` |

リポジトリ全体の Python 方針は [ルート README](../README.md#python-環境uv) を参照。

## 新規調査の追加手順

```bash
cd research
mkdir 20260526-My-Topic
cd 20260526-My-Topic

uv init --python 3.14   # 必要なバージョンを指定
uv add <packages>
uv sync
```

Jupyter を使う場合:

```bash
uv add ipykernel jupyterlab
uv run python -m ipykernel install --user --name 20260526-my-topic --display-name "My Topic (Python 3.14)"
```

**Cursor / VS Code でカーネル候補に出すため**、`.vscode/settings.json` の `python.venvFolders` に新ディレクトリを追加する。

```json
"python.venvFolders": [
  "develop/api",
  "research/20260526-Search-Tree",
  "research/20260526-My-Topic"
]
```

## 既存プロジェクト

| ディレクトリ | Python | 用途 |
|-------------|--------|------|
| [20260526-Search-Tree](./20260526-Search-Tree/) | 3.14 | 8パズル探索木（DFS / BFS） |
