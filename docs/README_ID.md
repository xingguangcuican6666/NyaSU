[English](README.md) | [Español](README_ES.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md) | [한국어](README_KR.md) | [Polski](README_PL.md) | [Português (Brasil)](README_PT-BR.md) | [Türkçe](README_TR.md) | [Русский](README_RU.md) | [Tiếng Việt](README_VI.md) | **Indonesia** | [עברית](README_IW.md) | [हिंदी](README_IN.md) | [Italiano](README_IT.md)

# NyaSU

<img src="https://raw.githubusercontent.com/xingguangcuican6666/NyaSU/main/website/docs/public/logo.png" style="width: 96px;" alt="logo">

Solusi root berbasis kernel untuk perangkat Android.

[![Latest release](https://img.shields.io/github/v/release/xingguangcuican6666/NyaSU?label=Release&logo=github)](https://github.com/xingguangcuican6666/NyaSU/releases/latest)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-orange.svg?logo=gnu)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![GitHub License](https://img.shields.io/github/license/xingguangcuican6666/NyaSU?logo=gnu)](/LICENSE)

## Upstream

NyaSU adalah turunan dari [KernelSU](https://github.com/tiann/KernelSU), solusi root sumber terbuka berbasis kernel yang dibuat oleh tiann dan para kontributornya. Desain sisi kernel, antarmuka supercall, dan format modul berasal dari proyek tersebut; untuk hal yang tidak dibahas di dokumentasi repositori ini, acuannya adalah upstream.

Lisensinya sama dengan upstream: berkas di dalam `kernel/` berlisensi GPL-2.0-only, sisanya GPL-3.0-or-later. Hak cipta kode asli tetap milik para penulisnya.

## Fitur

1. Akses `su` dan manajemen hak akses root berbasis kernel.
2. Sistem modul berbasis [metamodules](../website/docs/id_ID/guide/metamodule.md): Infrastruktur yang dapat dicopot-pasang untuk modifikasi systemless.
3. [Profil Aplikasi](../website/docs/id_ID/guide/app-profile.md): Kendalikan hak akses root secara aman.

## Status Kompatibilitas

NyaSU secara resmi mendukung perangkat Android GKI 2.0 (dengan kernel 5.10+), kernel lama (4.14+) juga didukung, tetapi kernel perlu dikompilasi secara manual.

Dengan dukungan ini WSA, ChromeOS, dan Android berbasis kontainer semuanya dapat dijalankan.

Saat ini, arsitektur `arm64-v8a` dan `x86_64` sudah didukung.

> [!CAUTION]
> Versi kernel terbaru menerapkan perubahan besar yang menyebabkan NyaSU gagal dan berpotensi memicu kernel panic pada `x86_64`! Cek situs web untuk informasi lebih lanjut!

## Penggunaan

- [Pemasangan](../website/docs/id_ID/guide/installation.md)
- [Cara Build](../website/docs/id_ID/guide/how-to-build.md)
- [Situs Web Resmi](../website/docs/id_ID/index.md)

## Terjemahan

Terjemahan di direktori ini dibuat dengan LLM.

Jika ingin menambahkan bahasa baru, silakan buka PR. Perubahan pada teks bahasa Inggris dan Mandarin yang sudah ada tidak diterima.

## Keamanan

Untuk informasi mengenai pelaporan kerentanan keamanan di NyaSU, lihat [SECURITY.md](/SECURITY.md).

## Lisensi

- Berkas di bawah direktori `kernel` berlisensi [GPL-2-only](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html).
- Seluruh bagian lainnya kecuali direktori `kernel` berlisensi [GPL-3.0-or-later](https://www.gnu.org/licenses/gpl-3.0.html).

## Kredit

- [kernel-assisted-superuser](https://git.zx2c4.com/kernel-assisted-superuser/about/): Gagasan utama KernelSU.
- [Magisk](https://github.com/topjohnwu/Magisk): Alat root yang andal.
- [genuine](https://github.com/brevent/genuine/): Validasi tanda tangan APK v2.
- [Diamorphine](https://github.com/m0nad/Diamorphine): Beberapa keahlian rootkit.
