// Chụp file HTML thành ảnh. Cách dùng: node tools/render_cover.js input.html output.jpg [rộng cao] (mặc định 1200x630)
const { chromium } = require("playwright");

(async () => {
  const [input, output, width = 1200, height = 630] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: +width, height: +height } });
  await page.goto("file://" + require("path").resolve(input));
  await page.waitForTimeout(300);
  await page.screenshot({ path: output, type: "jpeg", quality: 88 });
  await browser.close();
})();
