"""合并多个模块对同一 KernelSU 函数的改动。

规则（定稿）：

* 每个被 hook 的函数生成一个包装 `<target>(...)`，原定义改名为 `<target>__orig`。
* `inject` 链：按 (order, 模块 priority, 模块 id, hook id) 排序后依次调用，
  原函数最后执行。注入点返回值非 0 即短路：包装直接返回该值，原函数不再执行。
* `replace`：每个函数最多一个，接管全部逻辑；多个直接报冲突。
* `inject` 与 `replace` 混用：同一函数上不允许，报冲突。

排序刻意完全确定，使同一输入永远产出同一份补丁。
"""

from __future__ import annotations

from dataclasses import dataclass

from .errors import GenerateError
from .spec import Hook, Module


@dataclass(frozen=True)
class Plan:
    module: Module
    hook: Hook


@dataclass(frozen=True)
class TargetPlan:
    """一个被 hook 的 KernelSU 函数的合并结果。"""

    target: str
    mode: str
    replace: Plan | None
    chain: tuple[Plan, ...]

    @property
    def module_ids(self) -> tuple[str, ...]:
        plans = ([self.replace] if self.replace else []) + list(self.chain)
        return tuple(dict.fromkeys(p.module.id for p in plans if p is not None))


def _sort_key(plan: Plan) -> tuple[int, int, str, str]:
    return (plan.hook.order, -plan.module.priority, plan.module.id, plan.hook.id)


def build_plan(modules: list[Module]) -> tuple[TargetPlan, ...]:
    by_target: dict[str, list[Plan]] = {}
    for module in modules:
        for hook in module.hooks:
            by_target.setdefault(hook.target, []).append(Plan(module=module, hook=hook))

    plans: list[TargetPlan] = []
    for target in sorted(by_target):
        entries = sorted(by_target[target], key=_sort_key)
        replaces = [e for e in entries if e.hook.mode == "replace"]
        injects = [e for e in entries if e.hook.mode == "inject"]

        if len(replaces) > 1:
            who = ", ".join(e.hook.key for e in replaces)
            raise GenerateError(f"同一函数只能有一个 replace，冲突方: {who}", target)
        if replaces and injects:
            who = ", ".join(e.hook.key for e in replaces + injects)
            raise GenerateError("同一函数上不能混用 replace 与 inject", f"{target} ({who})")

        if replaces:
            plans.append(TargetPlan(target=target, mode="replace", replace=replaces[0], chain=()))
        else:
            if not injects:
                continue
            plans.append(
                TargetPlan(target=target, mode="inject", replace=None, chain=tuple(injects))
            )
    return tuple(plans)
