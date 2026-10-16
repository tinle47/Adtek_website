// In một file HTML nhiều trang (mỗi trang là một .page cùng kích thước) thành PDF, kèm ảnh xem trước từng trang.
// Cách dùng: node tools/render_pages.js trang.html ra.pdf rộng cao [thư-mục-ảnh-xem-trước]
// Trang HTML đặt @page{size:<rộng>px <cao>px;margin:0} và mỗi .page ngắt trang sau nó.
const { chromium } = require("playwright");
const path = require("path");

(async () => {
  const [input, output, width, height, previews] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: +width, height: +height } });
  await page.goto("file://" + path.resolve(input), { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  await page.pdf({ path: output, width: width + "px", height: height + "px", printBackground: true, preferCSSPageSize: true });
  if (previews) {
    const pages = await page.$$(".page");
    for (let i = 0; i < pages.length; i++) {
      await pages[i].screenshot({ path: path.join(previews, String(i + 1).padStart(2, "0") + ".jpg"), type: "jpeg", quality: 82 });
    }
  }
  await browser.close();
})();
