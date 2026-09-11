# Gemini Enterprise 管理者向け Antigravity ハンズオン

Gemini Enterprise 管理者を対象にした 3 時間のワークショップ教材です。
受講者は各自のローカル PC 上の **Antigravity 2.0** から、Antigravity と対話しながら
エージェントの**開発規約を定め、生成させ、審査し、全社公開する**までを体験します。

📄 **設計書（正本）**: [Google Docs](https://docs.google.com/document/d/1j0rVQYcEe66Qm3IFMxkFXi3OvW7_e7CFgw3eWzMHsvE/edit) / [docs/workshop-guide.md](docs/workshop-guide.md)

## 前提：2 つの層を混同しないこと

| | 開発時ハーネス | 実行時エージェント |
|---|---|---|
| 成果物 | `AGENTS.md` / `skills/*/SKILL.md` | `agent.py` の `instruction=` |
| 読み手 | **Antigravity**（コーディングエージェント） | デプロイされた ADK エージェント |
| デプロイ | **されない** | される |
| 誰が書くか | **受講者（管理者）** | **Antigravity が生成する** |

> [!IMPORTANT]
> `SKILL.md` は Antigravity を動かすためのものであり、エージェント本体の中身ではありません。
> 本ワークショップの因果は **「規約を書く → Antigravity が生成する → 品質が変わる」** という間接的なものです。

## 学習の流れ

```
[配布] 事業部から申請された低品質なエージェント（instruction が 1 文だけ）
   │
   ① AGENTS.md を「全社エージェント開発規約」に書き換える     ← 受講者が書く
   ② /masakari スキルを作成する                                ← 受講者が書く
   ③ Antigravity に agent.py を再生成させる                    ← Antigravity が書く
       └─→ --no-wait で配備を先行起動（＝技術的配備）
   ④ agents-cli eval run → 受入判定シートに記入 → 公開可否を判断 ★山場
   ⑤ 配備の完了確認
   ⑥ Gemini Enterprise に登録 ＝ 全社公開
```

> [!TIP]
> **デプロイ（技術的配備）と公開（承認を伴う経営判断）は別物です。**
> ③ の直後に配備を始め、④ の承認が下りてから ⑥ で公開します。

> [!NOTE]
> Eval は「赤 → 緑の修正ループ」ではなく **「公開してよいかを判断するための受入検査」** です。
> LLM の判定は確率的なため、特定のテストが必ず落ちる前提の設計は当日の運任せになります。
> 本設計では**スコアが何点でも演習が成立**します。判断すること自体が学習目標です。

## タイムテーブル（概要）

| 時間 | パート | 内容 |
| --- | --- | --- |
| 70 分 | 第 1 部 座学 | エージェントの進化 / ハーネス工学（AGENTS.md・SKILL.md・Hooks・MCP）/ SDD |
| 10 分 | 休憩 | 環境の最終疎通確認 |
| 80 分 | 第 2 部 ハンズオン | ①〜⑥ |
| 20 分 | 第 3 部 | ガバナンス（Model Armor / Agent Gateway / IAM）・FinOps・ラップアップ |

## ディレクトリ構成

| パス | 配布 | 内容 |
| --- | --- | --- |
| [`docs/workshop-guide.md`](docs/workshop-guide.md) | 講師 | ワークショップ設計書（本体） |
| [`docs/prerequisites.md`](docs/prerequisites.md) | 受講者 | 事前準備チェックリスト（PC 環境 / API / IAM / GE App） |
| [`starter-kit/`](starter-kit/) | 受講者 | 配布用一式（緩い `AGENTS.md` ＋ 低品質な `agent.py`） |
| [`answers/`](answers/) | 講師のみ | 模範解答。脱落者救済用 |
| [`governance/`](governance/) | 講師 | Model Armor / Agent Gateway の設定サンプル（第 3 部で解説） |

### starter-kit の中身

| ファイル | 層 | 状態 |
| --- | --- | --- |
| `AGENTS.md` | 開発時 | ⚠️ 事業部が書いた 6 行の雑な方針。① で書き換える |
| `agent.py` | 実行時 | ⚠️ `instruction` が 1 文だけ。**手で編集しない** |
| `skills/publish-gemini-enterprise/SKILL.md` | 開発時 | ✅ 講師提供（デプロイ・登録の自動化） |
| `tests/eval/eval_config.yaml` | — | ✅ 安全性 2 種・業務品質 2 種のメトリクス定義 |
| `tests/eval/ACCEPTANCE_CRITERIA.md` | — | ✅ **④ の成果物**となる受入判定シート |

> [!WARNING]
> `answers/` を受講者に事前共有しないでください。演習が成立しなくなります。

## 事前準備

受講者は開催前までに [`docs/prerequisites.md`](docs/prerequisites.md) をすべて完了させてください。

- ローカル PC への Antigravity 2.0 / `uv` / `gcloud` のインストール
- `uv tool install google-agents-cli`
- 必須 API の有効化（`aiplatform` / `cloudbuild` / `artifactregistry` / `discoveryengine`）
- IAM ロールの付与
- Gemini Enterprise アプリの事前作成

> [!CAUTION]
> **講師は開催前に必ず事前ドライランを実施してください**（設計書 7-3）。
> `agents-cli eval run` がスキーマエラーなく完走することの確認が最優先です。

## 受講者の始め方

```bash
cp -r workshops/gemini-enterprise-admin/starter-kit ~/ge-workshop
cd ~/ge-workshop

agents-cli eval run \
  --dataset tests/eval/datasets/agent_eval.json \
  --config  tests/eval/eval_config.yaml
```
