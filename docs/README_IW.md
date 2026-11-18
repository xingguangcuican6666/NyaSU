[English](README.md) | [Español](README_ES.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md) | [한국어](README_KR.md) | [Polski](README_PL.md) | [Português (Brasil)](README_PT-BR.md) | [Türkçe](README_TR.md) | [Русский](README_RU.md) | [Tiếng Việt](README_VI.md) | [Indonesia](README_ID.md) | **עברית** | [हिंदी](README_IN.md) | [Italiano](README_IT.md)

# NyaSU

<img src="https://raw.githubusercontent.com/xingguangcuican6666/NyaSU/main/website/docs/public/logo.png" style="width: 96px;" alt="logo">

פתרון לניהול root מבוסס על Kernel עבור מכשירי Android.

[![Latest release](https://img.shields.io/github/v/release/xingguangcuican6666/NyaSU?label=Release&logo=github)](https://github.com/xingguangcuican6666/NyaSU/releases/latest)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-orange.svg?logo=gnu)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![GitHub License](https://img.shields.io/github/license/xingguangcuican6666/NyaSU?logo=gnu)](/LICENSE)

## הפרויקט המקורי

NyaSU הוא פרויקט נגזר של [KernelSU](https://github.com/tiann/KernelSU), פתרון root בקוד פתוח מבוסס ליבה שיצרו tiann והתורמים שלו. התכנון בצד הליבה, ממשק ה-supercall ופורמט המודולים מקורם בפרויקט הזה; כל מה שאינו מכוסה בתיעוד של מאגר זה יש לבדוק בפרויקט המקורי.

הרישיונות זהים לאלה של הפרויקט המקורי: קבצים תחת `kernel/` הם GPL-2.0-only, וכל השאר GPL-3.0-or-later. זכויות היוצרים בקוד המקורי נשארות בידי מחבריו.

## תכונות

1. ניהול root ו־`su` מבוססים על Kernel.
2. מערכת מודולים מבוססת [metamodules](../website/docs/guide/metamodule.md): תשתית מודולרית לשינויים systemless.
3. [פרופיל אפליקציה](../website/docs/guide/app-profile.md): נעילת גישת root בכלוב.

## מצב תאימות

NyaSU תומך במכשירי Android GKI 2.0 (kernel 5.10+) באופן רשמי. לליבות ישנות (4.14+) יש גם תאימות, אך יידרש לבנות את הליבה באופן ידני.

באמצעות זה, תמיכה זמינה גם ל-WSA, ChromeOS ומכשירי Android המבוססים על מיכלים.

כיום, נתמכות הארכיטקטורות `arm64-v8a` ו-`x86_64`.

> [!CAUTION]
> גרסאות קרנל אחרונות יישמו שינוי שובר תאימות הגורם ל-NyaSU להיכשל ועלול לעורר kernel panic ב-`x86_64`! בדוק באתר למידע נוסף!

## שימוש

- [הוראות התקנה](../website/docs/guide/installation.md)
- [איך לבנות?](../website/docs/guide/how-to-build.md)
- [האתר רשמי](../website/docs/index.md)

## תרגום

התרגומים בספרייה זו נוצרים בעזרת LLM.

להוספת שפה חדשה אפשר לפתוח PR. לא מתקבלים שינויים בטקסטים הקיימים באנגלית ובסינית.

## רשיון

- קבצים תחת הספרייה `kernel` מוגנים על פי [GPL-2.0-only](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html).
- כל החלקים האחרים, למעט הספרייה `kernel`, מוגנים על פי [GPL-3.0-or-later](https://www.gnu.org/licenses/gpl-3.0.html).

## קרדיטים

- [kernel-assisted-superuser](https://git.zx2c4.com/kernel-assisted-superuser/about/): הרעיון של KernelSU.
- [Magisk](https://github.com/topjohnwu/Magisk): הכלי הסופר חזק לניהול root.
- [genuine](https://github.com/brevent/genuine/): אימות חתימת apk v2.
- [Diamorphine](https://github.com/m0nad/Diamorphine): כמה יכולות רוט.
