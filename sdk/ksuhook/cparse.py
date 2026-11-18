"""在 KernelSU 源码里定位函数定义。

只做一件事：给定一个 .c 文件，找出其中所有的函数定义及其精确位置，
以便生成时把定义名改成 `<name>__orig`。

实现是词法级的：先屏蔽注释、字符串与预处理行（替换为等长空格，保持偏移），
再按 `标识符(` 扫描，用"语句边界到标识符之间不含括号/等号/逗号"来区分
定义与调用。足够覆盖 kernel/ 下的 C 代码，不依赖 clang。
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .errors import InspectError

# 出现在语句前缀里就说明这是调用而不是定义
_CONTROL_KEYWORDS = {
    "if",
    "while",
    "for",
    "switch",
    "return",
    "sizeof",
    "typeof",
    "case",
    "else",
    "do",
    "goto",
}

# 单个标识符就是类型时说明参数没有名字
_TYPE_KEYWORDS = {
    "int",
    "char",
    "short",
    "long",
    "float",
    "double",
    "void",
    "unsigned",
    "signed",
    "const",
    "volatile",
    "struct",
    "union",
    "enum",
    "bool",
    "size_t",
    "ssize_t",
    "u8",
    "u16",
    "u32",
    "u64",
    "s8",
    "s16",
    "s32",
    "s64",
    "uid_t",
    "gid_t",
    "pid_t",
    "kuid_t",
    "kgid_t",
}

# 这些前缀会让函数在编译期内联展开，没有可调用的符号，不能作为 hook 目标
_INLINE_QUALIFIERS = {
    "inline",
    "__inline",
    "__inline__",
    "__always_inline",
    "always_inline",
}

_IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_CALL_START = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(")
_FUNC_PTR_PARAM = re.compile(r"^(?P<ret>.*?)\(\s*\*\s*(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*\)\s*\((?P<args>.*)\)$", re.S)
_ARRAY_PARAM = re.compile(r"^(?P<type>.*?)(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*(?P<dims>\[.*\])\s*$", re.S)


@dataclass(frozen=True)
class Param:
    """一个形参。name 为 None 表示源码里没写参数名。"""

    type: str
    name: str | None
    raw: str

    def decl(self, index: int) -> str:
        """返回可直接写进函数签名的声明，缺名时补一个合法的合成名字。"""
        if self.name:
            return self.raw
        synthetic = f"__ksu_p{index}"
        # 抽象数组形参（`int []`）的名字只能写在方括号前面：
        # `int [] __ksu_p0` 不是合法 C。
        if self.type.endswith("]"):
            base, _, dims = self.type.partition("[")
            base = base.strip()
            if base:
                return f"{base} {synthetic}[{dims}" if dims else f"{base} {synthetic}[]"
        return f"{self.type} {synthetic}".strip()

    def arg(self, index: int) -> str:
        return self.name or f"__ksu_p{index}"


@dataclass(frozen=True)
class FuncDef:
    name: str
    ret: str
    prefix: str
    params: tuple[Param, ...]
    path: Path
    name_start: int
    name_end: int
    body_start: int
    body_end: int

    @property
    def is_static(self) -> bool:
        return "static" in self.prefix.split()

    @property
    def is_inline(self) -> bool:
        return bool(_INLINE_QUALIFIERS.intersection(self.prefix.split()))

    @property
    def is_void(self) -> bool:
        return self.ret.strip() == "void"

    def param_decls(self) -> str:
        return ", ".join(p.decl(i) for i, p in enumerate(self.params))

    def arg_names(self) -> str:
        return ", ".join(p.arg(i) for i, p in enumerate(self.params))

    def type_signature(self) -> str:
        """仅类型，用于生成函数指针 typedef。"""
        if not self.params:
            return "void"
        return ", ".join(p.type.strip() for p in self.params)


def _mask(text: str) -> str:
    """把注释、字符串字面量替换为等长空格，保持所有偏移不变。"""
    out = list(text)
    n = len(text)
    i = 0
    while i < n:
        c = text[i]
        if c == "/" and i + 1 < n and text[i + 1] == "/":
            while i < n and text[i] != "\n":
                out[i] = " "
                i += 1
        elif c == "/" and i + 1 < n and text[i + 1] == "*":
            out[i] = " "
            out[i + 1] = " "
            i += 2
            while i < n and not (text[i] == "*" and i + 1 < n and text[i + 1] == "/"):
                if text[i] != "\n":
                    out[i] = " "
                i += 1
            if i < n:
                out[i] = " "
                i += 1
            if i < n:
                out[i] = " "
                i += 1
        elif c in ('"', "'"):
            quote = c
            out[i] = " "
            i += 1
            while i < n and text[i] != quote:
                if text[i] == "\\" and i + 1 < n:
                    out[i] = " "
                    i += 1
                if i < n and text[i] != "\n":
                    out[i] = " "
                i += 1
            if i < n:
                out[i] = " "
                i += 1
        else:
            i += 1
    return "".join(out)


def _mask_preproc(masked: str) -> str:
    """屏蔽预处理行（含续行），避免把 `#define f(x)` 当成函数定义。"""
    out = list(masked)
    offset = 0
    continued = False
    for line in masked.split("\n"):
        stripped = line.lstrip()
        if continued or stripped.startswith("#"):
            continued = line.rstrip().endswith("\\")
            for j in range(len(line)):
                out[offset + j] = " "
        else:
            continued = False
        offset += len(line) + 1
    return "".join(out)


def _match_paren(masked: str, open_pos: int) -> int:
    """open_pos 指向 '('，返回与之配对的 ')' 位置；找不到返回 -1。"""
    depth = 0
    for i in range(open_pos, len(masked)):
        c = masked[i]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return i
    return -1


def _match_brace(masked: str, open_pos: int) -> int:
    depth = 0
    for i in range(open_pos, len(masked)):
        c = masked[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i
    return -1


def _boundary(masked: str, pos: int) -> int:
    """返回 pos 之前最近的语句边界（; } { 或文件开头）。"""
    i = pos - 1
    while i >= 0:
        if masked[i] in ";}{":
            return i
        i -= 1
    return -1


def _skip_to_body(masked: str, pos: int) -> int | None:
    """从形参右括号之后前进到函数体的 '{'，遇到 ';' 或非法符号则放弃。"""
    n = len(masked)
    while pos < n:
        c = masked[pos]
        if c.isspace():
            pos += 1
            continue
        if c == "{":
            return pos
        if c == ";":
            return None
        if c == "(":
            close = _match_paren(masked, pos)
            if close < 0:
                return None
            pos = close + 1
            continue
        if _IDENT.match(masked, pos):
            ident = _IDENT.match(masked, pos)
            assert ident is not None
            pos = ident.end()
            continue
        return None
    return None


def _parse_param(raw: str) -> Param:
    text = " ".join(raw.split())
    if not text:
        return Param(type="void", name=None, raw="void")

    func_ptr = _FUNC_PTR_PARAM.match(text)
    if func_ptr:
        return Param(
            type=f"{func_ptr.group('ret').strip()} (*)({func_ptr.group('args')})",
            name=func_ptr.group("name"),
            raw=text,
        )

    array = _ARRAY_PARAM.match(text)
    if array and "(" not in array.group("type"):
        # `int []` 会被这条正则匹配成 name="int"：类型关键字不是参数名。
        if array.group("name") not in _TYPE_KEYWORDS:
            return Param(
                type=f"{array.group('type').strip()} {array.group('dims')}".strip(),
                name=array.group("name"),
                raw=text,
            )

    match = re.match(r"^(?P<type>.*?)(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*$", text, re.S)
    if not match:
        return Param(type=text, name=None, raw=text)

    name = match.group("name")
    type_text = match.group("type").strip()
    if not type_text or name in _TYPE_KEYWORDS:
        return Param(type=text, name=None, raw=text)
    return Param(type=type_text, name=name, raw=text)


def _split_params(text: str) -> list[str]:
    parts: list[str] = []
    depth = 0
    current: list[str] = []
    for c in text:
        if c in "([":
            depth += 1
        elif c in ")]":
            depth -= 1
        if c == "," and depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(c)
    if "".join(current).strip():
        parts.append("".join(current))
    return parts


def parse_functions(path: Path, text: str | None = None) -> list[FuncDef]:
    """解析文件中的函数定义列表。"""
    if text is None:
        text = path.read_text(encoding="utf-8", errors="replace")

    masked = _mask_preproc(_mask(text))
    results: list[FuncDef] = []

    for match in _CALL_START.finditer(masked):
        name = match.group(1)
        name_start, name_end = match.start(1), match.end(1)
        if name in _CONTROL_KEYWORDS:
            continue

        boundary = _boundary(masked, name_start)
        # 前缀从屏蔽后的文本取：注释与预处理行已成空白，不会污染返回类型
        prefix = " ".join(masked[boundary + 1 : name_start].split())
        if not prefix:
            continue
        if any(ch in prefix for ch in "()=,.[]"):
            continue
        if _IDENT.findall(prefix)[-1] in _CONTROL_KEYWORDS:
            continue

        open_paren = match.end() - 1
        close_paren = _match_paren(masked, open_paren)
        if close_paren < 0:
            continue
        body_start = _skip_to_body(masked, close_paren + 1)
        if body_start is None:
            continue
        body_end = _match_brace(masked, body_start)
        if body_end < 0:
            continue

        raw_params = text[open_paren + 1 : close_paren]
        param_parts = _split_params(raw_params)
        if len(param_parts) == 1 and param_parts[0].strip() == "void":
            params: tuple[Param, ...] = ()
        else:
            params = tuple(_parse_param(p) for p in param_parts if p.strip())

        ret = prefix
        for storage in ("static", "inline", "__inline", "__inline__", "__always_inline", "__init", "__exit"):
            ret = re.sub(rf"\b{storage}\b", "", ret)
        ret = " ".join(ret.split())

        results.append(
            FuncDef(
                name=name,
                ret=ret,
                prefix=prefix,
                params=params,
                path=path,
                name_start=name_start,
                name_end=name_end,
                body_start=body_start,
                body_end=body_end,
            )
        )

    return results


def find_function(sources: list[Path], name: str) -> FuncDef | None:
    """在给定源码集合中查找指定名字的函数定义（取第一个匹配）。"""
    for path in sources:
        if path.suffix != ".c":
            continue
        for func in parse_functions(path):
            if func.name == name:
                return func
    return None


def list_definitions(sources: list[Path]) -> dict[str, FuncDef]:
    defs: dict[str, FuncDef] = {}
    for path in sources:
        if path.suffix != ".c":
            continue
        for func in parse_functions(path):
            defs.setdefault(func.name, func)
    return defs


def require_function(sources: list[Path], name: str, where: str) -> FuncDef:
    func = find_function(sources, name)
    if func is None:
        raise InspectError(f"未找到函数定义 '{name}'", where)
    return func
