"""社内 IT ヘルプデスク・アシスタント。

事業部から全社公開の申請が出ているエージェント。
あなたは Gemini Enterprise 管理者として、これを審査する立場にある。

【重要】このファイルを手で編集しないこと。
        修正が必要な場合は .agents/AGENTS.md（全社エージェント開発規約）を整備し、
        Antigravity に直させること。
"""

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

MODEL = "gemini-3.8-flash"

# --- 社内チケットシステム (ITSM) への接続情報 -------------------------------
ITSM_ENDPOINT = "https://itsm.example.corp/api/v1"
ITSM_API_KEY = "sk-itsm-live-9f3a2b7c8d1e4f60"


# --- ダミーデータ -----------------------------------------------------------
# 本ワークショップでは外部システムに接続しない。
_FAQ = {
    "vpn": "VPN に接続できない場合は、社内 Wi-Fi を一度切断してから再接続してください。",
    "password": "パスワードの再設定は社内ポータルの「アカウント管理」から行えます。",
    "printer": "プリンタが見つからない場合は、IP アドレス 10.0.32.15 を手動で追加してください。",
    "vdi": "VDI が遅い場合は、セッションを一度サインアウトしてから再接続してください。",
}

_TICKETS = {
    "INC-1001": {"status": "対応中", "assignee": "IT 基盤チーム", "summary": "VPN 接続不可"},
    "INC-1002": {"status": "解決済", "assignee": "ヘルプデスク", "summary": "パスワードロック"},
    "INC-1003": {"status": "保留", "assignee": "調達チーム", "summary": "モニタ交換依頼"},
}


def search_faq(keyword: str) -> dict:
    """社内 IT の FAQ をキーワードで検索する。

    Args:
      keyword: 検索キーワード（例: "vpn", "password"）。

    Returns:
      一致した FAQ の辞書。
    """
    hits = {k: v for k, v in _FAQ.items() if keyword.lower() in k}
    return {"results": hits}


def lookup_ticket(ticket_id: str) -> dict:
    """チケット ID を指定して、問い合わせの対応状況を照会する。

    Args:
      ticket_id: チケット ID（例: "INC-1001"）。

    Returns:
      チケットの状態。
    """
    # 本来はここで ITSM API を呼び出す。
    _headers = {"Authorization": f"Bearer {ITSM_API_KEY}"}
    return _TICKETS.get(ticket_id, {"error": "該当するチケットがありません"})


root_agent = Agent(
    name="helpdesk_agent",
    model=Gemini(model=MODEL, retry_options=types.HttpRetryOptions(attempts=3)),
    description="社内 IT の問い合わせに対応するヘルプデスク・アシスタント",
    instruction="社内 IT の問い合わせに答えてください。",
    tools=[search_faq, lookup_ticket],
)

app = App(root_agent=root_agent, name="app")
