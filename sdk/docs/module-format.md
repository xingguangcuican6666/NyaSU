# 模块格式规范 v1

模块是 **纯构建期源码包**：只描述"要改 KernelSU 的哪个函数、用哪段 C 代码改"。
它不产出可刷入的 ZIP，也不含 `customize.sh` / `service.sh` / `webroot`。

## 目录布局

```bash
<module>/
├── module.prop      # 元数据（必填）
├── hooks.toml       # hook 声明（必填，至少一条）
├── src/             # C 载荷（必填，至少一个 .c）
│   ├── <name>.c
│   └── <name>.h     # 可选；有头文件时会 include 进生成的包装
├── tests/           # 模块单测（可选，`ksuhook dev` 会编译运行）
│   └── *.c          # 第一个文件需提供 main()
├── patches/         # 可选：按内核版本分化的源码补丁（由编排器消费）
│   └── <android>-<kernel>/   # 例如 android14-6.1
└── docs/            # 可选说明
```

`patches/` 供构建编排器使用：`ksuhook.orchestrator apply` 会读取
`patches/<android>-<kernel>/` 下的 `*.patch` / `*.diff`，自 `depends` 连通的每个分组
各自在独立 worktree 中应用。SDK 的 `validate` / `generate` 本身不读取它。

## `module.prop`

`key=value` 每行一条，`#` 开头为注释。与 KernelSU 模块格式一致，去掉了运行时字段。

| 字段 | 必填 | 说明 |
|:--|:--:|:--|
| `id` | ✅ | 模块标识，须匹配 `^[A-Za-z_][A-Za-z0-9_]*$`（会出现在生成路径里） |
| `name` | ✅ | 展示名 |
| `version` | ✅ | 字符串版本 |
| `versionCode` | | 整数，默认 `1` |
| `priority` | | 整数，默认 `50`；**越大越先执行** |
| `description` | | 说明 |
| `author` | | 作者 |
| `depends` | | 逗号分隔的模块 id 列表；由构建期编排器 `ksuhook.orchestrator` 据此分组，SDK 的 `validate`/`generate` 只校验格式 |

## `hooks.toml`

```toml
[[hook]]
id     = "audit_setresuid"          # 模块内唯一
target = "ksu_handle_setresuid"     # KernelSU 中的函数名
entry  = "uid_audit_on_setresuid"   # 本模块 C 中的入口函数
mode   = "inject"                   # inject | replace
order  = 10                         # 越小越先执行，默认 100
```

字段规则：

- `target` 必须是 `kernel/` 下**确有其定义**的函数（`ksuhook validate` 会检查）。
- 同一模块内 `target` 不能重复；不同模块可以指向同一 `target`，由 SDK 合并。
- `mode = "inject"`：签名与 `target` 相同，返回 `int`。返回 `0` 表示"没有意见"，
  继续下一个注入并最终执行原函数；返回非 `0` 则短路，原函数不再执行。
- `mode = "replace"`：签名与返回类型与 `target` 相同，完全接管。每个 `target`
  最多一个 `replace`，且不能与 `inject` 混用，否则生成阶段报冲突。
- `order` 相同且 `priority` 相同时，按模块 `id`、再按 hook `id` 排序。排序完全确定，
  同一输入永远产出同一份补丁。

## `src/` 的编写约束

- 只能用内核头文件（`<linux/...>`）与 KernelSU 的 `kernel/include`；
  主机侧单测由 `devkit/shim` 提供替身。
- 不要 `#include "path/to/ksu/header.h"`，用相对的模块头（如 `"uid_audit.h"`）。
  生成的包装只按 `modules/<id>/<header>` 引用模块自己的头文件。
- 载荷会被复制进 `kernel/sdkgen/modules/<id>/`，因此文件名之间不要冲突。

## `tests/`

第一个 `*.c` 必须提供 `main()`，返回 0 表示通过。可用 `devkit/shim` 中的
`ksuhook_test_log()` 捕获 `pr_info` 输出做断言。若要覆盖 `current`，
自行定义强符号 `struct task_struct *ksuhook_current`（弱符号桩已提供）。

## 生成物

编排器在合并后的 KernelSU 树上用 SDK 生成一次补丁：

```bash
python3 -m ksuhook generate --repo /path/to/KernelSU --packs modules/ --out ksu-sdkgen.patch
```

补丁包含：

1. `kernel/<file>`：把目标函数定义名改为 `<name>__orig`（只改名字，逻辑不动）。
2. `kernel/sdkgen/<name>.c`：同名包装，按合并顺序分发。
3. `kernel/sdkgen/modules/<id>/*`：模块载荷副本。
4. `kernel/Kbuild`：末尾追加 `kernelsu-objs += …`。

由 GKI 构建流程执行 `git apply` 后编译。
