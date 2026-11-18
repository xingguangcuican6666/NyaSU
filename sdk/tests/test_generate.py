"""generate + patch：产物内容与"可 git apply"。"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from conftest import make_module
from ksuhook.cparse import list_definitions
from ksuhook.errors import GenerateError
from ksuhook.generate import generate
from ksuhook.merge import build_plan
from ksuhook.patch import build_patch, validate
from ksuhook.spec import discover


def _generate(repo: Path, packs: Path):
    modules = discover([packs])
    plans = build_plan(modules)
    defs = list_definitions(sorted((repo / "kernel").rglob("*.c")))
    kbuild = repo / "kernel" / "Kbuild"
    return generate(plans, defs, kbuild), kbuild


def test_wrapper_chain_and_rename(fake_repo: Path, tmp_path: Path):
    make_module(tmp_path / "packs" / "a", "mod_a", "ksu_handle_setresuid", "a_entry", order=10)
    make_module(tmp_path / "packs" / "b", "mod_b", "ksu_handle_setresuid", "b_entry", order=20)
    gen, kbuild = _generate(fake_repo, tmp_path / "packs")

    wrapper = next(f for f in gen.files if f.path.name == "ksu_handle_setresuid.c")
    text = wrapper.content
    assert "int ksu_handle_setresuid__orig(uid_t old_uid, uid_t new_uid);" in text
    assert text.index("a_entry(") < text.index("b_entry(")
    assert "return ksu_handle_setresuid__orig(old_uid, new_uid);" in text

    patch = build_patch(gen, fake_repo, kbuild)
    assert "-int ksu_handle_setresuid(" in patch
    assert "+int ksu_handle_setresuid__orig(" in patch
    assert "kernelsu-objs += sdkgen/ksu_handle_setresuid.o" in patch


def test_replace_mode_does_not_call_original(fake_repo: Path, tmp_path: Path):
    make_module(
        tmp_path / "packs" / "r",
        "mod_r",
        "ksu_handle_setresuid",
        "r_entry",
        mode="replace",
    )
    gen, _ = _generate(fake_repo, tmp_path / "packs")
    text = next(f for f in gen.files if f.path.name == "ksu_handle_setresuid.c").content
    assert "return r_entry(old_uid, new_uid);" in text
    assert "int ksu_handle_setresuid__orig(uid_t old_uid, uid_t new_uid);" in text
    body = text.split("int ksu_handle_setresuid(uid_t old_uid, uid_t new_uid)")[1]
    assert "__orig(" not in body


def test_rejects_inline_target(fake_repo: Path, tmp_path: Path):
    make_module(tmp_path / "packs" / "i", "mod_i", "helper", "i_entry")
    with pytest.raises(GenerateError, match="inline"):
        _generate(fake_repo, tmp_path / "packs")


def test_rejects_missing_target(fake_repo: Path, tmp_path: Path):
    make_module(tmp_path / "packs" / "m", "mod_m", "does_not_exist", "m_entry")
    with pytest.raises(GenerateError, match="未在源码中找到定义"):
        _generate(fake_repo, tmp_path / "packs")


def test_validate_clean_output(fake_repo: Path, tmp_path: Path):
    make_module(tmp_path / "packs" / "a", "mod_a", "ksu_handle_setresuid", "a_entry")
    gen, kbuild = _generate(fake_repo, tmp_path / "packs")
    assert validate(gen, fake_repo, kbuild) == []


def test_is_deterministic(fake_repo: Path, tmp_path: Path):
    make_module(tmp_path / "packs" / "a", "mod_a", "ksu_handle_setresuid", "a_entry")
    make_module(tmp_path / "packs" / "b", "mod_b", "ksu_handle_setresuid", "b_entry", order=5)
    first, kbuild = _generate(fake_repo, tmp_path / "packs")
    second, _ = _generate(fake_repo, tmp_path / "packs")
    assert build_patch(first, fake_repo, kbuild) == build_patch(second, fake_repo, kbuild)


@pytest.mark.skipif(shutil.which("git") is None, reason="需要 git 才能验证补丁")
def test_patch_applies_with_git(fake_repo: Path, tmp_path: Path):
    make_module(tmp_path / "packs" / "a", "mod_a", "ksu_handle_setresuid", "a_entry")
    gen, kbuild = _generate(fake_repo, tmp_path / "packs")

    work = tmp_path / "work"
    shutil.copytree(fake_repo, work)
    subprocess.run(["git", "init", "-q"], cwd=work, check=True)
    subprocess.run(["git", "add", "-A"], cwd=work, check=True)
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init"],
        cwd=work,
        check=True,
    )

    patch_file = tmp_path / "out.patch"
    patch_file.write_text(build_patch(gen, fake_repo, kbuild), encoding="utf-8")
    subprocess.run(["git", "apply", "--check", str(patch_file)], cwd=work, check=True)
    subprocess.run(["git", "apply", str(patch_file)], cwd=work, check=True)

    renamed = (work / "kernel" / "hook" / "setuid_hook.c").read_text(encoding="utf-8")
    assert "int ksu_handle_setresuid__orig(" in renamed
    assert "int ksu_handle_setresuid(" not in renamed
    assert (work / "kernel" / "sdkgen" / "ksu_handle_setresuid.c").is_file()
    assert (work / "kernel" / "sdkgen" / "modules" / "mod_a" / "mod_a.c").is_file()
    assert "sdkgen/ksu_handle_setresuid.o" in (work / "kernel" / "Kbuild").read_text(encoding="utf-8")


def test_rejects_static_target(fake_repo: Path, tmp_path: Path):
    """static 函数只有内部链接：改个名放到 kernel/sdkgen 里永远链不上。"""
    source = fake_repo / "kernel" / "hook" / "setuid_hook.c"
    source.write_text(
        source.read_text(encoding="utf-8")
        + "\nstatic int ksu_static_helper(uid_t uid)\n{\n    return uid != 0;\n}\n",
        encoding="utf-8",
    )
    make_module(tmp_path / "packs" / "s", "mod_s", "ksu_static_helper", "s_entry")
    with pytest.raises(GenerateError, match="static"):
        _generate(fake_repo, tmp_path / "packs")


def test_includes_every_module_header(fake_repo: Path, tmp_path: Path):
    """模块有多个头文件时全部包含；入口不在头文件里时仍要给出 extern 原型。"""
    pack = make_module(tmp_path / "packs" / "a", "mod_a", "ksu_handle_setresuid", "a_entry")
    (pack / "src" / "aaa_extra.h").write_text("int a_extra(void);\n", encoding="utf-8")

    gen, _ = _generate(fake_repo, tmp_path / "packs")
    text = next(f for f in gen.files if f.path.name == "ksu_handle_setresuid.c").content
    assert '#include "modules/mod_a/aaa_extra.h"' in text
    assert '#include "modules/mod_a/mod_a.h"' in text
    assert "extern int a_entry(uid_t old_uid, uid_t new_uid);" not in text

    # 头文件里没有声明入口时，包装必须自带原型，否则调用点会被当成隐式声明
    (pack / "src" / "mod_a.h").write_text("/* no declaration here */\n", encoding="utf-8")
    gen, _ = _generate(fake_repo, tmp_path / "packs")
    text = next(f for f in gen.files if f.path.name == "ksu_handle_setresuid.c").content
    assert "extern int a_entry(uid_t old_uid, uid_t new_uid);" in text


def test_kbuild_append_does_not_duplicate(fake_repo: Path, tmp_path: Path):
    """同一个条目已在 Kbuild 里时不再追加，避免重复对象。"""
    make_module(tmp_path / "packs" / "a", "mod_a", "ksu_handle_setresuid", "a_entry")
    kbuild = fake_repo / "kernel" / "Kbuild"
    kbuild.write_text(
        kbuild.read_text(encoding="utf-8").replace(
            "kernelsu-objs := core/init.o",
            "kernelsu-objs := core/init.o\nkernelsu-objs += sdkgen/modules/mod_a/mod_a.o",
        ),
        encoding="utf-8",
    )
    gen, kbuild = _generate(fake_repo, tmp_path / "packs")
    patch = build_patch(gen, fake_repo, kbuild)
    added = [line for line in patch.splitlines() if line.startswith("+kernelsu-objs")]
    assert "kernelsu-objs += sdkgen/modules/mod_a/mod_a.o" not in added


@pytest.mark.skipif(shutil.which("git") is None, reason="需要 git 才能验证补丁")
def test_patch_applies_without_trailing_newline(fake_repo: Path, tmp_path: Path):
    """源文件末尾没有换行时，diff 必须带 `\\ No newline at end of file`。"""
    source = fake_repo / "kernel" / "hook" / "setuid_hook.c"
    source.write_text(source.read_text(encoding="utf-8").rstrip(), encoding="utf-8")
    kbuild = fake_repo / "kernel" / "Kbuild"
    kbuild.write_text(kbuild.read_text(encoding="utf-8").rstrip(), encoding="utf-8")

    make_module(tmp_path / "packs" / "a", "mod_a", "ksu_handle_setresuid", "a_entry")
    gen, kbuild = _generate(fake_repo, tmp_path / "packs")

    work = tmp_path / "work"
    shutil.copytree(fake_repo, work)
    subprocess.run(["git", "init", "-q"], cwd=work, check=True)
    subprocess.run(["git", "add", "-A"], cwd=work, check=True)
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "init"],
        cwd=work,
        check=True,
    )
    patch_file = tmp_path / "out.patch"
    patch_file.write_text(build_patch(gen, fake_repo, kbuild), encoding="utf-8")
    subprocess.run(["git", "apply", "--check", str(patch_file)], cwd=work, check=True)
