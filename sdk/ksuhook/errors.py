"""SDK 共用的错误类型。

每个错误都带 `where`（文件、行或字段），让 CLI 能直接指出该改哪一处，
而不需要阅读生成器源码。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SdkError(Exception):
    message: str
    where: str = ""

    def __str__(self) -> str:
        return f"{self.where}: {self.message}" if self.where else self.message


class SpecError(SdkError):
    """hookpack.toml 格式错误或违反规则。"""


class GenerateError(SdkError):
    """已通过校验的包无法生成 C 代码。"""


class InspectError(SdkError):
    """无法在 KernelSU 源码中定位 hook 目标。"""
