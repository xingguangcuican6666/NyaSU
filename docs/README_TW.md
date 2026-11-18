[English](README.md) | [Español](README_ES.md) | [简体中文](README_CN.md) | **繁體中文** | [日本語](README_JP.md) | [한국어](README_KR.md) | [Polski](README_PL.md) | [Português (Brasil)](README_PT-BR.md) | [Türkçe](README_TR.md) | [Русский](README_RU.md) | [Tiếng Việt](README_VI.md) | [Indonesia](README_ID.md) | [עברית](README_IW.md) | [हिंदी](README_IN.md) | [Italiano](README_IT.md)

# NyaSU

<img src="https://raw.githubusercontent.com/xingguangcuican6666/NyaSU/main/website/docs/public/logo.png" style="width: 96px;" alt="標誌">

一套基於 Android 裝置核心的 Root 解決方案。

[![最新版本](https://img.shields.io/github/v/release/xingguangcuican6666/NyaSU?label=%e7%99%bc%e8%a1%8c%e7%89%88%e6%9c%ac&logo=github)](https://github.com/xingguangcuican6666/NyaSU/releases/latest)
[![授權條款：《GPL v2》](https://img.shields.io/badge/%e6%8e%88%e6%ac%8a%e6%a2%9d%e6%ac%be-%E3%80%8AGPL%20v2%E3%80%8B-orange.svg?logo=gnu)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![GitHub 授權條款](https://img.shields.io/github/license/xingguangcuican6666/NyaSU?logo=gnu)](/LICENSE)

## 上游專案

NyaSU 衍生自 [KernelSU](https://github.com/tiann/KernelSU) —— 由 tiann 與其貢獻者打造的開源、基於核心的 Android Root 方案。核心端設計、supercall 介面與模組格式皆源自該專案；本倉庫文件未涵蓋的內容，仍以上游為準。

授權條款與上游一致：`kernel` 資料夾下的檔案為 GPL-2.0-only，其餘部分為 GPL-3.0-or-later。上游程式碼的著作權仍屬原作者所有。

## 特色功能

1. 以核心內 `su` 管理 Root 存取。
2. 以 [metamodules](../website/docs/zh_TW/guide/metamodule.md) 運作模組系統：可插拔的無系統修改基礎架構。
3. [App Profile](../website/docs/zh_TW/guide/app-profile.md)：使 Root 掌握的生殺大權受制於此。

## 相容事態

理論上採以 Android GKI 2.0 的裝置（核心版本 5.10+），皆受 NyaSU 支援；採以老舊核心版本（4.14+）的裝置在手動建置核心後，亦受支援。

另可在 WSA、ChromeOS 一類的容器式 Android 中運作。

目前支援 `arm64-v8a` 和 `x86_64` 架構。

> [!CAUTION]
> 最近的核心版本引入了一項破壞性更改，導致 NyaSU 在 `x86_64` 上執行失敗，甚至可能引發核心恐慌 (kernel panic)！請查看網站獲取更多資訊！

## 使用手冊

- [安裝教學](../website/docs/zh_TW/guide/installation.md)
- [如何建置 NyaSU？](../website/docs/zh_TW/guide/how-to-build.md)
- [官方網站](../website/docs/zh_TW/index.md)

## 多語翻譯

本目錄下的多語 README 由 LLM 產生。

若想新增語言，歡迎提交 PR；既有的英文與中文文本不接受變更。

## 安全政策

欲要得知、回報 NyaSU 的安全性漏洞，請參閱 [SECURITY.md](/SECURITY.md)。

## 授權條款

- 位於 `kernel` 資料夾的檔案以[《GPL-2.0-only》](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)規範。
- 非位於 `kernel` 資料夾的其他檔案以[《GPL-3.0-or-later》](https://www.gnu.org/licenses/gpl-3.0.html)規範。

## 致謝名單

- [kernel-assisted-superuser](https://git.zx2c4.com/kernel-assisted-superuser/about/)：KernelSU 的靈感來源。
- [Magisk](https://github.com/topjohnwu/Magisk)：強而有力的 Root 工具。
- [genuine](https://github.com/brevent/genuine/)：用於確效 Apk v2 簽章。
- [Diamorphine](https://github.com/m0nad/Diamorphine): 用於增進 Rootkit 技巧。
