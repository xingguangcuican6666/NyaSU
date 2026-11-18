"""命令行入口：validate / plan / generate / dev。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .cparse import list_definitions
from .devkit import build_and_run
from .errors import SdkError
from .generate import generate
from .merge import build_plan
from .patch import build_patch, validate as patch_validate
from .spec import discover


def _ksu_sources(repo: Path) -> list[Path]:
    kernel = repo / "kernel"
    if not kernel.is_dir():
        raise SdkError("找不到 kernel/ 目录", str(repo))
    return sorted(kernel.rglob("*.c"))


def _plan(repo: Path, packs: list[Path]):
    modules = discover(packs)
    plans = build_plan(modules)
    defs = list_definitions(_ksu_sources(repo))
    return modules, plans, defs


def cmd_validate(args: argparse.Namespace) -> int:
    modules, plans, defs = _plan(Path(args.repo), [Path(p) for p in args.packs])
    problems: list[str] = []
    for plan in plans:
        if plan.target not in defs:
            problems.append(f"{plan.target}: kernel/ 中找不到函数定义")
    for module in modules:
        if module.patches_dir is not None:
            print(f"note: {module.id} 提供 patches/，当前版本不处理（预留）")
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 1
    print(f"ok: {len(modules)} 个模块，{len(plans)} 个被 hook 的函数")
    return 0


def cmd_plan(args: argparse.Namespace) -> int:
    _, plans, _ = _plan(Path(args.repo), [Path(p) for p in args.packs])
    for plan in plans:
        print(f"kernel/sdkgen/{plan.target}.c  [{plan.mode}]")
        for dep in plan.module_ids:
            print(f"  <- {dep}")
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    repo = Path(args.repo)
    _, plans, defs = _plan(repo, [Path(p) for p in args.packs])
    kbuild = repo / "kernel" / "Kbuild"
    generation = generate(plans, defs, kbuild)
    problems = patch_validate(generation, repo, kbuild)
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 1
    text = build_patch(generation, repo, kbuild)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    if not text.strip():
        print(f"wrote {out} (0 lines)：没有任何被 hook 的函数，补丁为空")
    else:
        print(f"wrote {out} ({len(text.splitlines())} lines)")
    return 0


def cmd_dev(args: argparse.Namespace) -> int:
    modules = discover([Path(p) for p in args.packs])
    failed = 0
    for module in modules:
        result = build_and_run(module)
        status = "ok" if result.ok else "FAIL"
        print(f"[{status}] {module.id}: {result.output.strip() or 'no output'}")
        failed += 0 if result.ok else 1
    return 1 if failed else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ksuhook", description="KernelSU 按函数生成 hook 的工具")
    parser.add_argument("--version", action="version", version=f"ksuhook {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    common_packs = dict(nargs="+", help="模块目录或其父目录")

    p = sub.add_parser("validate", help="校验模块与目标函数")
    p.add_argument("--repo", required=True, help="KernelSU 仓库根目录")
    p.add_argument("--packs", **common_packs)
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("plan", help="打印合并后的执行顺序")
    p.add_argument("--repo", required=True)
    p.add_argument("--packs", **common_packs)
    p.set_defaults(func=cmd_plan)

    p = sub.add_parser("generate", help="生成可 git apply 的补丁")
    p.add_argument("--repo", required=True)
    p.add_argument("--packs", **common_packs)
    p.add_argument("--out", required=True, help="补丁输出路径")
    p.set_defaults(func=cmd_generate)

    p = sub.add_parser("dev", help="编译并运行模块自带单测")
    p.add_argument("--packs", **common_packs)
    p.set_defaults(func=cmd_dev)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except SdkError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
