"""Root Agent definition for Gemini Enterprise using Google ADK."""

import os
from google.adk.agents import Agent

# AGENTS.md の内容を読み込んでシステム指示としてバインド
AGENTS_MD_PATH = os.path.join(os.path.dirname(__file__), "AGENTS.md")
instructions = "You are a professional enterprise advisory assistant."
if os.path.exists(AGENTS_MD_PATH):
    with open(AGENTS_MD_PATH, "r", encoding="utf-8") as f:
        instructions = f.read()

# ADK root_agent の定義（ツール依存なし・ハーネス＆スキル連携）
root_agent = Agent(
    name="enterprise_advisory_agent",
    model="gemini-2.5-flash",
    description="全社向け業務課題解決・企画立案・戦略サマリー作成を支援する認定エージェント",
    instruction=instructions,
)
