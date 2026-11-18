[English](README.md) | [Español](README_ES.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md) | [한국어](README_KR.md) | [Polski](README_PL.md) | [Português (Brasil)](README_PT-BR.md) | [Türkçe](README_TR.md) | [Русский](README_RU.md) | [Tiếng Việt](README_VI.md) | [Indonesia](README_ID.md) | [עברית](README_IW.md) |  **हिंदी** | [Italiano](README_IT.md)

# NyaSU

<img src="https://raw.githubusercontent.com/xingguangcuican6666/NyaSU/main/website/docs/public/logo.png" style="width: 96px;" alt="logo">

Android उपकरणों के लिए कर्नेल-आधारित रूट समाधान।

[![Latest release](https://img.shields.io/github/v/release/xingguangcuican6666/NyaSU?label=Release&logo=github)](https://github.com/xingguangcuican6666/NyaSU/releases/latest)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-orange.svg?logo=gnu)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![GitHub License](https://img.shields.io/github/license/xingguangcuican6666/NyaSU?logo=gnu)](/LICENSE)

## अपस्ट्रीम

NyaSU, [KernelSU](https://github.com/tiann/KernelSU) का व्युत्पन्न है — एक ओपन-सोर्स, कर्नेल-आधारित Android रूट समाधान जिसे tiann और उनके योगदानकर्ताओं ने बनाया है। कर्नेल-साइड डिज़ाइन, supercall इंटरफ़ेस और मॉड्यूल प्रारूप उसी प्रोजेक्ट से आए हैं; इस रिपॉज़िटरी के दस्तावेज़ों में जो नहीं है, उसके लिए अपस्ट्रीम ही संदर्भ है।

लाइसेंस अपस्ट्रीम के समान हैं: `kernel/` के अंतर्गत फ़ाइलें GPL-2.0-only हैं, और शेष सब GPL-3.0-or-later। मूल कोड का कॉपीराइट उसके लेखकों के पास ही रहता है।

## विशेषताएँ

1. कर्नेल-आधारित `su` और रूट एक्सेस प्रबंधन।
2. [metamodules](../website/docs/guide/metamodule.md) पर आधारित मॉड्यूल प्रणाली: Systemless संशोधनों के लिए प्लगेबल इंफ्रास्ट्रक्चर।
3. [App Profile](../website/docs/guide/app-profile.md): Root शक्ति को पिंजरे में बंद कर दो।

## अनुकूलता अवस्था

NyaSU आधिकारिक तौर पर Android GKI 2.0 डिवाइस (कर्नेल 5.10+) का समर्थन करता है। पुराने कर्नेल (4.14+) भी संगत हैं, लेकिन कर्नेल को मैन्युअल रूप से बनाना होगा।

इसके साथ, WSA, ChromeOS और कंटेनर-आधारित Android सभी समर्थित हैं।

वर्तमान में, `arm64-v8a` और `x86_64` आर्किटेक्चर समर्थित हैं।

> [!CAUTION]
> हाल ही के कर्नेल संस्करणों में एक ऐसा बदलाव लागू किया गया है जिससे NyaSU विफल हो सकता है और `x86_64` पर कर्नेल पैनिक (kernel panic) ट्रिगर हो सकता है! अधिक जानकारी के लिए वेबसाइट देखें!

## प्रयोग

- [स्थापना निर्देश](../website/docs/guide/installation.md)
- [कैसे बनाना है ?](../website/docs/guide/how-to-build.md)
- [आधिकारिक वेबसाइट](../website/docs/index.md)

## अनुवाद करना

इस निर्देशिका के अनुवाद LLM से बनाए जाते हैं।

नई भाषा जोड़ने के लिए PR भेजें। मौजूदा अंग्रेज़ी और चीनी पाठ में बदलाव स्वीकार नहीं किए जाते।

## लाइसेंस

- `Kernel` निर्देशिका के अंतर्गत फ़ाइलें हैं [GPL-2-only](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
- `Kernel` निर्देशिका को छोड़कर अन्य सभी भाग हैं [GPL-3.0-or-later](https://www.gnu.org/licenses/gpl-3.0.html)

## आभार सूची

- [kernel-assisted-superuser](https://git.zx2c4.com/kernel-assisted-superuser/about/): KernelSU विचार।
- [Magisk](https://github.com/topjohnwu/Magisk): शक्तिशाली root उपकरण।
- [genuine](https://github.com/brevent/genuine/): apk v2 हस्ताक्षर सत्यापन।
- [Diamorphine](https://github.com/m0nad/Diamorphine): कुछ रूटकिट कौशल।
