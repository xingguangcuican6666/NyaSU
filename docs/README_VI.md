[English](README.md) | [Español](README_ES.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md) | [한국어](README_KR.md) | [Polski](README_PL.md) | [Português (Brasil)](README_PT-BR.md) | [Türkçe](README_TR.md) | [Русский](README_RU.md) | **Tiếng Việt** | [Indonesia](README_ID.md) | [עברית](README_IW.md) | [हिंदी](README_IN.md) | [Italiano](README_IT.md)

# NyaSU

<img src="https://raw.githubusercontent.com/xingguangcuican6666/NyaSU/main/website/docs/public/logo.png" style="width: 96px;" alt="logo">

Giải pháp root thông qua thay đổi trên Kernel hệ điều hành cho các thiết bị Android.

[![Latest release](https://img.shields.io/github/v/release/xingguangcuican6666/NyaSU?label=Release&logo=github)](https://github.com/xingguangcuican6666/NyaSU/releases/latest)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-orange.svg?logo=gnu)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![GitHub License](https://img.shields.io/github/license/xingguangcuican6666/NyaSU?logo=gnu)](/LICENSE)

## Dự án gốc

NyaSU được phát triển dựa trên [KernelSU](https://github.com/tiann/KernelSU), giải pháp root mã nguồn mở hoạt động ở tầng kernel do tiann và những người đóng góp xây dựng. Thiết kế phía kernel, giao diện supercall và định dạng mô-đun đều bắt nguồn từ dự án đó; những nội dung không có trong tài liệu của kho lưu trữ này nên tham khảo dự án gốc.

Giấy phép giữ nguyên như dự án gốc: các tệp trong `kernel/` dùng GPL-2.0-only, phần còn lại dùng GPL-3.0-or-later. Bản quyền mã nguồn gốc vẫn thuộc về các tác giả ban đầu.

## Tính năng

1. Hỗ trợ gói thực thi `su` và quản lý quyền root.
2. Hệ thống mô-đun thông qua [metamodules](../website/docs/vi_VN/guide/metamodule.md): Cơ sở hạ tầng có thể cắm cho các sửa đổi systemless.
3. [App Profile](../website/docs/vi_VN/guide/app-profile.md): Hạn chế quyền root của ứng dụng.

## Tình trạng tương thích

NyaSU chính thức hỗ trợ các thiết bị Android với kernel GKI 2.0 (phiên bản kernel 5.10+), các phiên bản kernel cũ hơn (4.14+) cũng tương thích, nhưng bạn cần phải tự biên dịch.

WSA, ChromeOS và Android dựa trên container(container-based) cũng được hỗ trợ bởi NyaSU.

Hiện tại, các kiến trúc `arm64-v8a` và `x86_64` được hỗ trợ.

> [!CAUTION]
> Các phiên bản kernel gần đây đã áp dụng một thay đổi lớn có thể khiến NyaSU gặp lỗi và có khả năng gây ra kernel panic trên `x86_64`! Hãy kiểm tra trang web để biết thêm thông tin!

## Sử dụng

- [Hướng dẫn cài đặt](../website/docs/vi_VN/guide/installation.md)
- [Cách để build?](../website/docs/vi_VN/guide/how-to-build.md)
- [Website Chính Thức](../website/docs/vi_VN/index.md)

## Hỗ trợ dịch

Các bản dịch trong thư mục này được tạo bằng LLM.

Nếu muốn thêm ngôn ngữ mới, hãy mở PR. Không chấp nhận chỉnh sửa đối với bản tiếng Anh và tiếng Trung hiện có.

## Giấy phép

- Tất cả các file trong thư mục `kernel` dùng giấy phép [GPL-2-only](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html).
- Tất cả các thành phần khác ngoại trừ thư mục `kernel` dùng giấy phép [GPL-3-or-later](https://www.gnu.org/licenses/gpl-3.0.html).

## Lời cảm ơn

- [kernel-assisted-superuser](https://git.zx2c4.com/kernel-assisted-superuser/about/): ý tưởng cho KernelSU.
- [Magisk](https://github.com/topjohnwu/Magisk): công cụ root mạnh mẽ.
- [genuine](https://github.com/brevent/genuine/): phương pháp xác thực apk v2.
- [Diamorphine](https://github.com/m0nad/Diamorphine): các phương pháp ẩn của rootkit.
