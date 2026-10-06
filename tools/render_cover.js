// Chụp file HTML thành ảnh bìa 1200x630. Cách dùng: node tools/render_cover.js input.html output.jpg
const { chromium } = require("playwright");

(async () => {
  const [input, output] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
  await page.goto("file://" + require("path").resolve(input));
  await page.waitForTimeout(300);
  await page.screenshot({ path: output, type: "jpeg", quality: 88 });
  await browser.close();
})();
