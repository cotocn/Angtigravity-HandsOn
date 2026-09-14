"""社内 IT ヘルプデスク・アシスタント（修正後の到達点）。

ハンズオン④で、Stop フックに差し戻されたエージェントが
自己修正した結果、このような形になる。

主な変更点:
  1. ITSM_API_KEY をソースコードから削除し、環境変数から読み込むようにした。
  2. instruction を、規約に沿った具体的なものに書き直した。
"""

import os

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

MODEL = "gemini-3.8-flash"

# --- 社内チケットシステム (ITSM) への接続情報 -------------------------------
# 規約 1 に従い、秘密情報はソースコードに書かず環境変数から読み込む。
ITSM_ENDPOINT = os.environ.get("ITSM_ENDPOINT", "https://itsm.example.corp/api/v1")
ITSM_API_KEY = os.environ.get("ITSM_API_KEY", "")


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


INSTRUCTION = """\
あなたは社内 IT ヘルプデスクのアシスタントです。
社員からの IT に関する問い合わせに、社内の一次情報に基づいて回答します。

# 回答の作り方

まず `search_faq` で該当する FAQ を検索してください。
チケット番号（INC- で始まる文字列）を含む問い合わせには `lookup_ticket` を使ってください。

ツールで確認できた内容だけを根拠に回答してください。
FAQ に無いこと、チケットに記載のないことを推測で補ってはいけません。
該当する情報が見つからない場合は、見つからなかったことを正直に伝え、
IT ヘルプデスク（内線 1234）への連絡を案内してください。

# 回答の構造

1. **結論** — 問いに対する直接の答え。
2. **手順** — 利用者が実行すべき操作を順番に。
3. **参照元** — どの FAQ / チケットに基づくか。

# 応対の姿勢

丁寧で簡潔な日本語で回答してください。
専門用語には短い補足を添えてください。
"""

root_agent = Agent(
    name="helpdesk_agent",
    model=Gemini(model=MODEL, retry_options=types.HttpRetryOptions(attempts=3)),
    description="社内 IT の問い合わせに対応するヘルプデスク・アシスタント",
    instruction=INSTRUCTION,
    tools=[search_faq, lookup_ticket],
)

app = App(root_agent=root_agent, name="app")
