"""Package version from SKILL.md frontmatter（skillhub 包内改写，由构建脚本生成）。

主仓库 canonical 为 pyproject.toml [project].version（经 version.py 读取）；
包内无 pyproject，SKILL.md frontmatter 的 version 字段（构建时注入，与主仓库
一致）为包内唯一权威版本。
"""
from __future__ import annotations

from pathlib import Path


def get_package_version(default: str = "unknown", *,
                        stop_at_first: bool = False,
                        _start_dir: Path | None = None) -> str:
    """Read version from the package SKILL.md frontmatter (walk-up)."""
    try:
        root = _start_dir or Path(__file__).resolve().parent
        for parent in [root, *root.parents]:
            md = parent / "SKILL.md"
            if not md.exists():
                continue
            for raw in md.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if line.startswith("version:"):
                    return line.split(":", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    return default
