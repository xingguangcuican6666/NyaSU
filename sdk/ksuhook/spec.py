"""模块清单解析：`hooks.toml`。

模块是**纯构建期源码包**，不产出任何可刷入的 ZIP：

    <module>/
      module.prop        # id / 版本 / 优先级（与 KernelSU 模块同格式的超集）
      hooks.toml         # hook 声明
      src/*.c            # C 载荷
      tests/             # 模块单测（devkit 使用）
      patches/           # 预留：按内核版本分化的源码补丁（当前不使用）

`patches/<kernel-line>/` 目录结构在这里不做解析，只校验其存在性，
为后续"针对真内核源码的定制"留出位置。
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .errors import SpecError

if sys.version_info >= (3, 11):
    import tomllib as _tomllib
else:  # pragma: no cover - 仅在 3.10 触发
    _tomllib = None

MODES = ("inject", "replace")
VALID_IDENT = __import__("re").compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _load_toml(text: str, origin: str) -> dict[str, Any]:
    if _tomllib is None:
        raise SpecError("需要 Python 3.11+ 才能解析 hooks.toml", origin)
    try:
        return _tomllib.loads(text)
    except Exception as exc:
        raise SpecError(f"TOML 解析失败: {exc}", origin) from exc


def _req(table: dict[str, Any], key: str, where: str) -> Any:
    if key not in table:
        raise SpecError(f"缺少必填字段 '{key}'", where)
    return table[key]


def _ident(value: str, where: str, what: str = "标识符") -> str:
    if not VALID_IDENT.match(value):
        raise SpecError(f"{what} '{value}' 不是合法的 C 标识符", where)
    return value


@dataclass(frozen=True)
class Hook:
    module_id: str
    id: str
    target: str  # 要包装的 KernelSU 函数名
    entry: str  # 模块提供的入口函数名
    mode: str
    order: int
    source: Path  # 模块内 C 文件，None 时取 src/*.c 全部

    @property
    def key(self) -> str:
        return f"{self.module_id}/{self.id}"


@dataclass(frozen=True)
class Module:
    root: Path
    id: str
    name: str
    version: str
    version_code: int
    priority: int
    description: str
    author: str
    hooks: tuple[Hook, ...]
    sources: tuple[Path, ...]
    patches_dir: Path | None
    tests_dir: Path | None
    raw: dict[str, Any] = field(default=None, repr=False)  # type: ignore[assignment]


def _read_prop(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise SpecError("缺少 module.prop", str(path))
    props: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        props[key.strip()] = value.strip()
    return props


def parse_module(root: Path) -> Module:
    """解析一个模块目录，返回校验后的描述。"""
    root = root.resolve()
    if not root.is_dir():
        raise SpecError("模块目录不存在", str(root))

    props = _read_prop(root / "module.prop")
    where_prop = str(root / "module.prop")
    module_id = _ident(str(_req(props, "id", where_prop)), where_prop, "模块 id")

    hooks_file = root / "hooks.toml"
    if not hooks_file.is_file():
        raise SpecError("缺少 hooks.toml", str(hooks_file))
    raw = _load_toml(hooks_file.read_text(encoding="utf-8"), str(hooks_file))

    hooks: list[Hook] = []
    for item in raw.get("hook", []):
        if not isinstance(item, dict):
            raise SpecError("每个 [[hook]] 必须是表", str(hooks_file))
        hook_id = _ident(str(_req(item, "id", "[[hook]]")), "[[hook]]", "hook id")
        target = _ident(str(_req(item, "target", f"[[hook]] {hook_id}")), f"hook {hook_id}", "target")
        entry = _ident(str(_req(item, "entry", f"[[hook]] {hook_id}")), f"hook {hook_id}", "entry")
        mode = str(item.get("mode", "inject"))
        if mode not in MODES:
            raise SpecError(f"mode 必须是 {MODES} 之一", f"hook {hook_id}")
        order = int(item.get("order", 100))
        source = None
        if "source" in item:
            source = (root / str(item["source"])).resolve()
            try:
                source.relative_to(root)
            except ValueError as exc:
                raise SpecError(
                    f"source '{item['source']}' 必须位于模块目录内", f"hook {hook_id}"
                ) from exc
            if not source.is_file():
                raise SpecError(f"source '{item['source']}' 不存在", f"hook {hook_id}")
        hooks.append(
            Hook(
                module_id=module_id,
                id=hook_id,
                target=target,
                entry=entry,
                mode=mode,
                order=order,
                source=source if source is not None else Path(),
            )
        )

    if not hooks:
        raise SpecError("至少需要一个 [[hook]]", str(hooks_file))

    seen: dict[str, str] = {}
    targets: dict[str, str] = {}
    for hook in hooks:
        if hook.id in seen:
            raise SpecError(f"hook id '{hook.id}' 重复", str(hooks_file))
        seen[hook.id] = hook.target
        if hook.target in targets:
            raise SpecError(
                f"target '{hook.target}' 同时被 '{targets[hook.target]}' 与 '{hook.id}' hook；"
                "请合并成一个 hook",
                str(hooks_file),
            )
        targets[hook.target] = hook.id

    sources = tuple(sorted((root / "src").glob("*.c"))) if (root / "src").is_dir() else ()
    if not sources:
        raise SpecError("src/ 下没有 C 源文件", str(root))

    patches_dir = root / "patches" if (root / "patches").is_dir() else None
    tests_dir = root / "tests" if (root / "tests").is_dir() else None

    return Module(
        root=root,
        id=module_id,
        name=str(_req(props, "name", where_prop)),
        version=str(_req(props, "version", where_prop)),
        version_code=int(props.get("versionCode", "1")),
        priority=int(props.get("priority", "50")),
        description=str(props.get("description", "")),
        author=str(props.get("author", "")),
        hooks=tuple(hooks),
        sources=sources,
        patches_dir=patches_dir,
        tests_dir=tests_dir,
        raw=raw,
    )


def discover(packs: list[Path]) -> list[Module]:
    """接受模块目录或其父目录，展开成模块列表。"""
    modules: list[Module] = []
    for pack in packs:
        pack = pack.resolve()
        if (pack / "module.prop").is_file():
            modules.append(parse_module(pack))
            continue
        for child in sorted(pack.iterdir()):
            if child.is_dir() and (child / "module.prop").is_file():
                modules.append(parse_module(child))
    if not modules:
        raise SpecError("没有找到任何模块", ", ".join(str(p) for p in packs))
    ids = [m.id for m in modules]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise SpecError(f"模块 id 重复: {sorted(dupes)}")
    return modules
