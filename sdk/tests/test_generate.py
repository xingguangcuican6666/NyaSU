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
