"""Package-local path bootstrap（由 build_skillhub_packages.py 生成）。

主仓库的 skills/lib/invest_path.py 负责跨 skill 路径引导（resolve 到
invest-a-stock / invest-a-etf / invest-a-gap-scan 各自的 scripts/lib）；
包内所有模块单份落在本 lib 包，sys.path[0] 已覆盖，目录函数直接指向包内
scripts/lib。load_*_module 用包导入（import_module("lib.X")），与包内其它
引用共享同一模块实例（主仓库按文件路径加载会产生双实例，包内无此问题）。
"""
from __future__ import annotations

import importlib as _il
import sys
from pathlib import Path

__all__ = [
    "invest_a_scripts_dir",
    "invest_a_etf_lib_dir",
    "ensure_invest_a_scripts_on_path",
    "ensure_shared_lib_on_path",
    "load_gap_scan_module",
    "load_invest_a_etf_module",
]


def invest_a_scripts_dir() -> Path:
    """包内 scripts 目录（sys.path[0]，lib 包所在父目录）。"""
    return Path(__file__).resolve().parent.parent


def invest_a_etf_lib_dir() -> Path:
    """包内 lib 目录（etf_data 等模块所在）。"""
    return Path(__file__).resolve().parent


def gap_scan_lib_dir() -> Path:
    """包内 lib 目录（gap-scan canonical 模块合并后所在）。"""
    return Path(__file__).resolve().parent


def ensure_invest_a_scripts_on_path() -> Path:
    """包内 scripts 已在 sys.path[0]（脚本运行时），幂等补插。"""
    scripts = invest_a_scripts_dir()
    s = str(scripts)
    if s not in sys.path:
        sys.path.insert(0, s)
    return scripts


def ensure_shared_lib_on_path() -> Path:
    """包内 lib 目录（相对导入消费方无需路径引导），幂等补插。"""
    d = Path(__file__).resolve().parent
    s = str(d)
    if s not in sys.path:
        sys.path.insert(0, s)
    return d


_GAP_SCAN_KLINE_SOURCE_NAME = "gap_scan_kline_source"


def load_gap_scan_module(module_file: str = "kline_source"):
    """包内加载 gap-scan canonical 模块（import_module("lib.X")，共享同一实例）。"""
    mod_name = f"{_GAP_SCAN_KLINE_SOURCE_NAME}_{module_file}"
    mod = sys.modules.get(mod_name)
    if mod is not None:
        return mod
    mod = _il.import_module(f"lib.{module_file}")
    sys.modules[mod_name] = mod
    return mod


_INVEST_A_ETF_MODULE_NAME = "invest_a_etf_etf_data"


def load_invest_a_etf_module():
    """包内加载 etf_data（import_module("lib.etf_data")，共享同一实例）。"""
    mod = sys.modules.get(_INVEST_A_ETF_MODULE_NAME)
    if mod is not None:
        return mod
    mod = _il.import_module("lib.etf_data")
    sys.modules[_INVEST_A_ETF_MODULE_NAME] = mod
    return mod
