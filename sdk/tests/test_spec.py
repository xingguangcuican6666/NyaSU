"""spec：模块目录与 hooks.toml 的校验规则。"""

from __future__ import annotations

from pathlib import Path

import pytest

from conftest import make_module
from ksuhook.errors import SpecError
from ksuhook.spec import discover, parse_module


def test_parses_minimal_module(tmp_path: Path):
    root = make_module(tmp_path / "m1", "m_one", "ksu_handle_setresuid", "m_one_entry")
    module = parse_module(root)
    assert module.id == "m_one"
    assert module.hooks[0].target == "ksu_handle_setresuid"
    assert module.hooks[0].mode == "inject"
    assert module.patches_dir is None


def test_rejects_bad_module_id(tmp_path: Path):
    root = make_module(tmp_path / "m1", "m_one", "ksu_handle_setresuid", "e")
    (root / "module.prop").write_text("id=1bad\nname=x\nversion=1\n", encoding="utf-8")
    with pytest.raises(SpecError, match="不是合法的 C 标识符"):
        parse_module(root)


def test_rejects_unknown_mode(tmp_path: Path):
    root = make_module(tmp_path / "m1", "m_one", "t", "e", mode="wrap")
    with pytest.raises(SpecError, match="mode"):
        parse_module(root)


def test_rejects_same_target_twice(tmp_path: Path):
    root = make_module(tmp_path / "m1", "m_one", "t", "e")
    hooks = root / "hooks.toml"
    hooks.write_text(
        hooks.read_text(encoding="utf-8")
        + '\n[[hook]]\nid = "second"\ntarget = "t"\nentry = "e2"\nmode = "inject"\n',
        encoding="utf-8",
    )
    with pytest.raises(SpecError, match="同时被"):
        parse_module(root)


def test_rejects_missing_src(tmp_path: Path):
    root = make_module(tmp_path / "m1", "m_one", "t", "e")
    for f in (root / "src").iterdir():
        f.unlink()
    with pytest.raises(SpecError, match="src/"):
        parse_module(root)


def test_discover_expands_parent_dir(tmp_path: Path):
    make_module(tmp_path / "a", "mod_a", "t", "a_entry")
    make_module(tmp_path / "b", "mod_b", "t", "b_entry")
    modules = discover([tmp_path])
    assert [m.id for m in modules] == ["mod_a", "mod_b"]


def test_discover_rejects_duplicate_ids(tmp_path: Path):
    make_module(tmp_path / "a", "same", "t", "a_entry")
    make_module(tmp_path / "b", "same", "t", "b_entry")
    with pytest.raises(SpecError, match="重复"):
        discover([tmp_path])


def test_reserves_patches_dir(tmp_path: Path):
    root = make_module(tmp_path / "m1", "m_one", "t", "e")
    (root / "patches" / "android14-6.1").mkdir(parents=True)
    module = parse_module(root)
    assert module.patches_dir is not None


def test_rejects_non_numeric_version_code(tmp_path: Path):
    root = make_module(tmp_path / "m1", "m_one", "t", "e")
    (root / "module.prop").write_text(
        "id=m_one\nname=one\nversion=1.0.0\nversionCode=abc\n", encoding="utf-8"
    )
    with pytest.raises(SpecError, match="versionCode"):
        parse_module(root)


def test_rejects_non_numeric_priority(tmp_path: Path):
    root = make_module(tmp_path / "m1", "m_one", "t", "e")
    (root / "module.prop").write_text(
        "id=m_one\nname=one\nversion=1.0.0\nversionCode=1\npriority=high\n", encoding="utf-8"
    )
    with pytest.raises(SpecError, match="priority"):
        parse_module(root)


def test_rejects_non_numeric_order(tmp_path: Path):
    root = make_module(tmp_path / "m1", "m_one", "t", "e")
    hooks = root / "hooks.toml"
    hooks.write_text(hooks.read_text(encoding="utf-8").replace("order = 100", 'order = "x"'), encoding="utf-8")
    with pytest.raises(SpecError, match="order"):
        parse_module(root)


def test_discover_rejects_missing_path(tmp_path: Path):
    with pytest.raises(SpecError, match="不存在"):
        discover([tmp_path / "nope"])
