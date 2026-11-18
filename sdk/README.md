# ksuhook SDK

面向 **GKI** 的 KernelSU 函数级 hook 开发工具。模块声明"要改 KernelSU 的哪个函数"，
SDK 收集、合并多个模块的声明，产出 `.patch`，由构建流程 `git apply` 后编译进内核镜像。

不涉及 LKM / `.ko`；作用域只限 KernelSU 自己加入 `kernel/` 的源码，不分析上游 mainline。

## 它解决什么

| 问题 | 做法 |
|:--|:--|
| 模块想改 KSU 行为 | 在 `hooks.toml` 里声明 `target` + `entry` |
| 多个模块改同一函数 | `inject` 按 `order`→`priority`→`id` 排成链；`replace` 每函数最多一个 |
| 如何"覆写"又不丢原逻辑 | 原定义改名 `<name>__orig`，生成的同名包装接管调用 |
| 不想每次编整颗内核 | `ksuhook dev` 在主机上编译运行模块自带单测 |

## 快速开始

```bash
cd sdk
python3 -m ksuhook validate --repo .. --packs examples
python3 -m ksuhook plan     --repo .. --packs examples
python3 -m ksuhook generate --repo .. --packs examples --out dist/ksu-sdkgen.patch
python3 -m ksuhook dev      --packs examples
python3 -m pytest -q
```

`generate` 的产物在 GKI 树根执行 `git apply -p1 dist/ksu-sdkgen.patch` 即可。

## 产物长什么样

原函数只改名，逻辑一行不动：

```c
-int ksu_handle_setresuid(uid_t old_uid, uid_t new_uid)
+int ksu_handle_setresuid__orig(uid_t old_uid, uid_t new_uid)
```

新增 `kernel/sdkgen/ksu_handle_setresuid.c`：

```c
#include "modules/uid_audit/uid_audit.h"

int ksu_handle_setresuid__orig(uid_t old_uid, uid_t new_uid);

int ksu_handle_setresuid(uid_t old_uid, uid_t new_uid)
{
    int __ret;

    __ret = uid_audit_on_setresuid(old_uid, new_uid);
    if (__ret)
        return __ret;

    return ksu_handle_setresuid__orig(old_uid, new_uid);
}
```

并在 `kernel/Kbuild` 末尾追加：

```
# ksuhook: 按模块生成的 hook（追加，不修改既有条目）
kernelsu-objs += sdkgen/ksu_handle_setresuid.o
kernelsu-objs += sdkgen/modules/uid_audit/uid_audit.o
```

## 文档

- [模块格式 v1](docs/module-format.md) —— 目录布局、`module.prop`、`hooks.toml`
- [写一个模块](docs/authoring.md) —— 从零写注入包并本地验证
- [示例：uid_audit](examples/uid_audit) —— 可运行的最小注入包

## 设计边界

- **只做加法**：生成的代码只新增符号；对既有源码的唯一改写是函数定义改名。
- **不猜内核**：目标函数必须在 `kernel/` 里能找到定义，找不到直接报错。
- **确定性**：同一输入永远产出逐字节相同的补丁，便于 diff 与缓存。
- **不代劳打包**：SDK 不产出 ZIP，也不碰运行时脚本。分发包形态由构建侧决定。

## 环境

- Python 3.11+（解析 TOML 依赖 `tomllib`；3.10 会给出明确报错）。
- `pytest` 用于 SDK 自身测试。
- 主机 `cc`（gcc/clang）用于模块单测；缺失时自动跳过。
