"""cparse：在真实 kernel/ 源码与合成用例上都要准确。"""

from __future__ import annotations

import inspect
import tempfile
from pathlib import Path

import pytest

from conftest import KSU_C
from ksuhook.cparse import find_function, parse_functions

REPO_KERNEL = Path(__file__).resolve().parent.parent.parent / "kernel"


def _names(text: str) -> set[str]:
    return {f.name for f in parse_functions(Path("x.c"), text)}


def _write(text: str) -> Path:
    tmp = tempfile.NamedTemporaryFile("w", suffix=".c", delete=False, encoding="utf-8")
    tmp.write(text)
    tmp.close()
    return Path(tmp.name)


def test_finds_plain_definition():
    funcs = parse_functions(Path("x.c"), KSU_C)
    names = {f.name for f in funcs}
    assert {"ksu_handle_setresuid", "ksu_is_allow_uid", "helper"} <= names


def test_returns_and_params():
    func = find_function([_write(KSU_C)], "ksu_handle_setresuid")
    assert func is not None
    assert func.ret == "int"
    assert func.param_decls() == "uid_t old_uid, uid_t new_uid"


def test_skips_comment_and_preprocessor():
    text = """\
#include <linux/types.h>
#define INLINE_ME(x) ((x) + 1)
/* int fake(int a) { return a; } */
// int fake2(int b) { return b; }
int real(int a)
{
    return INLINE_ME(a);
}
"""
    names = _names(text)
    assert names == {"real"}


def test_skips_calls_and_control_flow():
    text = """\
void a(void)
{
    if (1) { }
    while (0) { }
    for (;;) { break; }
    b();
    if (c()) { }
}
"""
    assert _names(text) == {"a"}


def test_function_pointer_param():
    text = "void ksu_prune(bool (*is_valid)(uid_t, char *, void *), void *data)\n{\n}\n"
    func = find_function([_write(text)], "ksu_prune")
    assert func is not None
    assert func.param_decls() == "bool (*is_valid)(uid_t, char *, void *), void *data"


def test_inline_and_static_flags():
    text = "static inline bool helper(uid_t uid)\n{\n    return uid != 0;\n}\n"
    func = find_function([_write(text)], "helper")
    assert func is not None
    assert func.is_inline and func.is_static


@pytest.mark.skipif(not REPO_KERNEL.is_dir(), reason="需要 KernelSU kernel/ 源码")
def test_real_repo_targets():
    sources = sorted(REPO_KERNEL.rglob("*.c"))
    func = find_function(sources, "ksu_handle_setresuid")
    assert func is not None
    assert func.path.name == "setuid_hook.c"
    assert func.param_decls() == "uid_t old_uid, uid_t new_uid"

    # 解析器不能把控制流或预处理当成定义
    assert inspect.cleandoc(func.prefix) == "int"


@pytest.mark.skipif(not REPO_KERNEL.is_dir(), reason="需要 KernelSU kernel/ 源码")
def test_real_repo_no_false_positives():
    sources = sorted(REPO_KERNEL.rglob("*.c"))
    for path in sources:
        for func in parse_functions(path):
            assert func.name not in {"if", "for", "while", "switch", "return"}
            assert "#" not in func.ret
            assert "//" not in func.ret


def test_always_inline_and_inline_qualifiers():
    """`__always_inline` / `__inline__` 同样是内联，不能当成可包装的普通函数。"""
    text = """\
static __always_inline bool my_do_syscall_x64(int nr)
{
    return nr != 0;
}

static __inline__ int other(int b)
{
    return b;
}
"""
    funcs = {f.name: f for f in parse_functions(Path("x.c"), text)}
    assert funcs["my_do_syscall_x64"].is_inline and funcs["my_do_syscall_x64"].is_static
    assert funcs["other"].is_inline
    # 返回类型里不能残留 `__inline__` 之类的存储类关键字
    assert funcs["other"].ret == "int"


def test_abstract_array_param_is_not_a_name():
    """`int []` 里的 `int` 是类型，不是参数名；补出的名字要能编译。"""
    text = "int unnamed_arr(int [], int n)\n{\n    return n;\n}\n"
    func = find_function([_write(text)], "unnamed_arr")
    assert func is not None
    assert func.param_decls() == "int __ksu_p0[], int n"
    assert func.arg_names() == "__ksu_p0, n"
