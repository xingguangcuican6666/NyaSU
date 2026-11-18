"""merge：执行顺序与冲突规则。"""

from __future__ import annotations

from pathlib import Path

import pytest

from conftest import make_module
from ksuhook.errors import GenerateError
from ksuhook.merge import build_plan
from ksuhook.spec import discover


def _plan(tmp_path: Path):
    return build_plan(discover([tmp_path]))


def test_order_then_priority_then_id(tmp_path: Path):
    make_module(tmp_path / "a", "mod_a", "t", "a_entry", order=20, priority=10)
    make_module(tmp_path / "b", "mod_b", "t", "b_entry", order=10, priority=10)
    make_module(tmp_path / "c", "mod_c", "t", "c_entry", order=10, priority=90)
    plan = _plan(tmp_path)[0]
    # order 10 的两个模块中，priority 高的先执行；order 20 最后
    assert [p.module.id for p in plan.chain] == ["mod_c", "mod_b", "mod_a"]


def test_deterministic_across_runs(tmp_path: Path):
    make_module(tmp_path / "a", "mod_a", "t", "a_entry", order=10, priority=50)
    make_module(tmp_path / "b", "mod_b", "t", "b_entry", order=10, priority=50)
    first = [p.module.id for p in _plan(tmp_path)[0].chain]
    second = [p.module.id for p in _plan(tmp_path)[0].chain]
    assert first == second


def test_two_replaces_conflict(tmp_path: Path):
    make_module(tmp_path / "a", "mod_a", "t", "a_entry", mode="replace")
    make_module(tmp_path / "b", "mod_b", "t", "b_entry", mode="replace")
    with pytest.raises(GenerateError, match="只能有一个 replace"):
        _plan(tmp_path)


def test_replace_and_inject_conflict(tmp_path: Path):
    make_module(tmp_path / "a", "mod_a", "t", "a_entry", mode="replace")
    make_module(tmp_path / "b", "mod_b", "t", "b_entry", mode="inject")
    with pytest.raises(GenerateError, match="不能混用"):
        _plan(tmp_path)


def test_independent_targets(tmp_path: Path):
    make_module(tmp_path / "a", "mod_a", "target_x", "a_entry")
    make_module(tmp_path / "b", "mod_b", "target_y", "b_entry")
    plans = _plan(tmp_path)
    assert [p.target for p in plans] == ["target_x", "target_y"]
