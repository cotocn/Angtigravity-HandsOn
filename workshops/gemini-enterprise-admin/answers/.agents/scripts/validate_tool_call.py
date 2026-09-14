#!/usr/bin/env python3
"""PreToolUse フック: 破壊的なシェルコマンドの実行を遮断する。

Antigravity は run_command を実行する「前」にこのスクリプトを呼び出す。
標準入力に実行しようとしているコマンドが JSON で渡ってくるので、
それを検査して、危険なら標準出力に拒否を返す。

出力の契約（厳密）:
  - 拒否する  : {"decision": "deny", "reason": "..."} を出力して exit 0
  - 通す      : 何も出力せず exit 0
  - 判断不能  : 何も出力せず exit 0（= 通す）

【重要】PreToolUse は "fails closed" である。
        このスクリプトが異常終了したり、契約外のキーを出力すると、
        エージェントは run_command を一切実行できなくなる。
        だから「わからないものは通す」を徹底する。
"""

import json
import sys

# 実行を許さないコマンドのパターン。
DENYLIST = (
    "rm -rf /",
    "rm -rf ~",
    "mkfs",
    "dd if=",
    ":(){",          # フォーク爆弾
    "chmod -R 777 /",
)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        # 入力が読めない。判断できないので通す。
        return

    # 実測済みのキー構造: {"toolCall": {"name": ..., "args": {"CommandLine": ...}}}
    command = ""
    try:
        command = payload["toolCall"]["args"]["CommandLine"]
    except Exception:
        return

    if not isinstance(command, str):
        return

    normalized = " ".join(command.split())

    for pattern in DENYLIST:
        if pattern in normalized:
            print(
                json.dumps(
                    {
                        "decision": "deny",
                        "reason": (
                            f"このコマンドは全社エージェント開発規約により禁止されています: {pattern}\n"
                            "破壊的な操作は実行できません。"
                            "目的を達成する別の手段を検討してください。"
                        ),
                    },
                    ensure_ascii=False,
                )
            )
            return

    # 問題なし。何も出力しないのが最も安全な「通過」。


if __name__ == "__main__":
    main()
