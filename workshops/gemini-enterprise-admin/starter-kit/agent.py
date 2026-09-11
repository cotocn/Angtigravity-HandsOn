"""事業部が作成した業務改善アドバイザーエージェント。

全社公開の申請が出ている状態。あなたは Gemini Enterprise 管理者として
このエージェントを審査する立場にある。

【重要】このファイルを手で編集しないこと。
        修正が必要な場合は AGENTS.md（全社エージェント開発規約）を整備し、
        Antigravity に再生成させること。
"""

from google.adk.agents import Agent

root_agent = Agent(
    name="enterprise_advisory_agent",
    model="gemini-2.5-flash",
    description="業務改善アドバイザー",
    instruction=(
        "あなたは業務改善アドバイザーです。"
        "社内のビジネスユーザーからの相談に、親切に答えてください。"
    ),
)
