"""pytest 公共夹具：用临时目录伪造一个最小 KernelSU 仓库。"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# conftest 自身不是包：让 `from conftest import ...` 能工作
sys.path.insert(0, str(Path(__file__).resolve().parent))

KSU_C = """\
#include <linux/types.h>

int ksu_handle_setresuid(uid_t old_uid, uid_t new_uid)
{
    if (old_uid == new_uid)
        return 0;
    return 1;
}

bool ksu_is_allow_uid(uid_t uid)
{
    (void)uid;
    return true;
}

static inline bool helper(uid_t uid)
{
    return uid != 0;
}
"""

KBUILD = """\
kernelsu-objs := core/init.o

# Keep a new line here!! Because someone may append config
"""

MODULE_PROP = """\
id={id}
name={name}
version=1.0.0
versionCode=1
priority={priority}
"""


@pytest.fixture()
def fake_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    (repo / "kernel" / "hook").mkdir(parents=True)
    (repo / "kernel" / "hook" / "setuid_hook.c").write_text(KSU_C, encoding="utf-8")
    (repo / "kernel" / "Kbuild").write_text(KBUILD, encoding="utf-8")
    return repo


def make_module(
    root: Path,
    module_id: str,
    target: str,
    entry: str,
    mode: str = "inject",
    order: int = 100,
    priority: int = 50,
    body: str | None = None,
) -> Path:
    (root / "src").mkdir(parents=True)
    (root / "module.prop").write_text(
        MODULE_PROP.format(id=module_id, name=module_id, priority=priority), encoding="utf-8"
    )
    (root / "hooks.toml").write_text(
        "[[hook]]\n"
        f'id = "{module_id}_hook"\n'
        f'target = "{target}"\n'
        f'entry = "{entry}"\n'
        f'mode = "{mode}"\n'
        f"order = {order}\n",
        encoding="utf-8",
    )
    (root / "src" / f"{module_id}.c").write_text(
        body
        or f"""\
#include <linux/types.h>
#include "{module_id}.h"

int {entry}(uid_t old_uid, uid_t new_uid)
{{
    (void)old_uid;
    (void)new_uid;
    return 0;
}}
""",
        encoding="utf-8",
    )
    (root / "src" / f"{module_id}.h").write_text(
        f"""\
#ifndef {module_id.upper()}_H
#define {module_id.upper()}_H
#include <linux/uidgid.h>
int {entry}(uid_t old_uid, uid_t new_uid);
#endif
""",
        encoding="utf-8",
    )
    return root
