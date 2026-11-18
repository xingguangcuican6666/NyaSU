"""cli：命令行入口的错误码与"不要二次生成"的守卫。"""

from __future__ import annotations

from pathlib import Path

from conftest import make_module
from ksuhook.cli import _ksu_sources, main


def test_generate_round_trip(fake_repo: Path, tmp_path: Path):
    packs = tmp_path / "packs"
    make_module(packs / "a", "mod_a", "ksu_handle_setresuid", "a_entry")
    out = tmp_path / "out" / "ksu.patch"
    rc = main(["generate", "--repo", str(fake_repo), "--packs", str(packs), "--out", str(out)])
    assert rc == 0
    assert "sdkgen/ksu_handle_setresuid.o" in out.read_text(encoding="utf-8")


def test_ksu_sources_skips_sdkgen(fake_repo: Path):
    """生成物不能被当成源码：否则二次生成会把包装自己的定义改名。"""
    generated = fake_repo / "kernel" / "sdkgen" / "ksu_handle_setresuid.c"
    generated.parent.mkdir(parents=True)
    generated.write_text("int ksu_handle_setresuid(int a) { return a; }\n", encoding="utf-8")
    sources = _ksu_sources(fake_repo)
    assert generated not in sources
    assert fake_repo / "kernel" / "hook" / "setuid_hook.c" in sources


def test_generate_refuses_patched_tree(fake_repo: Path, tmp_path: Path):
    packs = tmp_path / "packs"
    make_module(packs / "a", "mod_a", "ksu_handle_setresuid", "a_entry")
    generated = fake_repo / "kernel" / "sdkgen" / "ksu_handle_setresuid.c"
    generated.parent.mkdir(parents=True)
    generated.write_text("/* already generated */\n", encoding="utf-8")

    out = tmp_path / "out.patch"
    rc = main(["generate", "--repo", str(fake_repo), "--packs", str(packs), "--out", str(out)])
    assert rc == 2
    assert not out.exists()


def test_validate_reports_missing_target(fake_repo: Path, tmp_path: Path):
    packs = tmp_path / "packs"
    make_module(packs / "a", "mod_a", "no_such_function", "a_entry")
    rc = main(["validate", "--repo", str(fake_repo), "--packs", str(packs)])
    assert rc == 1
