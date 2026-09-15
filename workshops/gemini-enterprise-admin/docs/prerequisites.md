# ワークショップ事前準備チェックリスト

開催前日までに以下の準備を完了してください。

---

## 1. 【管理者・情シス】GCP 環境の準備

### 1-1. GCP プロジェクトの選定・準備
以下のいずれかの方針でプロジェクトを準備してください。

- **パターン 1（推奨）：新規プロジェクトを作成する**
  - 既存リソースへの影響がなく、ワークショップ終了後にプロジェクトごと削除できるため管理が容易です。
- **パターン 2：既存の開発・検証用（Sandbox）プロジェクトを利用する**
  - 受講者にデプロイやビルドの権限を付与するため、本番環境や機密データが存在するプロジェクトは避けてください。

### 1-2. API の有効化
プロジェクトで必要な API を有効化します。

```bash
gcloud services enable \
  aiplatform.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  discoveryengine.googleapis.com \
  --project=YOUR_PROJECT_ID
```

### 1-3. 受講者アカウントへの IAM ロール付与
受講者の Google アカウントに以下のロールを付与します。

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
> サンプルエージェントは外部システムに接続せず、コード内のダミーデータを返すため、BigQuery などのデータストア権限は不要です。

### 1-4. Gemini Enterprise App の作成
Cloud Console の **Gemini Enterprise** → **Apps** から、登録先となるアプリを事前に 1 つ作成してください。

### 1-5. 受講者への案内
準備完了後、受講者に **GCP プロジェクト ID** を共有してください。

---

## 2. 【受講者】PC 環境のセットアップ

### 2-1. Antigravity 2.0 のインストール
Antigravity を起動し、チャットが応答することを確認してください。

### 2-2. uv のインストール
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# PATH の設定
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 確認
uv --version
```

### 2-3. agents-cli のインストール
```bash
uv tool install google-agents-cli

# 確認
agents-cli --version
```

---

## 3. 【受講者】事前疎通テスト

管理者から共有された `PROJECT_ID` を設定し、以下のコマンドをターミナルで実行してください。

```bash
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

すべて ✅ OK と表示されるかご確認ください。
※ 「❌ ADC」と表示された場合は、`gcloud auth application-default login` を実行して再試行してください。
