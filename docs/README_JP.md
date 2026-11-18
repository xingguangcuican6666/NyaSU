[English](README.md) | [Español](README_ES.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | **日本語** | [한국어](README_KR.md) | [Polski](README_PL.md) | [Português (Brasil)](README_PT-BR.md) | [Türkçe](README_TR.md) | [Русский](README_RU.md) | [Tiếng Việt](README_VI.md) | [Indonesia](README_ID.md) | [עברית](README_IW.md) | [हिंदी](README_IN.md) | [Italiano](README_IT.md)

# NyaSU

<img src="https://raw.githubusercontent.com/xingguangcuican6666/NyaSU/main/website/docs/public/logo.png" style="width: 96px;" alt="logo">

Android におけるカーネルベースの root ソリューションです。

[![Latest release](https://img.shields.io/github/v/release/xingguangcuican6666/NyaSU?label=Release&logo=github)](https://github.com/xingguangcuican6666/NyaSU/releases/latest)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-orange.svg?logo=gnu)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![GitHub License](https://img.shields.io/github/license/xingguangcuican6666/NyaSU?logo=gnu)](/LICENSE)

## 上流プロジェクト

NyaSU は [KernelSU](https://github.com/tiann/KernelSU) の派生プロジェクトです。KernelSU は tiann とその貢献者による、オープンソースのカーネルベース Android root ソリューションです。カーネル側の設計、supercall インターフェース、モジュール形式はいずれも同プロジェクトに由来し、本リポジトリのドキュメントで扱っていない事項は上流を参照してください。

ライセンスは上流と同一です。`kernel` ディレクトリ配下は GPL-2.0-only、それ以外は GPL-3.0-or-later です。上流コードの著作権は元の作者に帰属します。

## 特徴

1. カーネルベースの `su` と権限管理。
2. [metamodules](../website/docs/ja_JP/guide/metamodule.md) に基づくモジュールシステム: プラグイン可能なシステムレス変更インフラストラクチャ。
3. [アプリのプロファイル](../website/docs/ja_JP/guide/app-profile.md): root の権限をケージ内に閉じ込めます。

## 対応状況

NyaSU は GKI 2.0 デバイス（カーネルバージョン 5.10 以上）を公式にサポートしています。古いカーネル（4.14以上）とも互換性がありますが、自分でカーネルをビルドする必要があります。

WSA 、ChromeOS とコンテナ上で動作する Android でも NyaSU を統合して動かせます。

現在、`arm64-v8a` および `x86_64` アーキテクチャがサポートされています。

> [!CAUTION]
> 最近のカーネルバージョンでは、NyaSU が機能しなくなり、`x86_64` 上でカーネルパニックを引き起こす可能性のある破壊的な変更が実装されています！詳細についてはウェブサイトを確認してください！

## 使用方法

- [インストール方法はこちら](../website/docs/ja_JP/guide/installation.md)
- [ビルド方法はこちら](../website/docs/ja_JP/guide/how-to-build.md)
- [公式サイト](../website/docs/ja_JP/index.md)

## 翻訳

本ディレクトリの多言語 README は LLM によって生成されています。

新しい言語の追加は PR で受け付けます。既存の英語・中国語テキストの変更は受け付けません。

## ライセンス

- `kernel` ディレクトリの下にあるすべてのファイル： [GPL-2-only](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)。
- `kernel` ディレクトリ以外のすべてのファイル： [GPL-3.0-or-later](https://www.gnu.org/licenses/gpl-3.0.html)。

## クレジット

- [kernel-assisted-superuser](https://git.zx2c4.com/kernel-assisted-superuser/about/)：KernelSU のアイデア元。
- [Magisk](https://github.com/topjohnwu/Magisk)：強力な root ツール。
- [genuine](https://github.com/brevent/genuine/)：apk v2 の署名検証。
- [Diamorphine](https://github.com/m0nad/Diamorphine): rootkit のスキル。
