# 写一个模块

以 [`examples/uid_audit`](../examples/uid_audit) 为模板，四步走。

## 1. 建目录与元数据

```bash
mkdir -p my_module/src my_module/tests
```

`my_module/module.prop`：

```properties
id=my_module
name=My Module
version=1.0.0
versionCode=1
priority=50
description=一句话说明
```

`priority` 只在多个模块 `order` 相同时用于决定先后，**越大越先**。

## 2. 选一个目标函数

先用 `validate` 看看目标是否存在：

```bash
python3 -m ksuhook validate --repo ../.. --packs my_module
```

目标必须出现在 `kernel/` 下某个 `.c` 的定义里。`inline` / `__always_inline` /
`__inline__` 函数会被拒绝（GKI 下会被内联展开，没有可调用的符号）；`static`
函数也会被拒绝（只有内部链接，`kernel/sdkgen` 下的包装永远链不上）。

## 3. 声明 hook 并写载荷

`my_module/hooks.toml`：

```toml
[[hook]]
id     = "my_hook"
target = "ksu_handle_setresuid"
entry  = "my_module_entry"
mode   = "inject"   # 或 "replace"
order  = 100
```

`my_module/src/my_module.c` —— 签名与目标一致，`inject` 返回 `int`：

```c
#include <linux/printk.h>
#include <linux/uidgid.h>

#include "my_module.h"

int my_module_entry(uid_t old_uid, uid_t new_uid)
{
    if (old_uid != new_uid)
        pr_info("my_module: %u -> %u\n", old_uid, new_uid);
    return 0;  /* 0 = 没有意见，继续原逻辑 */
}
```

`my_module/src/my_module.h`：

```c
#ifndef MY_MODULE_H
#define MY_MODULE_H
#include <linux/uidgid.h>
int my_module_entry(uid_t old_uid, uid_t new_uid);
#endif
```

想完全接管就把 `mode` 改成 `replace`，入口返回类型随之改成目标的返回类型。

## 4. 本地单测

`my_module/tests/test_my_module.c`，第一个文件需要 `main()`：

```c
#include <stdio.h>
#include <stdarg.h>
#include <linux/uidgid.h>
#include "my_module.h"

static int logs;
void ksuhook_test_log(const char *fmt, ...)
{
    va_list ap; (void)fmt;
    va_start(ap, fmt); va_end(ap);
    logs++;
}

int main(void)
{
    my_module_entry(1000, 1000);
    if (logs != 0) { puts("FAIL: unchanged uid logged"); return 1; }
    my_module_entry(1000, 2000);
    if (logs != 1) { puts("FAIL: change not logged"); return 1; }
    puts("ok");
    return 0;
}
```

然后：

```bash
python3 -m ksuhook dev --packs my_module
```

## 5. 生成补丁

```bash
python3 -m ksuhook generate --repo ../.. --packs my_module --out dist/my.patch
# 在 GKI 树根：
git apply -p1 dist/my.patch
```

## 提交前检查清单

- [ ] `validate` 通过，`plan` 打印的执行顺序符合预期
- [ ] `dev` 全部通过
- [ ] `generate` 产出的补丁 `git apply --check` 无冲突
- [ ] 没有修改 `src/` 之外的内核文件；没有触碰上游 mainline 代码
- [ ] 若提供了 `patches/`，确认当前 SDK 版本不读取它（仅预留）
