# KernelSU 智能体指南

> **已归档 / 仅作参考** —— 本文档仅保留作参考，不再作为生效的智能体指令。
> 其中关于管理器应用（`/manager/`）的章节属于历史参考，不属于当前工作流。

## 智能体快速上手

- 对于重要功能或重构，先草拟一份计划（Plan）；并在工作过程中持续更新它。
- 当涉及不熟悉的 crate、Android API 或 JS 依赖时，使用 Context7 获取库/API 文档。
- 搜索默认使用 `rg`；编辑内容保持 ASCII，除非文件本身已使用非 ASCII 字符。
- 交付前运行下方各组件对应的检查；不要跳过失败的步骤。
- 拿不准该走哪条路时，优先选择风险最小、且不破坏 kernel/userspace 契约的改动。

## 项目概览

KernelSU 是一个基于内核的 Android root 解决方案，包含内核模块、Rust 用户态守护进程、Kotlin 管理器应用以及文档/Web 资源。

## 仓库结构

```bash
/kernel/                      # 内核模块 —— 用于 Linux 内核集成的 C 代码
/userspace/ksud/              # 用户态守护进程 —— 负责用户态与内核通信的 Rust 可执行文件
/userspace/meta-overlayfs/    # Meta-overlay 文件系统实现 —— Rust 可执行文件 + 脚本
/manager/                     # Android 管理器应用 —— Kotlin/Jetpack Compose UI
/website/                     # 文档网站 —— VitePress
/js/                          # 用于模块 WebUI 的 JavaScript 库
/.github/workflows/           # 用于构建与测试的 CI/CD 工作流
/scripts/                     # 构建自动化脚本（Python）
```

## 核心概念

- **supercall**：由 `[ksu_driver]` 匿名 inode 暴露、并在 `kernel/supercalls.c` 中通过重启 kprobe 钩子安装的内核侧 IOCTL 接口。它映射了诸如 allowlist/app-profile 管理、功能开关、sepolicy 变更等命令。Rust 用户态通过 `userspace/ksud/src/ksucalls.rs` 访问它（扫描或安装 FD、封装 IOCTL），而管理器 JNI 桥接层在 `manager/app/src/main/cpp/ksu.cc` 中镜像了相同的 IOCTL。
- **module**：可刷入的 ZIP，由 `userspace/ksud/src/module.rs` 解压到 `/data/adb/modules/`（`userspace/ksud/src/defs.rs`），其生命周期脚本（`post-fs-data.sh`、`service.sh` 等）由 ksud 的 init 事件（`userspace/ksud/src/init_event.rs`）执行。Android 管理器在 `manager/app/src/main/java/me/weishu/kernelsu/ui/viewmodel/ModuleViewModel.kt` 中呈现来自 ksud 的模块状态。
- **metamodule**：一种特殊模块，在 `module.prop` 中以 `metamodule=1` 标记（参见 `userspace/meta-overlayfs/metamodule/module.prop`）。ksud 强制仅允许一个活动 metamodule，创建 `/data/adb/metamodule -> /data/adb/modules/<id>` 符号链接，并通过 `userspace/ksud/src/metamodule.rs` 委派挂载/meta 安装钩子；在 `userspace/ksud/src/init_event.rs` 中，metamodule 脚本先于普通模块运行。管理器 UI 会高亮 metamodule，并在卸载时给出警告（`manager/app/src/main/java/me/weishu/kernelsu/ui/screen/Module.kt`）。
- **app profile**：定义于 `kernel/app_profile.h`、并在 `kernel/allowlist.c` 中校验/持久化的按应用策略结构体，用于控制 root 授权与非 root 行为（例如累积 umount 策略）。supercall IOCTL `KSU_IOCTL_GET/SET_APP_PROFILE` 位于 `kernel/supercalls.c`，由 ksud/管理器通过 JNI 桥接层（`manager/app/src/main/cpp/ksu.cc`）以及 Kotlin 模型 `Natives.Profile`（`manager/app/src/main/java/me/weishu/kernelsu/Natives.kt`）消费。
- **sucompat**：Exec/FS 兼容层，对已授权 UID 将 `/system/bin/su` 重定向到 ksud，从而保持旧式“调用 su 获取 root”的流程可用。相关钩子位于 `kernel/sucompat.c`，由系统调用钩子管理器注册；功能开关 `KSU_FEATURE_SU_COMPAT` 通过 supercall 暴露，并经 `manager/app/src/main/cpp/ksu.cc`（`is_su_enabled` / `set_su_enabled`）呈现给管理器。
- **allowlist**：由内核管理的、允许获取 root 的 UID 列表，持久化于 `/data/adb/ksu/.allowlist`，包含默认的 root/非 root 配置。核心逻辑位于 `kernel/allowlist.c`（位图存储、持久化、默认 profile 缓存），并由 `kernel/ksu.c` 初始化；`kernel/supercalls.c` 中的 supercall 处理函数暴露了 getter、拒绝列表检查以及“是否应 umount 模块”的判定。管理器通过 `manager/app/src/main/cpp/ksu.cc` 中的 JNI 调用和 Kotlin 门面 `Natives` 读取并修改它。

## 组件工作流

### 内核（`kernel/`）

- 内核改动仅限 C；保持接口与用户态/管理器所期望的 supercall 和 allowlist 一致。
- 如果你改动了 IOCTL 或 profile，请同步更新 ksud（`ksucalls.rs`）和管理器 JNI（`manager/app/src/main/cpp/ksu.cc`）中对应的封装。

### 用户态 Rust（`userspace/ksud`、`userspace/meta-overlayfs`）

对于 `userspace/ksud` 和 `userspace/meta-overlayfs` 中的 Rust 项目，修改代码后**务必**按顺序运行以下命令：

1. `cargo ndk -t arm64-v8a check`（验证编译）
2. `cargo ndk -t arm64-v8a clippy`（lint 与警告）
3. `cargo fmt`（格式化）
4. 在认为任务完成前修复所有错误或警告。

### Android 管理器应用（`manager/`）

```bash
cd manager
# 必须先准备好 ksud 二进制文件！
mkdir -p app/src/main/jniLibs/arm64-v8a
cp ../userspace/ksud/target/aarch64-linux-android/release/ksud app/src/main/jniLibs/arm64-v8a/libksud.so

# 然后构建
./gradlew clean assembleRelease
```

重要：管理器构建**要求**在构建前 `jniLibs` 中已存在 ksud 二进制文件。

### 网站（`website/`）

```bash
cd website
# 使用 bun（推荐）
bun install
bun run docs:build  # 生产构建
```

### JavaScript Web UI（`js/`）

- JS 包用于支撑模块 WebUI 的各个部分；遵循现有的包管理器 lockfile，并在发布改动前运行相关的 lint/测试脚本。

## 常见陷阱

- 只能有一个 metamodule 处于活动状态；保持 meta 钩子与 ksud 的预期一致。
- 管理器 JNI 镜像了每一个 supercall；内核或 ksud 的 API 变更必须同步反映到那里，以避免运行时漂移。
- 不要跳过 `cargo ndk` 步骤；单纯的 `cargo check` 无法验证 Android 目标。
- 若缺少 `libksud.so`，管理器构建会失败；在执行任何 Gradle 命令前先创建它。

### 网站（`website/`）

```bash
cd website
# 使用 bun（推荐）
bun install
bun run docs:build  # 生产构建
```

### JavaScript Web UI（`js/`）

- JS 包用于支撑模块 WebUI 的各个部分；遵循现有的 lockfile，并在发布改动前运行相关的 lint/测试脚本。

> **已归档，仅作参考：** 管理器应用（`/manager/`）的构建流程不在本文范围内。

## 常见陷阱

- 只能有一个 metamodule 处于活动状态；保持 meta 钩子与 ksud 的预期一致。
- 不要跳过 `cargo ndk` 步骤；单纯的 `cargo check` 无法验证 Android 目标。

## Git 提交

- 与现有历史风格保持一致：`<scope>: <summary>`，其中 scope 为与改动区域相关的短小写标识（例如 `kernel`、`ksud`、`manager`、`meta-overlayfs`、`docs`、`scripts`）。摘要保持简洁、使用句首大写，且结尾不加句号。
- 优先使用单一 scope；若多个区域有改动，选择主要的那一个，而不要串联多个 scope。仅文档改动使用 `docs:`；多语言字符串更新若与日志历史相符，则使用 `translations:`。
- 保持标题行简短（目标 ≤72 字符），除非必要否则不写正文。如需引用 PR/issue，按历史惯例在末尾追加 `(#1234)`。
- 提交前先浏览最近的 `git log --oneline`，以保持与本仓库当前使用的前缀和大小写风格一致。
