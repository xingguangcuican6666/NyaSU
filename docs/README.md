**English** | [Español](README_ES.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md) | [한국어](README_KR.md) | [Polski](README_PL.md) | [Português (Brasil)](README_PT-BR.md) | [Türkçe](README_TR.md) | [Русский](README_RU.md) | [Tiếng Việt](README_VI.md) | [Indonesia](README_ID.md) | [עברית](README_IW.md) | [हिंदी](README_IN.md) | [Italiano](README_IT.md)

# NyaSU

<img src="https://raw.githubusercontent.com/xingguangcuican6666/NyaSU/main/website/docs/public/logo.png" style="width: 96px;" alt="logo">

A kernel-based root solution for Android devices.

[![Latest release](https://img.shields.io/github/v/release/xingguangcuican6666/NyaSU?label=Release&logo=github)](https://github.com/xingguangcuican6666/NyaSU/releases/latest)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-orange.svg?logo=gnu)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![GitHub License](https://img.shields.io/github/license/xingguangcuican6666/NyaSU?logo=gnu)](/LICENSE)

## Upstream

NyaSU is a derivative work of [KernelSU](https://github.com/tiann/KernelSU), an open-source kernel-based root solution created by tiann and its contributors. The kernel-side design, the supercall interface and the module format all originate from that project, and upstream remains the authoritative reference for anything this repository's documentation does not cover.

NyaSU keeps the same licenses as upstream: every file under `kernel/` is GPL-2.0-only, and everything else is GPL-3.0-or-later. Copyright in the upstream code remains with its original authors.

## Features

1. Kernel-based `su` and root access management.
2. Module system based on [metamodules](../website/docs/guide/metamodule.md): Pluggable infrastructure for systemless modifications.
3. [App Profile](../website/docs/guide/app-profile.md): Lock up the root power in a cage.

## Compatibility state

NyaSU officially supports Android GKI 2.0 devices (kernel 5.10+). Older kernels (4.14+) are also supported, but the kernel will need to be built manually.

With this, WSA, ChromeOS, and container-based Android are all supported.

Currently, the `arm64-v8a` and `x86_64` architectures are supported.

> [!CAUTION]
> Recent kernel versions have implemented a breaking change causing NyaSU to fail and potentially trigger a kernel panic on `x86_64`! Check the website for more info!

## Usage

- [Installation](../website/docs/guide/installation.md)
- [How to build](../website/docs/guide/how-to-build.md)
- [Official website](../website/docs/index.md)

## Translation

Translations are produced with LLMs; the localized READMEs in this directory are generated this way.

If you would like to add support for a new language, feel free to open a PR. Modifications to the existing English and Chinese texts are not accepted.

## Security

For information on reporting security vulnerabilities in NyaSU, see [SECURITY.md](/SECURITY.md).

## License

- Files under the `kernel` directory are [GPL-2.0-only](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html).
- All other parts except the `kernel` directory are [GPL-3.0-or-later](https://www.gnu.org/licenses/gpl-3.0.html).

## Credits

- [Kernel-Assisted Superuser](https://git.zx2c4.com/kernel-assisted-superuser/about/): The KernelSU idea.
- [Magisk](https://github.com/topjohnwu/Magisk): The powerful root tool.
- [genuine](https://github.com/brevent/genuine/): APK v2 signature validation.
- [Diamorphine](https://github.com/m0nad/Diamorphine): Some rootkit skills.
