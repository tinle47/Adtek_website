// Chụp file HTML thành ảnh.
// Cách dùng: node tools/render_cover.js input.html output.jpg [rộng cao] (mặc định 1200x630)
//        hoặc node tools/render_cover.js danh-sach.json   (mảng {input, output, width, height}, chụp nhiều ảnh trong một lần mở trình duyệt)
// Chờ font tải xong; nếu trang có script co chữ thì chờ thêm body[data-done].
const { chromium } = require("playwright");
const path = require("path");

async function shot(browser, { input, output, width = 1200, height = 630 }) {
  const page = await browser.newPage({ viewport: { width: +width, height: +height } });
  await page.goto("file://" + path.resolve(input));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForFunction(() => !document.body.hasAttribute("data-fit") || document.body.dataset.done, null, { timeout: 5000 }).catch(() => {});
  await page.waitForTimeout(150);
  await page.screenshot({ path: output, type: "jpeg", quality: 88 });
  await page.close();
}

(async () => {
  const args = process.argv.slice(2);
  const jobs = args[0].endsWith(".json")
    ? require(path.resolve(args[0]))
    : [{ input: args[0], output: args[1], width: args[2], height: args[3] }];
  const browser = await chromium.launch();
  for (const job of jobs) await shot(browser, job);
  await browser.close();
})();
