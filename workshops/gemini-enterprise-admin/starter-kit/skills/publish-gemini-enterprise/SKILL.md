---
name: publish-gemini-enterprise
description: >
  ADK エージェントを Agent Runtime にデプロイし（非同期デプロイ対応）、
  Gemini Enterprise の Agent Registry に自動登録・社内公開するスキル。
  「Agent Runtime にデプロイして」「デプロイの状況を確認して」「Gemini Enterprise に登録して」
  「社員が使えるように公開して」と指示された際に呼び出されます。
---

# Agent Runtime デプロイ ＆ Gemini Enterprise 登録スキル

エージェントを Vertex AI Agent Runtime にデプロイし、Gemini Enterprise の全社カタログから呼び出せるようにする自動実行手順です。

> [!IMPORTANT]
> **デプロイは 5〜10 分（初回はさらに長い）かかります。**
> ワークショップでは必ず `--no-wait` による**非同期デプロイ**を使い、待ち時間中に品質評価（Eval）を進めてください。

## 実行手順

### ステップ 1: 前提条件のチェック
- ワークスペース内に `agent.py`（`root_agent`）が存在することを確認します。
- 環境変数 `GOOGLE_CLOUD_PROJECT` と `GEMINI_ENTERPRISE_APP_ID` が設定されているか確認します。
- 必要な API（`aiplatform`, `cloudbuild`, `artifactregistry`, `discoveryengine`）が有効か確認します。

### ステップ 2: Agent Runtime への非同期デプロイ開始
```bash
agents-cli deploy --deployment-target agent_runtime --no-wait
```

- コマンドは即座に戻り、デプロイはクラウド側でバックグラウンド進行します。
- ユーザーに「デプロイを開始しました。完了までの間に品質評価（Eval）を進めましょう」と案内してください。

### ステップ 3: デプロイ完了の確認
```bash
agents-cli deploy --status
```

- 完了が検出されると `deployment_metadata.json`（Agent Runtime ID を含む）が自動生成されます。
- まだ実行中の場合は、数分待ってから再度確認するよう案内してください。

### ステップ 4: Gemini Enterprise Agent Registry への登録
`deployment_metadata.json` から Agent Runtime ID が自動検出されるため、以下のコマンドのみで登録が完了します。

```bash
agents-cli publish gemini-enterprise \
  --registration-type adk \
  --gemini-enterprise-app-id "$GEMINI_ENTERPRISE_APP_ID" \
  --display-name "業務改善・戦略アドバイザリー" \
  --description "業務課題の構造化、施策立案、提案サマリー作成を支援する全社認定AIアシスタント" \
  --tool-description "業務課題の分析と改善提案骨子の作成"
```

> **補足**: ADK エージェントを Agent Runtime にデプロイした場合、Gemini Enterprise は `:streamQuery` を通じてネイティブに呼び出すため、Agent Card URL やプロキシ設定は不要です。

### ステップ 5: 完了報告
登録完了後、受講者に以下を案内してください：
1. Gemini Enterprise の Web コンソール URL
2. 社内エージェントカタログに「業務改善・戦略アドバイザリー」が追加された旨
3. **カタログへの反映には数分のラグが生じる場合がある**こと
4. エンドユーザーとしてチャット対話し、最終的な動作確認を行う手順
