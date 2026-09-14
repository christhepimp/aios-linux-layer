#!/usr/bin/env python3
"""Aether session — the face of the AI OS.

This is a local, offline control loop so the repo runs with zero API keys.
Swap `think()` later for a real model that emits tool calls.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow `python3 aether.py` from this folder.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import tools

BANNER = """
Aether OS session  v0
Linux stays the kernel. I am the operating layer.

Commands:
  facts          who/where am I
  ls [path]      list a directory
  read [path]    read a text file
  exec <cmd>     run an allowlisted binary (see policy/allowlist.yaml)
  help           this text
  exit           leave the session

Type like a person. I will map it onto tools.
""".strip()


def think(user: str) -> str:
    text = user.strip()
    low = text.lower()

    if low in {"help", "?"}:
        return BANNER
    if low in {"facts", "who are you", "where am i", "status"}:
        return tools.host_facts()
    if low.startswith("ls") or low.startswith("list "):
        parts = text.split(maxsplit=1)
        path = parts[1] if len(parts) > 1 else "."
        return tools.list_dir(path)
    if low.startswith("read ") or low.startswith("cat "):
        path = text.split(maxsplit=1)[1]
        return tools.read_text(path)
    if low.startswith("exec "):
        cmd = text.split(maxsplit=1)[1].split()
        if not cmd:
            return "exec what?"
        # Hard deny the worst verbs even in the stub.
        if cmd[0] in {"rm", "dd", "mkfs", "reboot"}:
            return f"denied by policy: {cmd[0]}"
        return tools.run(cmd)
    if "kernel" in low or "linux" in low:
        return (
            "I am running on a Linux kernel. Replacing that kernel is Phase 6.\n"
            "Right now I own the session and the tool surface. Type `facts`."
        )
    if "os" in low or "who" in low:
        return "I am Aether, the AI operating layer. Linux is my body. You talk to me."

    return (
        "I heard you. In v0 I only run local tools.\n"
        "Try: facts | ls /proc | read /proc/version | exec uname -a"
    )


def main() -> int:
    print(BANNER)
    print()
    print(tools.host_facts())
    print()
    while True:
        try:
            user = input("aether> ")
        except (EOFError, KeyboardInterrupt):
            print("\nbye")
            return 0
        if user.strip().lower() in {"exit", "quit"}:
            print("bye")
            return 0
        print(think(user))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
