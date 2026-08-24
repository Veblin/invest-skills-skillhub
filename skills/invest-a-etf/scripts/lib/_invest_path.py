"""包内路径 shim（由 build_skillhub_packages.py 生成）。

主仓库的 shim 把共享 skills/lib 加入 sys.path；包内全部模块单份落在本 lib 包，
本模块可能在顶层上下文被裸导入（__package__ 为空）→ 内部用裸导入。
把 lib 目录与包根/scripts 加入 sys.path，使裸 `invest_path` 与 `lib.X` 均可解析。
"""
from __future__ import annotations

import sys
from pathlib import Path

_lib = Path(__file__).resolve().parent
if str(_lib) not in sys.path:
    sys.path.insert(0, str(_lib))

_scripts = Path(__file__).resolve().parent.parent.parent
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from invest_path import (  # noqa: E402
    ensure_invest_a_scripts_on_path,
    ensure_shared_lib_on_path,
    load_invest_a_etf_module,
)

ensure_skills_lib_on_path = ensure_shared_lib_on_path

__all__ = [
    "ensure_invest_a_scripts_on_path",
    "ensure_skills_lib_on_path",
    "ensure_shared_lib_on_path",
    "load_invest_a_etf_module",
]
