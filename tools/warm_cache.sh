#!/bin/bash
# Làm nóng cache WP-Optimize: tải mọi URL trong sitemap một lần (không cookie) cho cả bản máy tính và bản mobile,
# vì theme hiển thị khác nhau trên mobile (wp_is_mobile) nên WP-Optimize lưu 2 bộ cache riêng, và Google thu thập chủ yếu bằng Googlebot mobile.
# Cách dùng: tools/warm_cache.sh [thư mục ghi log] [desktop|mobile|both]  (mặc định: thư mục hiện tại, both)
# Dùng sau khi xóa cache toàn site, hoặc khi kiểm tra thấy trang mobile chưa có cache.
S=${1:-.}
MODE=${2:-both}
DESKTOP="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 AdtekCacheWarm/1.1"
MOBILE="Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36 AdtekCacheWarm/1.1"
case $MODE in desktop) UAS=("$DESKTOP");; mobile) UAS=("$MOBILE");; *) UAS=("$DESKTOP" "$MOBILE");; esac
: > $S/warm.log
URLS=$(for sm in $(curl -sS --max-time 60 https://adtek.agency/sitemap_index.xml | grep -o '<loc>[^<]*' | sed 's/<loc>//'); do curl -sS --max-time 60 "$sm" | grep -o '<loc>[^<]*' | sed 's/<loc>//'; done)
for ua in "${UAS[@]}"; do
  kind=$([[ $ua == *Mobile* ]] && echo mobile || echo desktop)
  for u in $URLS; do
    st=$(curl -sS -D - -o /dev/null --max-time 60 -A "$ua" -w "CODE %{http_code} %{time_starttransfer}" "$u" | grep -i "wpo-cache-status\|^CODE" | tr -d '\r' | tr '\n' ' ')
    echo "$kind $st $u" >> $S/warm.log
    sleep 1
  done
done
echo DONE >> $S/warm.log
