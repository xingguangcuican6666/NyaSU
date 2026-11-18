[English](README.md) | [Español](README_ES.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md) | [한국어](README_KR.md) | **Polski** | [Português (Brasil)](README_PT-BR.md) | [Türkçe](README_TR.md) | [Русский](README_RU.md) | [Tiếng Việt](README_VI.md) | [Indonesia](README_ID.md) | [עברית](README_IW.md) | [हिंदी](README_IN.md) | [Italiano](README_IT.md)

# NyaSU

<img src="https://raw.githubusercontent.com/xingguangcuican6666/NyaSU/main/website/docs/public/logo.png" style="width: 96px;" alt="logo">

Rozwiązanie root oparte na jądrze dla urządzeń z systemem Android.

[![Latest release](https://img.shields.io/github/v/release/xingguangcuican6666/NyaSU?label=Release&logo=github)](https://github.com/xingguangcuican6666/NyaSU/releases/latest)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-orange.svg?logo=gnu)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![GitHub License](https://img.shields.io/github/license/xingguangcuican6666/NyaSU?logo=gnu)](/LICENSE)

## Projekt upstream

NyaSU jest pochodną [KernelSU](https://github.com/tiann/KernelSU) — otwartoźródłowego rozwiązania root opartego na jądrze, stworzonego przez tiann i współtwórców. Projekt po stronie jądra, interfejs supercall oraz format modułów pochodzą z tego projektu; w sprawach nieopisanych w dokumentacji tego repozytorium obowiązuje upstream.

Licencje są takie same jak w upstreamie: pliki w `kernel/` są na licencji GPL-2.0-only, a cała reszta na GPL-3.0-or-later. Prawa autorskie do oryginalnego kodu pozostają u jego autorów.

## Cechy

1. Oparte na jądrze `su` i zarządzanie dostępem roota.
2. System modułów oparty na [metamodules](../website/docs/guide/metamodule.md): Wtykowa infrastruktura dla modyfikacji systemless.

## Kompatybilność

NyaSU oficjalnie obsługuje urządzenia z Androidem GKI 2.0 (z jądrem 5.10+), starsze jądra (4.14+) są również kompatybilne, ale musisz sam skompilować jądro.

WSA i Android oparty na kontenerach również powinny działać ze zintegrowanym NyaSU.

Obecnie obsługiwane są architektury `arm64-v8a` oraz `x86_64`.

> [!CAUTION]
> Nowsze wersje jądra wprowadzają zmianę, która powoduje awarię NyaSU i może wywołać kernel panic na `x86_64`! Sprawdź stronę internetową po więcej informacji!

## Użycie

- [Instalacja](../website/docs/guide/installation.md)
- [Jak skompilować?](../website/docs/guide/how-to-build.md)

## Tłumaczenie

Tłumaczenia w tym katalogu są generowane za pomocą LLM.

Aby dodać nowy język, otwórz PR. Zmiany w istniejących tekstach angielskim i chińskim nie są przyjmowane.

## Bezpieczeństwo

Informacje na temat zgłaszania luk w zabezpieczeniach w NyaSU można znaleźć w pliku [SECURITY.md](/SECURITY.md).

## Licencja

- Pliki w katalogu `kernel` są na licencji [GPL-2-only](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html).
- Wszystkie inne części poza katalogiem `kernel` są na licencji [GPL-3-or-later](https://www.gnu.org/licenses/gpl-3.0.html).

## Podziękowania

- [kernel-assisted-superuser](https://git.zx2c4.com/kernel-assisted-superuser/about/): pomysłodawca KernelSU.
- [Magisk](https://github.com/topjohnwu/Magisk): implementacja sepolicy.
- [genuine](https://github.com/brevent/genuine/): walidacja podpisu apk v2.
- [Diamorphine](https://github.com/m0nad/Diamorphine): cenna znajomość rootkitów.
