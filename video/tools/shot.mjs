// Chụp màn hình trang báo hoặc báo cáo có chứa con số, để dùng trong cảnh "shot" của video.
// Cách dùng: node tools/shot.mjs <url> "<đoạn chữ cần tô sáng>" <tên-file> [--width 360]
// Kết quả: public/shots/<tên-file>.png và public/shots/<tên-file>.json (vị trí đoạn chữ trên ảnh, url, tiêu đề trang).
// Đoạn chữ phải khớp nguyên văn trên trang (kể cả dấu). Chỉ chụp trang gốc của nguồn, không chụp trang tổng hợp.
import { chromium } from "playwright-core";
import { writeFileSync } from "node:fs";
import path from "node:path";

const ROOT = path.resolve(import.meta.dirname, "..");
const args = process.argv.slice(2);
const flag = (name, def) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? args.splice(i, 2)[1] : def;
};
const width = Number(flag("width", 360)); // khổ hẹp để chữ đủ to khi lên video
const [url, find, name] = args;
if (!url || !find || !name) {
  console.error('Cách dùng: node tools/shot.mjs <url> "<đoạn chữ cần tô sáng>" <tên-file> [--width 360]');
  process.exit(1);
}

const SCALE = 3; // ảnh nét khi phóng to trong video
const ABOVE = 420; // phần trang giữ lại phía trên đoạn chữ (px CSS)
const HEIGHT = 900; // chiều cao vùng chụp (px CSS)

const browser = await chromium.launch({
  executablePath: process.env.REMOTION_BROWSER || "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell",
});
const page = await browser.newPage({ viewport: { width, height: 900 }, deviceScaleFactor: SCALE, locale: "vi-VN" });
await page.goto(url, { waitUntil: "networkidle", timeout: 60000 });
// Ảnh tải chậm (lazy) phải tải hết trước khi chụp, nếu không sẽ thành ô trống.
await page.evaluate(async () => {
  for (const img of document.querySelectorAll("img")) {
    img.loading = "eager";
    const lazy = img.dataset.lazySrc || img.dataset.src;
    if (lazy && !img.src.startsWith("http")) img.src = lazy;
  }
  for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 120)); }
  window.scrollTo(0, 0);
});
await page.waitForLoadState("networkidle");

// Tìm đoạn chữ, lấy khung của từng dòng chữ (đoạn chữ có thể xuống dòng).
const found = await page.evaluate((needle) => {
  const norm = (s) => s.replace(/\s+/g, " ");
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    const text = norm(n.textContent);
    const at = text.indexOf(needle);
    if (at < 0) continue;
    const el = n.parentElement;
    el.scrollIntoView({ block: "center" });
    // Vị trí trong chuỗi gốc (trước khi gộp khoảng trắng) để tạo Range đúng.
    let raw = 0, seen = 0;
    const src = n.textContent;
    while (seen < at && raw < src.length) {
      if (/\s/.test(src[raw])) { while (raw + 1 < src.length && /\s/.test(src[raw + 1])) raw++; }
      raw++; seen++;
    }
    const range = document.createRange();
    range.setStart(n, raw);
    range.setEnd(n, Math.min(src.length, raw + needle.length));
    const rects = [...range.getClientRects()].filter((r) => r.width > 2).map((r) => ({
      x: r.left + window.scrollX, y: r.top + window.scrollY, w: r.width, h: r.height,
    }));
    return { rects, title: document.title };
  }
  return null;
}, find);
if (!found) {
  console.error(`Không thấy "${find}" trên trang. Kiểm tra lại nguyên văn.`);
  await browser.close();
  process.exit(1);
}

// Ẩn thanh menu dính đầu trang, popup cookie để không che nội dung.
await page.evaluate(() => {
  for (const el of document.querySelectorAll("body *")) {
    const s = getComputedStyle(el);
    if ((s.position === "fixed" || s.position === "sticky") && el.getBoundingClientRect().height < window.innerHeight * 0.6) el.style.visibility = "hidden";
  }
});

const top = Math.max(0, Math.min(...found.rects.map((r) => r.y)) - ABOVE);
const clip = { x: 0, y: top, width, height: HEIGHT };
await page.screenshot({ path: path.join(ROOT, "public", "shots", `${name}.png`), clip, fullPage: true });
await browser.close();

const meta = {
  url,
  title: found.title,
  captured: new Date().toISOString().slice(0, 10),
  width: width * SCALE,
  height: HEIGHT * SCALE,
  highlight: found.rects.map((r) => ({ x: r.x * SCALE, y: (r.y - top) * SCALE, w: r.w * SCALE, h: r.h * SCALE })),
};
writeFileSync(path.join(ROOT, "public", "shots", `${name}.json`), JSON.stringify(meta, null, 1));
console.log(`Đã chụp public/shots/${name}.png (${meta.highlight.length} dòng được tô sáng) từ "${meta.title}"`);
