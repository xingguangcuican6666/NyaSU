"""ksuhook — 为 KernelSU GKI 构建按函数生成 hook 的开发工具。"""

from .errors import GenerateError, InspectError, SdkError, SpecError

__all__ = ["SdkError", "SpecError", "GenerateError", "InspectError"]
__version__ = "1.0.0"
