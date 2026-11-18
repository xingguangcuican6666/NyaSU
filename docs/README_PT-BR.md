[English](README.md) | [Español](README_ES.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md) | [한국어](README_KR.md) | [Polski](README_PL.md) | **Português (Brasil)** | [Türkçe](README_TR.md) | [Русский](README_RU.md) | [Tiếng Việt](README_VI.md) | [Indonesia](README_ID.md) | [עברית](README_IW.md) | [हिंदी](README_IN.md) | [Italiano](README_IT.md)

# NyaSU

<img src="https://raw.githubusercontent.com/xingguangcuican6666/NyaSU/main/website/docs/public/logo.png" style="width: 96px;" alt="logo">

Uma solução root baseada em kernel para dispositivos Android.

[![Latest release](https://img.shields.io/github/v/release/xingguangcuican6666/NyaSU?label=Release&logo=github)](https://github.com/xingguangcuican6666/NyaSU/releases/latest)
[![License: GPL v2](https://img.shields.io/badge/Licença-GPL%20v2-orange.svg?logo=gnu)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![GitHub License](https://img.shields.io/github/license/xingguangcuican6666/NyaSU?logo=gnu)](/LICENSE)

## Upstream

O NyaSU é um derivado do [KernelSU](https://github.com/tiann/KernelSU), uma solução root de código aberto baseada em kernel criada por tiann e seus colaboradores. O projeto do lado do kernel, a interface supercall e o formato de módulos vêm desse projeto; o upstream continua sendo a referência para tudo o que não estiver coberto pela documentação deste repositório.

As licenças são as mesmas do upstream: os arquivos em `kernel/` são GPL-2.0-only e todo o restante é GPL-3.0-or-later. Os direitos autorais do código original permanecem com seus autores.

## Características

1. `su` e gerenciamento de acesso root baseado em kernel.
2. Sistema de módulos baseado em [metamodules](../website/docs/pt_BR/guide/metamodule.md): Infraestrutura plugável para modificações systemless.
3. [Perfil do Aplicativo](../website/docs/pt_BR/guide/app-profile.md): Tranque o poder root em uma gaiola.

## Estado de compatibilidade

O NyaSU oferece suporte oficial a dispositivos Android GKI 2.0 (kernel 5.10+). Kernels mais antigos (4.14+) também são compatíveis, mas será necessário construir o kernel manualmente.

Com isso, WSA, ChromeOS e Android baseado em contêiner são todos suportados.

Atualmente, as arquiteturas `arm64-v8a` e `x86_64` são suportadas.

> [!CAUTION]
> Versões recentes do kernel implementaram uma mudança que quebra a compatibilidade, fazendo com que o NyaSU falhe e potencialmente cause um kernel panic no `x86_64`! Verifique o site para mais informações!

## Uso

 - [Instalação](../website/docs/pt_BR/guide/installation.md)
 - [Como compilar](../website/docs/pt_BR/guide/how-to-build.md)
 - [Site oficial](../website/docs/pt_BR/index.md)

## Tradução

As traduções deste diretório são geradas com LLM.

Para adicionar um novo idioma, abra um PR. Alterações nos textos existentes em inglês e chinês não são aceitas.

## Segurança

Para obter informações sobre como relatar vulnerabilidades de segurança do NyaSU, consulte [SECURITY.md](/SECURITY.md).

## Licença

- Os arquivos no diretório `kernel` são [GPL-2.0-only](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html).
- Todas as outras partes, exceto o diretório `kernel` são [GPL-3.0-or-later](https://www.gnu.org/licenses/gpl-3.0.html).

## Créditos

- [Kernel-Assisted Superuser](https://git.zx2c4.com/kernel-assisted-superuser/about/): A ideia do KernelSU.
- [Magisk](https://github.com/topjohnwu/Magisk): A poderosa ferramenta root.
- [genuine](https://github.com/brevent/genuine/): Validação de assinatura APK v2.
- [Diamorphine](https://github.com/m0nad/Diamorphine): Algumas habilidades de rootkit.
