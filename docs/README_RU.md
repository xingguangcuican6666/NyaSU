[English](README.md) | [Español](README_ES.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md) | [한국어](README_KR.md) | [Polski](README_PL.md) | [Português (Brasil)](README_PT-BR.md) | [Türkçe](README_TR.md) | **Русский** | [Tiếng Việt](README_VI.md) | [Indonesia](README_ID.md) | [עברית](README_IW.md) | [हिंदी](README_IN.md) | [Italiano](README_IT.md)

# NyaSU

<img src="https://raw.githubusercontent.com/xingguangcuican6666/NyaSU/main/website/docs/public/logo.png" style="width: 96px;" alt="logo">

Решение на основе ядра root для Android-устройств.

[![Latest release](https://img.shields.io/github/v/release/xingguangcuican6666/NyaSU?label=Release&logo=github)](https://github.com/xingguangcuican6666/NyaSU/releases/latest)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-orange.svg?logo=gnu)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![GitHub License](https://img.shields.io/github/license/xingguangcuican6666/NyaSU?logo=gnu)](/LICENSE)

## Апстрим

NyaSU — производный проект от [KernelSU](https://github.com/tiann/KernelSU), открытого root-решения на основе ядра, созданного tiann и его участниками. Архитектура ядерной части, интерфейс supercall и формат модулей происходят из того проекта; во всём, что не описано в документации этого репозитория, следует опираться на апстрим.

Лицензии те же, что и у апстрима: файлы в `kernel/` — GPL-2.0-only, всё остальное — GPL-3.0-or-later. Авторские права на исходный код остаются у его авторов.

## Особенности

1. Управление `su` и root-доступом на основе ядра.
2. Система модулей на основе [metamodules](../website/docs/ru_RU/guide/metamodule.md): Подключаемая инфраструктура для безсистемных модификаций.
3. [Профиль приложений](../website/docs/ru_RU/guide/app-profile.md): Запри корневую силу в клетке.

## Совместимость

NyaSU официально поддерживает устройства на базе Android GKI 2.0 (с ядром 5.10+), старые ядра (4.14+) также совместимы, но для этого необходимо собрать ядро самостоятельно.

WSA и Android на основе контейнеров также должны работать с интегрированным NyaSU.

В настоящее время поддерживаются архитектуры `arm64-v8a` и `x86_64`.

> [!CAUTION]
> В последних версиях ядра реализовано критическое изменение, из-за которого NyaSU перестает работать и может вызвать панику ядра (kernel panic) на `x86_64`! Дополнительную информацию смотрите на сайте!

## Использование

- [Установка](../website/docs/ru_RU/guide/installation.md)
- [Как собрать?](../website/docs/ru_RU/guide/how-to-build.md)
- [официальный сайт](../website/docs/ru_RU/index.md)

## Лицензия

- Файлы в директории `kernel` [GPL-2-only](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html).
- Все остальные части, кроме директории `kernel` [GPL-3-or-later](https://www.gnu.org/licenses/gpl-3.0.html).

## Благодарности

- [kernel-assisted-superuser](https://git.zx2c4.com/kernel-assisted-superuser/about/): идея KernelSU.
- [Magisk](https://github.com/topjohnwu/Magisk): реализация sepolicy.
- [genuine](https://github.com/brevent/genuine/): проверка подписи apk v2.
- [Diamorphine](https://github.com/m0nad/Diamorphine): некоторые навыки руткита.
