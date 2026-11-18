[English](REAME.md) | [Español](README_ES.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md) | [한국어](README_KR.md) | [Polski](README_PL.md) | [Português (Brasil)](README_PT-BR.md) | [Türkçe](README_TR.md) | [Русский](README_RU.md) | [Tiếng Việt](README_VI.md) | [Indonesia](README_ID.md) | [עברית](README_IW.md) | [हिंदी](README_IN.md) | **Italiano**

# NyaSU

<img src="https://raw.githubusercontent.com/xingguangcuican6666/NyaSU/main/website/docs/public/logo.png" style="width: 96px;" alt="logo">

Una soluzione per il root basata sul kernel per i dispositivi Android. 

[![Latest release](https://img.shields.io/github/v/release/xingguangcuican6666/NyaSU?label=Release&logo=github)](https://github.com/xingguangcuican6666/NyaSU/releases/latest)
[![Licenza componenti kernel: GPL v2](https://img.shields.io/badge/License-GPL%20v2-orange.svg?logo=gnu)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![Licenza elementi non kern](https://img.shields.io/github/license/xingguangcuican6666/NyaSU?logo=gnu)](/LICENSE)

## Progetto upstream

NyaSU è un derivato di [KernelSU](https://github.com/tiann/KernelSU), soluzione root open source basata sul kernel creata da tiann e dai suoi contributori. Il design lato kernel, l'interfaccia supercall e il formato dei moduli provengono da quel progetto; l'upstream resta il riferimento per tutto ciò che non è trattato dalla documentazione di questo repository.

Le licenze sono le stesse dell'upstream: i file in `kernel/` sono GPL-2.0-only, tutto il resto è GPL-3.0-or-later. Il copyright del codice originale resta ai suoi autori.

## Funzionalità

1. `su` e accesso root basato sul kernel.
2. Sistema di moduli basato su [metamodules](../website/docs/guide/metamodule.md): Infrastruttura modulare per modifiche systemless.
3. [App profile](../website/docs/guide/app-profile.md): Limita i poteri dell'accesso root a permessi specifici.

## Compatibilità

NyaSU supporta ufficialmente i dispositivi Android GKI 2.0 (kernel 5.10 o superiore). I kernel precedenti (kernel 4.14+) sono anche compatibili, ma il kernel deve essere compilato manualmente.

Questo implica che WSA, ChromeOS e tutti le varianti di Android basate su container e virtualizzazione sono supportate.

Attualmente sono supportate le architetture `arm64-v8a` e `x86_64`.

> [!CAUTION]
> Le versioni recenti del kernel hanno implementato una modifica che causa il fallimento di NyaSU e potenzialmente innesca un kernel panic su `x86_64`! Controlla il sito web per maggiori informazioni!

## Utilizzo

- [Istruzioni per l'installazione](../website/docs/guide/installation.md)
- [Come compilare manualmente?](../website/docs/guide/how-to-build.md)
- [Sito web ufficiale](../website/docs/index.md)

## Traduzioni

Le traduzioni di questa directory sono generate con LLM.

Per aggiungere una nuova lingua apri una PR. Le modifiche ai testi esistenti in inglese e cinese non sono accettate.

## Securezza

Per informazioni riguardo la segnalazione di vulnerabilità di sicurezza per NyaSU, leggi [SECURITY.md](/SECURITY.md).

## Licenza

- I file nella cartella `kernel` sono forniti secondo la licenza [GPL-2.0-only](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html).
- Tutte le altre parti, ad eccezione della certella `kernel`, seguono la licenza [GPL-3.0-or-later](https://www.gnu.org/licenses/gpl-3.0.html).

## Riconoscimenti e attribuzioni

- [kernel-assisted-superuser](https://git.zx2c4.com/kernel-assisted-superuser/about/): l'idea alla base di KernelSU.
- [Magisk](https://github.com/topjohnwu/Magisk): la potente utilità per il root.
- [genuine](https://github.com/brevent/genuine/): verifica della firma apk v2.
- [Diamorphine](https://github.com/m0nad/Diamorphine): alcune capacità di rootkit.
