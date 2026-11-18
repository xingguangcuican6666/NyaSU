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


def test_depends_defaults_to_empty(tmp_path: Path):
    root = make_module(tmp_path / "m1", "m_one", "t", "e")
    assert parse_module(root).depends == ()


def test_parses_comma_separated_depends(tmp_path: Path):
    root = make_module(tmp_path / "m1", "m_one", "t", "e")
    prop = root / "module.prop"
    prop.write_text(
        prop.read_text(encoding="utf-8") + "depends = mod_b , mod_c,mod_b\n",
        encoding="utf-8",
    )
    assert parse_module(root).depends == ("mod_b", "mod_c")


def test_rejects_bad_depends_identifier(tmp_path: Path):
    root = make_module(tmp_path / "m1", "m_one", "t", "e")
    prop = root / "module.prop"
    prop.write_text(prop.read_text(encoding="utf-8") + "depends=1bad\n", encoding="utf-8")
    with pytest.raises(SpecError, match="depends"):
        parse_module(root)


def test_discover_ignores_missing_depends_by_default(tmp_path: Path):
    root = make_module(tmp_path / "m1", "m_one", "t", "e")
    prop = root / "module.prop"
    prop.write_text(prop.read_text(encoding="utf-8") + "depends=absent\n", encoding="utf-8")
    modules = discover([root])
    assert modules[0].depends == ("absent",)


def test_discover_checks_depends_when_asked(tmp_path: Path):
    root = make_module(tmp_path / "m1", "m_one", "t", "e")
    prop = root / "module.prop"
    prop.write_text(prop.read_text(encoding="utf-8") + "depends=absent\n", encoding="utf-8")
    with pytest.raises(SpecError, match="依赖不存在"):
        discover([root], check_depends=True)


def test_discover_accepts_satisfied_depends(tmp_path: Path):
    make_module(tmp_path / "a", "mod_a", "t", "a_entry")
    root = make_module(tmp_path / "b", "mod_b", "t", "b_entry")
    prop = root / "module.prop"
    prop.write_text(prop.read_text(encoding="utf-8") + "depends=mod_a\n", encoding="utf-8")
    modules = discover([tmp_path], check_depends=True)
    assert [m.id for m in modules] == ["mod_a", "mod_b"]
