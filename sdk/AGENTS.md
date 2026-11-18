# 构建与测试

所有命令在 `sdk/` 目录下执行，不依赖内核树，也不需要 Android NDK。

## 目录

```bash
ksuhook/            # SDK 本体（纯 Python，标准库 + pytest）
  cparse.py         # 解析 KernelSU 源码里的函数定义
  spec.py           # 解析 hookpack.toml
  merge.py          # 合并多个模块对同一函数的改动
  generate.py       # 生成 C 分发代码
  patch.py          # 生成 unified diff
  devkit.py         # 模块单测环境
  cli.py            # 命令行入口
devkit/shim/        # 主机侧内核头文件替身（只用于单测）
examples/uid_audit/ # 示例注入包
tests/              # pytest
```

## 验证

```bash
python3 -m pytest -q
python3 -m ksuhook validate --repo .. --packs examples
python3 -m ksuhook generate --repo .. --packs examples --out dist/ksu-sdkgen.patch
```

## 环境要求

- Python 3.11+（3.10 缺少 `tomllib`，`spec.py` 会给出明确报错）。
- 单测编译需要主机 `cc`（gcc 或 clang）；缺失时相关用例自动跳过。
