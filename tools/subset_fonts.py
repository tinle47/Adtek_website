"""Tạo bản rút gọn của font Roboto và Oswald cho mu-plugin adtek-performance.

Font gốc của theme (template/assets/fonts) chứa cả chữ Cyrillic, Hy Lạp... nặng khoảng 66 KB mỗi file.
Bản rút gọn chỉ giữ Latin, tiếng Việt và dấu câu thông dụng, bỏ dữ liệu hinting (như Google Fonts),
còn khoảng 14 KB mỗi file. Ký tự nằm ngoài bộ này sẽ hiển thị bằng font dự phòng của hệ thống.

Cách dùng: pip install fonttools brotli
           python3 tools/subset_fonts.py
Kết quả ghi vào wordpress/mu-plugins/adtek-performance/fonts/.
"""
import os
import subprocess
import sys
import tempfile
import urllib.request

BASE = "https://adtek.agency/template/assets/fonts"
FONTS = {
    "Roboto": ["Thin", "ThinItalic", "Light", "LightItalic", "Regular", "Italic", "Medium", "MediumItalic",
               "Bold", "BoldItalic", "Black", "BlackItalic"],
    "Oswald": ["ExtraLight", "Light", "Regular", "Medium", "SemiBold", "Bold"],
}
UNICODES = ",".join([
    "U+0000-00FF",  # Latin cơ bản và Latin-1
    "U+0102-0103,U+0110-0111,U+0128-0129,U+0168-0169,U+01A0-01A1,U+01AF-01B0",  # Ă Đ Ĩ Ũ Ơ Ư
    "U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC",
    "U+0300-0301,U+0303-0304,U+0308-0309,U+0323,U+0329",  # dấu thanh dạng tổ hợp
    "U+1EA0-1EF9",  # chữ tiếng Việt dựng sẵn (ạ ả ấ ... ỹ)
    "U+2000-206F,U+20AB,U+20AC,U+2122,U+2190-2193,U+2212,U+2215,U+FEFF,U+FFFD",  # dấu câu, ₫ € ™ mũi tên
])
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "wordpress", "mu-plugins", "adtek-performance", "fonts")


def main():
    os.makedirs(OUT, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for family, styles in FONTS.items():
            for style in styles:
                name = f"{family}-{style}.woff2"
                src = os.path.join(tmp, name)
                urllib.request.urlretrieve(f"{BASE}/{family}/{name}", src)
                dst = os.path.join(OUT, name)
                subprocess.run([
                    sys.executable, "-m", "fontTools.subset", src, f"--unicodes={UNICODES}",
                    "--layout-features=kern,liga,clig,calt,ccmp,locl,mark,mkmk", "--no-hinting",
                    "--flavor=woff2", f"--output-file={dst}",
                ], check=True)
                print(f"{name}: {os.path.getsize(src):,} -> {os.path.getsize(dst):,} bytes")


if __name__ == "__main__":
    main()
