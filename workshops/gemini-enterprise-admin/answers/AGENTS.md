# Coding Agent Guide

## Prerequisites

Install the CLI (one-time):
```bash
uv tool install google-agents-cli
```

---

## Development Phases

### Phase 1: Understand Requirements
Before writing any code, understand the project's requirements, constraints, and success criteria.

### Phase 2: Build and Implement
Implement agent logic in `app/`. Use `agents-cli playground` for interactive testing. Iterate based on user feedback.

### Phase 3: The Evaluation Loop (Main Iteration Phase)
Start with 1-2 eval cases, run `agents-cli eval run`, iterate by making changes and rerunning it until satisfied. Expect 5-10+ iterations. Once you have a baseline, reach for `agents-cli eval compare` (regression diffs), `agents-cli eval analyze` (cluster failure modes), and `agents-cli eval optimize` (auto-tune prompts). See the **Evaluation Guide** for metrics, dataset schema, LLM-as-judge config, and common gotchas.

### Phase 4: Pre-Deployment Tests
Run `uv run pytest tests/unit tests/integration`. Fix issues until all tests pass.

### Phase 5: Deploy to Dev
**Requires explicit human approval.** Run `agents-cli deploy` only after user confirms. See the **Deployment Guide** for details.

### Phase 6: Production Deployment
Ask the user: Option A (simple single-project) or Option B (full CI/CD pipeline with `agents-cli infra cicd`).

## Development Commands

| Command | Purpose |
|---------|---------|
| `agents-cli playground` | Interactive local testing |
| `uv run pytest tests/unit tests/integration` | Run unit and integration tests |
| `agents-cli eval dataset synthesize` | Synthesize multi-turn eval scenarios for your agent |
| `agents-cli eval run` | Run the agent over the eval dataset and grade the traces |
| `agents-cli eval generate` / `agents-cli eval grade` | Decoupled form: produce traces, then grade them |
| `agents-cli eval compare` | Compare two grade-results files (regression check) |
| `agents-cli eval analyze` | Cluster failure modes from grade results |
| `agents-cli eval metric list` | List built-in metrics available in the SDK |
| `agents-cli eval optimize` | Auto-tune agent prompts using eval data |
| `agents-cli lint` | Check code quality |
| `agents-cli infra single-project` | Set up project infrastructure (Terraform) |
| `agents-cli deploy` | Deploy to dev |
| `agents-cli scaffold enhance` | Add deployment target or CI/CD to project |
| `agents-cli scaffold upgrade` | Upgrade project to latest version |

---

## Operational Guidelines for Coding Agents

- **Code preservation**: Only modify code directly targeted by the user's request. Preserve all surrounding code, config values (e.g., `model`), comments, and formatting.
- **NEVER change the model** unless explicitly asked.
- **Model 404 errors**: Fix `GOOGLE_CLOUD_LOCATION` (e.g., `global` instead of `us-east1`), not the model name.
- **ADK tool imports**: Import the tool instance, not the module: `from google.adk.tools.load_web_page import load_web_page`
- **Run Python with `uv`**: `uv run python script.py`. Run `agents-cli install` first.
- **Stop on repeated errors**: If the same error appears 3+ times, fix the root cause instead of retrying.
- **Terraform conflicts** (Error 409): Use `terraform import` instead of retrying creation.

---

## 全社エージェント開発規約

本プロジェクトで作業するエージェント（Antigravity）は、以下に必ず従うこと。

### 1. シークレットをソースコードに書かない

API キー・アクセストークン・パスワードなどの秘密情報を、
Python ファイルに文字列として直接記述してはならない。必ず環境変数から読み込むこと。

```python
# ❌ 禁止
ITSM_API_KEY = "sk-itsm-live-9f3a2b7c8d1e4f60"

# ✅ 正しい
import os
ITSM_API_KEY = os.environ.get("ITSM_API_KEY", "")
```

秘密情報の実体は `.env` に置く。`.env` はバージョン管理に含めない。
`.env.example` にはキーの名前だけを書き、値は空にしておくこと。

### 2. シェル実行の制限

`.agents/hooks.json` で明示的に承認されていない限り、
破壊的なシェルコマンドを実行してはならない。
ファイルの削除・権限変更・ディスク操作が必要な場合は、実行前に理由を説明すること。

### 3. ブロック時の是正ループ

ガードレール（フック）によって作業がブロックされた場合、
**それを「修正すべき欠陥が見つかった」という通知として扱うこと。**

1. ブロックの理由を最後まで読む。指摘されたファイル名と行番号を確認する。
2. 指摘された箇所を修正する。
3. 修正が正しいことを確認する。
4. 再度、作業の完了を試みる。

> [!IMPORTANT]
> **ブロックを回避しようとしてはならない。**
> チェックを無効化する、検査対象から外す、別名にして隠す——といった対応は禁止する。
> ブロックされたまま「対応できませんでした」と報告して終わることも禁止する。

### 4. 一次情報の検証

推測で回答してはならない。
ファイルの内容・コマンドの出力を実際に確認したうえで述べること。
確認できていないことは「確認できていない」と明示する。

---

> [!NOTE]
> **この規約は Antigravity（コーディングエージェント）に向けたものです。**
> デプロイされるエージェント本体の振る舞いを決めるのは `app/agent.py` の
> `instruction=` であり、このファイルではありません。両者を混同しないこと。
