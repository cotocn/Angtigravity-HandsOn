# 【必読】ワークショップ事前準備チェックリスト

> **開催前日までに必ず完了させ、講師までご報告ください。**
> 未完了の場合、当日のハンズオン（受入評価やデプロイ）で進行できなくなります。

---

## A. 受講者 PC 環境（各自で実施）

### A-1. Antigravity 2.0 のインストール
アプリを起動し、チャットが正常に応答することを確認してください。

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

# PATH の永続化（★必ず実行してください）
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 確認
uv --version
```

### A-4. agents-cli のインストール【最重要】
```bash
uv tool install google-agents-cli

# 確認コマンド（★このコマンドが通ることを必ず確認してください）
agents-cli --version
```

---

### A-5. 事前疎通テスト（ワンライナー実行）【必ず実施】

各自の PC 環境および GCP 権限が正しく設定されているかを、以下のコマンドをターミナルに貼り付けて一括検証してください。

```bash
# プロジェクトIDを設定して実行（YOUR_PROJECT_ID を当日のプロジェクトIDに置き換えてください）
PROJECT_ID="YOUR_PROJECT_ID"

echo "=== 1. CLI ツールの確認 ==="
which uv >/dev/null && echo "✅ uv: OK" || echo "❌ uv: 未インストールです"
which agents-cli >/dev/null && echo "✅ agents-cli: OK ($(agents-cli --version))" || echo "❌ agents-cli: PATH が通っていません (export PATH=\"\$HOME/.local/bin:\$PATH\" を実行してください)"

echo "=== 2. ADC 認証の確認 ==="
test -f ~/.config/gcloud/application_default_credentials.json && echo "✅ ADC: OK" || echo "❌ ADC: gcloud auth application-default login を実行してください"

echo "=== 3. クラウド接続・権限の確認 ==="
gcloud ai endpoints list --region=us-east1 --project="$PROJECT_ID" --limit=1 >/dev/null 2>&1 \
  && echo "✅ Vertex AI 権限: OK" || echo "❌ Vertex AI: aiplatform.googleapis.com 未有効化、または roles/aiplatform.user 権限が不足しています"

gcloud builds list --project="$PROJECT_ID" --limit=1 >/dev/null 2>&1 \
  && echo "✅ Cloud Build 権限: OK" || echo "❌ Cloud Build: roles/cloudbuild.builds.editor 権限が不足しています"
```

> [!IMPORTANT]
> **すべて ✅ OK と表示された画面（または実行ログ）を、前日 17:00 までに講師へご報告ください。**

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

> API 有効化の反映には時間がかかる場合があります。**当日ではなく前日までに**実施してください。

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
