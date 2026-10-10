import { useLayoutEffect } from "react";
import { continueRender, delayRender, useCurrentFrame } from "remotion";

// Chỉ bật khi chạy tools/check.mjs: đo vị trí thật của từng dòng chữ đang hiện trên khung hình
// rồi in ra console để công cụ kiểm tra chữ bị cắt, chữ chồng nhau, chữ nằm dưới nút TikTok.
// Phần tử cố ý đè lên chữ khác (con dấu "SAI") hay cố ý nằm ngoài vùng an toàn (tên miền) gắn data-audit="skip".
export const Audit: React.FC = () => {
  const frame = useCurrentFrame();
  useLayoutEffect(() => {
    // Đo sau khi trình duyệt dựng xong khung (requestAnimationFrame), Remotion chờ continueRender rồi mới chụp.
    const handle = delayRender("Đo chữ");
    requestAnimationFrame(() => {
      measure();
      continueRender(handle);
    });
  });
  const measure = () => {
    const out: { s: string; x0: number; y0: number; x1: number; y1: number; cut?: boolean; el: number }[] = [];
    const ids = new Map<Element, number>();
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      const s = (n.textContent ?? "").trim();
      const el = n.parentElement;
      if (!s || !el || el.closest("[data-audit=skip]")) continue;
      // Độ mờ thật = tích độ mờ của mọi lớp cha; chữ đang mờ dần (dưới 0.6) chưa tính là đang hiện.
      let alpha = 1;
      let clipBox: DOMRect | null = null;
      for (let a: Element | null = el; a; a = a.parentElement) {
        const cs = getComputedStyle(a);
        alpha *= Number(cs.opacity);
        if (!clipBox && a !== el && cs.overflow !== "visible") clipBox = a.getBoundingClientRect();
      }
      if (alpha < 0.6) continue;
      if (!ids.has(el)) ids.set(el, ids.size);
      const r = document.createRange();
      r.selectNodeContents(n);
      for (const b of r.getClientRects()) {
        if (b.width < 2 || b.height < 2) continue;
        const cut = !!clipBox && (b.left < clipBox.left - 3 || b.right > clipBox.right + 3 || b.top < clipBox.top - 3 || b.bottom > clipBox.bottom + 3);
        out.push({ s: s.slice(0, 40), x0: b.left, y0: b.top, x1: b.right, y1: b.bottom, cut, el: ids.get(el)! });
      }
    }
    console.debug(`AUDIT ${JSON.stringify({ frame, boxes: out })}`);
  };
  return null;
};
