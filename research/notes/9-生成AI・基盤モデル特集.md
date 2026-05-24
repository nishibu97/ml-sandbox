# 9. 生成AI・基盤モデル特集

生成AI・基盤モデルに関する知識を集約した特集。3・4と一部重複するが、検索性のため独立化。

---

## 基盤モデル（Foundation Model, FM）

- **定義**：大規模・多様なデータで自己教師あり学習し、多様な下流タスクに転用可能なモデル（Stanford HAI, Bommasani et al. 2021 で提唱）
- **特徴**：
  - **規模**：パラメータ数・学習データ・計算量がスケール
  - **転移性**：ファインチューニングやプロンプトで多用途に
  - **創発的能力（Emergent Abilities）**：規模を超えると突然新タスクを解けるようになる現象
- 代表：GPT-4, Claude, Gemini, Llama, BERT, CLIP, Stable Diffusion

---

## Transformer（2017, Vaswani et al. "Attention Is All You Need"）

LLM・拡散モデルの土台となる中核アーキテクチャ。

- **構成**：Encoder + Decoder（用途で片方のみ使う場合あり）
- **Self-Attention（自己注意）**：系列内の各位置が他の全位置を参照、長距離依存を1ステップで捉える
- **Multi-Head Attention**：複数の注意ヘッドで多様な関係を並列に学習
- **Positional Encoding**：系列順序情報を加算（Transformer自体は順序を持たない）
- **メリット**：RNNと違い**並列化可能**、長距離依存に強い
- **デメリット**：計算量が系列長 N に対し **O(N²)**

### Transformer 派生

| モデル | 構造 | 用途 |
|---|---|---|
| **BERT** (2018) | Encoderのみ | 文の理解（分類・抽出）。MLM + NSP |
| **GPT** | Decoderのみ | 文生成。次トークン予測（自己回帰） |
| **T5** | Encoder-Decoder | あらゆるNLPをtext-to-textに統一 |
| **BART** | Encoder-Decoder | ノイズ除去型事前学習、要約に強い |
| **ViT** (Vision Transformer) | Encoder | 画像分類（パッチ分割→Transformer） |
| **Swin Transformer** | 階層型 | 高解像度画像 |

---

## 大規模言語モデル（LLM）

### 代表モデル

| モデル | 開発元 | 特徴 |
|---|---|---|
| **GPT-3** (2020) | OpenAI | 1750億パラメータ、Few-shot学習で話題化 |
| **GPT-3.5 / ChatGPT** (2022.11) | OpenAI | RLHF適用、対話インターフェース |
| **GPT-4** (2023) | OpenAI | マルチモーダル、推論能力向上 |
| **GPT-4o / o1 / o3** | OpenAI | マルチモーダル統合、推論モデル |
| **Claude** (2023〜) | Anthropic | Constitutional AI、長文脈 |
| **Gemini** (2023〜) | Google DeepMind | ネイティブマルチモーダル |
| **Llama** | Meta | オープンモデル（重み公開） |
| **PaLM / PaLM 2** | Google | 大規模・多言語 |
| **Mistral / Mixtral** | Mistral AI | オープン、Mixtral は MoE |

### 学習の3段階（典型的なLLM）

1. **事前学習（Pre-training）**
   - 大規模コーパスで**次トークン予測**（自己教師あり）
2. **教師ありファインチューニング（SFT）**
   - 指示と理想の応答ペアで微調整（Instruction Tuning）
3. **アライメント / 選好学習**
   - **RLHF**（人間の選好を報酬モデル化 → PPO等で最適化）
   - **DPO**（Direct Preference Optimization, 報酬モデル不要）
   - **Constitutional AI**（憲法ルールに基づくAIフィードバック, Anthropic）

### スケーリング則（Scaling Laws）

- **Kaplan et al. 2020**：性能 ∝ パラメータ・データ・計算量のべき乗
- **Chinchilla（DeepMind, 2022）**：パラメータ数とデータ量を**同等にスケール**するのが計算効率最適
- **創発的能力**：閾値を超える規模で性能が階段状に向上する現象

---

## ファインチューニング・効率化

### PEFT（Parameter-Efficient Fine-Tuning）

巨大モデルの全パラメータ更新は高コスト → 一部のみ更新する手法。

| 手法 | 概要 |
|---|---|
| **LoRA**（Low-Rank Adaptation） | 重みの**低ランク差分行列**のみ学習。元の重みは凍結 |
| **QLoRA** | LoRA + **量子化**（4bit）でメモリ削減 |
| **Adapter** | 各層に小さなモジュール挿入 |
| **Prefix-Tuning / P-Tuning** | プロンプト相当のベクトルのみ学習 |

### 量子化・蒸留

- **量子化（Quantization）**：FP32→INT8/INT4等で軽量化
- **蒸留（Knowledge Distillation）**：大モデル（教師）の出力を小モデル（生徒）が模倣
- **プルーニング**：重要度の低い重みを削除

---

## プロンプトエンジニアリング

| 手法 | 概要 |
|---|---|
| **Zero-shot** | 例示なしで指示のみ |
| **Few-shot / In-Context Learning（ICL）** | 入力に例を数件提示 |
| **Chain-of-Thought（CoT）** | 「ステップバイステップで考えて」と促し中間推論を出させる |
| **Self-Consistency** | 複数のCoTを生成し多数決 |
| **ReAct** | Reasoning + Acting、ツール使用と推論を交互に |
| **Tree of Thoughts (ToT)** | 思考を木構造で探索 |
| **Role Prompting** | 「あなたは〜の専門家です」と役割設定 |

---

## RAG（Retrieval-Augmented Generation, 検索拡張生成）

- **目的**：LLMの知識不足・古さ・ハルシネーション軽減
- **流れ**：質問 → ベクトル検索でドキュメント取得 → LLMにコンテキストとして渡し回答生成
- **構成要素**：
  - **Embedding モデル**（テキスト→ベクトル）
  - **ベクトルDB**（Pinecone, Weaviate, FAISS, pgvector 等）
  - **チャンク分割**戦略
- **効果**：最新情報の参照、企業内データ活用、出典明示

---

## エージェント / ツール使用

- **AIエージェント**：LLMがツール（検索、コード実行、API）を使って多段階タスクを遂行
- **Function Calling / Tool Use**：構造化された関数呼び出しをLLMが生成
- **MCP（Model Context Protocol）**：Anthropic提唱、ツール接続の標準プロトコル
- 代表：AutoGPT, BabyAGI, LangChain, Claude Code

---

## 拡散モデル（Diffusion Models）

画像・動画・音声生成の主流。

- **基本アイデア**：データに**徐々にノイズを加える順過程**と、**ノイズから復元する逆過程**を学習
- **DDPM**（Denoising Diffusion Probabilistic Model, 2020）：基礎
- **Latent Diffusion Model（LDM）**：潜在空間で拡散 → **Stable Diffusion** の基盤
- **Classifier-Free Guidance**：条件付き生成の強度調整

### 代表モデル

| モデル | 開発元 | 特徴 |
|---|---|---|
| **Stable Diffusion** | Stability AI | オープン、LDMベース |
| **DALL·E 2 / 3** | OpenAI | テキスト→画像 |
| **Midjourney** | Midjourney | 高品質画風 |
| **Imagen** | Google | T5 を条件付けに利用 |
| **Sora** | OpenAI | テキスト→動画 |
| **Veo** | Google | テキスト→動画 |

---

## マルチモーダル / VLM

- **CLIP**（OpenAI, 2021）：画像とテキストを**対照学習**で同じ埋め込み空間に → ゼロショット画像分類が可能に
- **Flamingo**（DeepMind）：少数例での画像-言語タスク
- **GPT-4V / GPT-4o**：画像入力対応LLM
- **Gemini**：ネイティブマルチモーダル（画像・音声・動画・テキスト統合）

---

## GAN / VAE（生成モデルの古典）

詳細比較は [10-混同しやすい用語の対比表](10-混同しやすい用語の対比表.md) 参照。

### GAN（Generative Adversarial Network, 2014, Goodfellow）

- **Generator** と **Discriminator** が敵対的に学習（**ミニマックスゲーム**）
- **モード崩壊**：多様性を失い同じ出力ばかり生成する問題
- 派生：DCGAN, Conditional GAN, CycleGAN, StyleGAN, BigGAN, Pix2Pix

### VAE（Variational Autoencoder, 2014, Kingma & Welling）

- 潜在変数の**事後分布を変分推論**で近似
- **ELBO**（Evidence Lower Bound）を最大化
- **再パラメータ化トリック**で勾配を流す
- GANより安定だが画像はぼやけやすい

---

## 生成AI特有の課題・リスク

| 課題 | 概要 | 対策 |
|---|---|---|
| **ハルシネーション** | 事実と異なる内容を自信ありげに生成 | RAG、出典明示、検証 |
| **プロンプトインジェクション** | 悪意ある指示で挙動を乗っ取る | 入出力フィルタ、サンドボックス |
| **ジェイルブレイク** | 安全制約を回避させる | アライメント強化、レッドチーミング |
| **著作権侵害** | 学習データ・生成物の権利問題 | オプトアウト、来歴管理（C2PA） |
| **ディープフェイク** | 偽動画・偽音声 | 電子透かし、検出器 |
| **バイアス** | 学習データの偏りを反映・増幅 | 多様データ、評価 |
| **環境負荷** | 学習・推論の電力消費 | 効率化、量子化、蒸留 |
| **データ汚染（Data Poisoning）** | 学習データに悪意ある混入 | データ来歴管理 |

---

## 法規制・ガイドライン（生成AI関連）

詳細は 6 参照。

- **EU AI Act**（2024成立）：リスクベース規制、汎用AIモデル（GPAI）規定
- **AI事業者ガイドライン**（経産省・総務省, 2024）：開発・提供・利用者の3区分
- **広島AIプロセス**（G7, 2023）：基盤モデル開発者向け国際指針
- **Bletchley宣言**（2023）：AI安全サミット
- **米大統領令 14110**（2023, バイデン）→ 2025年トランプ政権で撤回方向
- **著作権法30条の4**（日本）：情報解析目的の機械学習は原則合法（享受目的を除く）

---

## 評価ベンチマーク

| ベンチマーク | 評価対象 |
|---|---|
| **MMLU** | 多分野知識 |
| **HellaSwag** | 常識推論 |
| **HumanEval** | コード生成 |
| **GSM8K / MATH** | 数学推論 |
| **BIG-bench** | 多様タスク |
| **TruthfulQA** | 真実性 |
| **HELM** | 包括的評価 |
| **Chatbot Arena** | 人間によるペアワイズ比較 |
