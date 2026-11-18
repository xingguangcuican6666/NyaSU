"""产出可 `git apply` 的 unified diff。

特意不依赖 `git`：补丁在 CI 与本地都要能生成，生成结果必须稳定可比对。
统一使用 a/ b/ 前缀，因此既能在仓库根执行 `git apply -p1`，也能在
`kernel/` 里用 `-p2` 应用。
"""

from __future__ import annotations

import difflib
from pathlib import Path

from .generate import Generation, apply_edits


def _rel(path: Path, repo: Path) -> str:
    try:
        return path.resolve().relative_to(repo.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _header(old_name: str, new_name: str) -> list[str]:
    return [f"diff --git a/{old_name} b/{new_name}", f"--- a/{old_name}", f"+++ b/{new_name}"]


def _new_file_header(name: str) -> list[str]:
    return [
        f"diff --git a/{name} b/{name}",
        "new file mode 100644",
        "--- /dev/null",
        f"+++ b/{name}",
    ]


def _join(lines: list[str]) -> str:
    """拼 unified diff，给缺尾换行的最后一行补上 git 的标记。

    `difflib` 不会输出 `\\ No newline at end of file`：源文件最后一行没有换行时，
    diff 里的那一行会被当成"有换行"，`git apply` 直接报 patch does not apply。
    """
    out: list[str] = []
    for line in lines:
        if line.endswith("\n"):
            out.append(line)
            continue
        out.append(line + "\n")
        out.append("\\ No newline at end of file\n")
    return "".join(out)


def build_patch(generation: Generation, repo: Path, kbuild: Path) -> str:
    chunks: list[str] = []

    diffs = apply_edits(generation.edits, _read)

    if generation.kbuild_append:
        diffs[kbuild] = _append_block(_read(kbuild), generation.kbuild_append)

    for path, new_text in sorted(diffs.items()):
        rel = _rel(path, repo)
        old_text = _read(path)
        if old_text == new_text:
            continue
        lines = list(
            difflib.unified_diff(
                old_text.splitlines(keepends=True),
                new_text.splitlines(keepends=True),
                fromfile=f"a/{rel}",
                tofile=f"b/{rel}",
                n=3,
            )
        )
        if not lines:
            continue
        body = _join(lines[2:])
        chunks.append("\n".join(_header(rel, rel)) + "\n" + body)

    for gen_file in sorted(generation.files, key=lambda f: f.path.as_posix()):
        rel = gen_file.path.as_posix()
        if (repo / rel).exists():
            continue
        lines = gen_file.content.splitlines()
        if lines and lines[-1] == "":
            lines = lines[:-1]
        body = "".join(f"+{line}\n" for line in lines)
        chunks.append(
            "\n".join(_new_file_header(rel)) + f"\n@@ -0,0 +1,{len(lines)} @@\n" + body
        )

    return "".join(chunk + "\n" for chunk in chunks)


def _append_block(original: str, block: tuple[str, ...]) -> str:
    """追加构建条目；已经在文件里的条目不重复追加，保证重复生成不会写出重复对象。"""
    text = original if original.endswith("\n") else original + "\n"
    present = {line.strip() for line in original.splitlines()}
    missing = tuple(line for line in block if line.strip() not in present)
    if not missing:
        return text
    return text + "\n# ksuhook: 按模块生成的 hook（追加，不修改既有条目）\n" + "".join(
        line + "\n" for line in missing
    )


def validate(generation: Generation, repo: Path, kbuild: Path) -> list[str]:
    """生成结果的自检，返回问题列表；空列表表示可以应用。"""
    problems: list[str] = []
    for edit in generation.edits:
        if not edit.path.is_file():
            problems.append(f"编辑目标不存在: {_rel(edit.path, repo)}")
    if generation.kbuild_append and not kbuild.is_file():
        problems.append(f"Kbuild 不存在: {_rel(kbuild, repo)}")
    produced = {f.path.as_posix() for f in generation.files}
    if len(produced) != len(generation.files):
        problems.append("有生成文件路径重复")
    return problems
