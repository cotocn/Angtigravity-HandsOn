# Gemini Enterprise 管理者向け Antigravity ハンズオン

Gemini Enterprise 管理者を対象にした 3 時間のワークショップ教材です。
受講者は各自のローカル PC 上の **Antigravity 2.0** から、Antigravity と対話しながら段階的にエージェントを組み上げます。

## 学習の流れ

```
① AGENTS.md 作成 → ② Skill 作成 → ③ Eval 自動生成（赤）
   → ④ AGENTS.md / SKILL.md 修正（緑）→ ⑤ Agent Runtime デプロイ → ⑥ Gemini Enterprise 登録
```

講師が用意した **意図的に欠陥のあるベースエージェント** に対して Antigravity に Eval を自動生成させ、
テストが落ちる（赤）ことを確認 → コードではなく `AGENTS.md` / `SKILL.md` を修正して通す（緑）、という
「Quality Flywheel」を体験するのが本ワークショップの核です。

> [!IMPORTANT]
> 受講者に Python コードは修正させません。エージェントの振る舞いは
> **ハーネス（AGENTS.md / SKILL.md）で制御できる**ことを体感させるのが狙いです。

## タイムテーブル（概要）

| 時間 | パート | 内容 |
| --- | --- | --- |
| 70 分 | 第 1 部 座学 | エージェントの進化 / ハーネス工学（AGENTS.md・SKILL.md・Hooks・MCP）/ SDD |
| 10 分 | 休憩 | ※ この間に Agent Runtime への非同期デプロイを先行実行 |
| 80 分 | 第 2 部 ハンズオン | ①〜⑥ |
| 20 分 | 第 3 部 | ガバナンス（Model Armor / Agent Gateway / IAM）・FinOps・ラップアップ |

詳細は [`docs/workshop-guide.md`](docs/workshop-guide.md) を参照してください。

## ディレクトリ構成

| パス | 配布 | 内容 |
| --- | --- | --- |
| [`docs/workshop-guide.md`](docs/workshop-guide.md) | 講師 | ワークショップ設計書（本体） |
| [`docs/prerequisites.md`](docs/prerequisites.md) | 受講者 | 事前準備チェックリスト（PC 環境 / API / IAM / GE App） |
| [`starter-kit/`](starter-kit/) | 受講者 | 配布用のベースエージェント一式（**意図的な欠陥入り**） |
| [`answers/`](answers/) | 講師のみ | 模範解答。脱落者救済用 |
| [`governance/`](governance/) | 講師 | Model Armor / Agent Gateway の設定サンプル（第 3 部で解説） |

> [!WARNING]
> `answers/` を受講者に事前共有しないでください。演習が成立しなくなります。

## 事前準備

受講者は開催前までに [`docs/prerequisites.md`](docs/prerequisites.md) をすべて完了させてください。
主な項目は以下の通りです。

- ローカル PC への Antigravity 2.0 / `uv` / `gcloud` のインストール
- `uv tool install google-agents-cli`
- 必須 API の有効化（`aiplatform` / `cloudbuild` / `artifactregistry` / `discoveryengine`）
- IAM ロールの付与
- Gemini Enterprise アプリの事前作成

## 受講者の始め方

```bash
# starter-kit をローカルにコピーして作業ディレクトリとする
cp -r workshops/gemini-enterprise-admin/starter-kit ~/ge-workshop
cd ~/ge-workshop

# 以降は Antigravity 2.0 のターミナル / チャットから作業する
```
