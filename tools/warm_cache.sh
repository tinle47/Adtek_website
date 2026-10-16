#!/bin/bash
# Cách dùng: tools/warm_cache.sh <thư mục ghi log> (mặc định thư mục hiện tại). Dùng sau khi xóa cache toàn site hoặc khi WP-Optimize chưa bật preload.
# Làm nóng cache WP-Optimize: tải mọi URL trong sitemap một lần (không cookie), ghi trạng thái cache và thời gian.
S=${1:-.}
: > $S/warm.log
for sm in $(curl -sS --max-time 60 https://adtek.agency/sitemap_index.xml | grep -o '<loc>[^<]*' | sed 's/<loc>//'); do
  for u in $(curl -sS --max-time 60 "$sm" | grep -o '<loc>[^<]*' | sed 's/<loc>//'); do
    st=$(curl -sS -D - -o /dev/null --max-time 60 -A "Mozilla/5.0 (compatible; AdtekCacheWarm/1.0)" -w "CODE %{http_code} %{time_starttransfer}" "$u" | grep -i "wpo-cache-status\|^CODE" | tr -d '\r' | tr '\n' ' ')
    echo "$st $u" >> $S/warm.log
    sleep 1
  done
done
echo DONE >> $S/warm.log
