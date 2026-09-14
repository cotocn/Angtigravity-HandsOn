# 【必読】ワークショップ事前準備チェックリスト

> **開催前日までに必ず完了させ、講師までご報告ください。**
> 未完了の場合、当日のデプロイ・登録フェーズで進行できなくなります。

---

## A. 受講者 PC 環境（各自で実施）

### A-1. Antigravity 2.0 のインストール
アプリを起動し、チャットが応答することを確認してください。

### A-2. Google Cloud CLI の認証
```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
gcloud config list
```

### A-3. uv のインストール
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 確認
uv --version
```

### A-4. agents-cli のインストール【最重要】
```bash
uv tool install google-agents-cli

# 確認（★このコマンドが通ることを必ず報告してください）
agents-cli --version
```

---

## B. GCP プロジェクト側の準備（情シス・管理者が実施）

### B-1. 必須 API の有効化
```bash
gcloud services enable \
  aiplatform.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  discoveryengine.googleapis.com \
  --project=YOUR_PROJECT_ID
```

> API 有効化の伝播には時間がかかる場合があります。**当日ではなく前日までに**実施してください。

### B-2. 受講者アカウントに付与する IAM ロール

| ロール | 用途 |
|---|---|
| `roles/aiplatform.user` | Gemini モデル呼び出し、Agent Runtime へのデプロイ |
| `roles/discoveryengine.admin` | Gemini Enterprise Agent Registry への登録 |
| `roles/cloudbuild.builds.editor` | デプロイ時のコンテナイメージビルド |
| `roles/storage.objectUser` | ビルド成果物の読み書き |
| `roles/iam.serviceAccountUser` | エージェント実行サービスアカウントの引き受け |

```bash
# 付与例
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="user:participant@example.com" \
  --role="roles/aiplatform.user"
```

> [!NOTE]
> 本ワークショップのサンプルエージェントは **外部システムに接続しません**。
> FAQ 検索もチケット照会もコード内のダミーデータを返すだけなので、
> BigQuery などデータストア側の権限は一切不要です。


### B-3. Gemini モデルの疎通確認【必ず実施】

前日までに、受講者アカウント（もしくは同等の権限）で以下が通ることを確認してください。

```bash
gcloud ai endpoints list --region=us-east1 --project=YOUR_PROJECT_ID >/dev/null \
  && echo "aiplatform への疎通 OK"
```

> モデルは `gemini-3.8-flash` を使用します。対象プロジェクト／リージョンで
> 当該モデルが利用可能かを、講師が事前に 1 度呼び出して確認しておいてください。

### B-4. デプロイ時の環境変数の受け渡し

ハンズオン④で、受講者はソースコードに直書きされた `ITSM_API_KEY` を
**環境変数から読み込む形へ修正**します。デプロイ後もエージェントが同じ値を
参照できるよう、環境変数を渡す手段を確認しておいてください。

```bash
# .env に定義した値をデプロイ時に引き渡す
agents-cli deploy --update-env-vars "ITSM_API_KEY=${ITSM_API_KEY}"
```

> [!NOTE]
> 本ワークショップの `ITSM_API_KEY` は**ダミー値**です。実在のシステムには接続しません。
> 「直書きをやめて外から注入する」という**型を体験すること**が目的です。

> [!TIP]
> `agents-cli deploy` は Secret Manager からの注入にも対応しています。
> 本番ではこちらを使ってください。
>
> ```bash
> agents-cli deploy --secrets "ITSM_API_KEY=itsm-api-key:latest"
> ```
>
> この場合、エージェント実行サービスアカウントに
> `roles/secretmanager.secretAccessor` の付与が必要です。
> 第3部のガバナンス講義でこの流れを解説します。




---

## C. Gemini Enterprise 側の準備（管理者が実施）

### C-1. Gemini Enterprise App の作成
Cloud Console → **Gemini Enterprise** → **Apps** から、登録先となるアプリを事前に作成してください。

### C-2. App ID の控えと受講者への配布
以下の形式のフルリソース名を控え、受講者に配布します。

```
projects/<PROJECT_NUMBER>/locations/global/collections/default_collection/engines/<APP_ID>
```

### C-3. 受講者側での環境変数設定
```bash
export GEMINI_ENTERPRISE_APP_ID="projects/.../engines/your-app"
```

---

## D. 講師側の当日リスク対策

| リスク | 対策 |
|---|---|
| **クォータ枯渇** | 同時デプロイが集中する場合は 2 バッチに分割、または受講者ごとにプロジェクトを分離 |
| **デプロイ長時間化** | `--no-wait` による非同期デプロイを徹底し、待ち時間中に Eval を実施 |
| **脱落者の発生** | 完成済みプロジェクトを講師が画面共有し、詰まった受講者も流れを追えるようにする |
| **カタログ反映ラグ** | Gemini Enterprise への反映待ち時間に第3部の講義を先行開始できるよう進行を調整 |
