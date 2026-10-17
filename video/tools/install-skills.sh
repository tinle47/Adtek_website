#!/bin/bash
# Cài skill hướng dẫn cho Claude vào ~/.claude/skills mỗi khi phiên cloud khởi động (SessionStart hook trong .claude/settings.json).
# Mỗi phiên cloud là máy mới nên phải cài lại. Khóa theo commit đã đọc kỹ (17/10/2026): bản mới hơn không tự lọt vào;
# muốn nâng cấp thì đọc lại mã của bản mới rồi mới đổi mã commit ở dưới. Hai repo không có file giấy phép (Remotion Skills)
# hoặc là MIT (GSAP Skills); chỉ tải về máy để dùng, không chép vào repo này.
#   Remotion Skills: chỉ lấy skill remotion-best-practices (đã gồm các phần con: markup, maps, render...).
#   GSAP Skills: bỏ gsap-scrolltrigger (cuộn trang web, video không dùng).
# Lỗi mạng thì bỏ qua, không chặn phiên.
set -u
DEST="$HOME/.claude/skills"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$DEST"

fetch() { # fetch <repo> <commit> <thư mục>
  git -c advice.detachedHead=false init -q "$3" &&
    git -C "$3" fetch -q --depth 1 "https://github.com/$1" "$2" &&
    git -C "$3" checkout -q FETCH_HEAD
}

if [ ! -d "$DEST/remotion-best-practices" ] && fetch remotion-dev/skills 1441a11e95db35443bd76bb318386c0d3ca00053 "$TMP/remotion"; then
  cp -r "$TMP/remotion/skills/remotion-best-practices" "$DEST/"
fi
if [ ! -d "$DEST/gsap-core" ] && fetch greensock/gsap-skills aed9cfd3277740755f6bfc1155c7aa645403b760 "$TMP/gsap"; then
  for s in "$TMP"/gsap/skills/gsap-*; do
    [ "$(basename "$s")" = gsap-scrolltrigger ] || cp -r "$s" "$DEST/"
  done
fi
exit 0
