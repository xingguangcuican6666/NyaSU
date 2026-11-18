[English](README.md) | [Español](README_ES.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md) | **한국어** | [Polski](README_PL.md) | [Português (Brasil)](README_PT-BR.md) | [Türkçe](README_TR.md) | [Русский](README_RU.md) | [Tiếng Việt](README_VI.md) | [Indonesia](README_ID.md) | [עברית](README_IW.md) | [हिंदी](README_IN.md) | [Italiano](README_IT.md)

# NyaSU

<img src="https://raw.githubusercontent.com/xingguangcuican6666/NyaSU/main/website/docs/public/logo.png" style="width: 96px;" alt="logo">

안드로이드 기기에서 사용되는 커널 기반 루팅 솔루션입니다.

[![Latest release](https://img.shields.io/github/v/release/xingguangcuican6666/NyaSU?label=Release&logo=github)](https://github.com/xingguangcuican6666/NyaSU/releases/latest)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-orange.svg?logo=gnu)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![GitHub License](https://img.shields.io/github/license/xingguangcuican6666/NyaSU?logo=gnu)](/LICENSE)

## 업스트림

NyaSU는 tiann과 기여자들이 만든 오픈소스 커널 기반 Android 루팅 솔루션 [KernelSU](https://github.com/tiann/KernelSU)의 파생 프로젝트입니다. 커널 측 설계, supercall 인터페이스, 모듈 형식은 모두 해당 프로젝트에서 비롯되었으며, 이 저장소의 문서가 다루지 않는 내용은 업스트림을 기준으로 합니다.

라이선스는 업스트림과 동일합니다. `kernel` 디렉터리 아래 파일은 GPL-2.0-only, 나머지는 GPL-3.0-or-later입니다. 업스트림 코드의 저작권은 원저작자에게 있습니다.

## 기능들

1. 커널 기반 `su` 및 루트 액세스 관리.
2. [metamodules](../website/docs/guide/metamodule.md) 기반 모듈 시스템: 플러그인 가능한 시스템리스 수정 인프라.
3. [App Profile](../website/docs/guide/app-profile.md): 루트 권한을 케이지에 가둡니다.

## 호환 상태

NyaSU는 공식적으로 안드로이드 GKI 2.0 디바이스(커널 5.10 이상)를 지원합니다. 오래된 커널(4.14 이상)도 사용할 수 있지만, 커널을 수동으로 빌드해야 합니다.

NyaSU는 WSA, ChromeOS, 컨테이너 기반 안드로이드 모두를 지원합니다.

현재 `arm64-v8a` 및 `x86_64` 아키텍처가 지원됩니다.

> [!CAUTION]
> 최신 커널 버전에는 NyaSU가 실패하고 `x86_64`에서 커널 패닉을 일으킬 수 있는 치명적인 변경 사항이 적용되었습니다! 자세한 내용은 웹사이트를 확인하세요!

## 사용 방법

- [설치 방법](../website/docs/guide/installation.md)
- [어떻게 빌드하나요?](../website/docs/guide/how-to-build.md)
- [공식 웹사이트](../website/docs/index.md)

## 번역

이 디렉터리의 다국어 README는 LLM으로 생성됩니다.

새 언어 지원은 PR로 환영합니다. 기존 영어·중국어 텍스트의 수정은 받지 않습니다.

## 보안

NyaSU의 보안 취약점 보고에 대한 자세한 내용은 [SECURITY.md](/SECURITY.md)를 참조하세요.

## 저작권

- `kernel` 디렉터리 아래의 파일은 [GPL-2.0 전용](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)입니다.
- `kernel` 디렉토리를 제외한 다른 모든 부분은 [GPL-3.0-이상](https://www.gnu.org/licenses/gpl-3.0.html)입니다.

## 크래딧

- [kernel-assisted-superuser](https://git.zx2c4.com/kernel-assisted-superuser/about/): KernelSU의 아이디어.
- [Magisk](https://github.com/topjohnwu/Magisk): 강력한 루팅 도구.
- [genuine](https://github.com/brevent/genuine/): apk v2 서명 유효성 검사.
- [Diamorphine](https://github.com/m0nad/Diamorphine): 일부 rootkit 스킬.
