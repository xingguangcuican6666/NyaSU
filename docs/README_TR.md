[English](README.md) | [Español](README_ES.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md) | [한국어](README_KR.md) | [Polski](README_PL.md) | [Português (Brasil)](README_PT-BR.md) | **Türkçe** | [Русский](README_RU.md) | [Tiếng Việt](README_VI.md) | [Indonesia](README_ID.md) | [עברית](README_IW.md) | [हिंदी](README_IN.md) | [Italiano](README_IT.md)

# NyaSU

<img src="https://raw.githubusercontent.com/xingguangcuican6666/NyaSU/main/website/docs/public/logo.png" style="width: 96px;" alt="logo">

Android cihazlar için çekirdek tabanlı root çözümü.

[![Latest release](https://img.shields.io/github/v/release/xingguangcuican6666/NyaSU?label=Release&logo=github)](https://github.com/xingguangcuican6666/NyaSU/releases/latest)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-orange.svg?logo=gnu)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![GitHub License](https://img.shields.io/github/license/xingguangcuican6666/NyaSU?logo=gnu)](/LICENSE)

## Üst proje

NyaSU, tiann ve katkıda bulunanlar tarafından geliştirilen açık kaynaklı, çekirdek tabanlı Android root çözümü [KernelSU](https://github.com/tiann/KernelSU)'nun bir türevidir. Çekirdek tarafı tasarım, supercall arayüzü ve modül biçimi bu projeden gelir; bu deponun belgelerinde yer almayan konularda üst proje esas alınır.

Lisanslar üst projeyle aynıdır: `kernel/` altındaki dosyalar GPL-2.0-only, geri kalan her şey GPL-3.0-or-later'dir. Orijinal kodun telif hakları yazarlarında kalır.

## Özellikler

1. Çekirdek-tabanlı `su` ve root erişimi yönetimi.
2. [metamodules](../website/docs/guide/metamodule.md)'ye dayalı modül sistemi: Sistemsiz modifikasyonlar için takılabilir altyapı.
3. [Uygulama profili](../website/docs/guide/app-profile.md): Root gücünü bir kafese kapatın.

## Uyumluluk Durumu

NyaSU resmi olarak Android GKI 2.0 cihazlarını (5.10+ çekirdekli) destekler, eski çekirdeklerle de (4.14+) uyumludur, ancak çekirdeği kendiniz derlemeniz gerekir.

Bununla birlikte; WSA, ChromeOS ve konteyner tabanlı Android'in tamamı desteklenmektedir.

Şu anda `arm64-v8a` ve `x86_64` mimarileri desteklenmektedir.

> [!CAUTION]
> Yeni çekirdek sürümleri, NyaSU'nun çökmesine ve `x86_64` üzerinde kernel panic tetiklemesine neden olabilecek uyumsuz bir değişiklik uyguladı! Daha fazla bilgi için web sitesini kontrol edin!

## Kullanım

- [Yükleme yönergeleri](../website/docs/guide/installation.md)
- [Nasıl derlenir?](../website/docs/guide/how-to-build.md)
- [Resmi WEB sitesi](../website/docs/index.md)

## Çeviri

Bu dizindeki çeviriler LLM ile üretilir.

Yeni bir dil eklemek için PR açabilirsiniz. Mevcut İngilizce ve Çince metinlerde değişiklik kabul edilmez.

## Güvenlik

NyaSU'daki güvenlik açıklarını bildirme hakkında bilgi için, bkz [SECURITY.md](/SECURITY.md).

## Lisans

- `kernel` klasöründeki dosyalar [GPL-2-only](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html) lisansı altındadır.
- `kernel` klasörü dışındaki bütün diğer bölümler [GPL-3-veya-sonraki](https://www.gnu.org/licenses/gpl-3.0.html) lisansı altındadır.

## Krediler

- [kernel-assisted-superuser](https://git.zx2c4.com/kernel-assisted-superuser/about/): KernelSU fikri.
- [Magisk](https://github.com/topjohnwu/Magisk): güçlü root aracı.
- [genuine](https://github.com/brevent/genuine/): apk v2 imza doğrulaması.
- [Diamorphine](https://github.com/m0nad/Diamorphine): bazı rootkit becerileri.
