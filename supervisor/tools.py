#!/usr/bin/env python3
"""Small audited tool surface. The model only sees these, not a raw root shell."""

from __future__ import annotations

import datetime as dt
import os
import subprocess
from pathlib import Path

AUDIT = Path(os.environ.get("AETHER_AUDIT", "/data/local/tmp/aether-audit.log"))
# Fall back to cwd when we are not on-device yet.
if not AUDIT.parent.exists():
    AUDIT = Path("./aether-audit.log")


def audit(event: str, detail: str) -> None:
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    line = f"{dt.datetime.utcnow().isoformat()}Z\t{event}\t{detail}\n"
    AUDIT.open("a", encoding="utf-8").write(line)


def run(cmd: list[str], timeout: int = 15) -> str:
    audit("exec", " ".join(cmd))
    try:
        p = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError:
        return f"command not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return f"timeout: {cmd[0]}"
    out = (p.stdout or "") + (p.stderr or "")
    return out.strip() or f"(exit {p.returncode}, empty output)"


def host_facts() -> str:
    bits = [
        run(["uname", "-a"]),
        run(["id"]),
    ]
    if Path("/system/build.prop").exists():
        bits.append(run(["getprop", "ro.build.version.release"]))
        bits.append(run(["getprop", "ro.product.model"]))
    return "\n".join(bits)


def list_dir(path: str) -> str:
    target = Path(path)
    if not target.exists():
        return f"missing: {path}"
    audit("ls", path)
    names = []
    try:
        for child in sorted(target.iterdir()):
            mark = "/" if child.is_dir() else ""
            names.append(child.name + mark)
    except PermissionError as e:
        return str(e)
    return "\n".join(names[:200])


def read_text(path: str, limit: int = 4000) -> str:
    target = Path(path)
    if not target.is_file():
        return f"not a file: {path}"
    audit("read", path)
    try:
        data = target.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return str(e)
    return data[:limit]
