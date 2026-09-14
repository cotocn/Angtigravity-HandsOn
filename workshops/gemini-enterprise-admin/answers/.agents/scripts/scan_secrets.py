#!/usr/bin/env python3
"""Stop フック: シークレットがソースコードに直書きされていないか検査する。

Antigravity が「作業を終えよう」とした瞬間にこのスクリプトが呼ばれる。
問題が見つかれば、終了を拒否してエージェントに差し戻す。

出力の契約（厳密）:
  - 差し戻す: {"decision": "continue", "reason": "..."} を出力して exit 0
  - 通す    : 何も出力せず exit 0

【重要 1】decision が "continue" または "block" のときだけエージェントは続行する。
          それ以外の値を返すと、そのまま終了してしまう。
【重要 2】reason はシステムメッセージとしてエージェントに届く。
          「何が悪いか」だけでなく「どう直すか」を書くこと。
【重要 3】Stop フックは "fails open"。このスクリプトが異常終了すると、
          ブロックされずに終了してしまう（しかも何も表示されない）。
          だから絶対に例外を外に出さない。
"""

import json
import os
import pathlib
import re
import sys
import tempfile

# 「〜KEY / 〜TOKEN / 〜SECRET / 〜PASSWORD」という名前の変数に、
# 16 文字以上の文字列リテラルを直接代入している行を探す。
#
#   NG: ITSM_API_KEY = "sk-itsm-live-9f3a2b7c8d1e4f60"
#   OK: ITSM_API_KEY = os.environ.get("ITSM_API_KEY", "")   ← 右辺が文字列リテラルでない
SECRET_PATTERN = re.compile(
    r"""(\w*(?:KEY|TOKEN|SECRET|PASSWORD))\s*=\s*["']([^"']{16,})["']""",
    re.IGNORECASE,
)

# 同じ会話で何度もブロックし続けると無限ループになるため、上限を設ける。
MAX_BLOCKS_PER_CONVERSATION = 3

# プロジェクトのルート（このスクリプトは <root>/.agents/scripts/ に置かれている）。
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]
SCAN_TARGET = PROJECT_ROOT / "app"


def find_secrets() -> list[str]:
    """直書きされたシークレットを探して、指摘文のリストを返す。"""
    findings = []
    if not SCAN_TARGET.is_dir():
        return findings

    for path in sorted(SCAN_TARGET.rglob("*.py")):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        for lineno, line in enumerate(lines, start=1):
            match = SECRET_PATTERN.search(line)
            if match:
                rel = path.relative_to(PROJECT_ROOT)
                findings.append(f"  - {rel}:{lineno}  変数 {match.group(1)}")
    return findings


def block_count(conversation_id: str) -> int:
    """この会話で既に何回ブロックしたかを数える（無限ループ防止）。"""
    if not conversation_id:
        return 0
    marker = pathlib.Path(tempfile.gettempdir()) / f"scan_secrets_{conversation_id}.count"
    try:
        count = int(marker.read_text()) if marker.exists() else 0
        marker.write_text(str(count + 1))
        return count
    except Exception:
        return 0


def main() -> None:
    conversation_id = ""
    try:
        payload = json.load(sys.stdin)
        conversation_id = str(payload.get("conversationId", ""))
    except Exception:
        pass

    try:
        findings = find_secrets()
    except Exception:
        # 検査そのものが壊れた。止める根拠がないので通す。
        return

    if not findings:
        return

    if block_count(conversation_id) >= MAX_BLOCKS_PER_CONVERSATION:
        # 何度差し戻しても直らない。これ以上は人間が見る。
        return

    reason = (
        "【ガードレールによる差し戻し】\n"
        "シークレットがソースコードに直書きされています。\n\n"
        + "\n".join(findings)
        + "\n\n"
        "全社エージェント開発規約に従い、環境変数から読み込むよう修正してください。\n"
        "例:\n"
        '    ITSM_API_KEY = os.environ.get("ITSM_API_KEY", "")\n\n'
        "修正したうえで、再度作業を完了してください。"
    )

    print(json.dumps({"decision": "continue", "reason": reason}, ensure_ascii=False))


if __name__ == "__main__":
    main()
