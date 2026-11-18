[English](README.md) | [Español](README_ES.md) | **简体中文** | [繁體中文](README_TW.md) | [日本語](README_JP.md) | [한국어](README_KR.md) | [Polski](README_PL.md) | [Português (Brasil)](README_PT-BR.md) | [Türkçe](README_TR.md) | [Русский](README_RU.md) | [Tiếng Việt](README_VI.md) | [Indonesia](README_ID.md) | [עברית](README_IW.md) | [हिंदी](README_IN.md) | [Italiano](README_IT.md)

# NyaSU

<img src="https://raw.githubusercontent.com/xingguangcuican6666/NyaSU/main/website/docs/public/logo.png" style="width: 96px;" alt="logo">

一个 Android 上基于内核的 root 方案。

[![Latest release](https://img.shields.io/github/v/release/xingguangcuican6666/NyaSU?label=Release&logo=github)](https://github.com/xingguangcuican6666/NyaSU/releases/latest)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-orange.svg?logo=gnu)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![GitHub License](https://img.shields.io/github/license/xingguangcuican6666/NyaSU?logo=gnu)](/LICENSE)

## 上游

NyaSU 派生自 [KernelSU](https://github.com/tiann/KernelSU) —— 由 tiann 及其贡献者创建的开源、基于内核的 Android root 方案。内核侧设计、supercall 接口与模块格式均来自该项目；本仓库文档未覆盖的部分，以上游为准。

许可证与上游保持一致：`kernel` 目录下的所有文件为 GPL-2.0-only，其余部分为 GPL-3.0-or-later。上游代码的著作权仍归原作者所有。

## 特性

- 基于内核的 `su` 和权限管理。
- 基于 [metamodules](../website/docs/zh_CN/guide/metamodule.md) 的模块系统：可插拔的模块架构。
- [App Profile](../website/docs/zh_CN/guide/app-profile.md): 把 Root 权限关进笼子里。

## 兼容状态

NyaSU 官方支持 GKI 2.0 的设备（内核版本5.10以上）；旧内核也是兼容的（最低4.14+），不过需要自己编译内核。

WSA, ChromeOS 和运行在容器上的 Android 也可以与 NyaSU 一起工作。

目前支持 `arm64-v8a` 和 `x86_64` 架构。

> [!CAUTION]
> 最近的内核版本引入了一项破坏性更改，导致 NyaSU 在 `x86_64` 上运行失败，甚至可能引发内核恐慌 (kernel panic)！请查看网站获取更多信息！

## 使用方法

- [安装教程](../website/docs/zh_CN/guide/installation.md)
- [如何构建？](../website/docs/zh_CN/guide/how-to-build.md)
- [官方网站](../website/docs/zh_CN/index.md)

## 参与翻译

本目录下的多语言 README 由 LLM 生成。

如需新增一种语言，欢迎提交 PR；已存在的英文与中文文本不接受修改。

## 安全性

有关报告 NyaSU 安全漏洞的信息，请参阅 [SECURITY.md](/SECURITY.md)。

## 许可证

- 目录 `kernel` 下所有文件为 [GPL-2.0-only](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)。
- 除 `kernel` 目录的其他部分均为 [GPL-3.0-or-later](https://www.gnu.org/licenses/gpl-3.0.html)。

## 鸣谢

- [kernel-assisted-superuser](https://git.zx2c4.com/kernel-assisted-superuser/about/)：KernelSU 的灵感。
- [Magisk](https://github.com/topjohnwu/Magisk)：强大的 root 工具箱。
- [genuine](https://github.com/brevent/genuine/)：apk v2 签名验证。
- [Diamorphine](https://github.com/m0nad/Diamorphine)：一些 rootkit 技巧。
