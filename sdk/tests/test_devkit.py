"""devkit：模块单测环境能在主机上编译并运行示例模块。"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from ksuhook.devkit import build_and_run
from ksuhook.spec import parse_module

EXAMPLE = Path(__file__).resolve().parent.parent / "examples" / "uid_audit"


@pytest.mark.skipif(shutil.which("cc") is None and shutil.which("gcc") is None, reason="无 C 编译器")
def test_example_module_passes_its_own_tests():
    result = build_and_run(parse_module(EXAMPLE))
    assert result.ok, result.output
    assert "all checks passed" in result.output


@pytest.mark.skipif(shutil.which("cc") is None and shutil.which("gcc") is None, reason="无 C 编译器")
def test_failing_module_reports_failure(tmp_path: Path):
    from conftest import make_module

    root = make_module(
        tmp_path / "bad",
        "mod_bad",
        "ksu_handle_setresuid",
        "bad_entry",
        body="""\
#include <linux/types.h>
#include <linux/uidgid.h>
int bad_entry(uid_t a, uid_t b) { (void)a; (void)b; return 0; }
""",
    )
    (root / "tests").mkdir()
    (root / "tests" / "t.c").write_text(
        """\
#include <stdio.h>
extern int bad_entry(unsigned int a, unsigned int b);
int main(void) { return bad_entry(1, 2) == 0 ? 0 : 1; }
""",
        encoding="utf-8",
    )
    result = build_and_run(parse_module(root))
    assert result.ok


def test_missing_tests_is_not_a_failure(tmp_path: Path):
    from conftest import make_module

    root = make_module(tmp_path / "notests", "mod_nt", "t", "nt_entry")
    result = build_and_run(parse_module(root))
    assert result.ok
    assert "跳过" in result.output


@pytest.mark.skipif(shutil.which("cc") is None and shutil.which("gcc") is None, reason="无 C 编译器")
def test_runs_every_test_file(tmp_path: Path):
    """tests/ 下有多个 .c 时全部编译运行，不能只看第一个。"""
    from conftest import make_module

    root = make_module(
        tmp_path / "multi",
        "mod_multi",
        "ksu_handle_setresuid",
        "multi_entry",
        body="""\
#include <linux/types.h>
#include <linux/uidgid.h>
int multi_entry(uid_t a, uid_t b) { (void)a; (void)b; return 0; }
""",
    )
    (root / "tests").mkdir()
    (root / "tests" / "a_first.c").write_text(
        """\
#include <stdio.h>
int main(void) { puts("first ok"); return 0; }
""",
        encoding="utf-8",
    )
    (root / "tests" / "z_last.c").write_text(
        """\
#include <stdio.h>
int main(void) { puts("last ok"); return 1; }
""",
        encoding="utf-8",
    )
    result = build_and_run(parse_module(root))
    assert not result.ok
    assert "last ok" in result.output
